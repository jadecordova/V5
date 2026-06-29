import os
import eel

from be.files import get_video_files, process_files, select_folder

# Set web files folder and allowed file extensions ---------------------------------------------------------------------------------
eel.init('web')

# ----------------------------------------------------------------------------------------------------------------------------------
@eel.expose
def Select_Folder():
    return select_folder()
    
# ----------------------------------------------------------------------------------------------------------------------------------
@eel.expose
def Import_Movies(folder):
    
    """Fetches and processes video files from a target folder."""

    raw_files = get_video_files(folder)
    processed_files = process_files(raw_files)
    return processed_files


# ----------------------------------------------------------------------------------------------------------------------------------
# Start the app
if __name__ == '__main__':
    # Open the index.html file in a new window
    eel.start('index.html', size=(1024, 768))
