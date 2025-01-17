#!/usr/bin/env python3

import argparse
import signal
import sys
from datetime import date
from typing import NoReturn, no_type_check

from constants import PROG_NAME
from mode_cli import (get_sem_version_cli, mode_cli, parse_args_cli,
                      valid_arg_iso8601_date_cli)
from mode_interactive import mode_interactive
from ui import welcome_screen
from visa import last_day_valid_stay_visa, valid_countries_visa


def get_sem_version() -> str:
    return get_sem_version_cli()


def parse_args() -> argparse.Namespace:
    return parse_args_cli()


def valid_arg_iso8601_date(date_arg: str) -> date:
    return valid_arg_iso8601_date_cli(date_arg)


def valid_countries() -> list[str]:
    return valid_countries_visa()


def last_day_valid_stay(days: int, date_entry: date = date.today()) -> date:
    return last_day_valid_stay_visa(days, date_entry)


@no_type_check  # Unclear of exact type of _frame.
def sigint_handler(_sig: int, _frame) -> NoReturn:
    print(f"\n\n\n🛑 Exiting {PROG_NAME}...")
    sys.exit(0)


def capture_interrupt_signal() -> None:
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
