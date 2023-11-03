import os
import sys

# TODO Add monthly, and yearly summarys
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


def analyze_data(account_history_path):
    """Analyze the data from the CSV file and return the dataframe with the results"""
    # Read the CSV file
    acc_df = pd.read_csv(account_history_path, sep=',')

    # remove whitespace from balance columns while keeping it a float
    acc_df['Balance Before'] = acc_df['Balance Before'].str.replace('\xa0', '').astype(float)
    acc_df['Balance After'] = acc_df['Balance After'].str.replace('\xa0', '').astype(float)

    # regex patterns to extract the data we need
    symbol_pattern = r"symbol (\w+:\w+)"
    closed_price_pattern = r"price (\d+\.\d+)"
    shares_pattern = r"for (\d+) shares"
    position_type_pattern = r"Close (long|short) position"

    total_commsission = 0.0

    # Apply the regex patterns to each element of the 'Action' column
    details_list = []
    for _, row in acc_df.iterrows():
        if "Commission" in row['Action']:
            total_commission += float(row['P&L'])
            continue
        position = re.search(position_type_pattern, row['Action']).group(1)  # long or short position
        symbol = re.search(symbol_pattern, row['Action']).group(1)  # symbol of the stock
        quantity = re.search(shares_pattern, row['Action']).group(1)  # quantity of shares
        opened_price = round(float(re.search(closed_price_pattern, row['Action']).group(1)) + ((row['Balance After'] - row['Balance Before']) / int(quantity)), 2)  # price at which the position was opened
        closed_price = round(float(re.search(closed_price_pattern, row['Action']).group(1)), 2)  # price at which the position was closed
        details_list.append({
            'Time': row['Time'],
            'Position': position,
            'Symbol': symbol,
            'Quantity': quantity,
            'Opened Price': opened_price,
            'Closed Price': closed_price,
            'Balance Before': round(row['Balance Before'], 2),
            'Balance After': round(row['Balance After'], 2),
            'P&L': round(row['Balance After'] - row['Balance Before'], 2),
            '%': round((row['Balance After'] - row['Balance Before']) / row['Balance Before'] * 100, 2),
        })

    # Create a new DataFrame with only the columns we need
    details_df = pd.DataFrame(details_list)

    total_return_amount = [details_df['P&L'].sum()]
    total_return_percentage = [round(details_df['%'].sum(), 2)]
    average_return_percentage = [round(details_df['%'].mean(), 2)]
    batting_average = [round(details_df[details_df['P&L'] > 0]['P&L'].count() / details_df['P&L'].count() * 100, 2)]
    average_win_percentage = [round(details_df[details_df['P&L'] > 0]['%'].mean(), 2)]
    average_loss_percentage = [round(details_df[details_df['P&L'] < 0]['%'].mean(), 2)]
    win_loss_ratio_percentage = [round(details_df[details_df['P&L'] > 0]['%'].mean() / abs(details_df[details_df['P&L'] < 0]['%'].mean()), 2)]

    # Create a new DataFrame with only the columns we need for total values
    total_df = pd.DataFrame({
        'Total Return': [f"{total_return_percentage[0]}%"],
        'Average Return': [f"{average_return_percentage[0]}%"],
        'Batting Average': [f"{batting_average[0]}%"],
        'Average Win': [f"{average_win_percentage[0]}%"],
        'Average Loss': [f"{average_loss_percentage[0]}%"],
        'Win Loss Ratio': [f"{win_loss_ratio_percentage[0]}%"],
        'Commission * Not Applied *': f"${total_commsission}",  # DEBUG Make sure this is negative
        'Net Profit': [f"${total_return_amount}"],
        'Gross Profit': "",  # TODO
        'Gross Loss': "",  # TODO
    })

    # Create the pie chart TODO make this a bar graphs of monthly data
    # labels = ['Total Return', 'Average Return', 'Batting Average', 'Average Win', 'Average Loss', 'Win Loss Ratio']
    # sizes = [total_return_percentage[0], average_return_percentage[0], batting_average[0], average_win_percentage[0], abs(average_loss_percentage[0]), win_loss_ratio_percentage[0]]
    # plt.bar(labels, sizes, color=['green', 'green', 'green', 'green', 'red', 'green'])
    # plt.savefig(os.path.join(str(Path(__file__).resolve()), 'output', 'pie_chart.png'))

    return details_df, total_df


def export_html(details_df, total_df, export_location):
    """Export the DataFrame to an HTML file"""
    if os.path.exists(export_location):
        os.remove(export_location)
    
    with open(export_location, 'w') as f:
        f.write('<html>\n')
        f.write('<head>\n')
        f.write('<style>\n')
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
        f.write('<h2>Trade Details</h2>\n')
        f.write(details_df.to_html(index=False, justify='center', border=1, bold_rows=True, na_rep=''))
        f.write('<h2>Total Values</h2>\n')
        f.write(total_df.to_html(index=False, justify='center', border=1, bold_rows=True, na_rep=''))
        # f.write('<img src="pie_chart.png" alt="Pie Chart">\n')
        f.write('</body>\n')
        f.write('</html>\n')


# Create the Tkinter root
root = tk.Tk()
root.title("Report Analyzer")
root.geometry("300x300")
root.resizable(True, True)
root.config(background='cyan')
root.iconphoto(False, tk.PhotoImage(data="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"))

# Create a frame with padding
content_frame = tk.Frame(root, padx=20, pady=20)
content_frame.pack(fill=tk.BOTH, expand=True)

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
        data_frames = analyze_data(account_history_path)
        export_location = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
            
        if export_location:
            export_html(data_frames[0], data_frames[1], export_location)  # TODO Error handling
            if tk.messagebox.askyesno("Success", "HTML file exported successfully. Do you want to open it?"):
                webbrowser.open(export_location)
        else:
            tk.messagebox.showerror("Error", "Please select a valid export location.")


acc_button = tk.Button(content_frame, text="Select 'Account History' CSV", command=get_account_path)
acc_button.configure(bg='grey', fg='black', font=('Arial', 12), width=30)
acc_button.pack()

export_button = tk.Button(content_frame, text="Export HTML", command=export)
export_button.configure(bg='red', fg='white', font=('Arial', 12), width=30)
export_button.pack()

version_label = tk.Label(root, text="Version Beta.1.0.1", font=('Arial', 10))
version_label.pack(side=tk.RIGHT, anchor=tk.S)

root.mainloop()
