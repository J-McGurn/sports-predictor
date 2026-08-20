import { Link } from "react-router-dom";

function Dashboard() {
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

          <div className="prediction-status-list">
            <div className="prediction-status-item">
              <div>
                <strong>Premier League</strong>
                <span>Final table</span>
              </div>

              <span className="status incomplete">
                Not completed
              </span>
            </div>

            <div className="prediction-status-item">
              <div>
                <strong>F1 Drivers</strong>
                <span>Drivers' Championship</span>
              </div>

              <span className="status incomplete">
                Not completed
              </span>
            </div>

            <div className="prediction-status-item">
              <div>
                <strong>F1 Constructors</strong>
                <span>Constructors' Championship</span>
              </div>

              <span className="status incomplete">
                Not completed
              </span>
            </div>
          </div>
        </section>
      </section>
    </main>
  );
}

export default Dashboard;