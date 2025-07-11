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

# def get_game_details(game_id):
#     """Fetch detailed game info"""
#     for player_id in [1, 2]:
#         try:
#             response = requests.post(
#                 f"{API_BASE}GetLobbyInfo.php",
#                 json={"gameName": game_id, "playerID": player_id},
#                 timeout=TIMEOUT
#             )
#             if response.status_code == 200:
#                 return response.json()
#         except requests.exceptions.RequestException as e:
#             log_message(f"⚠️ Game {game_id} detail error: {e}", False)
#     return None
            
# def get_complete_game_details(game_id):
#     """Fetch both players' perspectives"""
#     game_data = {
#         "player1_data": None,
#         "player2_data": None,
#         "format": None
#     }
    
#     for player_id in [1, 2]:
#         try:
#             response = requests.post(
#                 f"{API_BASE}GetLobbyInfo.php",
#                 json={"gameName": game_id, "playerID": player_id},
#                 timeout=TIMEOUT
#             )
#             if response.status_code == 200:
#                 data = response.json()
#                 if player_id == 1:
#                     game_data["player1_data"] = data
#                     game_data["format"] = data.get("deck", {}).get("format")
#                 else:
#                     game_data["player2_data"] = data
#         except requests.exceptions.RequestException:
#             continue
            
#     print("\n"*4)
#     print(game_data)
#     print("\n"*4)

#     return game_data if game_data["player1_data"] or game_data["player2_data"] else None

# def get_complete_game_details(game_id):
#     """Fetch both players' perspectives"""
#     game_data = {
#         "player1_data": None,
#         "player2_data": None,
#         "format": None
#     }
    
#     for player_id in [1, 2]:
#         try:
#             response = requests.post(
#                 f"{API_BASE}GetLobbyInfo.php",
#                 json={"gameName": game_id, "playerID": player_id},
#                 timeout=TIMEOUT
#             )
#             if response.status_code == 200:
#                 data = response.json()
#                 if player_id == 1:
#                     game_data["player1_data"] = data
#                 else:
#                     game_data["player2_data"] = data
                
#                 # Set format from whichever player responds first
#                 if game_data["format"] is None and data.get("deck"):
#                     game_data["format"] = data["deck"].get("format")
                    
#         except requests.exceptions.RequestException:
#             continue
            
#     return game_data if (game_data["player1_data"] or game_data["player2_data"]) else None
# # In api_client.py
def get_complete_game_details(game_id):
    """More robust game details fetching"""
    if not game_id:
        return None
        
    game_data = {
        "player1_data": None,
        "player2_data": None,
        "format": None
    }
    
    for player_id in [1, 2]:
        try:
            response = requests.post(
                f"{API_BASE}GetLobbyInfo.php",
                json={"gameName": game_id, "playerID": player_id},
                timeout=TIMEOUT
            )
            if response.status_code == 200:
                data = response.json()
                if not data:
                    continue
                    
                player_key = f"player{player_id}_data"
                game_data[player_key] = data
                
                # Safely get format
                if not game_data["format"] and isinstance(data.get("deck"), dict):
                    game_data["format"] = data["deck"].get("format")
                    
        except Exception as e:
            log_message(f"⚠️ Error fetching {game_id} player {player_id} data: {str(e)}")
            continue
            
    return game_data if (game_data["player1_data"] or game_data["player2_data"]) else None