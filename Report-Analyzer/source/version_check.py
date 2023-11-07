import requests

def get_version():
    version = None
    try:
        response = requests.get("https://raw.githubusercontent.com/Trogiken/stock-scripts/Version-Checking/Report-Analyzer/version.txt")
        version = response.text.strip()
    except Exception:
        pass

    return version
