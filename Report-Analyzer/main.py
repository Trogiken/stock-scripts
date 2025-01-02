"""
This program uses the 'Account History' csv file from tradingview to create a report

Compile Instructions:
1. Create a virtual environment and install the required packages
2. Install pyinstaller
3. Activate the virtual environment and run the following command:
    pyinstaller --noconfirm --onefile --windowed "path/to/main.py"
"""

import sys
from source.gui import GUI

VERSION = "2.5.6b1"


if __name__ == '__main__':
    OS_TYPE = None

    # check operating system
    if sys.platform.startswith('win'):
        OS_TYPE = "windows"
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        OS_TYPE = "unix"
    else:
        print("This program is not compatible with your operating system.")
        input("\nPress ENTER to exit...")
        sys.exit()

    GUI(OS_TYPE, VERSION)
