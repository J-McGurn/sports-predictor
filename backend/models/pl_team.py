from models import db


class PLTeam(db.Model):
    __tablename__ = "pl_teams"

    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(
        db.Integer,
        db.ForeignKey("seasons.id"),
        nullable=False
    )
    name = db.Column(db.String(100), nullable=False)

    season = db.relationship("Season", backref="pl_teams")

    __table_args__ = (
        db.UniqueConstraint(
            "season_id",
            "name",
            name="unique_team_per_season"
        ),
    )