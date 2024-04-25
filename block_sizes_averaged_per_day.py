import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import json
import os

# Function to process JSON files and extract timestamps and block sizes
def process_json_files(directory):
    block_data = []
    for filename in os.listdir(directory):
        if filename.startswith("block_") and filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                try:
                    data = json.load(file)
                    data['height'] = int(data['height'])
                    block_data.append(data)
                except json.decoder.JSONDecodeError as e:
                    print(f"Error decoding {filename}: {e}")
    # Sort the block data based on timestamp
    sorted_data = sorted(block_data, key=lambda x: x['time'])
    return sorted_data

# Define the directory where the JSON files are located
directory = '/home/uriel/work/tcc/scripts/blks_700k-800k/test_samples'

# Process JSON files to extract timestamps and block sizes
blocks = process_json_files(directory)

# Extract timestamps and block sizes
timestamps = [datetime.utcfromtimestamp(int(block['time'])) for block in blocks]
block_sizes = [block['size'] for block in blocks]

# Aggregate block sizes by day
daily_data = {}
for timestamp, size in zip(timestamps, block_sizes):
    day = timestamp.date()
    if day not in daily_data:
        daily_data[day] = []
    daily_data[day].append(size)

# Calculate daily averages
daily_averages = {}
for day, sizes in daily_data.items():
    daily_averages[day] = sum(sizes) / len(sizes)

# Convert block sizes from bytes to megabytes
for day, average_size in daily_averages.items():
    daily_averages[day] = average_size / (1024 * 1024)  # Convert from bytes to megabytes

# Sort daily averages by date
sorted_dates = sorted(daily_averages.keys())

# Extract sorted dates and corresponding daily averages
sorted_daily_averages = [daily_averages[date] for date in sorted_dates]

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(sorted_dates, sorted_daily_averages, linestyle='-', marker='o', color='b')
plt.title('Average Block Sizes per Day')
plt.xlabel('Date')
plt.ylabel('Average Block Size (MB)')
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Set major ticks to months
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format to display year-month
plt.grid(True)
plt.tight_layout()
plt.show()
