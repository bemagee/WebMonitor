# WebMonitor

A Python CLI tool to monitor website status, performance, and functional health.

## Features
- **HTTP Monitoring:** Real-time checks for status codes and response times.
- **E2E Testing:** Automated Playwright scripts for functional verification.
- **Performance Metrics:** Measures Page Load and Action/Login times during E2E tests.
- **Visual Diagnostics:** Automatically captures screenshots on E2E failures.
- **Secure Credentials:** Integrated `.env` support for safe password management.

## Installation

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Install Browsers:**
    ```bash
    playwright install chromium
    ```

## Usage

Run the monitor with your configuration file:

```bash
python monitor.py websites.json
```

### Performance Metrics (`E2E_PERF` Column)
- **L:** Page Load time (seconds)
- **A:** Action time (e.g., search or login duration in seconds)

### Diagnostics
If an E2E test fails, look in the `screenshots/` directory for an image showing the site's state at the moment of failure.

## Configuration
- `websites.json`: List of sites and paths to their test scripts.
- `.env`: Store `TEST_USER` and `TEST_PASSWORD`.
