#! /usr/bin/env dash

# ==============================================================================
# test07.sh
# Test the -f command line option
#
# Written by: Joel Abraham
# For COMP2041/9044 Assignment 2
# ==============================================================================

# Create some files to hold output.

expected_output="$(mktemp)"
actual_output="$(mktemp)"
command="$(mktemp)"

# Remove the temporary directory when the test is done.

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT

# Inputting commands into file
echo 4q   >  $command
echo /2/d >> $command

# Testing if -f command option works
seq 1 5 | 2041 slippy -f $command > $expected_output
seq 1 5 | ./slippy -f $command > $actual_output 

# Inputting same commands but reversed into file
echo /2/d > $command
echo 4q   >>  $command

# Testing commands file
seq 1 5 | 2041 slippy -f $command >> $expected_output
seq 1 5 | ./slippy -f $command >> $actual_output 

diff $expected_output $actual_output && echo "correct implementation" && exit 0

echo "incorrect implementation" && exit 1

