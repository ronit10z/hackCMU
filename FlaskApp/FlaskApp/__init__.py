# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

if __name__ == "__main__":
    app.run()
users = 100  # mods the hash
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'cards.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

if __name__ == "__main__":
    app.run()


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from cards order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into cards (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    db = get_db()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashid = abs(hash(username)) % users
        authenticated = False
        user_id = -1
        try:
            temp = db.execute(
                "SELECT id FROM user_data where id=" + str(hashid))
            user_id = temp.fetchone()[0]
        except:
            user_id = -2
            error = "User invalid"
        if user_id > 0:
            user_pd = db.execute(
                "SELECT password FROM user_data where id=" + str(hashid))
            user_pd = user_pd.fetchone()[0]
            if user_pd == password:
                authenticated = True
        if authenticated:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        if user_id == -2:
            error = "Invalid username or password"
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
