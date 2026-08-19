from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db
from models.season import Season
from models.pl_team import PLTeam
from models.pl_prediction import PLPrediction


pl = Blueprint("premier_league", __name__, url_prefix="/pl")


@pl.route("/teams", methods=["GET"])
def get_teams():
    season_id = request.args.get("season_id", type=int)

    if not season_id:
        return {
            "error": "season_id is required"
        }, 400

    season = Season.query.get(season_id)

    if not season:
        return {
            "error": "Season not found"
        }, 404

    teams = PLTeam.query.filter_by(
        season_id=season_id
    ).order_by(PLTeam.name).all()

    return {
        "season": season.name,
        "teams": [
            {
                "id": team.id,
                "name": team.name
            }
            for team in teams
        ]
    }, 200


@pl.route("/predictions", methods=["POST"])
@jwt_required()
def submit_prediction():
    user_id = get_jwt_identity()
    data = request.get_json()

    season_id = data.get("season_id")
    predictions = data.get("predictions")

    if not season_id or not predictions:
        return {
            "error": "season_id and predictions are required"
        }, 400

    season = Season.query.get(season_id)

    if not season:
        return {
            "error": "Season not found"
        }, 404

    if len(predictions) != 20:
        return {
            "error": "Exactly 20 predictions are required"
        }, 400

    team_ids = [prediction.get("team_id") for prediction in predictions]
    positions = [prediction.get("position") for prediction in predictions]

    if len(set(team_ids)) != 20:
        return {
            "error": "Each team must appear exactly once"
        }, 400

    if sorted(positions) != list(range(1, 21)):
        return {
            "error": "Positions must contain every number from 1 to 20 exactly once"
        }, 400

    valid_team_ids = {
        team.id
        for team in PLTeam.query.filter_by(
            season_id=season_id
        ).all()
    }

    if set(team_ids) != valid_team_ids:
        return {
            "error": "Predictions must contain every team in the selected season"
        }, 400

    existing_predictions = PLPrediction.query.filter_by(
        user_id=user_id,
        season_id=season_id
    ).all()

    for prediction in existing_predictions:
        db.session.delete(prediction)

    # Force the DELETE statements to be sent to the database
    # before inserting the replacement predictions.
    db.session.flush()

    for prediction in predictions:
        new_prediction = PLPrediction(
            user_id=user_id,
            season_id=season_id,
            team_id=prediction["team_id"],
            predicted_position=prediction["position"]
        )

        db.session.add(new_prediction)

    db.session.commit()

    return {
        "message": "Premier League prediction saved successfully"
    }, 201
    

@pl.route("/predictions", methods=["GET"])
@jwt_required()
def get_prediction():
    user_id = get_jwt_identity()
    season_id = request.args.get("season_id", type=int)

    if not season_id:
        return {
            "error": "season_id is required"
        }, 400

    season = Season.query.get(season_id)

    if not season:
        return {
            "error": "Season not found"
        }, 404

    predictions = (
        PLPrediction.query
        .filter_by(
            user_id=user_id,
            season_id=season_id
        )
        .order_by(PLPrediction.predicted_position)
        .all()
    )

    return {
        "season": season.name,
        "predictions": [
            {
                "position": prediction.predicted_position,
                "team": {
                    "id": prediction.team.id,
                    "name": prediction.team.name
                }
            }
            for prediction in predictions
        ]
    }, 200