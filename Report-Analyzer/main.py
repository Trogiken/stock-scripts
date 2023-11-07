"""This program uses the 'Account History' csv file from tradingview to create a report"""

import sys
from source.gui import GUI

version = "beta.2.2.3"

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
    
    GUI(os, version)