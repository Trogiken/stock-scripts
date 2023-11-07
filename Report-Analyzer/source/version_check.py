import sys

try:
    import requests
except ImportError:
    print("Please install the requests module: pip install requests")
    input("\nPress ENTER to exit...")
    sys.exit()


def get_latest(url: str):
    """Gets the latest version of the script from the GitHub repository."""
    version = None
    try:
        response = requests.get(url, timeout=3)
        version = response.text.strip()
    except Exception:
        pass

    return version
