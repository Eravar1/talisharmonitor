import requests
from datetime import datetime
import time
from .logger import log_message

API_BASE = "https://api.talishar.net/game/APIs/"
TIMEOUT = 10
MAX_RETRIES = 3

def get_active_games():
    """Fetch list of active games"""
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                f"{API_BASE}GetGameList.php",
                timeout=TIMEOUT
            )
            response.raise_for_status()
            return response.json().get("gamesInProgress", [])
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                log_message(f"⚠️ Failed to get active games: {e}", False)
                return []
            time.sleep(2)

def get_game_details(game_id):
    """Fetch detailed game info"""
    for player_id in [1, 2]:
        try:
            response = requests.post(
                f"{API_BASE}GetLobbyInfo.php",
                json={"gameName": game_id, "playerID": player_id},
                timeout=TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            log_message(f"⚠️ Game {game_id} detail error: {e}", False)
    return None