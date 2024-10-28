from datetime import datetime


def today_date():
    """
    Get the current date and format it as a string
    in the format 'Day, DD Month YYYY'.

    Returns:
        str: The formatted current date string.
    """
    today_date = datetime.today()

    formatted_date = today_date.strftime('%a, %d %B %Y')

    return formatted_date