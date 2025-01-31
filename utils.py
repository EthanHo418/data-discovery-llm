from datetime import datetime


def to_epoch(timestamp_str):
    """Convert 'YYYY-MM-DD HH:MM:SS' to epoch (Unix timestamp)."""
    dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")  # Parse string to datetime
    return int(dt.timestamp())  # Convert to epoch time (integer)
