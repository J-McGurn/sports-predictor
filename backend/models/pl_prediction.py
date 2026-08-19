from models import db


class PLPrediction(db.Model):
    __tablename__ = "pl_predictions"

    id = db.Column(db.Integer, primary_key=True)

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

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("pl_teams.id"),
        nullable=False
    )

    predicted_position = db.Column(
        db.Integer,
        nullable=False
    )

    user = db.relationship("User", backref="pl_predictions")
    season = db.relationship("Season", backref="pl_predictions")
    team = db.relationship("PLTeam", backref="predictions")

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "season_id",
            "team_id",
            name="unique_pl_prediction"
        ),
        db.UniqueConstraint(
            "user_id",
            "season_id",
            "predicted_position",
            name="unique_pl_position"
        ),
    )