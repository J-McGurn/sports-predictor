import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import app
from models import db
from models.season import Season
from models.pl_team import PLTeam
from models.f1_driver import F1Driver
from models.f1_constructor import F1Constructor


PL_TEAMS = [
    "Arsenal",
    "Aston Villa",
    "AFC Bournemouth",
    "Brentford",
    "Brighton & Hove Albion",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Fulham",
    "Leeds United",
    "Liverpool",
    "Manchester City",
    "Manchester United",
    "Newcastle United",
    "Nottingham Forest",
    "Sunderland",
    "Tottenham Hotspur",
    "Coventry City",
    "Ipswich Town",
    "Hull City",
]


F1_CONSTRUCTORS = [
    ("Mercedes", "MER"),
    ("Ferrari", "FER"),
    ("McLaren", "MCL"),
    ("Red Bull Racing", "RBR"),
    ("Racing Bulls", "RB"),
    ("Alpine", "ALP"),
    ("Haas", "HAA"),
    ("Audi", "AUD"),
    ("Williams", "WIL"),
    ("Aston Martin", "AST"),
    ("Cadillac", "CAD"),
]


F1_DRIVERS = [
    ("George Russell", "RUS", "Mercedes"),
    ("Kimi Antonelli", "ANT", "Mercedes"),

    ("Charles Leclerc", "LEC", "Ferrari"),
    ("Lewis Hamilton", "HAM", "Ferrari"),

    ("Lando Norris", "NOR", "McLaren"),
    ("Oscar Piastri", "PIA", "McLaren"),

    ("Max Verstappen", "VER", "Red Bull Racing"),
    ("Isack Hadjar", "HAD", "Red Bull Racing"),

    ("Liam Lawson", "LAW", "Racing Bulls"),
    ("Arvid Lindblad", "LIN", "Racing Bulls"),

    ("Pierre Gasly", "GAS", "Alpine"),
    ("Franco Colapinto", "COL", "Alpine"),

    ("Esteban Ocon", "OCO", "Haas"),
    ("Oliver Bearman", "BEA", "Haas"),

    ("Nico Hulkenberg", "HUL", "Audi"),
    ("Gabriel Bortoleto", "BOR", "Audi"),

    ("Carlos Sainz", "SAI", "Williams"),
    ("Alexander Albon", "ALB", "Williams"),

    ("Fernando Alonso", "ALO", "Aston Martin"),
    ("Lance Stroll", "STR", "Aston Martin"),

    ("Sergio Perez", "PER", "Cadillac"),
    ("Valtteri Bottas", "BOT", "Cadillac"),
]


with app.app_context():

    # --------------------------------------------------
    # SEASON
    # --------------------------------------------------

    season = Season.query.filter_by(
        sport="PL",
        name="2026/27"
    ).first()

    if not season:
        season = Season(
            sport="PL",
            name="2026/27",
            is_active=True
        )

        db.session.add(season)
        db.session.commit()

        print("Created season: 2026/27")
    else:
        print("Season already exists.")
        
        
    f1_season = Season.query.filter_by(
        sport="F1",
        name="2026"
    ).first()

    if not f1_season:
        f1_season = Season(
            sport="F1",
            name="2026",
            is_active=True
        )

        db.session.add(f1_season)
        db.session.commit()

        print("Created F1 season: 2026")
    else:
        print("F1 season already exists.")

    # --------------------------------------------------
    # PREMIER LEAGUE
    # --------------------------------------------------

    print("\nSeeding Premier League teams...")

    for team_name in PL_TEAMS:

        existing_team = PLTeam.query.filter_by(
            season_id=season.id,
            name=team_name
        ).first()

        if not existing_team:
            db.session.add(
                PLTeam(
                    season_id=season.id,
                    name=team_name
                )
            )

            print(f"Added PL team: {team_name}")

    # --------------------------------------------------
    # F1 CONSTRUCTORS
    # --------------------------------------------------

    print("\nSeeding F1 constructors...")

    constructors = {}

    for name, abbreviation in F1_CONSTRUCTORS:

        constructor = F1Constructor.query.filter_by(
            season_id=f1_season.id,
            name=name
        ).first()

        if not constructor:
            constructor = F1Constructor(
                season_id=f1_season.id,
                name=name,
                abbreviation=abbreviation
            )

            db.session.add(constructor)
            db.session.flush()

            print(f"Added F1 constructor: {name}")

        constructors[name] = constructor

    # --------------------------------------------------
    # F1 DRIVERS
    # --------------------------------------------------

    print("\nSeeding F1 drivers...")

    for name, abbreviation, constructor_name in F1_DRIVERS:

        existing_driver = F1Driver.query.filter_by(
            season_id=f1_season.id,
            name=name
        ).first()

        if not existing_driver:
            db.session.add(
                F1Driver(
                    season_id=f1_season.id,
                    name=name,
                    abbreviation=abbreviation,
                    constructor_id=constructors[constructor_name].id
                )
            )

            print(
                f"Added F1 driver: "
                f"{name} → {constructor_name}"
            )

    db.session.commit()

    print("\n===================================")
    print("Database seeded successfully!")
    print("===================================")