#!/bin/bash

# Define the range of block heights to fetch
start_height=700000
end_height=800000

# Define the number of parallel processes
num_processes=25

# Function to fetch blocks in parallel
fetch_blocks() {
    start=$1
    end=$2
    for ((height=start; height<=end; height++)); do
        # Fetch block for each height and redirect output to a file
        bitcoin-cli getblock $(bitcoin-cli getblockhash $height) > "block_$height.json"
    done
}

# Calculate the number of blocks per process
block_range=$(( ($end_height - $start_height + 1) / $num_processes ))

# Start parallel processes
for ((i=0; i<$num_processes; i++)); do
    start=$(( $start_height + $i * $block_range ))
    end=$(( $start + $block_range - 1 ))
    # Adjust the end height for the last process
    if [ $i -eq $(($num_processes - 1)) ]; then
        end=$end_height
    fi
    # Execute fetch_blocks function in background
    fetch_blocks $start $end &
done

# Wait for all processes to finish
wait
