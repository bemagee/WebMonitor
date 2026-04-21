# WebMonitor

A Python CLI tool to monitor website status, performance, and functional health, designed for automated execution via Ansible.

## Features
- **HTTP Monitoring:** Real-time checks for status codes and response times.
- **E2E Testing:** Automated Playwright scripts for functional verification.
- **Performance Metrics:** Measures Page Load and Action/Login times.
- **Visual Diagnostics:** Automatically captures screenshots on E2E failures.
- **AAP Ready:** Built-in support for Ansible Automation Platform scheduling and alerting.

## Installation & Local Usage

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```

2.  **Run Locally:**
    ```bash
    python monitor.py websites.json
    ```

---

## V4: Ansible Automation Platform (AAP) Integration

WebMonitor is designed to run as a scheduled Job Template in AAP.

### 1. Create a Custom Credential Type
In AAP, navigate to **Credential Types** and create a new type (e.g., "WebMonitor Credentials"):
- **Input Configuration (YAML):**
  ```yaml
  fields:
    - id: test_user
      type: string
      label: Test User
    - id: test_password
      type: string
      label: Test Password
      secret: true
  ```
- **Injector Configuration (YAML):**
  ```yaml
  env:
    TEST_USER: "{ { test_user } }"
    TEST_PASSWORD: "{ { test_password } }"
  ```
*(Note: Remove the space between the curly braces in the injector config).*

### 2. Configure the Job Template
1.  **Project:** Point to your GitHub repository.
2.  **Playbook:** Select `ansible/run_monitor.yml`.
3.  **Credentials:** Attach your "WebMonitor Credentials" and your machine/source control credentials.
4.  **Schedule:** Set the desired frequency (e.g., Every 1 hour).

### 3. Alerting
AAP will automatically mark the job as **Failed** if any website is DOWN or an E2E test fails. You can attach Slack or Email notifications to the Job Template to be alerted immediately.

---

## Configuration
- `websites.json`: List of sites and paths to their test scripts.
- `.env`: (Local Only) Store `TEST_USER` and `TEST_PASSWORD`.
