# India Metro Fuel-Price Time-Series API

A FastAPI-based service for daily retail Petrol & Diesel prices in Delhi, Mumbai, Chennai, and Kolkata. Provides raw, moving-average, and anomaly-flagged time-series data.

## Features
- **/ts/raw**: Raw daily price series
- **/ts/ma**: Moving average series (windowed)
- **/ts/anomaly**: Anomaly-flagged series (Z-score)

## Requirements
- Python 3.9–3.12
- [Poetry](https://python-poetry.org/)
- Docker (optional)

## Local Setup
1. **Install dependencies:**
   ```sh
   poetry install
   ```
2. **Run the server:**
   ```sh
   poetry run uvicorn manufac_assignment.main:app --reload
   ```
3. **Access the API docs:**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Docker Usage
1. **Build the image:**
   ```sh
   docker build -t manufac_assignment .
   ```
2. **Run the container:**
   ```sh
   docker run -p 8000:8000 manufac-assignment
   ```
3. **Access the API docs:**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Data
- The dataset should be placed in `data/Retail Selling Price (RSP) of Petrol and Diesel in Metro Cities.csv`.
- The app loads this data at startup.

## Endpoints
- `GET /ts/raw`: Raw price points
- `GET /ts/ma`: Moving average points (query param: `window`)
- `GET /ts/anomaly`: Anomaly-flagged points (query params: `window`, `z`)

See the OpenAPI spec or `/docs` for full details. 