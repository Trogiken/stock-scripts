"""This program uses the 'Account History' csv file from tradingview to create a report"""

import sys
from source.gui import GUI

current_version = "beta.2.3.3"
# TODO Change url's once merged
program_url = "https://github.com/Trogiken/stock-scripts/tree/Version-Checking/Report-Analyzer"
version_url = "https://raw.githubusercontent.com/Trogiken/stock-scripts/Version-Checking/Report-Analyzer/version.txt"

# TODO Work on commission calculations and usage
# TODO Add export as PDF option
# TODO Add option to export as Excel file
# TODO Create graphs


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
