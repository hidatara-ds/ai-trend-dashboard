from datetime import datetime

def format_number(val: float | int) -> str:
    """Format numbers into K / M short notation."""
    if val is None:
        return "0"
    n = float(val)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}K"
    else:
        return str(int(n))

def format_relative_time(iso_str: str) -> str:
    """Format ISO timestamp into relative time string (e.g. 2h ago)."""
    try:
        dt = datetime.fromisoformat(iso_str)
        now = datetime.utcnow()
        diff = now - dt
        seconds = diff.total_seconds()
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            return f"{int(seconds / 60)}m ago"
        elif seconds < 86400:
            return f"{int(seconds / 3600)}h ago"
        else:
            return f"{int(seconds / 86400)}d ago"
    except Exception:
        return "recently"
