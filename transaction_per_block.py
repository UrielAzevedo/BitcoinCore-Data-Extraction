import os
import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator

# Path to the directory containing block files
block_files_dir = '/home/uriel/work/tcc/scripts/blks_700k-800k'

# Function to parse block files and extract transactions and timestamp
def parse_block_files(directory):
    blocks = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                block_data = json.load(file)
                blocks.append(block_data)
    # Sort blocks by height
    blocks.sort(key=lambda x: x['height'])
    return blocks

# Function to calculate average transactions per day
def calculate_average_transactions(blocks):
    transactions_per_day = {}
    for block in blocks:
        timestamp = datetime.utcfromtimestamp(block['time'])
        date_key = timestamp.date()
        if date_key in transactions_per_day:
            transactions_per_day[date_key].append(block['nTx'])
        else:
            transactions_per_day[date_key] = [block['nTx']]
    # Calculate average transactions per day
    average_transactions_per_day = {date: np.mean(transactions) for date, transactions in transactions_per_day.items()}
    return average_transactions_per_day

# Parse block files and calculate average transactions per day
blocks = parse_block_files(block_files_dir)
average_transactions_per_day = calculate_average_transactions(blocks)

# Extract dates and transactions for plotting
dates = list(average_transactions_per_day.keys())
transactions = list(average_transactions_per_day.values())

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot_date(dates, transactions, linestyle='solid', marker='None')
plt.gca().xaxis.set_major_formatter(DateFormatter('%b\n%Y'))  # Month and year format
plt.gca().xaxis.set_major_locator(MonthLocator())
plt.ylabel('Average Transactions per Block')
plt.title('Average Transactions per Block Over Time (Ordered by Height)')
plt.grid(True)
plt.tight_layout()
plt.show()
