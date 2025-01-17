import sys
from datetime import date

import survey

from ui import print_last_day_valid, print_visa_info
from visa import valid_countries_visa


def ask_country(countries):
    country_idx = survey.routines.select(
        "🌎 Which country are you visiting? [select or type]: ", options=countries
    )
    return countries[country_idx]


def ask_date_entry() -> date:
    datetime = survey.routines.datetime(
        "What day did you get your entry stamp in your passport?: ",
        attrs=("year", "month", "day"),
    )
    return datetime.date()


def ask_days_permitted() -> int:
    days = 0
    while days < 1:
        days = survey.routines.numeric(
            "🔢 How many days is your entry stamp valid?\n[type or use up arrow]: ",
            decimal=False,
        )
        if days < 1:
            print(
                "An entry stamp is always at least one day valid. Enter again.",
                file=sys.stderr,
            )
    return days


def menu_visa_information():
    countries = valid_countries_visa()
    country = ask_country(countries)
    print_visa_info(country)


def menu_exit_calculator():
    date_entry: date = ask_date_entry()
    days_valid: int = ask_days_permitted()
    print_last_day_valid(days_valid, date_entry)


def mode_interactive():
    progs = ("ℹ️ Visa information for a country", "🖩 Visa exit date calculator")
    choice = survey.routines.select("Pick an option: ", options=progs)
    if choice == 0:
        menu_visa_information()
    else:
        menu_exit_calculator()
