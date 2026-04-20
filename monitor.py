import argparse
import json
import requests
import time

def check_website(name, url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
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

def main():
    parser = argparse.ArgumentParser(description="Monitor website status and response times.")
    parser.add_argument("config", help="Path to the JSON configuration file.")
    args = parser.parse_args()

    try:
        with open(args.config, 'r') as f:
            data = json.load(f)
            websites = data.get("websites", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading configuration file: {e}")
        return

    print(f"{'NAME':<20} {'STATUS':<10} {'CODE':<10} {'TIME':<10} {'URL'}")
    print("-" * 70)

    for site in websites:
        name = site.get("name", "Unknown")
        url = site.get("url")
        
        if not url:
            print(f"{name:<20} {'SKIP':<10} {'N/A':<10} {'N/A':<10} Missing URL")
            continue
            
        result = check_website(name, url)
        
        status_display = result["status"]
        code_display = result["code"]
        time_display = result["time"]
        
        print(f"{name:<20} {status_display:<10} {code_display:<10} {time_display:<10} {url}")

if __name__ == "__main__":
    main()
