from datetime import datetime
from functools import wraps
from flask import g, flash, redirect, request, url_for, session
from app_sport_team.tables_setUp import User

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

# Make some pages have the user logged-in first to make changes.
# This will be used in the views/routes.py 
def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash(u'You need to be signed in.')
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function
