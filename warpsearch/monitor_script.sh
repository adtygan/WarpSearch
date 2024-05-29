#!/bin/bash
FOLDER=$1

# Print out folder tracked for later reference
echo "[Monitoring folder] $FOLDER"


# Define a function to get the state of the directory
get_state() {
  find $FOLDER -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \)
}

# Initialize previous_state with the state of the directory
previous_state=$(get_state)


# Monitor the ~/Vault directory for changes
fswatch -0 -o $FOLDER | while read -d "" event; do
  # For each event, list current state of directory 
  current_state=$(get_state)
  # Diff current state with previous state
  diff <(echo "$previous_state") <(echo "$current_state") | while read line; do
    if [[ $line == ">"* ]]; then
      python warpsearch/vectorstore.py "${line:2}" 
    elif [[ $line == "<"* && ! -z "${line:2}" ]]; then
      echo "[File Deleted] ${line:2}"
    fi
  done
  previous_state=$current_state
done
