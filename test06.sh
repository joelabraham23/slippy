#! /usr/bin/env dash

# ==============================================================================
# test06.sh
# Testing the splitting of commands
#
# Written by: Joel Abraham
# For COMP2041/9044 Assignment 2
# ==============================================================================

# Create some files to hold output.

expected_output="$(mktemp)"
actual_output="$(mktemp)"

# Remove the temporary directory when the test is done.

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT

# Testing splitting with ;
seq 1 5 | 2041 slippy '4q;/2/d'> $expected_output 
seq 1 5 | ./slippy '4q;/2/d' > $actual_output 

# Testing splitting with new line
seq 1 5 | 2041 slippy '4q
/2/d'>> $expected_output 
seq 1 5 | ./slippy '4q
/2/d'>> $actual_output 


diff $expected_output $actual_output && echo "correct implementation" && exit 0

echo "incorrect implementation" && exit 1

