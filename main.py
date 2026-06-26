import os
import eel

# Set web files folder and allowed file extensions
eel.init('web')

# Python function that can be called from JavaScript
@eel.expose
def greet(name):
    """Greet a user from Python"""
    return f"Hello {name}! Greetings from Python."

@eel.expose
def get_python_info():
    """Return information from Python"""
    return {
        'message': 'This data comes from Python',
        'python_version': os.sys.version,
    }

# Start the app
if __name__ == '__main__':
    # Open the index.html file in a new window
    eel.start('index.html', size=(1024, 768))
