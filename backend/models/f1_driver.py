from models import db


class F1Driver(db.Model):
    __tablename__ = "f1_drivers"

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
        db.String(3),
        nullable=False
    )

    constructor_id = db.Column(
        db.Integer,
        db.ForeignKey("f1_constructors.id"),
        nullable=False
    )

    season = db.relationship(
        "Season",
        backref="f1_drivers"
    )

    constructor = db.relationship(
        "F1Constructor",
        backref="drivers"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "season_id",
            "name",
            name="unique_f1_driver_per_season"
        ),
    )