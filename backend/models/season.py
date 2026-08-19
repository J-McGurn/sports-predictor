from models import db


class Season(db.Model):
    __tablename__ = "seasons"

    id = db.Column(db.Integer, primary_key=True)

    sport = db.Column(
        db.String(20),
        nullable=False
    )

    name = db.Column(
        db.String(20),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "sport",
            "name",
            name="unique_sport_season"
        ),
    )