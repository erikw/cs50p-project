import argparse
from datetime import date

import constants # To not split PROG_SEM_VERSION to two symbols, preventing chaning value in test. Ref: https://stackoverflow.com/a/3536638
from constants import PROG_NAME, COMMAND_VISA_INFO, COMMAND_EXIT_CALC
from ui import print_visa_info, print_last_day_valid, print_valid_countries
from visa import valid_countries_visa

def get_sem_version_cli() -> str:
    return "{:d}.{:d}.{:d}".format(*constants.PROG_SEM_VERSION)

def valid_arg_iso8601_date_cli(date_arg: str) -> date:
    try:
        return date.fromisoformat(date_arg)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"The given date is not a valid ISO8601 date: {date_arg}"
        )

def parse_args_cli() -> int:
    parser = argparse.ArgumentParser(
        prog=PROG_NAME,
        description="Utility for Visa related queries. See subcommands. ",
        epilog="Find support and source code at https://github.com/erikw/cs50p-project",
    )
    parser.add_argument("-v", "--version", action="version", version=get_sem_version_cli())

    # Commmands
    subparsers = parser.add_subparsers(
        help="Optional Commands. If none is given, the program will run in interactive mode. Run $(python project.py <command> -h) for more info about a command.",
        dest="command",
    )
    subparsers.required = False

    subpar_visa_info = subparsers.add_parser(
        COMMAND_VISA_INFO,
        help="Get Visa information for a country.",
    )
    visa_args_group = subpar_visa_info.add_mutually_exclusive_group(required=True)
    visa_args_group.add_argument(
        "-c",
        "--country",
        type=str,
        choices=valid_countries_visa(),
        metavar="",
        help="The country that you will visit.",
    )  # EMpty metavar prevents printing all choices in the help text. Ref: https://stackoverflow.com/a/16985727
    visa_args_group.add_argument(
        "-l",
        "--list-countries",
        action="store_true",
        help="List available countries to check Visa info for.",
    )

    subpar_exit_calc = subparsers.add_parser(
        COMMAND_EXIT_CALC,
        help="Calculate the last day you can stay in a country given the entry date and entry stamp validity length.",
    )
    subpar_exit_calc.add_argument(
        "-e",
        "--entry-date",
        type=valid_arg_iso8601_date_cli,
        required=False,
        default=date.today(),
        help="The date you entered the country in ISO8601 format (YYYY-MMM-DD). Defaults to today.",
    )
    subpar_exit_calc.add_argument(
        "-d",
        "--days-valid",
        type=int,
        required=True,
        help="Number of days your entry is valid e.g. 90 days",
    )

    return parser.parse_args()


def mode_cli():
    args = parse_args_cli()

    if args.command == COMMAND_VISA_INFO:
        if args.country:
            print_visa_info(args.country)
        else:
            print_valid_countries()
    elif args.command == COMMAND_EXIT_CALC:
        if args.entry_date == date.today():
            print("No entry date given: assuming you entered the country today.\n")
        print_last_day_valid(args.days_valid, args.entry_date)
    else:
        print(
            f"Unknown command {args['command']}. Implementatin error. Contact developer and report bug.",
            file=sys.stderr,
        )
        sys.exit()
