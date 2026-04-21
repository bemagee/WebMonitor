import argparse
import json
import requests
import time
import subprocess
import os

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
        return "MISSING"
    
    try:
        # Run the script and wait for it to finish
        # We use 'py' launcher if on windows, or just 'python'
        cmd = ["py", script_path] if os.name == 'nt' else ["python3", script_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return "PASS"
        else:
            return "FAIL"
    except Exception:
        return "ERROR"

def main():
    parser = argparse.ArgumentParser(description="Monitor website status and response times.")
    parser.add_argument("config", help="Path to the JSON configuration file.")
    args = parser.parse_args()

    # Get the directory of the config file to resolve relative paths
    config_dir = os.path.dirname(os.path.abspath(args.config))

    try:
        with open(args.config, 'r') as f:
            data = json.load(f)
            websites = data.get("websites", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading configuration file: {e}")
        return

    # Header with new E2E column
    print(f"{'NAME':<20} {'STATUS':<10} {'CODE':<10} {'TIME':<10} {'E2E':<10} {'URL'}")
    print("-" * 85)

    for site in websites:
        name = site.get("name", "Unknown")
        url = site.get("url")
        test_script = site.get("test_script")
        
        if not url:
            print(f"{name:<20} {'SKIP':<10} {'N/A':<10} {'N/A':<10} {'N/A':<10} Missing URL")
            continue
            
        result = check_website(name, url)
        
        status_display = result["status"]
        code_display = result["code"]
        time_display = result["time"]
        e2e_display = "N/A"

        # Only run E2E if the site is UP and a script is defined
        if result["status"] == "UP" and test_script:
            # Resolve relative script path relative to the config file
            full_script_path = os.path.join(config_dir, test_script)
            e2e_display = run_e2e_test(full_script_path)
        
        print(f"{name:<20} {status_display:<10} {code_display:<10} {time_display:<10} {e2e_display:<10} {url}")

if __name__ == "__main__":
    main()
