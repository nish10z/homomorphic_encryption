import os
import sys
from random import randint
from argparse import ArgumentParser


def main(filename):
    if os.path.isfile(filename):
        print("File '{}' already exists. Please use a different filename".format(filename))
        sys.exit(1)

    with open(filename, 'w') as csvfile:
        for _ in range(100):
            csvfile.write(str(randint(1, 2**256)) + "\n")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename", help="The name of the CSV file")
    args = parser.parse_args()
    main(args.filename)