#!/usr/bin/env python3
from argparse import ArgumentParser
from sys import stderr
from time import time
from moving import MovingTrains


def get_arguments():
    parser = ArgumentParser(prog='Metro Network',
                            usage='[filename] --algo [ALGO] --gui')
    parser.add_argument('filename', help='A metro stations file')
    parser.add_argument('--algo', nargs='?', metavar='ALGO', default=0,
                        choices=[0, 1], type=int,
                        help='specify which algorithm to use for finding '
                             'the smallest number of turns')
    parser.add_argument('--gui', action='store_true',
                        help='visualize the Metro Network with Pyglet')
    return parser.parse_args()


def read_data_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.readlines()
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        stderr.write('Invalid file\n')
        exit(1)


def main():
    args = get_arguments()
    delhi_metro = MovingTrains(read_data_file(args.filename), args.algo)
    if args.gui:
        from visualize import GUI
        GUI(delhi_metro)


if __name__ == '__main__':
    start = time()
    main()
    print('\nRuntime: {}s'.format(round(time() - start, 5)))
