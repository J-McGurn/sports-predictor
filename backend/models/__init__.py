from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User

from models.season import Season
from models.pl_team import PLTeam
from models.pl_prediction import PLPrediction

from models.f1_driver import F1Driver
from models.f1_constructor import F1Constructor
from models.f1_driver_prediction import F1DriverPrediction
from models.f1_constructor_prediction import F1ConstructorPrediction