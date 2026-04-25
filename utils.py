# utils.py - Contains validation and scoring logic

import math

def compute_performance_score(bat_runs, bat_avg, bat_sr, fifties, hundreds, wickets, econ, matches):
    bat_score = (bat_runs/5000*30) + (bat_avg/60*35) + (bat_sr/170*20) + (fifties*1.5 + hundreds*3.5)
    bowl_score = (wickets/250*50) + ((8-econ)/8*30 if econ>0 else 0) + (0 if matches==0 else (matches/500*20))
    total = bat_score + bowl_score
    return min(100, total)

def compute_batting_consistency(recent_scores):
    if not recent_scores:
        return 0.0
    good_scores = sum(1 for x in recent_scores if x>=40)
    total = len(recent_scores)
    score = (good_scores/total)*100
    score += sum(min(x,100)/200 for x in recent_scores)
    return round(min(score, 100),2)

def compute_bowling_consistency(recent_figs):
    if not recent_figs:
        return 0.0
    wickets_per_match = []
    for f in recent_figs:
        try:
            w, r = f.strip().split("/")
            wickets_per_match.append(int(w))
        except:
            continue
    if not wickets_per_match:
        return 0.0
    score = 0.0
    total_matches = len(wickets_per_match)
    for w in wickets_per_match:
        if w==0:
            score += 10
        elif w==1:
            score += 20
        elif w==2:
            score += 28
        else:
            score += 30
    score = (score/ (total_matches*30))*100
    return round(min(score,100),2)

def compute_bowl_avg(runs, wickets):
    return runs / wickets if wickets > 0 else 0.0

def validate_inputs(player_name, matches, bat_innings, bat_runs, high_score, bat_avg, bat_sr,
                     fifties, hundreds, bowl_innings, overs, wickets, econ, bowl_sr,
                     recent_bat_scores_str, recent_bowl_figs_str):
    
    if not player_name.strip():
        return False, "Player name cannot be empty."

    # 1. Validate numerical inputs and convert
    try:
        num_fields = {
            'Matches': int(matches), 'Bat Innings': int(bat_innings), 'Batting Runs': int(bat_runs),
            'High Score': int(high_score), '50s': int(fifties), '100s': int(hundreds), 
            'Bowling Innings': int(bowl_innings), 'Wickets': int(wickets)
        }
        float_fields = {
            'Bat Avg': float(bat_avg), 'Bat SR': float(bat_sr), 'Overs': float(overs), 
            'Econ': float(econ), 'Bowl SR': float(bowl_sr)
        }
    except ValueError:
        return False, "All number fields must contain valid numerical values."

    # 2. Validate non-negativity
    for field, val in {**num_fields, **float_fields}.items():
        if val < 0:
            return False, f"{field} must be non-negative."

    # 3. Validate specific constraints
    if int((float_fields['Overs'] - int(float_fields['Overs'])) * 10) > 5:
        return False, "Overs must be a valid cricket over decimal (e.g., 10.3) where the decimal part is 0-5."

    # 4. Validate recent scores/figures
    try:
        recent_bat_scores = [int(x.strip()) for x in recent_bat_scores_str.split(",") if x.strip()]
        if any(score < 0 for score in recent_bat_scores):
             return False, "Recent batting scores must be non-negative integers."
    except ValueError:
        return False, "Recent batting scores must be comma-separated integers."

    if recent_bowl_figs_str.strip():
        try:
            figs = recent_bowl_figs_str.split(",")
            for f in figs:
                w,r = f.strip().split("/")
                if not int(w)>=0 or not int(r)>=0:
                    return False, "Bowling figures must be non-negative."
        except:
            return False, "Recent bowling figures must be in w/r format (e.g., 2/25, 1/30)."
            
    return True,""

# --- TEAM BALANCE AND SELECTION LOGIC ---

IDEAL_TEAM_QUOTA = {
    "Batsman": 4, 
    "Bowler": 3,
    "Allrounder": 4,
    "Wicketkeeper": 1
}
TEAM_SIZE = 11

def analyze_team_balance(player_list):
    """
    Analyzes the composition of an 11-player team against an ideal quota.
    Returns the role counts and the balance rating.
    """
    if len(player_list) != TEAM_SIZE:
        return None, "Error: Team must have exactly 11 players."

    role_counts = {role: 0 for role in IDEAL_TEAM_QUOTA}
    
    for player in player_list:
        role = player.get('role')
        if role in role_counts:
            role_counts[role] += 1

    # Heuristic adjustment for Wicketkeeper: Assume 1 Batsman/Allrounder is the WK
    wk_filled = 0
    if role_counts.get("Batsman", 0) > IDEAL_TEAM_QUOTA['Batsman'] - 1:
        wk_filled = 1
        role_counts["Batsman"] = max(0, role_counts["Batsman"] - 1)
        
    role_counts['Wicketkeeper'] = wk_filled

    # Compare to ideal quota and calculate a penalty score
    penalty_score = 0
    for role, ideal_count in IDEAL_TEAM_QUOTA.items():
        current_count = role_counts.get(role, 0)
        deviation = abs(current_count - ideal_count)
        
        if role == "Wicketkeeper":
            penalty_score += deviation * 3
        else:
            penalty_score += deviation * 1.5
            
    # Determine the rating
    if penalty_score == 0:
        balance_rating = "✅ Excellent"
    elif penalty_score <= 3:
        balance_rating = "👍 Good"
    elif penalty_score <= 6:
        balance_rating = "⚠️ Fair (Minor tweaks needed)"
    else:
        balance_rating = "❌ Poor (Major imbalance)"

    return role_counts, balance_rating

def select_teams(all_players):
    """
    (This function is kept for the split teams mode, but is not used in the new single team default flow)
    Divides all available players into two balanced teams (Team A and Team B)
    """
    
    # We will use the single team selector logic twice if splitting is needed, 
    # but for the requested feature, this function's output is not strictly needed. 
    # Returning a placeholder for now to avoid errors in app.py if it is called unexpectedly.
    return [], []


def get_best_team_from_selection(selected_players_data):
    """
    Selects the single best 11-man team from a list of selected players based on 
    performance score while meeting the user's specific quota.
    """
    if len(selected_players_data) < TEAM_SIZE:
        return None, f"Error: Need at least {TEAM_SIZE} players to form a team."

    sorted_players = sorted(selected_players_data, key=lambda x: x['performance_score'], reverse=True)
    
    final_team = []
    current_counts = {role: 0 for role in IDEAL_TEAM_QUOTA}
    
    # Use the IDEAL_TEAM_QUOTA for the greedy selection, excluding WK for simplicity
    selection_quota = { "Batsman": 4, "Bowler": 3, "Allrounder": 4}
    
    # 1. Greedy fill based on role quota and performance
    for role in ["Allrounder", "Bowler", "Batsman"]:
        quota = selection_quota.get(role, 0)
        players_in_role = [p for p in sorted_players if p['role'] == role]
        
        for player in players_in_role:
            if current_counts[role] < quota and player['name'] not in [p['name'] for p in final_team] and len(final_team) < TEAM_SIZE:
                final_team.append(player)
                current_counts[role] += 1
                
    # 2. Fill remaining slots (up to 11) with the highest-rated unselected players
    unselected_players = [p for p in sorted_players if p['name'] not in [t['name'] for t in final_team]]
    
    for player in unselected_players:
        if len(final_team) < TEAM_SIZE:
            final_team.append(player)
        else:
            break

    if len(final_team) != TEAM_SIZE:
        return None, f"Error: Could only form a team of {len(final_team)} players. Check player availability."

    # 3. Get final balance report
    role_counts, balance_rating = analyze_team_balance(final_team)

    return final_team, balance_rating