import requests

def get_version():
    """Gets the latest version of the script from the GitHub repository."""
    version = None
    try:
        response = requests.get("https://raw.githubusercontent.com/Trogiken/stock-scripts/Version-Checking/Report-Analyzer/version.txt")  # TODO Change url to main branch
        version = response.text.strip()
    except Exception:
        pass

    return version
