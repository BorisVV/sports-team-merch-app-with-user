
from datetime import datetime
from flask import Flask, session, g, render_template, current_app

app = Flask(__name__)

app.config.from_object('web_config')

@app.teardown_appcontext
def teardown_db(exception):
    # db_session = getattr(g, app.config['SQLALCHEMY_DATABASE_URI'], None)
    if db_session is None:
        db_session.close()

@app.teardown_request
def remove_db_session(exception):
    db_session.remove()

# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404  # TODO: Create a 404.html file in templates dir.

# TODO: create more views/files
from app_sport_team.views import routes
# etc.


# TODO: get register_blueprint/create files.
# app.register_blueprint(routes.mod)
#etc

from app_sport_team.tables_setUp import db_session, MerchandiseItems, SoldRecords, GamesDates

from app_sport_team import utils
app.jinja_env.filters['dateformat'] = utils.format_date_jinja
# TODO: check the code below and fix it
# from app_sport_team import utils #TODO create utils.py
# app.jinja_env.filters['displayopenid'] = utils.display_openid
