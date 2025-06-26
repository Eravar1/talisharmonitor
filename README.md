# Talishar.net Match Monitor

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A persistent monitoring bot that tracks specific players on [Talishar.net](https://talishar.net), the Flesh and Blood TCG online client.

## Features

- 🎯 **Player Tracking**: Monitor matches for configurable player lists
- 🃏 **Deck Analysis**: Logs complete decklists and equipment
- 📊 **Persistent Monitoring**: Maintains state across restarts
- 📅 **Automated Logging**: Daily log rotation with Gzip compression

## Installation

1. Clone the repository:
   ```bash
    git clone https://github.com/yourusername/talishar-monitor.git
    cd talishar-monitor
    ```
2. Install dependencies:
    ```bash
        pip install -r requirements.txt
    ```
## Configuration
Edit these variables in main.py:

    ```python
        WATCHED_PLAYERS = ["Player1", "Player2"]  # Players to track
        POLL_INTERVAL = 180  # Check every 3 minutes (in seconds)
    ```
##Usage
Run the monitor:

```bash
python main.py
```

##File Structure
```text
talishar-monitor/
├── main.py                 # Main application
├── monitor_utils/          # Core modules
│   ├── __init__.py
│   ├── logger.py           # Log management
│   ├── api_client.py       # Talishar API interactions
│   ├── state_manager.py    # Persistent state
│   └── deck_parser.py      # Deck analysis
├── logs/                   # Auto-generated logs
├── data/                   # Persistent state files
└── requirements.txt        # Dependencies
```