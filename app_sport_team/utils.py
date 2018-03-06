from datetime import datetime

#"format date(year-month-day) ints not string."
def format_date(dateAsString):
    # If the text box is left empty.
    if dateAsString == "":
        return ""
    # Otherwise return the string formatted to int.
    else:
        # This maps the string and converts them to int.
        # year, month, day = map(int, dateAsString.split('-'))
        return datetime.strptime(dateAsString, '%Y-%m-%d')

def format_date_jinja(dt):
    # This format is for use with templates, when dates are needed to be
    # displayed and will cause a problem since it will ask for string.
    return dt.strftime('%Y-%m-%d')
