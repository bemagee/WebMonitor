# WebMonitor

A simple Python CLI tool to monitor the status and response times of your favorite websites.

## Features
- Monitor multiple websites from a single JSON configuration file.
- Check HTTP status codes and response times.
- Clean console output.

## Prerequisites
- Python 3.x
- `pip` (Python package installer)

## Installation

1.  **Clone or navigate to the project directory:**
    ```bash
    cd WebMonitor
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
    Or simply install directly:
    ```bash
    pip install requests
    ```

## Configuration

The tool uses a JSON file to define which websites to monitor. Create a file (e.g., `websites.json`) with the following format:

```json
{
  "websites": [
    {"name": "Google", "url": "https://www.google.com"},
    {"name": "My Blog", "url": "https://example.com"}
  ]
}
```

## Usage

Run the tool by passing the path to your JSON configuration file:

```bash
python monitor.py websites.json
```

### Example Output
```
NAME                 STATUS     CODE       TIME       URL
----------------------------------------------------------------------
Google               UP         200        145.23ms   https://www.google.com
Example              UP         200        210.12ms   https://www.example.com
Invalid Site         ERROR      N/A        N/A        https://this-site-does-not-exist.com
```
