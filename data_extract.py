import requests
import json
import time
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

# Get schedule
schedule = api_call("games/2024/REG/schedule.json")
completed = [g for g in schedule['games'] if g['status'] == 'closed']

print(f"Found {len(completed)} completed games")
print(f"Collecting 100 games (will take ~3.5 minutes)...\n")

# Download 100 games
for i, game in enumerate(completed[:100], 1):
    game_id = game['id']
    print(f"[{i}/100] {game['away']['alias']} @ {game['home']['alias']}", end=" ")
    
    try:
        get_game_data(game_id)
        print("✓")
    except Exception as e:
        print(f"✗ {e}")

print(f"\nDone! 100 games saved to {OUTPUT_DIR}/")