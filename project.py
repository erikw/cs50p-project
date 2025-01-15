import argparse
import sys

from pyfiglet import Figlet

from datetime import date, timedelta


TERM_WIDTH = 120


def validity_days_args() -> int:
    parser = argparse.ArgumentParser(
        description="Helps you calculate the last valid day to stay in a country given an entry stamp in your passport"
    )
    parser.add_argument(
        "-d", type=int, help="Number of days your entry is valid e.g. 90 days"
    )
    args = parser.parse_args()
    return args.d


def validity_days_input() -> int:
    while True:
        try:
            return int(input("How many days is your entry stamp valid? "))
        except ValueError:
            pass


def last_day_valid_from_today(days: int) -> date:
    if days < 1:
        raise ValueError("An entry stamp is always at least one day valid.")

    delta = timedelta(days=days - 1)  # -1 because the entry day counts as day 1.
    return date.today() + delta


def welcome_screen() -> str:
    figlet: Figlet = Figlet(width=TERM_WIDTH, justify="center")
    # figlet.setFont(font='standard') # The only font guaranteed to exist it seems.
    figlet.setFont(font="slant")
    ascii = figlet.renderText("Visa Exit Calculator")  # TODO decide proper name.
    return ascii


def main() -> int:
    print(welcome_screen())

    visa_days: int
    if len(sys.argv) > 1:
        visa_days= validity_days_args()
    else:
        visa_days = validity_days_input()

    last_day: date = last_day_valid_from_today(visa_days)
    print("You need to leave the country latest on this day (before midnight):")
    print(last_day.isoformat())
    print(f"i.e. {last_day.strftime('%A %d, %B %Y')}")

    return 0

if __name__ == "__main__":
    main()
