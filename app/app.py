from flask import Flask, render_template, g, session
from classes.user import User
from flask_login import *
from funcs.logIn import hash_password
import mysql.connector

app = Flask(__name__)

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



# database functions
def get_db():
    if not hasattr(g, "_database"):
        g.db = mysql.connector.connect(host=app.config["DATABASE_HOST"], user=app.config["DATABASE_USER"],
                                       password=app.config["DATABASE_PASSWORD"], database=app.config["DATABASE_DB"])
    return g.db

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

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


# TODO everything
@app.route('/')
def index():
    """dev comment
    Because the code as is doesn't create a session object, it will always direct you to the login page.
    Uncomment the return statement below to bypass that and just have it send you to the index page.
    """
    # return render_template('index.html')
    if session_has_user():
        return render_template('index.html')
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run()
