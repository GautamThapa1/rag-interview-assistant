import re


def parse_booking(text: str):
    if not text.startswith("BOOKING_COMPLETE"):
        return None

    name = re.search(r"Name:\s*(.*)", text)
    email = re.search(r"Email:\s*(.*)", text)
    date = re.search(r"Date:\s*(.*)", text)
    time = re.search(r"Time:\s*(.*)", text)

    return {
        "name": name.group(1).strip(),
        "email": email.group(1).strip(),
        "date": date.group(1).strip(),
        "time": time.group(1).strip(),
    }