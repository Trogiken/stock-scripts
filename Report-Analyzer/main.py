"""
This program uses the 'Account History' csv file from tradingview to create a report

Compile Instructions:
1. Create a virtual environment and install the required packages
2. Install pyinstaller
3. Activate the virtual environment and run the following command:
    pyinstaller --noconfirm --onefile --windowed --add-data "path/to/version.txt;."  "path/to/main.py"
"""

import os
import sys
import pyupgrader
from source.gui import GUI

man = pyupgrader.UpdateManager(r'https://raw.githubusercontent.com/Trogiken/stock-scripts/pyupgrader-integration/Report-Analyzer/.pyupgrader', os.path.dirname(__file__))

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
    
    GUI(os, man)
