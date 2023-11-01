import pandas as pd
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

# Create a new DataFrame with the desired columns
new_df = df[['Time', 'Balance Before', 'Balance After', 'P&L', 'Action']]

# Calculate the percentage P&L for each trade
new_df['Percent P&L'] = (new_df['P&L'] / new_df['Balance Before']) * 100

# Export the new DataFrame to an HTML file
new_df.to_html('output.html', index=False, justify='center', border=1, bold_rows=True, na_rep='')
