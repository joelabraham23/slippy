#!/usr/bin/env python3
'''
Joel Abraham z5310056 
Slippy program
comp2041 ass2
'''


import sys
import re
from os.path import exists
flags = {
    'n': True,
    'i' : True,
    'f' : True

}

# q- quit command
# The Slippy q command causes slippy.py to exit
def quit_comm(command, n, line, print_by_default):
    # If address is regex string
    if command[0] == '/':
        command = command[1:-2]  
        if re.search(command,line):                                                                                                                                 
            if print_by_default:
                print(line, end = '')
            sys.exit()

    # Address is a number
    else:
        address = command[:-1]
        if address == '':
            address = 1
        elif not address.isnumeric():
            print("usage: slippy [-i] [-n] [-f <script-file> | <sed-command>] [<files>...]")
            sys.exit()
        if n == int(address) - 1:
            if print_by_default:
                print(line, end ='')
            sys.exit()





# p- print command
# The Slippy p commands prints the input line
def print_comm(command, n, line):
    # Address is a regex string
    if command[0] == '/':
        command = command[1:-2]
        if re.search(command,line):
            print(line, end = '')
    # Address is a number
    else:
        address = command[:-1]
        if address == '':
            print(line, end = '')
        elif not address.isnumeric():
            print("usage: slippy [-i] [-n] [-f <script-file> | <sed-command>] [<files>...]")
            sys.exit(1)
        elif n == int(address) - 1:
            print(line, end = '')



# d - delete command
# The slippy d command deletes the input line
def delete_comm(command, n, line):
    # If address is a regex string
    if command[0] == '/':
        command = command[1:-2]
        if re.search(rf"{command}", line):
            return False
    # If address is a number
    else:
        address = command[:-1]
        if address == '':
            sys.exit(1)
        if not address.isnumeric():
            print("usage: slippy [-i] [-n] [-f <script-file> | <sed-command>] [<files>...]")
            sys.exit(1)
        if n == int(address) - 1:
            return False
    return True

# s - substitute command
# The Slippy s command replaces the specified regex on the input line.
def substitute_comm(command, n, line):
    # Address is a regex string
    if command[0] == "/":
        address = command.split("/")[1]
        command = '/'.join(command.split("/")[2:])
        delim = command.partition('s')[2][0]
        subs = command.split(delim)
        if re.search(address, line):
            # If applying substitute to all instance in that line
            if command[-1] == "g":
                line = re.sub(subs[1], subs[2], line)
            # Applying to only the first instance of line
            else:
                line = re.sub(subs[1], subs[2], line, count=1)
            return line

    # If it has numerical address
    elif command[0].isdigit():
        address = command[:command.index("s")]
        # Making sure input is correct
        if not address.isnumeric():
            print("usage: slippy [-i] [-n] [-f <script-file> | <sed-command>] [<files>...]")
            sys.exit(1)
        address = int(address)
        # Setting delimeter to users choice
        delim = command.partition('s')[2][0]
        subs = command.split(delim)
        # If line is at the required adddress
        if n == address - 1:
            # If applying substitute to all instances in line
            if command[-1] == "g":
                line = re.sub(subs[1], subs[2], line)
            # Applying sub to only first instance in line
            else:
                line = re.sub(subs[1], subs[2], line, count=1)
        return line

    # Base case
    else:
        delim = command.partition('s')[2][0]
        subs = command.split(delim)
        if subs[-1] == "g":
            l = re.sub(subs[1], subs[2], line)
        else:
            l = re.sub(subs[1], subs[2], line, count=1)
        if l != line:
            return l


# Reads arguments and lets slippy know if any command options have been used
def read_in_command_line():
    if '-n' in sys.argv:
        flags['n'] = False
    if '-i' in sys.argv:
        flags['i'] = False
    if '-f' in sys.argv:
        flags['f'] = False
    


# Taking all the arguments and taking the commands or input files
def clean_args():
    args = []
    for arg in sys.argv:
        if arg[0] != '-' and arg != './slippy' and arg != 'slippy':
            args.append(arg)
    return args



# Removing any white space or comments from a list of commands
def removing_white_space(command):
    new_commands = []
    for comm in command:
        if "#" in comm:
            comm = comm.split("#")[0]
        comm = comm.replace(" ", "")
        new_commands.append(comm)
    return new_commands

def read_commands_file(commFile):
    with open(commFile, 'r') as inf:
            lines = inf.readlines()
            command = []
            for l in lines:
                if ";" in l:
                    ls = re.split(';|\n', l)
                    for lin in ls:
                        command.append(lin.strip())
                else:
                    command.append(l.strip())
    return command


# Reading lines from input files
def reading_input_files(sysargs, command):
    l = False
    n = 0
    # Looping through input files
    for file in sysargs[1:]:
        # Making sure input file exists
        if not exists(file):
            print("slippy: error")
            sys.exit(1)
        # Reading input file and going through each line of file
        with open(file, 'r') as inf:
            lines = inf.readlines()
            for line in lines:
                # Res to check if comm is deleted 
                res = True
                # Going through each command
                for comm in command:  
                    # If only last line is applied
                    if comm[0] == '$':
                        if n != len(lines) - 1:
                            continue
                        else:
                            comm = comm[1:]
                    # If comm has been deleted then dont apply any other command
                    if res:
                        if comm[-1] == "q":
                            quit_comm(comm, n, line, flags['n'])
                        elif comm[-1] == "d":
                            res = delete_comm(comm, n, line)
                        elif comm[-1] == "p":
                            # If line has not been substituted
                            if not l:
                                print_comm(comm, n, line)
                            if l:
                                continue
                        elif re.search(r"s[^ ].*[^ ].*[^ ]", comm):
                            l = substitute_comm(comm, n, line)
                        else:
                            print("slippy: command line: invalid command")
                            sys.exit(1)
                        
                # If printing all lines and no line has been deleted
                if (flags['n']) and res:
                    # If line has been substituted
                    if l:
                        print(l, end ='')
                    else:
                        print(line, end = '')
                # if res:
                n += 1

# Reading lines from stdin
def reading_stdin(command):
    l = False
    on_last_line = False
    # Looping through each stdin
    line = sys.stdin.readline()
    # Counter to keep track of number of lines read
    n = 0
    # print(command)
    while True:
        res = True
        # Checking second line to find out if end of stdin
        line2 = sys.stdin.readline()
        # Looping through commans
        for comm in command:  
            # If on last line
            if line2 == "":
                on_last_line = True
            # If only applying command to last line
            if comm[0] == '$':
                if not on_last_line:
                    continue
                comm = comm[1:]
            # If line has been deleted then dont apply any other commands
            if res:
                if comm[-1] == "q":
                    quit_comm(comm, n, line, flags['n'])
                elif comm[-1] == "d":
                    res = delete_comm(comm, n, line)
                elif comm[-1] == "p":
                    # If line has not been substituted
                    if not l:
                        print_comm(comm, n, line)
                    if l:
                        continue
                elif re.search(r"s[^ ].*[^ ].*[^ ]", comm):
                    l = substitute_comm(comm, n, line)
                else:
                    print("slippy: command line: invalid command")
                    sys.exit(1)
        # If default printing is set and line has not been deleted
        if (flags['n']) and res:
            if l:   
                print(l, end ='')
            else:
                print(line, end = '')
        if on_last_line:
            sys.exit(1)
        line = line2
        n += 1



def main():
    # Find out about argument parser
    read_in_command_line()
    sysargs = clean_args()
    commands = sysargs[0]    
    commands = re.split(';|\n', commands)
    # If commands file given
    if not flags['f']:
        if not exists(sysargs[0]):
            print("slippy: error")
            sys.exit(1)
        commands = read_commands_file(sysargs[0])
    commands = removing_white_space(commands)
    while "" in commands:
        commands.remove("")
    # If input files are given
    if len(sysargs) > 1:
        reading_input_files(sysargs, commands)
    else:
        reading_stdin(commands)


if __name__ == "__main__":
    main()
