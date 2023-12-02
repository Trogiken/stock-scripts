"""
This program uses the 'Account History' csv file from tradingview to create a report

Compile Instructions:
1. Create a virtual environment and install the required packages
2. Install pyinstaller
3. Activate the virtual environment and run the following command:
    pyinstaller --noconfirm --onefile --windowed --add-data "path/to/version.txt;."  "path/to/main.py"
"""

import sys
from source.gui import GUI
from pathlib import Path

try:
    with open(Path(__file__).resolve().parent / "version.txt", "r") as f:
        current_version = str(f.read().strip())
except BaseException:
    current_version = None

program_url = "https://github.com/Trogiken/stock-scripts/tree/master/Report-Analyzer"
version_url = "https://raw.githubusercontent.com/Trogiken/stock-scripts/master/Report-Analyzer/version.txt"


if __name__ == '__main__':
    os = None

    # check operating system
    if sys.platform.startswith('win'):
        os = "windows"
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        os = "unix"
    else:
        print("This program is not compatible with your operating system.")
        input("\nPress ENTER to exit...")
        sys.exit()
    
    GUI(os, current_version, version_url, program_url)
