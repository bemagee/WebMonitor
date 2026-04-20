# WebMonitor

A simple Python CLI tool to monitor the status, response times, and functional health (E2E) of your favorite websites.

## Features
- Monitor multiple websites from a single JSON configuration file.
- Check HTTP status codes and response times.
- **New:** Automatically run Playwright E2E tests for sites that are "UP".
- Secure credential management using `.env` files.
- Clean console output with status summaries.

## Prerequisites
- Python 3.x
- `pip` (Python package installer)

## Installation

1.  **Clone or navigate to the project directory:**
    ```bash
    cd WebMonitor
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Playwright Browsers:**
    ```bash
    playwright install
    ```

## Configuration

### 1. Websites (`websites.json`)
The tool uses a JSON file to define which websites to monitor. You can optionally add a `test_script` property pointing to a Playwright script.

```json
{
  "websites": [
    {"name": "Google", "url": "https://www.google.com"},
    {
      "name": "My App", 
      "url": "https://app.example.com",
      "test_script": "tests/login_test.py"
    }
  ]
}
```

### 2. Credentials (`.env`)
Create a `.env` file in the root directory to store credentials used by your E2E scripts:

```env
TEST_USER=admin
TEST_PASSWORD=secret
```

## Usage

Run the tool by passing the path to your JSON configuration file:

```bash
python monitor.py websites.json
```

### Example Output
```
NAME                 STATUS     CODE       TIME       E2E        URL
-------------------------------------------------------------------------------------
Google               UP         200        145.23ms   N/A        https://www.google.com
Example with E2E     UP         200        210.12ms   PASS       https://www.example.com
Invalid Site         ERROR      N/A        N/A        N/A        https://this-site-does-not-exist.com
```
