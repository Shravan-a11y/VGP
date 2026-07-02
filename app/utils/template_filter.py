from datetime import datetime


def format_datetime(value):

    if not value:
        return "-"

    try:

        dt = datetime.fromisoformat(value)

        return dt.strftime(
            "%d %b %Y, %I:%M %p"
        )

    except Exception:

        return value