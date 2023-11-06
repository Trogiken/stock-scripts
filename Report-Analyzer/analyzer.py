"""This program uses the 'Account History' csv file from trading view to create a report"""

import sys
from source.windows_gui import run_windows_gui
from source.unix_gui import run_unix_gui

# TODO Check if TK operations work on Mac and Linux, if not using Qt6
# TODO Add export as PDF option
# TODO Create graphs


if __name__ == '__main__':
    # check operating system
    if sys.platform.startswith('win'):
        run_windows_gui()
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        run_unix_gui()
    else:
        print("This program is not compatible with your operating system.")
        input("\nPress ENTER to exit...")
        sys.exit()