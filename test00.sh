#! /usr/bin/env dash

# ==============================================================================
# test00.sh
# Test the slippy quit comman
#
# Written by: Joel Abraham
# For COMP2041/9044 Assignment 1
# ==============================================================================

# Create some files to hold output.

expected_output="$(mktemp)"
actual_output="$(mktemp)"

# Remove the temporary directory when the test is done.

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT

# Testing address that is a number
seq 1 5 | 2041 slippy '3q' > $expected_output 
seq 1 5 | ./slippy '3q' > $actual_output 

# Testing address that is a regex
seq 1 5 | 2041 slippy '/4/q' >> $expected_output 
seq 1 5 | ./slippy '/4/q' >> $actual_output 


diff $expected_output $actual_output && echo "correct implementation" && exit 0

echo "incorrect implementation" && exit 1

