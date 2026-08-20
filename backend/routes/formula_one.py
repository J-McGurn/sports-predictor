from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db
from models.season import Season
from models.f1_driver import F1Driver
from models.f1_constructor import F1Constructor
from models.f1_driver_prediction import F1DriverPrediction
from models.f1_constructor_prediction import F1ConstructorPrediction


f1 = Blueprint("f1", __name__, url_prefix="/f1")


@f1.route("/drivers", methods=["GET"])
def get_drivers():
    season_id = request.args.get("season_id", type=int)

    if not season_id:
        return {
            "error": "season_id is required"
        }, 400

    season = Season.query.filter_by(
        id=season_id,
        sport="F1"
    ).first()

    if not season:
        return {
            "error": "F1 season not found"
        }, 404

    drivers = F1Driver.query.filter_by(
        season_id=season_id
    ).order_by(F1Driver.name).all()

    return {
        "season": season.name,
        "drivers": [
            {
                "id": driver.id,
                "name": driver.name,
                "abbreviation": driver.abbreviation,
                "constructor": {
                    "id": driver.constructor.id,
                    "name": driver.constructor.name,
                    "abbreviation": driver.constructor.abbreviation
                }
            }
            for driver in drivers
        ]
    }, 200


@f1.route("/constructors", methods=["GET"])
def get_constructors():
    season_id = request.args.get("season_id", type=int)

    if not season_id:
        return {
            "error": "season_id is required"
        }, 400

    season = Season.query.filter_by(
        id=season_id,
        sport="F1"
    ).first()

    if not season:
        return {
            "error": "F1 season not found"
        }, 404

    constructors = F1Constructor.query.filter_by(
        season_id=season_id
    ).order_by(F1Constructor.name).all()

    return {
        "season": season.name,
        "constructors": [
            {
                "id": constructor.id,
                "name": constructor.name,
                "abbreviation": constructor.abbreviation
            }
            for constructor in constructors
        ]
    }, 200
    
    
@f1.route("/predictions/drivers", methods=["POST"])
@jwt_required()
def submit_driver_prediction():
    user_id = get_jwt_identity()
    data = request.get_json()

    season_id = data.get("season_id")
    predictions = data.get("predictions")

    if not season_id or not predictions:
        return {
            "error": "season_id and predictions are required"
        }, 400

    season = Season.query.filter_by(
        id=season_id,
        sport="F1"
    ).first()

    if not season:
        return {
            "error": "F1 season not found"
        }, 404

    if len(predictions) != 22:
        return {
            "error": "Exactly 22 driver predictions are required"
        }, 400

    driver_ids = [
        prediction.get("driver_id")
        for prediction in predictions
    ]

    positions = [
        prediction.get("position")
        for prediction in predictions
    ]

    if len(set(driver_ids)) != 22:
        return {
            "error": "Each driver must appear exactly once"
        }, 400

    if sorted(positions) != list(range(1, 23)):
        return {
            "error": "Positions must contain every number from 1 to 22 exactly once"
        }, 400

    valid_driver_ids = {
        driver.id
        for driver in F1Driver.query.filter_by(
            season_id=season_id
        ).all()
    }

    if set(driver_ids) != valid_driver_ids:
        return {
            "error": "Predictions must contain every driver in the selected season"
        }, 400

    existing_predictions = F1DriverPrediction.query.filter_by(
        user_id=user_id,
        season_id=season_id
    ).all()

    for prediction in existing_predictions:
        db.session.delete(prediction)
        
    db.session.flush()

    for prediction in predictions:
        db.session.add(
            F1DriverPrediction(
                user_id=user_id,
                season_id=season_id,
                driver_id=prediction["driver_id"],
                predicted_position=prediction["position"]
            )
        )

    db.session.commit()

    return {
        "message": "F1 Drivers' Championship prediction saved successfully"
    }, 201
    
    
@f1.route("/predictions/constructors", methods=["POST"])
@jwt_required()
def submit_constructor_prediction():
    user_id = get_jwt_identity()
    data = request.get_json()

    season_id = data.get("season_id")
    predictions = data.get("predictions")

    if not season_id or not predictions:
        return {
            "error": "season_id and predictions are required"
        }, 400

    season = Season.query.filter_by(
        id=season_id,
        sport="F1"
    ).first()

    if not season:
        return {
            "error": "F1 season not found"
        }, 404

    if len(predictions) != 11:
        return {
            "error": "Exactly 11 constructor predictions are required"
        }, 400

    constructor_ids = [
        prediction.get("constructor_id")
        for prediction in predictions
    ]

    positions = [
        prediction.get("position")
        for prediction in predictions
    ]

    if len(set(constructor_ids)) != 11:
        return {
            "error": "Each constructor must appear exactly once"
        }, 400

    if sorted(positions) != list(range(1, 12)):
        return {
            "error": "Positions must contain every number from 1 to 11 exactly once"
        }, 400

    valid_constructor_ids = {
        constructor.id
        for constructor in F1Constructor.query.filter_by(
            season_id=season_id
        ).all()
    }

    if set(constructor_ids) != valid_constructor_ids:
        return {
            "error": "Predictions must contain every constructor in the selected season"
        }, 400

    existing_predictions = F1ConstructorPrediction.query.filter_by(
        user_id=user_id,
        season_id=season_id
    ).all()

    for prediction in existing_predictions:
        db.session.delete(prediction)
            
    db.session.flush()

    for prediction in predictions:
        db.session.add(
            F1ConstructorPrediction(
                user_id=user_id,
                season_id=season_id,
                constructor_id=prediction["constructor_id"],
                predicted_position=prediction["position"]
            )
        )

    db.session.commit()

    return {
        "message": "F1 Constructors' Championship prediction saved successfully"
    }, 201
    
    
@f1.route("/predictions/drivers", methods=["GET"])
@jwt_required()
def get_driver_prediction():
    user_id = get_jwt_identity()
    season_id = request.args.get("season_id", type=int)

    if not season_id:
        return {
            "error": "season_id is required"
        }, 400

    season = Season.query.filter_by(
        id=season_id,
        sport="F1"
    ).first()

    if not season:
        return {
            "error": "F1 season not found"
        }, 404

    predictions = (
        F1DriverPrediction.query
        .filter_by(
            user_id=user_id,
            season_id=season_id
        )
        .order_by(F1DriverPrediction.predicted_position)
        .all()
    )

    return {
        "season": season.name,
        "predictions": [
            {
                "position": prediction.predicted_position,
                "driver": {
                    "id": prediction.driver.id,
                    "name": prediction.driver.name,
                    "abbreviation": prediction.driver.abbreviation
                }
            }
            for prediction in predictions
        ]
    }, 200
    
    
@f1.route("/predictions/constructors", methods=["GET"])
@jwt_required()
def get_constructor_prediction():
    user_id = get_jwt_identity()
    season_id = request.args.get("season_id", type=int)

    if not season_id:
        return {
            "error": "season_id is required"
        }, 400

    season = Season.query.filter_by(
        id=season_id,
        sport="F1"
    ).first()

    if not season:
        return {
            "error": "F1 season not found"
        }, 404

    predictions = (
        F1ConstructorPrediction.query
        .filter_by(
            user_id=user_id,
            season_id=season_id
        )
        .order_by(F1ConstructorPrediction.predicted_position)
        .all()
    )

    return {
        "season": season.name,
        "predictions": [
            {
                "position": prediction.predicted_position,
                "constructor": {
                    "id": prediction.constructor.id,
                    "name": prediction.constructor.name,
                    "abbreviation": prediction.constructor.abbreviation
                }
            }
            for prediction in predictions
        ]
    }, 200