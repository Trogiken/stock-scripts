import requests

try:
    response = requests.get("https://github.com/Trogiken/stock-scripts/tree/master/Report-Analyzer/version.txt")
except Exception:
    pass

print(response.json())