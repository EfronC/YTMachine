from collections import deque

def tail_log(file_path: str, lines: int = 50) -> list[str]:
    """
    Fetch the last `lines` lines from a file.

    Args:
        file_path: Path to the log file.
        lines: Number of lines to fetch from the end.

    Returns:
        List of lines (each as a string, stripped of trailing newlines).
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.rstrip('\n') for line in deque(f, maxlen=lines)]