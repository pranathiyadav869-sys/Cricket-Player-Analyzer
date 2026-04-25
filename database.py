import sqlite3
import json

DB_NAME = 'player_stats.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def create_table():
    """Creates the player_data table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_data (
            player_name TEXT PRIMARY KEY,
            matches INTEGER,
            bat_innings INTEGER,
            bat_runs INTEGER,
            high_score INTEGER,
            bat_avg REAL,
            bat_sr REAL,
            fifties INTEGER,
            hundreds INTEGER,
            bowl_innings INTEGER,
            overs REAL,
            wickets INTEGER,
            econ REAL,
            bowl_sr REAL,
            recent_bat_scores_json TEXT,
            recent_bowl_figs_json TEXT,
            role TEXT,
            performance_score REAL,
            batting_consistency REAL,
            bowling_consistency REAL
        )
    """)
    conn.commit()
    conn.close()

def save_player_data(data):
    """Saves or updates player data, including new calculated scores and role."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    bat_scores_json = json.dumps(data.get('recent_bat_scores', []))
    bowl_figs_json = json.dumps(data.get('recent_bowl_figs', []))

    cursor.execute("""
        INSERT OR REPLACE INTO player_data VALUES (
            :player_name, :matches, :bat_innings, :bat_runs, :high_score, :bat_avg, 
            :bat_sr, :fifties, :hundreds, :bowl_innings, :overs, :wickets, :econ, 
            :bowl_sr, :recent_bat_scores_json, :recent_bowl_figs_json, :role,
            :performance_score, :batting_consistency, :bowling_consistency
        )
    """, {
        **data,
        'recent_bat_scores_json': bat_scores_json,
        'recent_bowl_figs_json': bowl_figs_json,
    })
    
    conn.commit()
    conn.close()

def get_all_player_names():
    """Retrieves all player names from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT player_name FROM player_data ORDER BY player_name")
    names = [row['player_name'] for row in cursor.fetchall()]
    conn.close()
    return names

def get_player_data(player_name):
    """Retrieves all data for a single player."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player_data WHERE player_name = ?", (player_name,))
    row = cursor.fetchone()
    conn.close()
    if row:
        data = dict(row)
        data['recent_bat_scores'] = json.loads(data.get('recent_bat_scores_json', '[]'))
        data['recent_bowl_figs'] = json.loads(data.get('recent_bowl_figs_json', '[]'))
        del data['recent_bat_scores_json']
        del data['recent_bowl_figs_json']
        return data
    return None

def get_players_by_role(role):
    """
    Retrieves player name and calculated scores for a given role,
    ordered by performance_score descending.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            player_name AS name, 
            performance_score, 
            batting_consistency, 
            bowling_consistency 
        FROM player_data 
        WHERE role = ? 
        ORDER BY performance_score DESC
    """, (role,))
    
    players = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return players

def get_all_players_data():
    """
    Retrieves all data for ALL players for the team generator.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            player_name AS name, 
            role, 
            performance_score, 
            batting_consistency, 
            bowling_consistency,
            bat_runs, bat_avg, bat_sr, wickets, econ 
        FROM player_data 
        ORDER BY performance_score DESC
    """)
    players = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return players