import csv
from urllib.error import URLError
from urllib.request import urlopen
from datetime import date, timedelta

from bs4 import BeautifulSoup

from constants import VISA_URL_FMT, COUNTRIES_CSV_PATH

# Cache of read countries.
countries = None

def valid_countries_visa():
    global countries
    if not countries:
        try:
            with open(COUNTRIES_CSV_PATH) as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header line.
                countries = sorted([row[0] for row in reader])
        except FileNotFoundError:
            sys.exit(f"The country list can't be read from path: {COUNTRIES_CSV_PATH}")
    return countries

def fetch_visa_info(country):
    url = VISA_URL_FMT.format(country=country)
    try:
        page = urlopen(url)
        html = page.read().decode("utf-8")
    except URLError:
        sys.exit("Could not fetch remote Visa info. Try again later.")

    try:
        soup = BeautifulSoup(html, "html.parser")
        t = soup.find(id="Table2")

        # Collect URLs in the text to display after, as we can't render text links in the terminal.
        links = []
        for link in t.find_all("a"):
            href = link.get("href").strip()
            if href and not href.startswith("/"):
                links.append(link.get("href"))
    except (AttributeError, KeyError):
        sys.exit("Could not parse remote Visa info page.")

    # Make more concise.
    info = t.text.replace("\n\n", "\n").strip()
    info += f"\nFetched from {url}\n"

    return (info, links)

def last_day_valid_stay_visa(days: int, date_entry: date = date.today()) -> date:
    if days < 1:
        raise ValueError("An entry stamp is always at least one day valid.")

    delta = timedelta(days=days - 1)  # -1 because the entry day counts as day 1.
    return date_entry + delta
