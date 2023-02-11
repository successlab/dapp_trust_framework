#!/bin/bash

# Read the .env file
while read line; do
    # Check if the line starts with a letter (to ignore comments)
    if [[ $line =~ ^[A-Za-z] ]]; then
        # Run the export command on the environment variable
        export $line
    fi
done < .env