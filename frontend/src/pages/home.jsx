import { Link } from "react-router-dom";

function Home() {
  return (
    <main className="home">
      <section className="hero">
        <h1>Sports Predictor</h1>

        <p className="hero-subtitle">
          Predict the season. Beat everyone.
        </p>

        <div className="sport-cards">
          <Link to="/premier-league" className="sport-card">
            <div className="sport-icon">⚽</div>

            <h2>Premier League</h2>

            <p>
              Predict the final Premier League table
              before the season begins.
            </p>
          </Link>

          <Link to="/formula-one" className="sport-card">
            <div className="sport-icon">🏎️</div>

            <h2>Formula 1</h2>

            <p>
              Predict the Drivers' and Constructors'
              Championships.
            </p>
          </Link>
        </div>

        <div className="auth-links">
          <Link to="/login">Login</Link>
          <Link to="/register" className="register-button">
            Register
          </Link>
        </div>
      </section>
    </main>
  );
}

export default Home;