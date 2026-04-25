from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import json
from database import create_table, save_player_data, get_all_player_names, get_player_data, get_players_by_role, get_all_players_data
from utils import (
    validate_inputs, compute_performance_score, compute_batting_consistency, 
    compute_bowling_consistency, compute_bowl_avg, select_teams, analyze_team_balance, get_best_team_from_selection
)

app = Flask(__name__)

# --- Global Artifacts and Mappings ---
try:
    clf = joblib.load("role_classifier_logreg.pkl")
    le = joblib.load("role_label_encoder.pkl")
    scaler = joblib.load("role_scaler.pkl")
except FileNotFoundError:
    print("CRITICAL ERROR: ML artifacts not found. Run 'python train_model.py' first.")

role_map = {
    "cluster0": "Batsman", "cluster1": "Bowler", "cluster2": "Allrounder",
    "batsman": "Batsman", "bowler": "Bowler", "allrounder": "Allrounder",
    "batter": "Batsman"
}

create_table()

# --- Flask Routes (analyze, player, compare, leaderboard remain mostly the same) ---

@app.route('/')
def index():
    player_names = get_all_player_names()
    return render_template('index.html', player_names=player_names)

@app.route('/api/analyze', methods=['POST'])
def analyze_player_api():
    data = request.get_json()
    valid, msg = validate_inputs(**data)
    if not valid:
        return jsonify({"status": "error", "message": msg}), 400

    try:
        processed_data = {k: float(v) if '.' in str(v) or k in ['bat_avg', 'bat_sr', 'econ', 'bowl_sr', 'overs'] else int(v) for k, v in data.items() if k not in ['player_name', 'recent_bat_scores_str', 'recent_bowl_figs_str']}
        processed_data['player_name'] = data['player_name']
        recent_bat_scores = [int(x.strip()) for x in data['recent_bat_scores_str'].split(",") if x.strip()]
        recent_bowl_figs = [x.strip() for x in data['recent_bowl_figs_str'].split(",") if x.strip()]
        processed_data['recent_bat_scores'] = recent_bat_scores
        processed_data['recent_bowl_figs'] = recent_bowl_figs

    except ValueError:
        return jsonify({"status": "error", "message": "Invalid numerical input."}), 400

    bowl_avg = compute_bowl_avg(processed_data['bat_runs'], processed_data['wickets'])
    
    # ML Role Prediction (using global scaler/clf)
    role = "Unknown"
    try:
        input_features = np.array([[
            processed_data['matches'], processed_data['bat_innings'], processed_data['bat_runs'], 
            processed_data['bat_avg'], processed_data['bat_sr'], processed_data['fifties'], 
            processed_data['hundreds'], processed_data['bowl_innings'], processed_data['overs'], 
            processed_data['wickets'], bowl_avg, processed_data['econ'], processed_data['bowl_sr']
        ]])
        input_scaled = scaler.transform(input_features)
        role_pred_idx = clf.predict(input_scaled)[0]
        role_raw = le.inverse_transform([role_pred_idx])[0]
        role = role_map.get(role_raw, role_raw)
        if role.lower() == 'batter':
            role = 'Batsman'
    except:
        pass # Keep 'Unknown' if ML fails

    perf_score = compute_performance_score(processed_data['bat_runs'], processed_data['bat_avg'], processed_data['bat_sr'], processed_data['fifties'], processed_data['hundreds'], processed_data['wickets'], processed_data['econ'], processed_data['matches'])
    bat_cons = compute_batting_consistency(recent_bat_scores)
    bowl_cons = compute_bowling_consistency(recent_bowl_figs)

    processed_data['role'] = role
    processed_data['performance_score'] = perf_score
    processed_data['batting_consistency'] = bat_cons
    processed_data['bowling_consistency'] = bowl_cons
    
    save_player_data(processed_data)

    metrics = ['Runs','Avg','SR','50s','100s','Wickets','Econ']
    values = [processed_data['bat_runs'], processed_data['bat_avg'], processed_data['bat_sr'], processed_data['fifties'], processed_data['hundreds'], processed_data['wickets'], processed_data['econ']]
    max_vals = [5000, 50, 150, 30, 5, 250, 10]
    values_norm = [min(v/m*100, 100) for v,m in zip(values,max_vals)]

    return jsonify({
        "status": "success",
        "player_name": processed_data['player_name'],
        "role": role,
        "performance_score": round(perf_score, 2),
        "batting_consistency": round(bat_cons, 2),
        "bowling_consistency": round(bowl_cons, 2),
        "radar_data": values_norm,
        "radar_labels": metrics,
        "all_player_names": get_all_player_names()
    })

@app.route('/api/player/<player_name>', methods=['GET'])
def get_player_api(player_name):
    data = get_player_data(player_name)
    if not data:
        return jsonify({"status": "error", "message": "Player not found"}), 404

    perf_score = compute_performance_score(data['bat_runs'], data['bat_avg'], data['bat_sr'], data['fifties'], data['hundreds'], data['wickets'], data['econ'], data['matches'])
    bat_cons = compute_batting_consistency(data['recent_bat_scores'])
    bowl_cons = compute_bowling_consistency(data['recent_bowl_figs'])

    metrics = ['Runs','Avg','SR','50s','100s','Wickets','Econ']
    values = [data['bat_runs'], data['bat_avg'], data['bat_sr'], data['fifties'], data['hundreds'], data['wickets'], data['econ']]
    max_vals = [5000, 50, 150, 30, 5, 250, 10]
    values_norm = [min(v/m*100, 100) for v,m in zip(values,max_vals)]

    return jsonify({
        "status": "success",
        "player_data": data,
        "performance_score": round(perf_score, 2),
        "batting_consistency": round(bat_cons, 2),
        "bowling_consistency": round(bowl_cons, 2),
        "radar_data": values_norm,
        "radar_labels": metrics,
    })

@app.route('/api/compare', methods=['POST'])
def compare_players_api():
    data = request.get_json()
    player1_name = data.get('player1')
    player2_name = data.get('player2')

    p1 = get_player_data(player1_name)
    p2 = get_player_data(player2_name)

    if not p1 or not p2:
        return jsonify({"status": "error", "message": "One or both players not found."}), 404

    perf1 = compute_performance_score(p1['bat_runs'], p1['bat_avg'], p1['bat_sr'], p1['fifties'], p1['hundreds'], p1['wickets'], p1['econ'], p1['matches'])
    perf2 = compute_performance_score(p2['bat_runs'], p2['bat_avg'], p2['bat_sr'], p2['fifties'], p2['hundreds'], p2['wickets'], p2['econ'], p2['matches'])

    metrics = ['Runs','Avg','SR','50s','100s','Wickets','Econ']
    max_vals = [5000, 50, 150, 30, 5, 250, 10]

    def normalize(p):
        values = [p["bat_runs"], p["bat_avg"], p["bat_sr"], p["fifties"], p["hundreds"], p["wickets"], p["econ"]]
        return [min(v/m*100, 100) for v,m in zip(values, max_vals)]

    vals1_norm = normalize(p1)
    vals2_norm = normalize(p2)

    comparison_results = {}
    metrics_full = ["Runs","Avg","SR","50s","100s","Wickets","Econ","Performance"]
    values1 = [p1["bat_runs"], p1["bat_avg"], p1["bat_sr"], p1["fifties"], p1["hundreds"], p1["wickets"], p1["econ"], perf1]
    values2 = [p2["bat_runs"], p2["bat_avg"], p2["bat_sr"], p2["fifties"], p2["hundreds"], p2["wickets"], p2["econ"], perf2]
    
    for m, v1, v2 in zip(metrics_full, values1, values2):
        if m == "Econ":
            stronger = player1_name if v1 < v2 else player2_name if v2 < v1 else "Tie"
        else:
            stronger = player1_name if v1 > v2 else player2_name if v2 > v1 else "Tie"
        comparison_results[m] = {
            player1_name: round(v1, 2),
            player2_name: round(v2, 2),
            "stronger": stronger
        }

    return jsonify({
        "status": "success",
        "radar_data": {
            player1_name: vals1_norm,
            player2_name: vals2_norm,
        },
        "radar_labels": metrics,
        "comparison_results": comparison_results
    })

@app.route('/api/players', methods=['GET'])
def get_players_list_api():
    player_names = get_all_player_names()
    return jsonify({"status": "success", "all_player_names": player_names})

@app.route('/leaderboard_data', methods=['GET'])
def get_leaderboard_data():
    role = request.args.get('role')
    if not role:
        return jsonify({"status": "error", "message": "Role parameter is required."}), 400

    players = get_players_by_role(role) 

    if not players:
        return jsonify({"status": "success", "players": [], "message": f"No players found for role: {role}"})

    return jsonify({
        "status": "success",
        "players": players,
        "message": f"Leaderboard for {role}"
    })

@app.route('/api/team_balance', methods=['POST'])
def team_balance_analyzer_api():
    data = request.get_json()
    player_names = data.get('players', [])
    
    if len(player_names) != 11:
        return jsonify({"status": "error", "message": "Team must have exactly 11 players for analysis."}), 400
        
    player_data = [get_player_data(name) for name in player_names]
    player_data = [p for p in player_data if p is not None]

    if len(player_data) != 11:
         return jsonify({"status": "error", "message": "Could not find all 11 selected players in the database."}), 400

    role_counts, rating = analyze_team_balance(player_data)
    
    if rating.startswith("Error"):
        return jsonify({"status": "error", "message": rating}), 400

    output = {
        "status": "success",
        "counts": role_counts,
        "rating": rating
    }
    return jsonify(output)


@app.route('/api/teams', methods=['GET', 'POST'])
def generate_teams_api():
    """
    Generates the best single team from ALL players (GET - NEW DEFAULT) OR 
    Generates the best single team from SELECTED players (POST).
    """
    if request.method == 'GET':
        # NEW DEFAULT: Generate a single best team from ALL players
        all_players = get_all_players_data()

        if len(all_players) < 11:
            return jsonify({"status": "error", "message": "Need at least 11 players registered to form a team."}), 400
        
        best_team, rating = get_best_team_from_selection(all_players)

        if best_team is None:
            return jsonify({"status": "error", "message": rating}), 400
        
        role_counts, _ = analyze_team_balance(best_team)

        team_players = [{"name": p['name'], "role": p['role'], "performance_score": round(p['performance_score'], 2)} for p in best_team]
        
        return jsonify({
            "status": "success",
            "mode": "best_team",
            "team": {
                "players": team_players,
                "counts": role_counts,
                "rating": rating,
                "total_perf": round(sum(p['performance_score'] for p in best_team), 2)
            }
        })
    
    elif request.method == 'POST':
        # Existing logic: Generate the best single team from a selected list
        data = request.get_json()
        selected_player_names = data.get('players', [])
        
        if len(selected_player_names) < 11:
            return jsonify({"status": "error", "message": "Select at least 11 players to form a team."}), 400
        
        selected_players_data = [get_player_data(name) for name in selected_player_names]
        selected_players_data = [p for p in selected_players_data if p is not None]
        
        best_team, rating = get_best_team_from_selection(selected_players_data)
        
        if best_team is None:
            return jsonify({"status": "error", "message": rating}), 400
        
        role_counts, _ = analyze_team_balance(best_team)

        team_players = [{"name": p['name'], "role": p['role'], "performance_score": round(p['performance_score'], 2)} for p in best_team]
        
        return jsonify({
            "status": "success",
            "mode": "best_team",
            "team": {
                "players": team_players,
                "counts": role_counts,
                "rating": rating,
                "total_perf": round(sum(p['performance_score'] for p in best_team), 2)
            }
        })

if __name__ == '__main__':
    app.run(debug=True)