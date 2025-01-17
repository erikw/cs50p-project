#!/usr/bin/env python3

import signal
import sys
from datetime import date

from mode_cli import (get_sem_version_cli, mode_cli, parse_args_cli,
                      valid_arg_iso8601_date_cli)
from mode_interactive import mode_interactive
from ui import welcome_screen
from visa import last_day_valid_stay_visa, valid_countries_visa


def get_sem_version() -> str:
    return get_sem_version_cli()


def parse_args():
    return parse_args_cli()


def valid_arg_iso8601_date(date_arg: str) -> date:
    return valid_arg_iso8601_date_cli(date_arg)


def valid_countries():
    return valid_countries_visa()


def last_day_valid_stay(days: int, date_entry: date = date.today()) -> date:
    return last_day_valid_stay_visa(days, date_entry)


def sigint_handler(_sig, _frame):
    print(f"\n\n\n🛑 Exiting {PROGRAM_NAME}...")
    sys.exit(0)


def capture_interrupt_signal():
    signal.signal(signal.SIGINT, sigint_handler)


def main() -> int:
    capture_interrupt_signal()
    print(welcome_screen())

    if len(sys.argv) > 1:
        mode_cli()
    else:
        mode_interactive()

    return 0


if __name__ == "__main__":
    main()
