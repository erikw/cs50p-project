from datetime import date

def read_visa_validity_days() -> int:
    while True:
        try:
            return int(input("How many days is your entry stamp valid? "))
        except ValueError:
            pass

def last_day_valid_from_today(days: int) -> date:
    pass


def main():
    visa_days: date = read_visa_validity_days()
    last_day: date = last_day_valid_from_today(visa_days)
    print(last_day)

if __name__ == '__main__':
    main()
