#! /usr/bin/env dash

# ==============================================================================
# test09.sh
# Testing slippy with input files and commands file
#
# Written by: Joel Abraham
# ==============================================================================

# Create some files to hold output.

expected_output="$(mktemp)"
actual_output="$(mktemp)"
two="$(mktemp)"
five="$(mktemp)"
command="$(mktemp)"

# Remove the temporary directory when the test is done.

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT

# Putting sequence into files
seq 1 2 > $two
seq 1 5 > $five

# Testing slippy with input files
2041 slippy '4q;/2/d' $two $five> $expected_output 
./slippy '4q;/2/d' $two $five> $actual_output 

# Testign slippy with input files and command file
echo 4q   >  $command
echo /2/d >> $command

2041 slippy -f $command $two $five> $expected_output 
./slippy -f $command $two $five> $actual_output 



diff $expected_output $actual_output && echo "correct implementation" && exit 0

echo "incorrect implementation" && exit 1

