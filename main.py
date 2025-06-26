#!/usr/bin/env python3
import signal
import sys
import os
from datetime import datetime, timedelta
import time
from monitor_utils.logger import setup_logging, log_message
from monitor_utils.api_client import get_active_games, get_game_details
from monitor_utils.state_manager import load_state, save_state
from monitor_utils.deck_parser import format_deck_info

# Configuration
WATCHED_PLAYERS = ["Eravar", "Verso"]
POLL_INTERVAL = 180  # 3 minutes in seconds
GAME_CACHE_DURATION = 3600  # 1 hour in seconds

class TalisharMonitor:
    def __init__(self):
        self.game_cache = {}
        self.should_exit = False
        self.processing_game = False

        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, sig, frame):
        """Handle shutdown signals gracefully"""
        if self.processing_game:
            log_message("⚠️ Received shutdown during game processing, will exit after current game")
        else:
            log_message("🛑 Received shutdown signal, exiting gracefully...")
        self.should_exit = True

    def check_for_target_players(self):
        """Check active games for watched players"""
        current_time = datetime.now()
        active_games = get_active_games()
        new_matches = []

        for game in active_games:
            if self.should_exit:
                break

            game_id = game.get("gameName")
            
            if game_id in self.game_cache:
                self.game_cache[game_id]["last_seen"] = current_time
                continue
                
            self.processing_game = True
            try:
                details = get_game_details(game_id)
            finally:
                self.processing_game = False
                
            if not details:
                continue
                
            self.game_cache[game_id] = {
                "last_seen": current_time,
                "data": details
            }
            
            display_name = details.get("displayName", "")
            if any(player.lower() in display_name.lower() for player in WATCHED_PLAYERS):
                log_message(f"\n🎯 MATCH FOUND IN NEW GAME: {display_name}")
                new_matches.append((game_id, details))
        
        # Clean expired games if not shutting down
        if not self.should_exit:
            expired = [
                gid for gid, data in self.game_cache.items()
                if (current_time - data["last_seen"]).total_seconds() > GAME_CACHE_DURATION
            ]
            for gid in expired:
                del self.game_cache[gid]
        
        return new_matches

    def log_match_details(self, game_id, details, match_type):
        """Log detailed match information"""
        log_message(f"\n=== {match_type} ===")
        log_message(f"Player: {details.get('displayName')}")
        log_message(f"Game ID: {game_id}")
        log_message(f"Deck Info:\n{format_deck_info(details.get('deck'))}")
        log_message(f"🔗 Spectate: https://talishar.net/game/FaB.php?gameID={game_id}&spectator=true")
        log_message(f"📅 First Seen: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def run(self):
        """Main monitoring loop"""
        try:
            # Initialize
            setup_logging()
            log_message(f"\n{'='*50}")
            log_message(f"🔍 Starting Talishar Monitor (Tracking: {', '.join(WATCHED_PLAYERS)})")
            log_message(f"🔄 Checking every {POLL_INTERVAL//60} minutes")
            log_message(f"💾 Cache duration: {GAME_CACHE_DURATION//3600} hour(s)")
            log_message(f"{'='*50}\n")

            # Load previous state
            self.game_cache = load_state()
            if self.game_cache:
                log_message(f"↩️ Loaded previous state with {len(self.game_cache)} cached games")

            # Initial scan
            log_message("🚀 Performing initial scan...")
            initial_matches = self.check_for_target_players()
            for game_id, details in initial_matches:
                if self.should_exit:
                    break
                self.log_match_details(game_id, details, "INITIAL MATCH")

            # Main monitoring loop
            while not self.should_exit:
                try:
                    next_scan_time = datetime.now() + timedelta(seconds=POLL_INTERVAL)
                    log_message(f"\n⏳ Next scan at {next_scan_time.strftime('%Y-%m-%d %H:%M:%S')}", False)

                    # Save state before sleeping
                    save_state(self.game_cache)

                    # Responsive sleep for shutdown
                    for _ in range(POLL_INTERVAL):
                        if self.should_exit:
                            break
                        time.sleep(1)

                    if self.should_exit:
                        break

                    log_message("\n🔄 Scanning for new games...")
                    new_matches = self.check_for_target_players()
                    for game_id, details in new_matches:
                        if self.should_exit:
                            break
                        self.log_match_details(game_id, details, "NEW MATCH")

                except Exception as e:
                    if not self.should_exit:
                        log_message(f"⚠️ Unexpected error: {str(e)}")
                        time.sleep(60)

        except Exception as e:
            log_message(f"⚠️ Critical error: {str(e)}")
        finally:
            # Final cleanup
            try:
                save_state(self.game_cache)
                log_message("🛑 Monitoring stopped")
            except Exception as e:
                print(f"Error during cleanup: {str(e)}")
            os._exit(0)

if __name__ == "__main__":
    monitor = TalisharMonitor()
    monitor.run()