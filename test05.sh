#! /usr/bin/env dash

# ==============================================================================
# test06.sh
# Test the slippy -n command
#
# Written by: Joel Abraham
# ==============================================================================

# Create some files to hold output.

expected_output="$(mktemp)"
actual_output="$(mktemp)"

# Remove the temporary directory when the test is done.

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT

# Testing address that is a number
seq 1 5 | 2041 slippy -n '3p' > $expected_output 
seq 1 5 | ./slippy -n '3p'> $actual_output 

# Testing address that is a regex
seq 2 3 20 | 2041 slippy -n '/^1/p' >> $expected_output 
seq 2 3 20 | ./slippy -n '/^1/p'>> $actual_output 


diff $expected_output $actual_output && echo "correct implementation" && exit 0

echo "incorrect implementation" && exit 1

