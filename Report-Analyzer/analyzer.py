"""This program uses the 'Account History' csv file from trading view to create a report"""

import os
import sys

# TODO Format HTML better
# TODO Check if TK operations work on Mac and Linux, if not using Qt6

import_error = False

try:
    import webbrowser
except ImportError:
    import_error = True
    print("Please install webbrowser package: pip install webbrowser")
try:
    import pandas as pd
except ImportError:
    import_error = True
    print("Please install pandas package: pip install pandas")
try:
    import matplotlib.pyplot as plt
except ImportError:
    import_error = True
    print("Please install matplotlib package: pip install matplotlib")
try:
    import tkinter as tk
    from tkinter import filedialog
except ImportError:
    import_error = True
    print("Please install tkinter package: pip install tkinter")
try:
    import re
except ImportError:
    import_error = True
    print("Please install re package: pip install re")
try:
    import shutil
except ImportError:
    import_error = True
    print("Please install shutil package: pip install shutil")

if import_error:
    input("\nPress ENTER to exit...")
    sys.exit()


def analyze_data(account_history_path, time_frame):
    """Analyze the data from the CSV file and return the dataframe with the results"""
    account_df = pd.read_csv(account_history_path, sep=',')

    # remove whitespace from balance columns while keeping it a float
    account_df['Balance Before'] = account_df['Balance Before'].str.replace('\xa0', '').astype(float)
    account_df['Balance After'] = account_df['Balance After'].str.replace('\xa0', '').astype(float)

    # regex patterns to extract the data
    symbol_pattern = r"symbol (\w+:\w+)"
    closed_price_pattern = r"price (\d+(?:\.\d+)?)"
    shares_pattern = r"for (\d+) shares"
    position_type_pattern = r"Close (long|short) position"

    dataframes = {}
    df_dict = {}

    for _, row in account_df.iterrows():
        # separate by time frame
        time = ""
        if time_frame == 1:  # daily
            time = row['Time'].split(' ')[0]
            if time not in df_dict:
                df_dict[time] = {"details": [], "commission": 0.0}
        elif time_frame == 2:  # monthly
            time = row['Time'].split(' ')[0].split('-')[0] + '-' + row['Time'].split(' ')[0].split('-')[1]
            if time not in df_dict:
                df_dict[time] = {"details": [], "commission": 0.0}
        elif time_frame == 3:  # quarterly # DEBUG
            time = row['Time'].split(' ')[0].split('-')[0] + '-' + str(int(row['Time'].split(' ')[0].split('-')[1]) // 3)
            if time not in df_dict:
                df_dict[time] = {"details": [], "commission": 0.0}
        elif time_frame == 4:  # yearly
            time = row['Time'].split(' ')[0].split('-')[0]
            if time not in df_dict:
                df_dict[time] = {"details": [], "commission": 0.0}

        if "Commission" in row['Action']:
            df_dict[time]["commission"] += float(row['P&L'])
            continue

        df_dict[time]["details"].append({
            'Time': row['Time'],
            'Position': re.search(position_type_pattern, row['Action']).group(1),  # long or short position,
            'Symbol': re.search(symbol_pattern, row['Action']).group(1),  # symbol of the stock,
            'Quantity': re.search(shares_pattern, row['Action']).group(1),  # quantity of shares,
            'Opened Price': round(float(re.search(closed_price_pattern, row['Action']).group(1)) + ((row['Balance After'] - row['Balance Before']) / int(re.search(shares_pattern, row['Action']).group(1))), 2),  # price at which the position was opened,
            'Closed Price': round(float(re.search(closed_price_pattern, row['Action']).group(1)), 2),  # price at which the position was closed
            'Balance Before': round(row['Balance Before'], 2),
            'Balance After': round(row['Balance After'], 2),
            'P&L': round(row['Balance After'] - row['Balance Before'], 2),
            '%': round((row['Balance After'] - row['Balance Before']) / row['Balance Before'] * 100, 2),
        })

    for time_frame in df_dict:
        details_df = pd.DataFrame(df_dict[time_frame]["details"])

        total_commission = round(df_dict[time_frame]["commission"], 2)
        number_of_trades = [details_df['P&L'].count()]
        number_of_long_trades = [details_df[details_df['Position'] == 'long']['P&L'].count()]
        number_of_short_trades = [details_df[details_df['Position'] == 'short']['P&L'].count()]
        net_profit_amount = [round(details_df['P&L'].sum(), 2)]
        total_profit_amount = [round(details_df[details_df['P&L'] > 0]['P&L'].sum(), 2)]
        total_loss_amount = [round(details_df[details_df['P&L'] < 0]['P&L'].sum(), 2)]
        total_return_percentage = [round(details_df['%'].sum(), 2)]
        average_return_percentage = [round(details_df['%'].mean(), 2)]
        batting_average = [round(details_df[details_df['P&L'] > 0]['P&L'].count() / details_df['P&L'].count() * 100, 2)]
        average_win_percentage = [round(details_df[details_df['P&L'] > 0]['%'].mean(), 2)]
        average_loss_percentage = [round(details_df[details_df['P&L'] < 0]['%'].mean(), 2)]
        win_loss_ratio_percentage = [round(details_df[details_df['P&L'] > 0]['%'].mean() / abs(details_df[details_df['P&L'] < 0]['%'].mean()), 2)]

        total_df = pd.DataFrame({
            'Number of Trades': [number_of_trades[0]],
            'Number of Long Trades': [number_of_long_trades[0]],
            'Number of Short Trades': [number_of_short_trades[0]],
            'Total Return': [f"{total_return_percentage[0]}%"],
            'Average Return': [f"{average_return_percentage[0]}%"],
            'Batting Average': [f"{batting_average[0]}%"],
            'Average Win': [f"{average_win_percentage[0]}%"],
            'Average Loss': [f"{average_loss_percentage[0]}%"],
            'Win Loss Ratio': [f"{win_loss_ratio_percentage[0]}%"],
            'Commission': [f"${total_commission}"],  # FIXME Commission is static accross all days
            'Net Profit': [f"${net_profit_amount[0]}"],
            'Gross Profit': [f"${total_profit_amount[0]}"],
            'Gross Loss': [f"${total_loss_amount[0]}"],
        })

        dataframes[time_frame] = {"details": details_df, "total": total_df}

    return dataframes


def export_html(dataframes: dict, export_location):
    """Export the DataFrame to an HTML file"""
    if os.path.exists(export_location):
        os.remove(export_location)
    
    with open(export_location, 'w') as f:
        f.write('<html>\n')
        f.write('<head>\n')
        f.write('<style>\n')
        f.write('h1 {\n')
        f.write('  margin-bottom: 0px;\n')
        f.write('}\n')
        f.write('table {\n')
        f.write('  border-collapse: collapse;\n')
        f.write('  width: 100%;\n')
        f.write('}\n')
        f.write('th, td {\n')
        f.write('  text-align: left;\n')
        f.write('  padding: 8px;\n')
        f.write('}\n')
        f.write('tr:nth-child(even) {\n')
        f.write('  background-color: #f2f2f2;\n')
        f.write('}\n')
        f.write('th {\n')
        f.write('  background-color: #4CAF50;\n')
        f.write('  color: white;\n')
        f.write('}\n')
        f.write('</style>\n')
        f.write('</head>\n')
        f.write('<body>\n')
        for time_frame in dataframes:
            details_df = dataframes[time_frame]["details"]
            total_df = dataframes[time_frame]["total"]
            f.write(f'<h1>{time_frame}</h1>\n')
            f.write('<hr>\n')
            f.write(total_df.to_html(index=False, justify='center', border=1, bold_rows=True, na_rep=''))
            f.write(details_df.to_html(index=False, justify='center', border=1, bold_rows=True, na_rep=''))
            
        f.write('</body>\n')
        f.write('</html>\n')


# Create the Tkinter root
root = tk.Tk()
root.title("Report Analyzer")
root.geometry("400x300")
root.resizable(False, False)
root.iconphoto(False, tk.PhotoImage(data="iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAADsAAAA7AF5KHG9AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAABcVJREFUWIXdl21MnWcZx3/X/ZzDAc44QAuFUmSlY2tpm9qkbkvUOPuhjWmaJnaBw6A0Nk02M1+21EwX4wtqzYyZJM4YLV9cgEN5idYtmYlrls1orC+0SdW4TgqWQsvcAU4Pp4cD5zzPffmhgHAGzZljMfFKrg/Pfd3X/f/dL9dzPw/8j03eV7aqNJzlE0b5NLAfqELZiDCplhsinLeGcwPNcmHdARp69OPG8rzfYUtlEanKIu4N+MgzAlZhPsP8RIJrbycIuZa3xPJM73EZXBeAcLc+K4ZTO8pwQwUUj0xzbTrJRmvZoEJclGLHMLmxkFtbN1IbmyV6dZJCC1/va5GfvC+Axi5tD/g4+pFqqt+aZHhqlmJVfugYzp1tlivAna2JsFuEowY+X15IbFsZNYNjRDPKmf4WOf1fATRF9KQRvv1wDZWD44ylXV63eXxhoFFur5XTHNFSV+ko8LNv3xZq/jDKpAdP9rXIL94TQGunbsoYrjxcQ+HlCcZn05zrb5Vnwt36NEr9XVIv9R2joynCmaJ89m8vo/LPN0im5rj/5ZOSMLkCpB2+Wn4P0WiSt1MZ/rlzmK8shJ5DuCyGi9muwj8QvoWIhpJ8bibFrdsZ4qX5xPLzOQWQE8AnX1cf0FpXRt3INEXG8KW2NrEAKCIwpcr3Ft0qR3pbpCNg6dKFVe54QjICp4YmcR7YxDajnMgZYNNNPprnkEilSahl6Gyz/GV53MvjZUe4b9E1j4bVxultld+6HnFrsY5D4LEe3ePLBUBgV3GA5DuzpNTwanbcmeeAFb6x9JyGpm5Npy2PrzLcq9Ekhwr9pGfm2ZkTgMLmgA8nlcZFGcuOewF+R4YnlrcZi2t8RD2bNRnheipNusCPzqSoygnAKD65s5mrVo1vjr3W8NmVSmSsy+nsTbaKLs5KBckJACE65+Hl+3AEqrPDLlw1wsCKFMX1lJlViGsKAvhvJUmj3MwJwBMuxecI1ldQMh7nIPDNFWIO96ErD55CxghXNGssIxwsL2TLeIy4wN9zAgjO88eUn5JgHkXG4YFwp+7uOy5/WxLzGBZn5QqoUiuG7wPeYltjt37MCKWOwXE90n2tcjmnMnzxhMwpdI9MMbS1hIQ6tLe16VKuMRwWKF3hwg7gsCjPAzx+Rv1Ae10Z7lCUEYQXIcf3wMIsn/tXgspNRVQWOtS9Wcd3AcTwNZQPq2XfcseSEeFEX6u0oyozQV4I5bEhFKBkOsUGH/wAILdDCDgOjyiYwTGiD9VQMzhGS7hLy/0eT3Udl+RaeQ39WuxE6Aj4eGhPFR+6cJ2owhcjx2QGcryMmiL6GVVOWzgo8GSBj0P7qql58x2Gp2cJobQ7hp/3tMjIYs5jPbrDWh5FeKo8SKyujNqLY0xkXH7W2ypti/3WBGg6q1vV41mEDMoRPA70HWeoMcKPBA47QsGOCmzQT9HwNNdjKcrVco/CFEKZA/HSIFPbNlAbTzE1NElA4Tu9LfLCcp1VARq6dLsRXqsKMRu9TUHG0ld/lS9fqeOnCjt9cCgj7DXKj/0Ooc0h5iuLqA348Hl652DNW9ITca5NzBB0Pa5Zw6mBFvlTtta7AMKduhvD+e3luNUlVKdd3AujRF3lBkrC5nFk6QNEVcIRDgBHRXgEuFctASApwqgKr1nh3ECz/GatlV4B0BDRvY7y6/oKMptDbFlsn8vg/n6UGRH2Z9+E71q9fnUGGsW7W5/ltlSG4W590FHO76rAWy4O4FrmFBBlzU+vRXsv4rBQhuFufVCEV3ZV4FYUsXl5h5l5EhfHSKvydM+x/5zy9TIJd+puMbyxpwpbFqR8eTA+R/ziOJ61nOxvlV+utziAEYdPlRQQzRaPpYgNjuNZaP2gxAGMzxKJzRG8HmN0sXF6ltilG6hCuL9FfvVBicNCFTRH9H4P3thehg34Cfz1JsYzPHq38llXAIBwp9aLw0tqKbQODXf7ofy/sn8Dpxhpdb4xu1QAAAAASUVORK5CYII="))

# Create a frame with padding
content_frame = tk.Frame(root)
content_frame.pack(fill=tk.BOTH, expand=True)
content_frame.config(padx=15, pady=15, background='teal', highlightbackground='black', highlightthickness=2)

# Create a container frame
container_frame = tk.Frame(content_frame)
container_frame.pack(fill=tk.BOTH, expand=True)
container_frame.config(padx=20, pady=20)

# Create a horizontal frame for radio buttons
radio_button_frame = tk.Frame(container_frame)
radio_button_frame.pack(fill=tk.BOTH, expand=True)
# radio_button_frame.config(padx=5, pady=5)

# Create a vertical frame for the file buttons
file_button_frame = tk.Frame(container_frame)
file_button_frame.pack(fill=tk.BOTH, expand=True)
# file_button_frame.config(padx=5, pady=5)

# Create a frame for the version label
version_frame = tk.Frame(container_frame)
version_frame.pack(fill=tk.BOTH, expand=True)

# Initialize values
radio_var = tk.IntVar()
radio_var.set(4)
account_history_path = ""

def get_account_path(): # TODO add correct csv file check
    """Open csv file and store path in global variable"""
    global account_history_path
    account_history_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if account_history_path:
        acc_button.configure(bg='green', fg='white')
        export_button.configure(bg='blue', fg='white')
    else:
        acc_button.configure(bg='grey', fg='black')
        export_button.configure(bg='red', fg='white')

def export():
    """Check if both csv files are selected, analyze data, and export html file"""
    if account_history_path == "":
        tk.messagebox.showerror("Error", f"Please select the account history CSV file.")
    else:
        data_frames = analyze_data(account_history_path, radio_var.get())
        export_location = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
            
        if export_location:
            export_html(data_frames, export_location)  # TODO Error handling
            if tk.messagebox.askyesno("Success", "HTML file exported successfully. Do you want to open it?"):
                webbrowser.open(export_location)
        else:
            tk.messagebox.showerror("Error", "Please select a valid export location.")


# Create and label radio buttons
report_title_label = tk.Label(radio_button_frame, text="Time Frame of Report")
report_title_label.pack(side=tk.TOP, anchor=tk.N)
report_title_label.config(font=('Arial', 12))


tk.Radiobutton(radio_button_frame, text="Daily", variable=radio_var, value=1, font=('Arial', 11)).pack(side=tk.LEFT, anchor=tk.N)
tk.Radiobutton(radio_button_frame, text="Monthly", variable=radio_var, value=2, font=('Arial', 11)).pack(side=tk.LEFT, anchor=tk.N)
tk.Radiobutton(radio_button_frame, text="Quarterly", variable=radio_var, value=3, font=('Arial', 11)).pack(side=tk.LEFT, anchor=tk.N)
tk.Radiobutton(radio_button_frame, text="Yearly", variable=radio_var, value=4, font=('Arial', 11)).pack(side=tk.LEFT, anchor=tk.N)

# Account History button
acc_button = tk.Button(file_button_frame, text="Select 'Account History' CSV", command=get_account_path)
acc_button.configure(bg='grey', fg='black', font=('Arial', 12), width=30)
acc_button.pack(pady=2)

# Export HTML button
export_button = tk.Button(file_button_frame, text="Export HTML", command=export)
export_button.configure(bg='red', fg='white', font=('Arial', 12), width=30)
export_button.pack(pady=2)

# Bind enter and leave events to change button borders
def on_enter(event):
    event.widget.original_highlightbackground = event.widget.cget("highlightbackground")
    event.widget.original_highlightthickness = event.widget.cget("highlightthickness")
    event.widget.original_borderwidth = event.widget.cget("borderwidth")
    event.widget.config(highlightbackground='black', highlightthickness=2, borderwidth=3)

def on_leave(event):
    event.widget.config(highlightbackground=event.widget.original_highlightbackground, highlightthickness=event.widget.original_highlightthickness, borderwidth=event.widget.original_borderwidth)

acc_button.bind("<Enter>", on_enter)
acc_button.bind("<Leave>", on_leave)

export_button.bind("<Enter>", on_enter)
export_button.bind("<Leave>", on_leave)

# Create version label
version_label = tk.Label(version_frame, text="Version Beta.1.1.1", font=('Arial', 10))  # TODO Change version nuber
version_label.pack(side=tk.RIGHT, anchor=tk.S)

root.mainloop()
