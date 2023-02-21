#! /usr/bin/env dash

# ==============================================================================
# test04.sh
# Test the slippy substitute command with different delimeter
#
# Written by: Joel Abraham
# For COMP2041/9044 Assignment 2
# ==============================================================================
PATH="$PATH:$(pwd)"

# Create some files to hold output.

expected_output="$(mktemp)"
actual_output="$(mktemp)"

# Remove the temporary directory when the test is done.

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT

# Testing delimeter with ?
seq 1 5 | 2041 slippy 's?[15]?zzz?' > $expected_output 2>&1
seq 1 5 | ./slippy 's?[15]?zzz?'> $actual_output  2>&1

# Testing for different delimeter
seq 1 5 | 2041 slippy 'sX[15]Xz/z/zX' >> $expected_output  2>&1
seq 1 5 | ./slippy 'sX[15]Xz/z/zX'>> $actual_output  2>&1


diff $expected_output $actual_output && echo "correct implementation" && exit 0

echo "incorrect implementation" && exit 1

