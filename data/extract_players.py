import json
import os
from collections import defaultdict

# Configuration
INPUT_FILE = 'data\monitor_state.json'  # Your large monitor file
OUTPUT_FILE = 'data\player_heroes.json'  # Persistent storage

def load_existing_data():
    """Load existing player data from the persistent file if it exists"""
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r') as f:
            try:
                data = json.load(f)
                # Convert back to defaultdict for easier handling
                result = defaultdict(list, data)
                return result
            except json.JSONDecodeError:
                # File exists but is empty/corrupt - start fresh
                return defaultdict(list)
    return defaultdict(list)

def save_data(data):
    """Save the player data to the persistent file"""
    with open(OUTPUT_FILE, 'w') as f:
        # Convert defaultdict to regular dict for JSON serialization
        json.dump(dict(data), f, indent=2)

def process_monitor_file(monitor_data, existing_data):
    """Process the monitor file and update the player data"""
    for game_id, game_data in monitor_data.items():
        # Process player1
        p1_name = game_data['player1']['displayName']
        p1_hero = game_data['player1']['deck']['heroName']
        if p1_hero not in existing_data[p1_name]:
            existing_data[p1_name].append(p1_hero)
        
        # Process player2
        p2_name = game_data['player2']['displayName']
        p2_hero = game_data['player2']['deck']['heroName']
        if p2_hero not in existing_data[p2_name]:
            existing_data[p2_name].append(p2_hero)
    
    return existing_data

def main():
    # Load existing player data
    player_data = load_existing_data()
    
    # Load the monitor file
    with open(INPUT_FILE, 'r') as f:
        monitor_data = json.load(f)
    
    # Process the monitor file and update player data
    updated_data = process_monitor_file(monitor_data, player_data)
    
    # Save the updated data
    save_data(updated_data)
    
    # Print results
    print("Player Hero Database:")
    print("=" * 40)
    for name, heroes in sorted(updated_data.items()):
        print(f"{name}: {', '.join(heroes)}")
    
    print(f"\nData saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()