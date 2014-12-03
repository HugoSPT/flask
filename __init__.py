from flask import Flask 
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {'DB': "test_db"}
app.config["SECRET_KEY"] = "pass"

db = MongoEngine(app)

def register_blueprints(app):
    # Prevents circular imports
    from views import users
    app.register_blueprint(users)

register_blueprints(app)

if __name__ == '__main__':
    app.run()
