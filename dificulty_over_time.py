import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def parse_block_file(file_path):
    with open(file_path, 'r') as f:
        block_data = json.load(f)
        timestamp = block_data['time']
        difficulty = block_data['difficulty']
        return timestamp, difficulty

def plot_difficulty_over_time(block_timestamps, difficulties):
    timestamps = [datetime.fromtimestamp(ts) for ts in block_timestamps]
    plt.plot(timestamps, difficulties)
    plt.xlabel('Time')
    plt.ylabel('Difficulty')
    plt.title('Bitcoin Difficulty Over Time')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()
    plt.show()

def main():
    block_file_path = '/home/uriel/work/tcc/scripts/blks_700k-800k'  # Adjust this path to your Bitcoin block files
    block_timestamps = []
    block_difficulties = []
    block_files = [f for f in os.listdir(block_file_path) if f.endswith('.json')]
    block_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    for file_name in block_files:
        file_path = os.path.join(block_file_path, file_name)
        timestamp, difficulty = parse_block_file(file_path)
        block_timestamps.append(timestamp)
        block_difficulties.append(difficulty)
    
    plot_difficulty_over_time(block_timestamps, block_difficulties)

if __name__ == "__main__":
    main()
