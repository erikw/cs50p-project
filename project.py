import argparse
import sys
import csv
import time

from pyfiglet import Figlet
import survey
from bs4 import BeautifulSoup
from urllib.request import urlopen
from colorama import Fore, Style

from datetime import date, timedelta


TERM_WIDTH = 120
COUNTRIES_CSV_PATH = "countries.csv"
VISA_URL_FMT = "https://www.projectvisa.com/visainformation/{country}"
VISA_INFO_BANNER_FMT = "!~~~~~~~~~~~~~~~~~~~ 🛂 Visa Information for {country:} ~~~~~~~~~~~~~~~~~~~!"


# TODO allow -c <country> for quick visa info too.
def validity_days_args() -> int:
    parser = argparse.ArgumentParser(
        description="Helps you calculate the last valid day to stay in a country given an entry stamp in your passport"
    )
    parser.add_argument(
        "-d", type=int, help="Number of days your entry is valid e.g. 90 days"
    )
    args = parser.parse_args()
    return args.d


def ask_days_permitted() -> int:
    # TODO also ask what day you got the stamp with  survey.routines.datetime instead of assuming today(). Makes testing easier too.
    days = 0
    while days < 1:
        days = survey.routines.numeric('🔢 How many days is your entry stamp valid?\n(type or use up arrow): ', decimal = False)
        if days < 1:
            print("An entry stamp is always at least one day valid. Enter again.", file=sys.stderr)
    return days


def last_day_valid_from_today(days: int) -> date:
    if days < 1:
        raise ValueError("An entry stamp is always at least one day valid.")

    delta = timedelta(days=days - 1)  # -1 because the entry day counts as day 1.
    return date.today() + delta


def welcome_screen() -> str:
    #figlet: Figlet = Figlet(width=TERM_WIDTH, justify="center")
    figlet: Figlet = Figlet(width=TERM_WIDTH, justify="left")
    # figlet.setFont(font='standard') # The only font guaranteed to exist it seems.
    figlet.setFont(font="slant")
    ascii = figlet.renderText("Visa Tool")  # TODO decide proper name.
    return ascii



# Just for fun, making the program look cooler...
def progress_bar_fetch():
    state = None
    with survey.graphics.SpinProgress(prefix = 'Loading ', suffix = lambda self: state, epilogue = 'Completed!') as progress:
        for state in (state, ' connecting...', ' parsing...', ' analyzing...'):
            time.sleep(0.75)

def print_visa_banner(country):
    print(Fore.GREEN, end='')
    print(VISA_INFO_BANNER_FMT.format(country=country))
    print(Style.RESET_ALL, end='')

def show_visa_info(country):
    progress_bar_fetch()

    # TODO what errors to catch?
    url = VISA_URL_FMT.format(country=country)
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    t = soup.find(id="Table2")

    # Collect URLs in the text to display after, as we can't render text links in the terminal.
    links = []
    for link in t.find_all("a"):
        href = link.get("href").strip()
        if href and not href.startswith("/"):
            links.append(link.get("href"))
            # link.decompose() # Nope, textual links still needed

    # Make more concise.
    info = t.text.replace("\n\n", "\n").strip()

    print_visa_banner(country)
    print(info)
    print(f"Fetched from {url}\n")
    if links:
        print("🔗 Links for more information:")
        print("\n".join(links))
    print_visa_banner(country)


def read_countries():
    try:
        with open(COUNTRIES_CSV_PATH) as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header line.
            return [row[0] for row in reader]
    except FileNotFoundError:
        sys.exit(f"The country list can't be read from path: {COUNTRIES_CSV_PATH}")

def ask_country(countries):
    country_idx = survey.routines.select(
        "🌎 Which country are you visiting?: ", options=countries
    )
    return countries[country_idx]

def menu_visa_information():
    countries = read_countries()
    country = ask_country(countries)
    show_visa_info(country)

def menu_exit_calculator():
    # TODO ask entry day with calendar picker.
    date_entry = ask_date_entry()
    print(f"Entered on: {date_entry}")
    days_valid = ask_days_permitted()

    last_day: date = last_day_valid_from_today(days_valid)

    print("📅 You need to leave the country latest on this day (before midnight):")
    print(Fore.RED, end='')
    print(last_day.isoformat())
    print(Style.RESET_ALL, end='')
    print(f"i.e. {last_day.strftime('%A %d, %B %Y')}")

def main() -> int:
    print(welcome_screen())

    visa_days: int
    if len(sys.argv) > 1:
        visa_days = validity_days_args()
    else:
        visa_days = ask_days_permitted()

    last_day: date = last_day_valid_from_today(visa_days)
    print("You need to leave the country latest on this day (before midnight):")
    print(last_day.isoformat())
    print(f"i.e. {last_day.strftime('%A %d, %B %Y')}")

    return 0

def main2():
    print(welcome_screen())

    progs = ("ℹ️ Visa information for a country", "🖩 Visa exit date calculator")
    choice = survey.routines.select("Pick an option: ", options=progs)
    if choice == 0:
        menu_visa_information()
    else:
        menu_exit_calculator()


if __name__ == "__main__":
    # main()
    main2()
