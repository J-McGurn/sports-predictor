import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  getActiveSeasons,
  getPLPrediction,
  getF1DriverPrediction,
  getF1ConstructorPrediction,
} from "../services/api";

function Dashboard() {
  const [statuses, setStatuses] = useState({
    premierLeague: false,
    f1Drivers: false,
    f1Constructors: false,
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadPredictionStatus() {
      try {
        const seasonData = await getActiveSeasons();

        const plSeason = seasonData.seasons.find(
          (season) => season.sport === "PL"
        );

        const f1Season = seasonData.seasons.find(
          (season) => season.sport === "F1"
        );

        const results = await Promise.all([
          plSeason
            ? getPLPrediction(plSeason.id)
            : Promise.resolve(null),

          f1Season
            ? getF1DriverPrediction(f1Season.id)
            : Promise.resolve(null),

          f1Season
            ? getF1ConstructorPrediction(f1Season.id)
            : Promise.resolve(null),
        ]);

        const [
          plPrediction,
          f1DriverPrediction,
          f1ConstructorPrediction,
        ] = results;

        setStatuses({
          premierLeague:
            plPrediction?.predictions?.length === 20,

          f1Drivers:
            f1DriverPrediction?.predictions?.length === 22,

          f1Constructors:
            f1ConstructorPrediction?.predictions?.length === 11,
        });
      } catch (error) {
        console.error(
          "Unable to load prediction status:",
          error
        );
      } finally {
        setLoading(false);
      }
    }

    loadPredictionStatus();
  }, []);

  return (
    <main className="dashboard">
      <section className="dashboard-container">

        <div className="dashboard-header">
          <h1>Welcome back!</h1>
          <p>What would you like to predict?</p>
        </div>

        <section>
          <h2>Choose a sport</h2>

          <div className="dashboard-sports">

            <Link
              to="/premier-league"
              className="dashboard-sport-card"
            >
              <div className="dashboard-sport-icon">
                ⚽
              </div>

              <div>
                <h3>Premier League</h3>
                <p>
                  Predict the final Premier League table.
                </p>
              </div>
            </Link>

            <Link
              to="/formula-one"
              className="dashboard-sport-card"
            >
              <div className="dashboard-sport-icon">
                🏎️
              </div>

              <div>
                <h3>Formula 1</h3>
                <p>
                  Predict the Drivers' and Constructors'
                  Championships.
                </p>
              </div>
            </Link>

          </div>
        </section>

        <section className="prediction-status">

          <h2>Your predictions</h2>

          {loading ? (
            <p>Loading prediction status...</p>
          ) : (
            <div className="prediction-status-list">

              <PredictionStatus
                title="Premier League"
                subtitle="Final table"
                completed={statuses.premierLeague}
                link="/premier-league"
              />

              <PredictionStatus
                title="F1 Drivers"
                subtitle="Drivers' Championship"
                completed={statuses.f1Drivers}
                link="/formula-one"
              />

              <PredictionStatus
                title="F1 Constructors"
                subtitle="Constructors' Championship"
                completed={statuses.f1Constructors}
                link="/formula-one"
              />

            </div>
          )}

        </section>

      </section>
    </main>
  );
}


function PredictionStatus({
  title,
  subtitle,
  completed,
  link,
}) {
  return (
    <Link
      to={link}
      className="prediction-status-item"
    >
      <div>
        <strong>{title}</strong>
        <span>{subtitle}</span>
      </div>

      <span
        className={`status ${
          completed ? "complete" : "incomplete"
        }`}
      >
        {completed ? "✓ Completed" : "Not completed"}
      </span>
    </Link>
  );
}

export default Dashboard;