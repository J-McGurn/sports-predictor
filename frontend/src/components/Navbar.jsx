import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const token = localStorage.getItem("access_token");

  function handleLogout() {
    localStorage.removeItem("access_token");
    navigate("/");
  }

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
          {token ? (
            <>
              <Link to="/dashboard">Dashboard</Link>

              <button
                onClick={handleLogout}
                className="navbar-logout"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login">Login</Link>

              <Link to="/register" className="navbar-register">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;