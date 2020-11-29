#!/usr/bin/env python3
import sys
import argparse

from numbersapi_client import get_number_fact, dateify, NumbersAPIException, NumbersAPIBugException


def _number_or_date_or_random(value: str):
    if value == 'random':
        return value
    try:
        return int(value)
    except ValueError:
        return dateify(value)


def main():
    parser = argparse.ArgumentParser(description="""Command-line client for NumbersAPI.
    The command-line client returns raw response from the server. If you need
    more protection, please use numbersapi_client as a library.
    """)

    typegroup = parser.add_mutually_exclusive_group()
    typegroup.add_argument('--trivia', action='store_const', dest='type', const='trivia', default='trivia',
                           help='trivia about a number')
    typegroup.add_argument('--math',   action='store_const', dest='type', const='math',
                           help='math fact about a number')
    typegroup.add_argument('--date',   action='store_const', dest='type', const='date',
                           help='fact about a date')
    typegroup.add_argument('--year',   action='store_const', dest='type', const='year',
                           help='fact about a year')

    parser.add_argument('--fragment', default=None, action='store_true',
                        help='fact as a sentence fragment')

    parser.add_argument('--default',  type=str, default=None,
                        help='what to return if the number is not found')
    parser.add_argument('--notfound', type=str, default=None,
                        choices=['default', 'floor', 'ceil'],
                        help='what to do if the number is not found')

    parser.add_argument('--min', type=int, help='start of the range for `random` option (inclusive)')
    parser.add_argument('--max', type=int, help=  'end of the range for `random` option (inclusive)')

    parser.add_argument('number', type=_number_or_date_or_random, default='random', nargs="?",
                        help='value to fetch the info about')

    args = parser.parse_args()

    # Some useful warnings

    if (args.notfound is not None and args.notfound != 'default') \
       and args.default is not None:
        print('Warning: --default value will likely be ignored by NumbersAPI '
              'when --notfound is not set to “default”', file=sys.stderr)

    if (args.min is not None or args.max is not None) and args.number != 'random':
        print('Warning: using --min or --max for '
              'non-random numbers is likely not useful', file=sys.stderr)

    try:
        if args.type != 'date' and args.number != 'random' \
           and args.number != int(float(args.number)):
            raise OverflowError()
    except OverflowError:
        print('Warning: NumbersAPI is likely to return incorrect answers for '
              'some very large numbers', file=sys.stderr)

    #

    try:
        print(get_number_fact(raw=True, **vars(args)))
    except NumbersAPIException:
        print('Error: NumbersAPI returned an error', file=sys.stderr)
        exit(1)
    except NumbersAPIBugException:
        print('Error: NumbersAPI got confused by the provided arguments', file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
