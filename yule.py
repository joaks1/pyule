#!/usr/bin/env python

"""
Yule model tree calculations.
"""

import os
import sys
import argparse
import re

__prog__ = os.path.basename(__file__)
__version__ = '0.1'
__description__ = __doc__
__author__ = 'Jamie Oaks'
__copyright__ = 'Copyright (C) 2013 Jamie Oaks.'


def expected_tree_height(ntips, birth_rate):
    height = 0
    for i in range(2, ntips + 1):
        height += float(1) / (i * birth_rate)
    return height

def get_birth_rate_from_expected_height(ntips, expected_height):
    tip_sum = 0
    for i in range(2, ntips + 1):
        tip_sum += float(ntips) / i
    return tip_sum / (expected_height * ntips)

def expected_tree_length(ntips, birth_rate):
    return float(ntips - 1) / birth_rate

def get_birth_rate_from_expected_length(ntips, expected_length):
    return float(ntips - 1) / expected_length

def main():
    parameter_options = ['rate', 'height', 'length']
    parser = argparse.ArgumentParser(description=__description__,
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version',
            action='version',
            version='%(prog)s ' + __version__,
            help='report version and exit')
    parser.add_argument('parameter',
            choices=parameter_options,
            nargs='?',
            default=parameter_options[0],
            help=('the parameter provided. Options include:\n'
                  '`rate`: the per-branch Yule birth rate\n'
                  '`height`: the expected root height of the tree\n'
                  '`length`: the expected total length of the tree\n'
                  'The default is to assume the value provided is the {0!r}.\n'
                  'You provide one of these three parameters along with the\n'
                  'number of terminals, and this program returns the other\n'
                  'two accordingly.'.format(parameter_options[0])))
    parser.add_argument('parameter_value',
            metavar='X',
            type=float,
            help=('value of the parameter'))
    parser.add_argument('ntips',
            metavar='N',
            type=int,
            help='number of terminal taxa')

    args = parser.parse_args()
    results = dict(zip(parameter_options,
            [None for k in parameter_options]))
    if args.parameter == 'rate':
        results['rate'] = args.parameter_value
        results['height'] = expected_tree_height(args.ntips, results['rate'])
        results['length'] = expected_tree_length(args.ntips, results['rate'])

    elif args.parameter == 'height':
        results['height'] = args.parameter_value
        results['rate'] = get_birth_rate_from_expected_height(args.ntips,
                results['height'])
        results['length'] = expected_tree_length(args.ntips, results['rate'])

    elif args.parameter == 'length':
        results['length'] = args.parameter_value
        results['rate'] = get_birth_rate_from_expected_length(args.ntips,
                results['length'])
        results['height'] = expected_tree_height(args.ntips, results['rate'])

    else:
        raise Exception('parameter option {0} is not valid'.format(
                args.parameter))

    if None in results.values():
        raise Exception('problem occured; please report this')
        
    sys.stdout.write('ntips = {0}\n'.format(args.ntips))
    for key in parameter_options:
        sys.stdout.write('{0} = {1}\n'.format(
                key,
                results[key]))

if __name__ == '__main__':
    main()
