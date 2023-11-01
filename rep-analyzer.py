import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import re
from tkinter import filedialog


# TODO add gui window to select file, date range, and output file location/name
# TODO store output data in a separate directory

# Create the Tkinter root
root = tk.Tk()
root.withdraw()

# Ask the user to select a CSV file
file_path = filedialog.askopenfilename()

# Read the CSV file
df = pd.read_csv(file_path, sep=',')

# remove whitespace from balance columns while keeping it a float
df['Balance Before'] = df['Balance Before'].str.replace('\xa0', '').astype(float)
df['Balance After'] = df['Balance After'].str.replace('\xa0', '').astype(float)

# regex patterns to extract the data we need
symbol_pattern = r"symbol (\w+:\w+)"
price_pattern = r"price (\d+\.\d+)"
shares_pattern = r"for (\d+) shares"
position_type_pattern = r"Close (long|short) position"

# Apply the regex patterns to each element of the 'Action' column
position = df['Action'].apply(lambda x: re.search(position_type_pattern, x).group(1))
symbol = df['Action'].apply(lambda x: re.search(symbol_pattern, x).group(1))
quantity = df['Action'].apply(lambda x: re.search(shares_pattern, x).group(1))
price = df['Action'].apply(lambda x: re.search(price_pattern, x).group(1))

# Create a new DataFrame with only the columns we need
details_df = pd.DataFrame({
    'Time': df['Time'],
    'Position': position,
    'Symbol': symbol,
    'Quantity': quantity,
    'Take Profit Price': price,  # This is not the price at which the position was opened, add that one too. Use the close time in the history csv file to match with this data.
    'Balance Before': df['Balance Before'],
    'Balance After': df['Balance After'],
    'P&L': df['Balance After'] - df['Balance Before'],
    '%': (df['Balance After'] - df['Balance Before']) / df['Balance Before'] * 100,
})

# total_return_amount = [details_df['P&L'].sum()]
total_return_percentage = [details_df['%'].sum()]
average_return_percentage = [details_df['%'].mean()]
batting_average = [details_df[details_df['P&L'] > 0]['P&L'].count() / details_df['P&L'].count() * 100]
average_win_percentage = [details_df[details_df['P&L'] > 0]['%'].mean()]
average_loss_percentage = [details_df[details_df['P&L'] < 0]['%'].mean()]
win_loss_ratio_percentage = [details_df[details_df['P&L'] > 0]['%'].mean() / abs(details_df[details_df['P&L'] < 0]['%'].mean())]

# Create the pie chart
labels = ['Total Return', 'Average Return', 'Batting Average', 'Average Win', 'Average Loss', 'Win Loss Ratio']
sizes = [total_return_percentage[0], average_return_percentage[0], batting_average[0], average_win_percentage[0], abs(average_loss_percentage[0]), win_loss_ratio_percentage[0]]
plt.bar(labels, sizes, color=['green', 'green', 'green', 'green', 'red', 'green'])

# Save the pie chart as an image
plt.savefig('pie_chart.png')

# Create a new DataFrame with only the columns we need for total values
total_df = pd.DataFrame({
    'Total Return': [f"{total_return_percentage[0]:,.2f}%"],
    'Average Return': [f"{average_return_percentage[0]:,.2f}%"],
    'Batting Average': [f"{batting_average[0]:,.2f}%"],
    'Average Win': [f"{average_win_percentage[0]:,.2f}%"],
    'Average Loss': [f"{average_loss_percentage[0]:,.2f}%"],
    'Win Loss Ratio': [f"{win_loss_ratio_percentage[0]:,.2f}%"],
})

# Export the new DataFrame and total DataFrame to an HTML file with CSS styling
with open('output.html', 'w') as f:
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
    f.write('<img src="pie_chart.png" alt="Pie Chart">\n')
    f.write('</body>\n')
    f.write('</html>\n')
