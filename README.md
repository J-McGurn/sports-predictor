# Sports Predictor

A web application that allows users to register, predict sporting championship outcomes, and compare their predictions with other users.

## Sports

The initial version will support:

- Premier League
  - Predict the final league table
- Formula 1
  - Predict the Drivers' Championship
  - Predict the Constructors' Championship

More sports and prediction types may be added in the future.

## Tech Stack

### Frontend

- React
- Vite
- React Router

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS

### Database

- PostgreSQL

## Project Structure

```text
sports-predictor/
├── backend/
│   ├── models/
│   ├── routes/
│   ├── scripts/
│   ├── app.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md