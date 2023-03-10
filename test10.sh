#! /usr/bin/env dash

# ==============================================================================
# test10.sh
# Testing slippy with invalid command given
#
# Written by: Joel Abraham
# For COMP2041/9044 Assignment 2
# ==============================================================================

# Create some files to hold output.

expected_output="$(mktemp)"
actual_output="$(mktemp)"

# Remove the temporary directory when the test is done.

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT


# Testing slippy with input files
seq 24 43 | 2041 slippy '2'> $expected_output 2>&1
seq 24 43 | ./slippy '2'> $actual_output 2>&1


diff $expected_output $actual_output && echo "correct implementation" && exit 0

echo "incorrect implementation" && exit 1

