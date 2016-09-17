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
    cur = db.execute('select title, author, description from cards order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, description, author) values (?, ?, ?)',
               [request.form['title'], request.form['description'], request.form['author']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/like',  methods=['GET', 'POST'])
def vote():
    db = get_db()
    target = request.get_data()
    target = target.split("_")[-1]
    cur = db.execute("select title, score from cards order by id desc")
    entries = cur.fetchall()
    result = None
    for entry in entries:
        if entry[0] == target:
            if entry[1] == None:
            result = str(int(entry[1]) + 1)
    print result, target
    db.execute('update cards set score=(?) where title=(?)',[result, target])
    db.commit()
    return redirect(url_for('show_entries'))

@app.route('/signup')
def add_user():
    db = get_db()
    db.execute('insert into user_data (name, password, rating, up) values (?, ?, ?)',
               request.form['name'], request.form['password'])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/new_card')
def new_card():
    db = get_db()
    author = "billy"
    db.execute('insert into cards (title, description, score, status, author, text) values (?, ?, ?, ?, ?, ?)',
                [request.form['title']], request.form['description'], str(0), "TODO", author, "")
    db.commit()
    return redirect(url_for('show_entries'))
