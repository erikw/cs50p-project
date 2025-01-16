import argparse
import sys
import csv
import time
import signal

from pyfiglet import Figlet
import survey
from bs4 import BeautifulSoup
from urllib.request import urlopen
from colorama import Fore, Style

from datetime import date, timedelta


PROG_NAME = "Visa Tool"
PROG_VERSION = (1, 0, 0)
TERM_WIDTH = 120
COUNTRIES_CSV_PATH = "countries.csv"
VISA_URL_FMT = "https://www.projectvisa.com/visainformation/{country}"
VISA_INFO_BANNER_FMT = (
    "!~~~~~~~~~~~~~~~~~~~ 🛂 Visa Information for {country:} ~~~~~~~~~~~~~~~~~~~!"
)
COMMAND_VISA_INFO = 'visa_info'
COMMAND_EXIT_CALC = 'exit_calc'

# Cache of read countries.
countries = None


def get_sem_version() -> str:
    return "{:d}.{:d}.{:d}".format(*PROG_VERSION)


def valid_arg_iso8601_date(date_arg: str) -> date:
    try:
        return date.fromisoformat(date_arg)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"The given date is not a valid ISO8601 date: {date_arg}"
        )


def parse_cli_args() -> int:
    parser = argparse.ArgumentParser(
        prog=PROG_NAME,
        description="Utility for Visa related queries. See subcommands. ",
        epilog="Find support and source code at https://github.com/erikw/cs50p-project",
    )
    parser.add_argument("-v", "--version", action="version", version=get_sem_version())

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
        choices=valid_countries(),
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
        type=valid_arg_iso8601_date,
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


def last_day_valid_stay(days: int, date_entry: date = date.today()) -> date:
    if days < 1:
        raise ValueError("An entry stamp is always at least one day valid.")

    delta = timedelta(days=days - 1)  # -1 because the entry day counts as day 1.
    return date_entry + delta


def welcome_screen() -> str:
    # figlet: Figlet = Figlet(width=TERM_WIDTH, justify="center")
    figlet: Figlet = Figlet(width=TERM_WIDTH, justify="left")
    # figlet.setFont(font='standard') # The only font guaranteed to exist it seems.
    figlet.setFont(font="slant")
    ascii = figlet.renderText(PROG_NAME)  # TODO decide proper name.
    return ascii


# Just for fun, making the program look cooler...
def progress_bar_fetch():
    state = None
    with survey.graphics.SpinProgress(
        prefix="Loading ", suffix=lambda self: state, epilogue="Completed!"
    ) as progress:
        for state in (state, " connecting...", " parsing...", " formatting..."):
            time.sleep(0.75)


def print_visa_banner(country):
    print(Fore.BLUE, end="")
    print(VISA_INFO_BANNER_FMT.format(country=country))
    print(Style.RESET_ALL, end="")


def fetch_visa_info(country):
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
    info += f"\nFetched from {url}\n"

    return (info, links)


def show_visa_info(country):
    progress_bar_fetch()

    info, links = fetch_visa_info(country)

    print_visa_banner(country)
    print(info)
    if links:
        print("🔗 Links for more information:")
        print("\n".join(links))
    print_visa_banner(country)


def valid_countries():
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


def ask_country(countries):
    country_idx = survey.routines.select(
        "🌎 Which country are you visiting? [select or type]: ", options=countries
    )
    return countries[country_idx]


def menu_visa_information():
    countries = valid_countries()
    country = ask_country(countries)
    show_visa_info(country)


def print_last_day_valid(days_valid, date_entry):
    last_day: date = last_day_valid_stay(days_valid, date_entry)

    print("📅 You need to leave the country latest on this day (before midnight):")
    print(Fore.RED, end="")
    print(last_day.isoformat(), end="")
    print(Style.RESET_ALL, end="")
    print(f" ({last_day.strftime('%A %d, %B %Y')})")


def menu_exit_calculator():
    date_entry: date = ask_date_entry()
    days_valid: int = ask_days_permitted()
    print_last_day_valid(days_valid, date_entry)


def sigint_handler(sig, frame):
    print(f"\n\n\n🛑 Exiting {PROGRAM_NAME}...")
    sys.exit(0)


def capture_interrupt_signal():
    signal.signal(signal.SIGINT, sigint_handler)

def print_valid_countries():
    countries = valid_countries()
    print("Valid countries to query about Visa information:")
    print("\n".join(countries))


def mode_cli():
    args = parse_cli_args()

    from pprint import pprint; pprint(args)

    if args.command == COMMAND_VISA_INFO:
        if args.country:
            show_visa_info(args.country)
        else:
            print_valid_countries()
    elif args.command == COMMAND_EXIT_CALC:
        print_last_day_valid(args.days_valid, args.entry_date)
    else:
        print(f"Unknown command {args['command']}. Implementatin error. Contact developer and report bug.", file=sys.stderr)
        sys.exit()




def mode_interactive():
    progs = ("ℹ️ Visa information for a country", "🖩 Visa exit date calculator")
    choice = survey.routines.select("Pick an option: ", options=progs)
    if choice == 0:
        menu_visa_information()
    else:
        menu_exit_calculator()


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
