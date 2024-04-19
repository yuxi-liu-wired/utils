#!/bin/bash

# Check if a folder name was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <folder-path>"
    exit 1
fi

# Assign the folder path to a variable
FOLDER_PATH="$1"

# Find and process .qmd files
find "$FOLDER_PATH" -type f -name "*.qmd" | while read -r file; do
    echo "Processing $file..."
    python proselint.py "$file"
done
