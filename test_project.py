import pytest
import argparse
import sys
from datetime import date, timedelta

import project
from project import get_sem_version, valid_arg_iso8601_date, parse_cli_args, last_day_valid_stay, valid_countries, COUNTRIES_CSV_PATH


def test_get_sem_version():
    project.PROG_SEM_VERSION = (1, 0, 0)
    assert "1.0.0" == get_sem_version()

    project.PROG_SEM_VERSION = (2, 3, 4)
    assert "2.3.4" == get_sem_version()


def test_valid_arg_iso8601_date():
    assert valid_arg_iso8601_date("0001-01-01")
    assert valid_arg_iso8601_date("1970-01-01")
    assert valid_arg_iso8601_date("9999-12-31")

    with pytest.raises(argparse.ArgumentTypeError):
        valid_arg_iso8601_date("111-01-01")

    with pytest.raises(argparse.ArgumentTypeError):
        valid_arg_iso8601_date("1970-1-01")

    with pytest.raises(argparse.ArgumentTypeError):
        valid_arg_iso8601_date("1970-01-1")

    with pytest.raises(argparse.ArgumentTypeError):
        valid_arg_iso8601_date("cat-01-01")

    with pytest.raises(argparse.ArgumentTypeError):
        valid_arg_iso8601_date("cat")

    with pytest.raises(argparse.ArgumentTypeError):
        valid_arg_iso8601_date("1970-01")

    with pytest.raises(argparse.ArgumentTypeError):
        valid_arg_iso8601_date("1970")


def test_parse_cli_args():
    sys.argv = ["prog_name", "visa_info", "-c", "Germany"]
    args = parse_cli_args()

    assert "visa_info", args.command
    assert "Germany", args.country


def test_parse_cli_args_visa_info_list():
    sys.argv = ["prog_name", "visa_info", "-l"]
    args = parse_cli_args()

    assert "visa_info", args.command
    assert not args.country
    assert args.list_countries

def test_parse_cli_args_exit_calc_default_entry():
    sys.argv = ["prog_name", "exit_calc", "-d", "5"]
    args = parse_cli_args()

    assert "exit_calc", args.command
    assert 5, args.days_valid
    assert date.today() == args.entry_date

def test_parse_cli_args_exit_calc_set_entry():
    sys.argv = ["prog_name", "exit_calc", "-d", "5", "-e", "2025-01-17"]
    args = parse_cli_args()

    assert "exit_calc", args.command
    assert 5, args.days_valid
    assert date.fromisoformat("2025-01-17") == args.entry_date


def test_last_day_valid_stay():
    days = 1
    date_entry = date.today()

    date_valid = date_entry + timedelta(days - 1)
    assert date_valid == last_day_valid_stay(days, date_entry)

def test_last_day_valid_stay_invalid():
    date_entry = date.today()

    with pytest.raises(ValueError):
        assert last_day_valid_stay(0, date_entry)

    with pytest.raises(ValueError):
        assert last_day_valid_stay(-1, date_entry)


def test_valid_countries():
    with open(COUNTRIES_CSV_PATH) as file:
        assert len(list(file)) - 1 == len(valid_countries())
