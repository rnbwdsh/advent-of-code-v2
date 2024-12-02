#!/bin/bash

count=0

while read -r line; do
    # Skip empty lines
    if [ -z "$line" ]; then
        continue
    fi

    # Split the line into an array of numbers
    read -ra nums <<< "$line"

    # If there's only one number, print the line and increment the count
    if [ "${#nums[@]}" -eq 1 ]; then
        echo "$line"
        ((count++))
        continue
    fi

    # Initialize flags
    non_strict_asc=true
    non_strict_desc=true

    # Check all consecutive pairs
    for (( i=0; i<${#nums[@]}-1; i++ )); do
        diff=$(( ${nums[i+1]} - ${nums[i]} ))
        if [ "$diff" -gt 3 ] || [ "$diff" -le 0 ]; then
            non_strict_asc=false
        fi
        if [ "$diff" -lt -3 ] || [ "$diff" -ge 0 ]; then
            non_strict_desc=false
        fi
    done

    # Print the line and increment the count if it is non-strictly ascending or descending
    if [ "$non_strict_asc" = true ] || [ "$non_strict_desc" = true ]; then
        echo "$line"
        ((count++))
    fi
done < 02.in

# Print the total count of matching lines
echo "Total matching lines: $count"