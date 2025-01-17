import time
from datetime import date

import inflect
import survey
from colorama import Fore, Style
from pyfiglet import Figlet

from constants import PROG_NAME, TERM_WIDTH, VISA_INFO_BANNER_FMT
from visa import fetch_visa_info, last_day_valid_stay_visa, valid_countries_visa


def welcome_screen() -> str:
    # figlet: Figlet = Figlet(width=TERM_WIDTH, justify="center")
    figlet: Figlet = Figlet(width=TERM_WIDTH, justify="left")
    # figlet.setFont(font='standard') # The only font guaranteed to exist it seems.
    figlet.setFont(font="slant")
    ascii = figlet.renderText(PROG_NAME)
    return ascii


# Just for fun, making the program look cooler...
def progress_bar_fetch():
    state = None
    with survey.graphics.SpinProgress(
        prefix="Loading ", suffix=lambda self: state, epilogue="Completed!"
    ):
        for state in (state, " connecting...", " parsing...", " formatting..."):
            time.sleep(0.75)


def print_visa_banner(country):
    print(Fore.BLUE, end="")
    print(VISA_INFO_BANNER_FMT.format(country=country))
    print(Style.RESET_ALL, end="")


def print_visa_info(country):
    progress_bar_fetch()

    info, links = fetch_visa_info(country)

    print_visa_banner(country)
    print(info)
    if links:
        print("🔗 Links for more information:")
        print("\n".join(links))
    print_visa_banner(country)


def print_last_day_valid(days_valid, date_entry):
    last_day: date = last_day_valid_stay_visa(days_valid, date_entry)
    days_from_now = (last_day - date.today()).days

    print("📅 You need to leave the country latest on this day (before midnight):")
    print(Fore.RED, end="")
    print(last_day.isoformat(), end="")
    print(Style.RESET_ALL, end="")
    print(f" ({last_day.strftime('%A %d, %B %Y')})")

    p = inflect.engine()
    days_pluralized = p.plural_noun("day", abs(days_from_now))
    if days_from_now < 0:
        print(
            f"That was {days_from_now * -1} {days_pluralized} ago from today (excluding today). What are you still doing in the country? Get out now!"
        )
    elif days_from_now > 0:
        print(
            f"That is {days_from_now} {days_pluralized} from today (excluding today)."
        )
    else:
        print(
            f"Panic! Today is your last valid day. Make sure to leave the country before midnight!!"
        )


def print_valid_countries():
    countries = valid_countries_visa()
    print("Valid countries to query about Visa information:")
    print("\n".join(countries))
