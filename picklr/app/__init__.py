import flask_sqlalchemy
import flask_migrate
import flask
import config

app = flask.Flask(__name__)
app.config.from_object(config.Config)

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)
