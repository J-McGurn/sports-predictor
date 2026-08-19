from models import db


class F1ConstructorPrediction(db.Model):
    __tablename__ = "f1_constructor_predictions"

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

    constructor_id = db.Column(
        db.Integer,
        db.ForeignKey("f1_constructors.id"),
        nullable=False
    )

    predicted_position = db.Column(
        db.Integer,
        nullable=False
    )

    user = db.relationship(
        "User",
        backref="f1_constructor_predictions"
    )

    season = db.relationship(
        "Season",
        backref="f1_constructor_predictions"
    )

    constructor = db.relationship(
        "F1Constructor",
        backref="predictions"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "season_id",
            "constructor_id",
            name="unique_f1_constructor_prediction"
        ),

        db.UniqueConstraint(
            "user_id",
            "season_id",
            "predicted_position",
            name="unique_f1_constructor_position"
        ),
    )