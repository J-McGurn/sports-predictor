from flask import Blueprint

from models.season import Season


season = Blueprint("season", __name__, url_prefix="/seasons")


@season.route("/active", methods=["GET"])
def get_active_seasons():
    seasons = Season.query.filter_by(
        is_active=True
    ).all()

    return {
        "seasons": [
            {
                "id": current_season.id,
                "sport": current_season.sport,
                "name": current_season.name
            }
            for current_season in seasons
        ]
    }, 200