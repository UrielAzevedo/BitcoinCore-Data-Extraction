import os
import json
import re
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def parse_block_file(file_path):
    with open(file_path, 'r') as f:
        block_data = json.load(f)
        timestamp = block_data['time']
        nonce = block_data['nonce']
        return timestamp, nonce

def calculate_hash_rate(block_timestamps):
    hash_rates = []
    prev_timestamp = None
    for timestamp in block_timestamps:
        if prev_timestamp is not None:
            time_diff = timestamp - prev_timestamp
            if time_diff <= 0:
                # Skip calculating hash rate if time difference is non-positive
                prev_timestamp = timestamp  # Update prev_timestamp for next iteration
                continue
            # Hash rate = 2^32 / time_diff (since Bitcoin uses 32-bit nonce)
            hash_rate = 2**32 / time_diff
            hash_rates.append(hash_rate)
        prev_timestamp = timestamp
    return hash_rates

def plot_hash_rate_over_time(block_timestamps, hash_rates):
    timestamps = [datetime.fromtimestamp(ts) for ts in block_timestamps[:len(hash_rates)]]
    plt.plot(timestamps, hash_rates)  
    plt.xlabel('Time')
    plt.ylabel('Hash Rate (hashes per second)')
    plt.title('Estimated Hash Rate Over Time')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()
    plt.show()

def main():
    block_file_path = '/home/uriel/work/tcc/scripts/blks_700k-800k'  # Adjust this path to your Bitcoin block files
    block_timestamps = []
    block_files = [f for f in os.listdir(block_file_path) if re.match(r'block_\d+\.json', f)]
    block_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))
    for file_name in block_files:
        file_path = os.path.join(block_file_path, file_name)
        timestamp, _ = parse_block_file(file_path)
        block_timestamps.append(timestamp)
    
    hash_rates = calculate_hash_rate(block_timestamps)
    plot_hash_rate_over_time(block_timestamps, hash_rates)

if __name__ == "__main__":
    main()
