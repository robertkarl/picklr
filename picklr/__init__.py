import flask_sqlalchemy
import flask_migrate
import flask

print('passing name {} to flask'.format(__name__))
app = flask.Flask(__name__, template_folder='templates')

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

def load_app():
    from picklr.blueprints import get_app
    return get_app()