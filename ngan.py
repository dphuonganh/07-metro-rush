#!/usr/bin/env python3
from argparse import ArgumentParser
from time import time


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


def main():
    args = get_arguments()


if __name__ == '__main__':
    start = time()
    main()
    print('\nRuntime: {}s'.format(round(time() - start, 5)))
