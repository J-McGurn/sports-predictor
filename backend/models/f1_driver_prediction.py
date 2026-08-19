from models import db


class F1DriverPrediction(db.Model):
    __tablename__ = "f1_driver_predictions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    season_id = db.Column(
        db.Integer,
        db.ForeignKey("seasons.id"),
        nullable=False
    )

    driver_id = db.Column(
        db.Integer,
        db.ForeignKey("f1_drivers.id"),
        nullable=False
    )

    predicted_position = db.Column(
        db.Integer,
        nullable=False
    )

    user = db.relationship(
        "User",
        backref="f1_driver_predictions"
    )

    season = db.relationship(
        "Season",
        backref="f1_driver_predictions"
    )

    driver = db.relationship(
        "F1Driver",
        backref="predictions"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "season_id",
            "driver_id",
            name="unique_f1_driver_prediction"
        ),

        db.UniqueConstraint(
            "user_id",
            "season_id",
            "predicted_position",
            name="unique_f1_driver_position"
        ),
    )