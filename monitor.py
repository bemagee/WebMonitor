import argparse
import json
import requests
import time
import subprocess
import os
import re
import sys

def check_website(name, url):
    try:
        start_time = time.time()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        end_time = time.time()
        
        status_code = response.status_code
        response_time = round((end_time - start_time) * 1000, 2)
        
        return {
            "name": name,
            "url": url,
            "status": "UP" if 200 <= status_code < 400 else "DOWN",
            "code": status_code,
            "time": f"{response_time}ms"
        }
    except requests.exceptions.RequestException as e:
        return {
            "name": name,
            "url": url,
            "status": "ERROR",
            "code": "N/A",
            "time": "N/A",
            "error": str(e)
        }

def run_e2e_test(script_path):
    if not os.path.exists(script_path):
        return "MISSING", "N/A"
    
    try:
        # Run the script and capture output
        cmd = ["py", script_path] if os.name == 'nt' else ["python3", script_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        perf_metrics = "N/A"
        # Search for metrics in stdout
        metrics_match = re.search(r"__METRICS__=(.*)", result.stdout)
        if metrics_match:
            try:
                metrics_data = json.loads(metrics_match.group(1))
                # Format metrics (e.g., L:1.2s A:0.5s)
                perf_metrics = " ".join([f"{k[0]}:{v:.2f}s" for k, v in metrics_data.items()])
            except json.JSONDecodeError:
                perf_metrics = "Parse Err"

        if result.returncode == 0:
            return "PASS", perf_metrics
        else:
            return "FAIL", "See Screenshot"
    except Exception:
        return "ERROR", "N/A"

def main():
    parser = argparse.ArgumentParser(description="Monitor website status and response times.")
    parser.add_argument("config", help="Path to the JSON configuration file.")
    args = parser.parse_args()

    config_dir = os.path.dirname(os.path.abspath(args.config))

    try:
        with open(args.config, 'r') as f:
            data = json.load(f)
            websites = data.get("websites", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading configuration file: {e}")
        return

    # Updated header with E2E_PERF column
    print(f"{'NAME':<20} {'STATUS':<10} {'CODE':<10} {'TIME':<10} {'E2E':<10} {'E2E_PERF':<20} {'URL'}")
    print("-" * 110)

    # Track global success for AAP integration
    global_success = True

    for site in websites:
        name = site.get("name", "Unknown")
        url = site.get("url")
        test_script = site.get("test_script")
        
        if not url:
            print(f"{name:<20} {'SKIP':<10} {'N/A':<10} {'N/A':<10} {'N/A':<10} {'N/A':<20} Missing URL")
            continue
            
        result = check_website(name, url)
        
        status_display = result["status"]
        code_display = result["code"]
        time_display = result["time"]
        e2e_display = "N/A"
        perf_display = "N/A"

        # Update global success based on HTTP status
        if result["status"] != "UP":
            global_success = False

        if result["status"] == "UP" and test_script:
            full_script_path = os.path.join(config_dir, test_script)
            e2e_display, perf_display = run_e2e_test(full_script_path)
            
            # Update global success based on E2E result
            if e2e_display == "FAIL":
                global_success = False
        
        print(f"{name:<20} {status_display:<10} {code_display:<10} {time_display:<10} {e2e_display:<10} {perf_display:<20} {url}")

    if not global_success:
        sys.exit(1)

if __name__ == "__main__":
    main()
