# Python/Eel/JavaScript Desktop App

A desktop application scaffold built with Python backend, Eel framework, and JavaScript/HTML/CSS frontend.

## Project Structure

```
.
├── hello.py              # Main Python entry point
├── requirements.txt      # Python dependencies
├── web/                  # Frontend files
│   ├── index.html       # Main HTML file
│   ├── css/
│   │   └── style.css    # Stylesheet
│   └── js/
│       └── main.js      # JavaScript logic
└── README.md            # This file
```

## Setup

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Installation

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

```bash
python hello.py
```

The application window will open automatically. You can interact with Python functions from the JavaScript frontend.

## Development

### Backend (Python)
- Edit `hello.py` to add Python functions
- Use the `@eel.expose` decorator to expose functions to JavaScript
- Functions are automatically available in JavaScript

### Frontend (JavaScript)
- Edit `web/index.html` for HTML structure
- Edit `web/css/style.css` for styling
- Edit `web/js/main.js` for JavaScript logic
- Call Python functions using `eel.function_name(args)(callback)`

## Building an Executable

To build a standalone .exe file:

```bash
pyinstaller --onedir --windowed --add-data "web;web" hello.py
```

The executable will be in the `dist/` folder.

## Communication

### Python to JavaScript
- Use `@eel.expose` decorator on Python functions
- Call from JavaScript: `eel.function_name()(callback)`

### JavaScript to Python
- Exposed Python functions are automatically callable from JavaScript
- Results are passed to callback functions

## License

MIT

## Support

For issues or questions about Eel, see: https://github.com/ChrisKnott/Eel
