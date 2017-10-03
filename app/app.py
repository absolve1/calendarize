from flask import Flask, render_template, g, session, request, url_for
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template
from classes.user import User
from flask_login import *
from funcs.logIn import hash_password
import mysql.connector
import logging

app = Flask(__name__)
Mobility(app)

# Flask configuration parameters #
# TODO set database vars
app.config["DATABASE_USER"] = ""
app.config["DATABASE_PASSWORD"] = ""
app.config["DATABASE_DB"] = ""
app.config["DATABASE_HOST"] = ""
app.config['debug'] = True  # Testing only
app.secret_key = 'hella secret'
login_manager = LoginManager()
login_manager.init_app(app)

hash_password("password")

# TODO implement necessary loggers
# Hold off on this until we have more than one python file to work with to avoid having to rework logging
loggers = {}  # dict of loggers to init


# database functions
def get_db():
    if not hasattr(g, "_database"):
        g.db = mysql.connector.connect(host=app.config["DATABASE_HOST"], user=app.config["DATABASE_USER"],
                                       password=app.config["DATABASE_PASSWORD"], database=app.config["DATABASE_DB"])
    return g.db


@login_manager.user_loader
def load_user(user_id):
    return User.get_id(user_id)


@app.teardown_appcontext
def teardown_db(error):
    """Closes the database at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def session_has_user():
    if "username" in session:
        return True
    return False


def setup_logging(log_name, log_file, log_level=logging.INFO):
    """
    :param log_name: String, descriptive name of log
    :param log_file: String, a path to .log file to write to
    :param log_level: logging.<PARAM>, INFO, DEBUG or WARNING, level of logging
    :return: log object, not necessary to use the returned object,
            but useful for storing logs in a list or dict for easier access
    """
    log = logging.getLogger(log_name)
    log.setLevel(log_level)
    handler = logging.FileHandler(filename=log_file, encoding='utf-8', mode='a')
    fmt = logging.Formatter('[%(asctime)s] :%(levelname)s: %(message)s', datefmt='%H:%M:%S')
    handler.setFormatter(fmt)
    log.addHandler(handler)
    return log


def end_logging(log):
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)


# TODO everything
@app.route('/')
@mobile_template('{mobile/}index.html')
@login_required
def index(template):
    """dev comment
    Because the code as is doesn't create a session object, it will always direct you to the login page.
    Uncomment the return statement below to bypass that and just have it send you to the index page.
    :param template: takes the template path as a parameter for mobile templates
    """
    # return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':

    active_loggers = []
    for log in loggers:
        lg = setup_logging(log, '{}.log'.format(log))
        active_loggers.append(lg)

    app.run()

    for log in active_loggers:
        end_logging(log)
