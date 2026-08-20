const API_URL = "http://127.0.0.1:5000";

async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("access_token");

  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || data.msg || "Something went wrong.");
  }

  return data;
}

export async function login(email, password) {
  return apiRequest("/login", {
    method: "POST",
    body: JSON.stringify({
      email,
      password,
    }),
  });
}

export async function register(username, email, password) {
  return apiRequest("/register", {
    method: "POST",
    body: JSON.stringify({
      username,
      email,
      password,
    }),
  });
}

export async function getActiveSeasons() {
  return apiRequest("/seasons/active");
}

export async function getPLTeams(seasonId) {
  return apiRequest(`/pl/teams?season_id=${seasonId}`);
}

export async function getPLPrediction(seasonId) {
  return apiRequest(`/pl/predictions?season_id=${seasonId}`);
}

export async function savePLPrediction(seasonId, predictions) {
  return apiRequest("/pl/predictions", {
    method: "POST",
    body: JSON.stringify({
      season_id: seasonId,
      predictions,
    }),
  });
}