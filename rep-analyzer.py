import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog

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
    'Price': price,  # This is not the price at which the position was opened, add that one too
    'Balance Before': df['Balance Before'],
    'Balance After': df['Balance After'],
    'P&L': df['Balance After'] - df['Balance Before'],
    '%': (df['Balance After'] - df['Balance Before']) / df['Balance Before'] * 100,
})

# Export the new DataFrame to an HTML file
new_df.to_html('output.html', index=False, justify='center', border=1, bold_rows=True, na_rep='')
