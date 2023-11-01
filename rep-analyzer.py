import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog

# TODO add gui window to select file, date range, and output file location/name

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
new_df = pd.DataFrame({
    'Time': df['Time'],
    'position': position,
    'Symbol': symbol,
    'Quantity': quantity,
    'Price *Not buy Price*': price,  # This is not the price at which the position was opened, add that one too
    'Balance Before': df['Balance Before'],
    'Balance After': df['Balance After'],
    'P&L': df['Balance After'] - df['Balance Before'],
    '%': (df['Balance After'] - df['Balance Before']) / df['Balance Before'] * 100,
})

# Create a new DataFrame with only the columns we need for total values
total_df = pd.DataFrame({
    'Total P&L': [new_df['P&L'].sum()],
    'Total %': [new_df['%'].sum()],
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
    f.write(new_df.to_html(index=False, justify='center', border=1, bold_rows=True, na_rep=''))
    f.write('<h2>Total Values</h2>\n')
    f.write(total_df.to_html(index=False, justify='center', border=1, bold_rows=True, na_rep=''))
    f.write('</body>\n')
    f.write('</html>\n')
