RATES = {"DOM": 3, "COM": 6}
SLAB = {"A": 1, "B": 2}


def units_consumed(reading):
    """Return units used from 'previous:current', or None if the input is invalid."""
    try:
        previous, current = reading.split(':')
        result = int(current) - int(previous)
    except (AttributeError, ValueError):
        return None
    if result < 0:  # current reading lower than previous is not valid
        return None
    return result


def daily_average(units_csv):
    """Return the average of comma-separated daily units, or None if invalid."""
    try:
        units = [int(u) for u in units_csv.split(',')]
        if any(u < 0 for u in units):
            return None
        return round(sum(units) / len(units), 2)
    except (AttributeError, ValueError, OverflowError, ZeroDivisionError):
        return None


def tariff_rate(code):
    """Return the rate for a code like 'DOM-A', or None if invalid."""
    try:
        category, slab = code.split('-')
        return RATES[category.upper()] * SLAB[slab.upper()]
    except (AttributeError, ValueError, KeyError):
        return None


def main():
    print("==== Running units_consumed ====")
    user_input = input("Enter meter readings as previous:current (e.g. 1200:1350): ")
    result = units_consumed(user_input)
    print("Units Consumed:", result if result is not None else "Invalid input")

    print("\n==== Running daily_average ====")
    user_input = input("Enter daily units as CSV (e.g. 5,7,6): ")
    result = daily_average(user_input)
    print("Daily Average:", result if result is not None else "Invalid input")

    print("\n==== Running tariff_rate ====")
    user_input = input("Enter a tariff code (e.g. DOM-A): ")
    result = tariff_rate(user_input)
    print("Rate per Unit:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()