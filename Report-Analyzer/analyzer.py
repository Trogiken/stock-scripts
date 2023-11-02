import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import re
import os
import shutil
from pathlib import Path
from tkinter import filedialog


# TODO add gui window to select file, date range, and output file location/name
# TODO if no date range, sort by months of data into separate tables
# TODO store output data in a separate directory

def analyze_data(account_history_path, history):
    """Analyze the data from the CSV files and return the dataframes with the results"""
    # Read the CSV file
    acc_df = pd.read_csv(account_history_path, sep=',')
    history_df = pd.read_csv(account_history_path, sep=',')

    # remove whitespace from balance columns while keeping it a float
    acc_df['Balance Before'] = acc_df['Balance Before'].str.replace('\xa0', '').astype(float)
    acc_df['Balance After'] = acc_df['Balance After'].str.replace('\xa0', '').astype(float)

    # regex patterns to extract the data we need
    symbol_pattern = r"symbol (\w+:\w+)"
    price_pattern = r"price (\d+\.\d+)"
    shares_pattern = r"for (\d+) shares"
    position_type_pattern = r"Close (long|short) position"

    # Apply the regex patterns to each element of the 'Action' column
    position = acc_df['Action'].apply(lambda x: re.search(position_type_pattern, x).group(1))
    symbol = acc_df['Action'].apply(lambda x: re.search(symbol_pattern, x).group(1))
    quantity = acc_df['Action'].apply(lambda x: re.search(shares_pattern, x).group(1))
    price = acc_df['Action'].apply(lambda x: re.search(price_pattern, x).group(1))

    # Create a new DataFrame with only the columns we need
    details_df = pd.DataFrame({
        'Time': acc_df['Time'],
        'Position': position,
        'Symbol': symbol,
        'Quantity': quantity,
        'Take Profit Price': price,  # This is not the price at which the position was opened, add that one too. Use the close time in the history csv file to match with this data.
        'Balance Before': acc_df['Balance Before'],
        'Balance After': acc_df['Balance After'],
        'P&L': acc_df['Balance After'] - acc_df['Balance Before'],
        '%': (acc_df['Balance After'] - acc_df['Balance Before']) / acc_df['Balance Before'] * 100,
    })

    # total_return_amount = [details_df['P&L'].sum()]
    total_return_percentage = [details_df['%'].sum()]
    average_return_percentage = [details_df['%'].mean()]
    batting_average = [details_df[details_df['P&L'] > 0]['P&L'].count() / details_df['P&L'].count() * 100]
    average_win_percentage = [details_df[details_df['P&L'] > 0]['%'].mean()]
    average_loss_percentage = [details_df[details_df['P&L'] < 0]['%'].mean()]
    win_loss_ratio_percentage = [details_df[details_df['P&L'] > 0]['%'].mean() / abs(details_df[details_df['P&L'] < 0]['%'].mean())]

    # Create a new DataFrame with only the columns we need for total values
    total_df = pd.DataFrame({
        'Total Return': [f"{total_return_percentage[0]:,.2f}%"],
        'Average Return': [f"{average_return_percentage[0]:,.2f}%"],
        'Batting Average': [f"{batting_average[0]:,.2f}%"],
        'Average Win': [f"{average_win_percentage[0]:,.2f}%"],
        'Average Loss': [f"{average_loss_percentage[0]:,.2f}%"],
        'Win Loss Ratio': [f"{win_loss_ratio_percentage[0]:,.2f}%"],
    })

    # Create the pie chart TODO make this a bar graphs of monthly data
    # labels = ['Total Return', 'Average Return', 'Batting Average', 'Average Win', 'Average Loss', 'Win Loss Ratio']
    # sizes = [total_return_percentage[0], average_return_percentage[0], batting_average[0], average_win_percentage[0], abs(average_loss_percentage[0]), win_loss_ratio_percentage[0]]
    # plt.bar(labels, sizes, color=['green', 'green', 'green', 'green', 'red', 'green'])
    # plt.savefig(os.path.join(str(Path(__file__).resolve()), 'output', 'pie_chart.png'))

    return details_df, total_df 


def export_html(details_df, total_df):
    """Export the DataFrame to an HTML file"""
    output_directory = os.path.join(str(Path(__file__).resolve().parents[0]), 'output')
    export_file_location = os.path.join(output_directory, 'report.html')

    if os.path.exists(output_directory):
        # remove dir even if files are inside
        shutil.rmtree(output_directory)
    os.makedirs(output_directory)
    
    with open(export_file_location, 'w') as f:
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
root.iconphoto(False, tk.PhotoImage(file=os.path.join(str(Path(__file__).resolve().parents[0]), 'ico.png')))

# Create a frame with padding
content_frame = tk.Frame(root, padx=20, pady=20)
content_frame.pack(fill=tk.BOTH, expand=True)

account_history_path = ""
history_path = ""

def get_account_path(): # TODO add correct csv file check
    """Open csv file and store path in global variable"""
    global account_history_path
    account_history_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if account_history_path:
        acc_button.configure(bg='green', fg='white')
    else:
        acc_button.configure(bg='grey', fg='black')

def get_history_path():  # TODO add correct csv file check
    """Open csv file and store path in global variable"""
    global history_path
    history_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if history_path:
        history_button.configure(bg='green', fg='white')
    else:
        history_button.configure(bg='grey', fg='black')

def export():
    """Check if both csv files are selected, analyze data, and export html file"""
    if account_history_path == "" or history_path == "":
        tk.messagebox.showerror("Error", "Please select both account history and history CSV files.")
    else:
        data_frames = analyze_data(account_history_path, history_path)
        export_html(data_frames[0], data_frames[1])


acc_button = tk.Button(content_frame, text="Select 'Account History' CSV", command=get_account_path)
acc_button.configure(bg='grey', fg='black', font=('Arial', 12), width=30)
acc_button.pack()

history_button = tk.Button(content_frame, text="Select 'History' CSV", command=get_history_path)
history_button.configure(bg='grey', fg='black', font=('Arial', 12), width=30)
history_button.pack()

export_button = tk.Button(content_frame, text="Export HTML", command=export)
export_button.configure(bg='red', fg='white', font=('Arial', 12), width=30)
export_button.pack()

root.mainloop()
