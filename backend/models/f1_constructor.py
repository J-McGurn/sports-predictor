from models import db


class F1Constructor(db.Model):
    __tablename__ = "f1_constructors"

    id = db.Column(db.Integer, primary_key=True)

    season_id = db.Column(
        db.Integer,
        db.ForeignKey("seasons.id"),
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    abbreviation = db.Column(
        db.String(10),
        nullable=False
    )

    season = db.relationship(
        "Season",
        backref="f1_constructors"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "season_id",
            "name",
            name="unique_f1_constructor_per_season"
        ),
    )