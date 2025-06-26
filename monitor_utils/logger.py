import gzip
import os
from datetime import datetime, timedelta
from pathlib import Path

LOG_DIR = "logs"
COMPRESS_LOGS_OLDER_THAN = 1  # Days before compression
current_log_file = None

def setup_logging():
    """Initialize logging system"""
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    rotate_logs()
    compress_old_logs()

def get_log_path():
    """Generate daily log file path"""
    return Path(LOG_DIR) / f"talishar_matches_{datetime.now().strftime('%Y-%m-%d')}.log"

def rotate_logs():
    """Handle daily log rotation"""
    global current_log_file
    
    new_path = get_log_path()
    if current_log_file and current_log_file.name != new_path.name:
        current_log_file.close()
    
    current_log_file = open(new_path, "a", encoding="utf-8")
    log_message(f"♻️ Rotated to new log file: {new_path.name}")

def compress_old_logs():
    """Compress logs older than threshold"""
    cutoff = datetime.now() - timedelta(days=COMPRESS_LOGS_OLDER_THAN)
    
    for log_file in Path(LOG_DIR).glob("talishar_matches_*.log"):
        try:
            date_str = log_file.stem.split("_")[-1]
            file_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            if file_date < cutoff.date():
                with open(log_file, "rb") as f_in:
                    with gzip.open(f"{log_file}.gz", "wb") as f_out:
                        f_out.writelines(f_in)
                os.remove(log_file)
        except Exception as e:
            print(f"⚠️ Error compressing {log_file}: {e}")

def log_message(message, to_console=True):
    """Log a message with timestamp"""
    global current_log_file
    
    if current_log_file is None:
        rotate_logs()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    current_log_file.write(log_entry)
    current_log_file.flush()
    
    if to_console:
        print(log_entry.strip())