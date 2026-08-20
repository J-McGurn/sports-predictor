import os

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from models import db
from routes.auth import auth
from routes.season import season
from routes.premier_league import pl
from routes.formula_one import f1


load_dotenv()

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173"
            ]
        }
    }
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

db.init_app(app)

jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(season)
app.register_blueprint(pl)
app.register_blueprint(f1)


@app.route("/health")
def health():
    return {"status": "API Running"}


@app.route("/db-test")
def db_test():
    try:
        db.session.execute(db.text("SELECT 1"))
        return {"status": "Database connected"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}, 500


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)