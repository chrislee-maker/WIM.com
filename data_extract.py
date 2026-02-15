import requests
import json
import time
import os
from pathlib import Path

# Your setup
API_KEY = "PKIBXaexPrQ7kjXPtsTEADiYfD3hE3Zla1zYkZqk"
BASE_URL = "https://api.sportradar.com/nba/trial/v8/en"
OUTPUT_DIR = "./nba_data"

Path(OUTPUT_DIR).mkdir(exist_ok=True)

def api_call(endpoint):
    url = f"{BASE_URL}/{endpoint}?api_key={API_KEY}"
    response = requests.get(url)
    time.sleep(1)  # Rate limit
    return response.json()

def get_game_data(game_id):
    pbp = api_call(f"games/{game_id}/pbp.json")
    with open(f"{OUTPUT_DIR}/pbp_{game_id}.json", 'w') as f:
        json.dump(pbp, f)
    
    summary = api_call(f"games/{game_id}/summary.json")
    with open(f"{OUTPUT_DIR}/summary_{game_id}.json", 'w') as f:
        json.dump(summary, f)

# Get already downloaded game IDs
existing_games = {f.replace('pbp_', '').replace('.json', '') 
                  for f in os.listdir(OUTPUT_DIR) if f.startswith('pbp_')}

# Get schedule
schedule = api_call("games/2024/REG/schedule.json")
completed = [g for g in schedule['games'] if g['status'] == 'closed']

# Filter out already downloaded games
new_games = [g for g in completed if g['id'] not in existing_games]

MAX_NEW_GAMES = 1000  # Change this to import more/less each run

print(f"Already have: {len(existing_games)} games")
print(f"Available new games: {len(new_games)}")
print(f"Collecting {min(MAX_NEW_GAMES, len(new_games))} new games...\n")

# Download new games
for i, game in enumerate(new_games[:MAX_NEW_GAMES], 1):
    game_id = game['id']
    print(f"[{i}/{min(MAX_NEW_GAMES, len(new_games))}] {game['away']['alias']} @ {game['home']['alias']}", end=" ")
    
    try:
        get_game_data(game_id)
        print("✓")
    except Exception as e:
        print(f"✗ {e}")

print(f"\nDone! Total games: {len(existing_games) + min(MAX_NEW_GAMES, len(new_games))}")