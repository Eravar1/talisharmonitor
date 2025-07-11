import json
from datetime import datetime
from pathlib import Path
from .logger import log_message

STATE_FILE = "data/monitor_state.json"

def load_state():
    """Load previous monitoring state"""
    if not Path(STATE_FILE).exists():
        return {}
    
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            
        state = {}
        for game_id, game_data in data.items():
            try:
                state[game_id] = {
                    "last_seen": datetime.fromisoformat(game_data["last_seen"]),
                    "data": game_data["data"]
                }
            except (KeyError, ValueError):
                continue
                
        return state
    except Exception as e:
        log_message(f"⚠️ Failed to load state: {e}")
        return {}

# def save_state(game_cache):
    # """Save current monitoring state"""
    # try:
    #     Path("data").mkdir(exist_ok=True)
    #     serialized = {
    #         game_id: {
    #             "last_seen": data["last_seen"].isoformat(),
    #             "data": data["data"]
    #         }
    #         for game_id, data in game_cache.items()
    #     }
        
    #     with open(STATE_FILE, "w") as f:
    #         json.dump(serialized, f, indent=2)
    # except Exception as e:
    #     log_message(f"⚠️ Failed to save state: {e}")

def save_state(game_cache):
    """Save enhanced game state with both players' data"""
    try:
        Path("data").mkdir(exist_ok=True)
        serialized = {
            game_id: {
                "timestamp": data["last_seen"].isoformat(),
                "player1": data["data"].get("player1_data", {}),
                "player2": data["data"].get("player2_data", {}),
                "game_info": {
                    "format": data["data"].get("format"),
                    "game_id": game_id
                }
            }
            for game_id, data in game_cache.items()
        }
        with open(STATE_FILE, "w") as f:
            json.dump(serialized, f, indent=2)
    except Exception as e:
        log_message(f"⚠️ Failed to save state: {e}")