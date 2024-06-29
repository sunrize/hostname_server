from hostname_server import app
from hostname_server.database import db_session, init_db, test_db
from hostname_server.hostnames.models import Hostname
from sqlalchemy.sql.expression import func
from sqlalchemy import text, select

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/init_db')
def view_init_db():
    init_db()
    return 'init db!'

@app.route('/test_db')
def view_test_db():
    test_db()
    return 'test db!'

@app.route('/db_add_hostname')
def view_db_add_hostname():
    new_hostname = Hostname('AD')
    db_session.add(new_hostname)
    db_session.commit()
    return 'new hostname'

@app.route('/db_hostnames')
def view_db_hostnames():
    result = db_session.scalars(select(Hostname)).all()
    return str(result)