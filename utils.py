from collections import deque
import os
from typing import List

PLAYLIST_DIR = "./playlists"

def tail_log(file_path: str, lines: int = 50) -> List[str]:
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


def _get_playlist_path(filename: str) -> str:
    """Return full path to playlist file."""
    return os.path.join(PLAYLIST_DIR, filename)


def _read_playlist_lines(path: str) -> List[str]:
    """Read playlist file and return stripped lines."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Playlist '{path}' does not exist.")

    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def _write_playlist_lines(path: str, lines: List[str]) -> None:
    """Write lines back to playlist file."""
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(f"{line}\n")

def _append_playlist_lines(path: str, lines: List[str]) -> None:
    """Write lines back to playlist file."""
    with open(path, "a", encoding="utf-8") as f:
        for line in lines:
            f.write(f"{line}\n")


# ---------------------------------------------------------
# Check if song exists
# ---------------------------------------------------------
def song_exists(playlist_filename: str, song_path: str) -> bool:
    path = _get_playlist_path(playlist_filename)
    lines = _read_playlist_lines(path)

    return song_path in lines


# ---------------------------------------------------------
# Add song (if not already present)
# ---------------------------------------------------------
def add_song(playlist_filename: str, song_path: str) -> bool:
    """
    Adds song to playlist.
    Returns True if added, False if already existed.
    """
    path = _get_playlist_path(playlist_filename)
    lines = _read_playlist_lines(path)

    if song_path in lines:
        return False  # already exists

    lines.append(song_path)
    _write_playlist_lines(path, lines)
    return True

def add_songs(playlist_filename: str, song_paths: List[str]) -> bool:
    """
    Adds song to playlist.
    Returns True if added, False if already existed.
    """
    path = _get_playlist_path(playlist_filename)
    lines = _read_playlist_lines(path)

    for song_path in song_paths:
        if song_path in lines:
            continue
        else:
            lines.append(song_path)

    _write_playlist_lines(path, lines)
    return True


# ---------------------------------------------------------
# Remove song (if present)
# ---------------------------------------------------------
def remove_song(playlist_filename: str, song_path: str) -> bool:
    """
    Removes song from playlist.
    Returns True if removed, False if not found.
    """
    path = _get_playlist_path(playlist_filename)
    lines = _read_playlist_lines(path)

    if song_path not in lines:
        return False

    lines = [line for line in lines if line != song_path]
    _write_playlist_lines(path, lines)
    return True

# ---------------------------------------------------------
# Create Playlist
# ---------------------------------------------------------
def create_playlist(playlist_filename: str, overwrite: bool = False) -> bool:
    """
    Creates a new empty M3U8 playlist file with #EXTM3U header.

    Args:
        playlist_filename (str): Name of the playlist file (e.g., "mylist.m3u8")
        overwrite (bool): If True, overwrite existing file.

    Returns:
        bool: True if created, False if file already exists and overwrite=False
    """
    os.makedirs(PLAYLIST_DIR, exist_ok=True)

    path = os.path.join(PLAYLIST_DIR, playlist_filename)

    if os.path.exists(path) and not overwrite:
        return False

    with open(path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")

    return True