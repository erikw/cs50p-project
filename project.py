import argparse
import sys
import csv

from pyfiglet import Figlet
import survey
from bs4 import BeautifulSoup
from urllib.request import urlopen

from datetime import date, timedelta


TERM_WIDTH = 120
COUNTRIES_CSV_PATH = 'countries.csv'
VISA_URL_FMT = "https://www.projectvisa.com/visainformation/{country}"


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


def validity_days_input() -> int:
    while True:
        try:
            # TODO use survey routine to enter manual input or common values [30, 60, 90]?
            # Else just survey.routines.numeric
            # TODO also ask what day you got the stamp with  survey.routines.datetime instead of assuming today(). Makes testing easier too.
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


def show_visa_info(country):
    # TODO what errors to catch?
    url = VISA_URL_FMT.format(country=country)
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    t = soup.find(id="Table2")

    # Collect URLs in the text to display after, as we can't render text links in the terminal.
    links = []
    for link in t.find_all("a"):
        links.append(link.get('href'))
        link.decompose()

    # Remoe empty spaces where URLs has been.
    info = t.text.replace("\n\n", "\n").strip()

    print("ℹ️", end='')
    print(info)
    print(f"Fetched from {url}\n")
    print("🔗 Links for more information:")
    print("\n".join(links))

def read_countries():
    try:
        with open(COUNTRIES_CSV_PATH) as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header line.
            return [row[0] for row in reader]
    except FileNotFoundError:
        sys.exit(f"The country list can't be read from path: {COUNTRIES_CSV_PATH}")

def visa_information():
    countries = read_countries()
    country_idx = survey.routines.select('🌎 Which country are you visiting?: ', options=countries)
    country = countries[country_idx]
    show_visa_info(country)

def main2():
    progs = ('ℹ️ Visa information for a country.', '🖩 Visa exit calculator')
    choice = survey.routines.select('Pick an option: ', options = progs)
    if choice == 0:
        visa_information()
    else:
        ... # TODO


if __name__ == "__main__":
    # main()
    main2()
