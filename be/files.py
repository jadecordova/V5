import json
import re
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from typing import Any, Dict

import eel

VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.mpg'}

#------------------------------------------------------------------------------------------- process_files
def process_files(files):
    
    """
    Takes a list of file dicts, applies parse_filename and get_video_data
    to each, and reports progress to the JS frontend after each file.
    """

    eel.ShowProgressDialog()  # Show the progress dialog before starting    

    total = len(files)
    results = []

    for index, file in enumerate(files):
        parsed   = parse_filename(file['filename'])
        video    = extract_video_metadata(file['full_path'])

        results.append({**file, **parsed, **video})

        eel.UpdateProgress(index + 1, total)()

    return results


#------------------------------------------------------------------------------------------- bytes_to_human
def bytes_to_human(size_bytes: str | int) -> str:
    
    """Convert bytes to human readable format (e.g. 1.45 GB)."""

    try:
        size = int(size_bytes)
    except (TypeError, ValueError):
        return "0 B"

    if size == 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1

    return f"{size:.2f} {units[i]}"


#------------------------------------------------------------------------------------------- get_empty_metadata
def get_empty_metadata() -> Dict[str, any]:
    
    """Returns safe default values when metadata extraction fails."""

    return {
        "size": "0",
        "size_human": "0 B",
        "duration": "00:00:00",
        "width": 0,
        "height": 0,
        "codec": "unknown",
        "fps": 0.0
    }


#------------------------------------------------------------------------------------------- extract_video_metadata
def extract_video_metadata(file_path: str) -> Dict[str, any]:

    """
    Extracts metadata using local ffprobe and returns:
        - size (raw bytes as string)
        - size_human (human readable, e.g. "1.45 GB")
        - duration
        - width, height
        - codec
        - fps
    """

    try:
        ffprobe = get_ffmpeg_path()

        command = [
            ffprobe,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(file_path)
        ]

        result = subprocess.run(command, capture_output=True, text=True, timeout=15)

        if result.returncode != 0:
            print(f"ffprobe error: {result.stderr.strip()}")
            return get_empty_metadata()

        data = json.loads(result.stdout)

        # Format info
        format_info = data.get("format", {})
        size_bytes = format_info.get("size", "0")
        duration_sec = float(format_info.get("duration", 0))

        # Video stream
        video_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})

        width = int(video_stream.get("width", 0))
        height = int(video_stream.get("height", 0))
        codec = video_stream.get("codec_name", "unknown")

        # FPS calculation
        fps_str = video_stream.get("r_frame_rate", "0/1")
        try:
            num, den = map(int, fps_str.split('/'))
            fps = round(num / den, 2) if den != 0 else 0.0
        except:
            fps = 0.0

        # Format duration
        hours = int(duration_sec // 3600)
        minutes = int((duration_sec % 3600) // 60)
        seconds = int(duration_sec % 60)
        duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        return {
            "size": size_bytes,                    # raw bytes (for DB)
            "size_human": bytes_to_human(size_bytes),  # human readable
            "duration": duration_str,
            "width": width,
            "height": height,
            "codec": codec,
            "fps": fps
        }

    except Exception as e:
        print(f"Metadata extraction failed for {file_path}: {e}")
        return get_empty_metadata()
    
    
#------------------------------------------------------------------------------------------- get_ffmpeg_path
def get_ffmpeg_path(binary: str = "ffprobe") -> str:
    
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys._MEIPASS)
    else:
        # Go up one level from be/ to reach project root
        base_dir = Path(__file__).resolve().parent.parent

    ffmpeg_dir = base_dir / "ffmpeg"

    possible_paths = [
        ffmpeg_dir / "bin" / f"{binary}.exe",
        ffmpeg_dir / f"{binary}.exe",
        ffmpeg_dir / "bin" / binary,
        ffmpeg_dir / binary,
    ]

    for path in possible_paths:
        if path.exists():
            return str(path)

    raise FileNotFoundError(f"{binary} not found in {ffmpeg_dir}")


#------------------------------------------------------------------------------------------- parse_filename
def parse_filename(filename: str, extension: str = "") -> Dict[str, Any]:

    """Parses one filename. Returns stars, tags, flag, rename."""

    stem = Path(filename).stem.strip()

    # Pattern 1: Original files (needs rename)
    pattern1 = re.compile(
    r'^(.*?)\s+'                    
    r'(\d{3,})\s+'                  
    r'(?:([A-Z][^,]*?(?:,\s*[A-Z][^,]*?)*)\s+)?'  # Tags and space now optional together
    r'\+(\d+)'                      
    r'(?:\s+([A-Za-z]+))?$'         
    )

    # Pattern 2: Already renamed files
    pattern2 = re.compile(
        r'^(.*?)\s+-\s+'                
        r'(?:([A-Z][^,-]*?(?:,\s*[A-Z][^,-]*?)*)\s+-\s+)?'  
        r'(\d+)\s+-\s+'                 
        r'\[(\d+)\]'                    
        r'(?:\s+([A-Za-z]+))?$'         
    )

    # Pattern 1 match
    match = pattern1.match(stem)
    if match:
        stars_str, _, tags_str, __, flag = match.groups()
        stars = [s.strip() for s in stars_str.split(',') if s.strip()]
        tags = [t.strip() for t in (tags_str or "").split(',') if t.strip()]
        return {
            "stars": stars,
            "tags": tags,
            "flag": flag,
            "valid": True
        }

    # Pattern 2 match
    match = pattern2.match(stem)
    if match:
        stars_str, tags_str, __, ___, flag = match.groups()
        stars = [s.strip() for s in stars_str.split(',') if s.strip()]
        tags = [t.strip() for t in (tags_str or "").split(',') if t.strip()]
        return {
            "stars": stars,
            "tags": tags,
            "flag": flag,
            "valid": True
        }

    return {
        "stars": [],
        "tags": [],
        "flag": None,
        "valid": False
    }
    

#------------------------------------------------------------------------------------------- select_folder
def select_folder():
    
    """Opens a folder select dialog and returns the selected path, or None if cancelled."""

    root = tk.Tk()
    root.withdraw()      # hide the root window
    root.wm_attributes('-topmost', True)  # dialog appears on top
    folder_path = filedialog.askdirectory()
    root.destroy()
    return folder_path if folder_path else None


#------------------------------------------------------------------------------------------- get_video_files
def get_video_files(folder_path):

    """Returns a list of dicts for all video files in the given folder."""

    videos = []
    
    # Convert input string to a Path object
    base_path = Path(folder_path)

    for entry in base_path.iterdir():
        if entry.is_file():
            if entry.suffix.lower() in VIDEO_EXTENSIONS:
                videos.append({
                    "full_path": str(entry.resolve()), # Yields clean, absolute system paths
                    "filename": entry.stem,            # Automatically gets name without extension
                    "extension": entry.suffix.lower()  # Gets the extension (e.g., '.mp4')
                })
    return videos

