from datetime import datetime
import sys
import os

import_error = False

try:
    import re
except ImportError:
    import_error = True
    print("Please install re package: pip install re")
try:
    import pandas as pd
except ImportError:
    import_error = True
    print("Please install pandas package: pip install pandas")

if import_error:
    input("\nPress ENTER to exit...")
    sys.exit()


def analyze_data(account_history_path: str, time_frame: int, custom_range=(None, None)) -> dict:
    """Analyze the data from the CSV file and return the dataframe with the results"""
    account_df = pd.read_csv(account_history_path, sep=',')

    # remove whitespace from balance columns while keeping it a float
    account_df['Balance Before'] = account_df['Balance Before'].apply(lambda x: float(str(x).replace('\xa0', '')))
    account_df['Balance After'] = account_df['Balance After'].apply(lambda x: float(str(x).replace('\xa0', '')))
    
    # regex patterns to extract the data
    symbol_pattern = r"symbol (\w+:\w+)"
    closed_price_pattern = r"price (\d+(?:\.\d+)?)"
    shares_pattern = r"for (\d+(\.\d+)?) shares"
    position_type_pattern = r"Close (long|short) position"

    dataframes = {}
    df_dict = {}
    
    # TODO Add another option for custom time frame
    for _, row in account_df.iterrows():
        date = row['Time'].split(' ')[0]
        year = date.split('-')[0]
        month = date.split('-')[1]
        #  day = date.split('-')[2]

        # separate by time frame
        time_interval = ""
        if time_frame == 1:  # daily
            time_interval = date
        elif time_frame == 2:  # monthly
            time_interval = year + '-' + month
        elif time_frame == 3:  # quarterly # DEBUG Check format of exported csv for single digit months ex: 2021-1 vs 2021-01
            time_interval = year + '-'
            if month in ["01", "02", "03"]:
                time_interval += "Q1"
            elif month in ["04", "05", "06"]:
                time_interval += "Q2"
            elif month in ["07", "08", "09"]:
                time_interval += "Q3"
            elif month in ["10", "11", "12"]:
                time_interval += "Q4"
            else:
                raise ValueError("Invalid month")
        elif time_frame == 4:  # yearly
            time_interval = year
        elif time_frame == 5:  # custom
            start, end = custom_range
            start = datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.strptime(end, "%Y-%m-%d").date()
            date = datetime.strptime(date, "%Y-%m-%d").date()
            if start is None or end is None:
                raise ValueError("Empty custom range")
            if start > end:
                raise ValueError("Invalid custom range (start > end)")

            if start <= date <= end:
                time_interval = date
            else:
                continue
        else:
            raise ValueError("Invalid time frame")

        if time_interval not in df_dict:
            df_dict[time_interval] = {"details": [], "commission": 0.0}

        if "Commission" in row['Action']:  # Add commission to the total and skip rest of processing
            df_dict[time_interval]["commission"] += float(row['Realized P&L (value)'])
            continue

        # Add the trade details to the dictionary for the time interval
        df_dict[time_interval]["details"].append({
            'Time': row['Time'],
            'Position': re.search(position_type_pattern, row['Action']).group(1),  # long or short position,
            'Symbol': re.search(symbol_pattern, row['Action']).group(1),  # symbol of the stock,
            'Quantity': re.search(shares_pattern, row['Action']).group(1),  # quantity of shares,
            # Removed because it's never right           'Opened Price': round(float(row['Balance Before']) - (float(re.search(closed_price_pattern, row['Action']).group(1)) * int(re.search(shares_pattern, row['Action']).group(1))) / int(re.search(shares_pattern, row['Action']).group(1)), 2),
            'Closed Price': round(float(re.search(closed_price_pattern, row['Action']).group(1)), 2),  # price at which the position was closed
            'Balance Before': round(float(row['Balance Before']), 2),
            'Balance After': round(float(row['Balance After']), 2),
            'P&L': round(float(row['Balance After']) - float(row['Balance Before']), 2),
            '%': round((float(row['Balance After']) - float(row['Balance Before'])) / float(row['Balance Before']) * 100, 2),
        })

    # Create total dataframes and append to dataframes dictionary
    for time_frame in df_dict:
        details_df = pd.DataFrame(df_dict[time_frame]["details"])
        if details_df.empty:  # Possible if only a commission was made that day and no trades
            # only display commisson
            total_df = pd.DataFrame({
                'Number of Trades': [0],
                'Number of Long Trades': [0],
                'Number of Short Trades': [0],
                'Total Return': [0],
                'Average Return': [0],
                'Batting Average': [0],
                'Average Win': [0],
                'Average Loss': [0],
                'Win Loss Ratio': [0],
                'Commission': [f"${round(df_dict[time_frame]['commission'], 2)}"],
                'Net Profit': [0],
                'Gross Profit': [0],
                'Gross Loss': [0],
            })
            dataframes[time_frame] = {"details": details_df, "total": total_df}
            continue

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
            'Commission': [f"${total_commission}"],
            'Net Profit': [f"${net_profit_amount[0]}"],
            'Gross Profit': [f"${total_profit_amount[0]}"],
            'Gross Loss': [f"${total_loss_amount[0]}"],
        })

        dataframes[time_frame] = {"details": details_df, "total": total_df}

    return dataframes


def export_html(dataframes: dict, export_location: str) -> None:
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
