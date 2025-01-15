def read_visa_validity_days():
    while True:
        try:
            return int(input("How many days is your entry stamp valid? "))
        except ValueError:
            pass


def main():
    visa_days = read_visa_validity_days()
    last_day = calc_last_day_from_today(visa_days)
    print(visa_days)

if __name__ == '__main__':
    main()
