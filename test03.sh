#! /usr/bin/env dash

# ==============================================================================
# test03.sh
# Test the slippy substitute command
#
# Written by: Joel Abraham
# ==============================================================================

# Create some files to hold output.

expected_output="$(mktemp)"
actual_output="$(mktemp)"

# Remove the temporary directory when the test is done.

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT

# Testing address that is a number
seq 1 5 | 2041 slippy 's/[15]/zzz/' > $expected_output 
seq 1 5 | ./slippy 's/[15]/zzz/' > $actual_output 

# Testing address that is a regex
seq 100 111 | 2041 slippy 's/11/zzz/' >> $expected_output 
seq 100 111 | ./slippy 's/11/zzz/' >> $actual_output 


diff $expected_output $actual_output && echo "correct implementation" && exit 0

echo "incorrect implementation" && exit 1

