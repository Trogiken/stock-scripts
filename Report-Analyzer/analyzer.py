"""This program uses the 'Account History' csv file from trading view to create a report"""

import sys
from source.windows_gui import GUI as windows_gui
from source.unix_gui import GUI as unix_gui

version = "beta.2.1.3"  #  TODO Change to beta.2.2.3 when ready to release

# TODO Check if TK operations work on Mac and Linux, if not using Qt6
# TODO Work on commission calculations and usage
# TODO Add export as PDF option
# TODO Add option to export as Excel file
# TODO Create graphs
# TODO Find a way to impliment cross-platform compatibility that doesn't involve so much repeated code. Maybe have one gui class that uses themes


if __name__ == '__main__':
    # check operating system
    if sys.platform.startswith('win'):
        gui = windows_gui(version)
        gui.run()
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        unix_gui(version)
    else:
        print("This program is not compatible with your operating system.")
        input("\nPress ENTER to exit...")
        sys.exit()