import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          Sports Predictor
        </Link>

        <div className="navbar-links">
          <Link to="/premier-league">Premier League</Link>
          <Link to="/formula-one">Formula 1</Link>
        </div>

        <div className="navbar-auth">
          <Link to="/login">Login</Link>

          <Link to="/register" className="navbar-register">
            Register
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;