#! /usr/bin/python3

import os
import sys
from random import randint
from argparse import ArgumentParser


def main(filename, num_lines):
    # Check if the file already exists
    if os.path.isfile(filename):
        print("File '{}' already exists. Please use a different filename".format(filename))
        sys.exit(1)

    # Write random integers to the file
    with open(filename, 'w') as csvfile:
        for _ in range(num_lines):
            csvfile.write(str(randint(1, 2**256)) + "\n")

if __name__ == "__main__":
    # Create parser and add arguments
    parser = ArgumentParser()
    parser.add_argument("filename", help="The name of the CSV file")
    parser.add_argument("num_lines", help="The number of integers in the file. A number in the range 2 <= n <= 100", type=int)
    args = parser.parse_args()
    
    # Call main with those arguments
    main(args.filename, args.num_lines)