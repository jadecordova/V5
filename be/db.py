import sys
from pathlib import Path

def get_database_path():

    """Return the database path for local development and PyInstaller builds."""

    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent

    db_path = base_path / "data" / "valerie.db"

    # Fallback if the file is not found in the bundled location
    if not db_path.exists():
        db_path = Path(__file__).resolve().parent / "data" / "valerie.db"

    return str(db_path)