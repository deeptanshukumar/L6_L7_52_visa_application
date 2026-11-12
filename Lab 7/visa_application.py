"""Input validation helpers; invalid input returns None."""
import math


def parse_application(text):
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2 or not parts[0].strip():
        return None
    try:
        entries = int(parts[1])
    except ValueError:
        return None
    return (parts[0].strip().title(), entries) if entries > 0 else None


def processing_average(days_csv):
    if not isinstance(days_csv, str):
        return None
    try:
        values = [int(item) for item in days_csv.split(',')]
        if any(value < 0 for value in values):
            return None
        result = sum(values) / len(values)
    except (ValueError, OverflowError):
        return None
    return result if math.isfinite(result) else None


def payable_fee(text):
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    try:
        fee, discount = map(float, parts)
    except ValueError:
        return None
    if not all(math.isfinite(x) and x >= 0 for x in (fee, discount)):
        return None
    total = fee * 1.18 - discount
    return max(total, 0.0) if math.isfinite(total) else None


def main():
    print("==== Running parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    result = parse_application(user_input)
    print("Visa Type and Entries:", result if result is not None else "Invalid input")

    print("\n==== Running processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    result = processing_average(user_input)
    print("Average Processing Days:", result if result is not None else "Invalid input")

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result if result is not None else "Invalid input")

if __name__ == "__main__":
    main()
