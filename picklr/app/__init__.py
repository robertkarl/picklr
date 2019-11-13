import flask_sqlalchemy
import flask_migrate
import flask

app = flask.Flask(__name__, template_folder='templates')

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)
