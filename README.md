# India Metro Fuel-Price Time-Series API

**Repository:** [https://github.com/Rishu9651/rishabh-singh-manufac-fast-api](https://github.com/Rishu9651/rishabh-singh-manufac-fast-api)

A FastAPI-based service for daily retail Petrol & Diesel prices in Delhi, Mumbai, Chennai, and Kolkata. Provides raw, moving-average, and anomaly-flagged time-series data.

## Features

- **Raw Time-Series Data**: Access unprocessed daily fuel prices
- **Moving Average Analysis**: Calculate rolling averages with configurable windows
- **Anomaly Detection**: Identify price anomalies using Z-score methodology
- **RESTful API**: Clean, documented endpoints with automatic OpenAPI specification
- **Docker Support**: Containerized deployment for easy setup

## Requirements

- Python 3.9–3.12
- [Poetry](https://python-poetry.org/) for dependency management
- Docker (optional, for containerized deployment)

## Installation & Setup

### Option 1: Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rishu9651/rishabh-singh-manufac-fast-api.git
   cd rishabh-singh-manufac-fast-api
   ```
2. **Install dependencies:**
   ```bash
   poetry install
   ```
3. **Run the server:**
   ```bash
   poetry run uvicorn manufac_assignment.main:app --reload
   ```
4. **Access the API documentation:**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Option 2: Docker Deployment

1. **Build the Docker image:**
   ```bash
   docker build -t manufac_assignment .
   ```
2. **Run the container:**
   ```bash
   docker run -p 8000:8000 manufac_assignment
   ```
3. **Access the API documentation:**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Data

The application uses the **Retail Selling Price (RSP) of Petrol and Diesel in Metro Cities** dataset from the National Data and Analytics Platform (NITI Aayog).

- **Data Location**: `data/Retail Selling Price (RSP) of Petrol and Diesel in Metro Cities.csv`
- **Cities Covered**: Delhi, Mumbai, Chennai, Kolkata
- **Products**: Petrol, Diesel
- **Missing Values**: Treated as 0

## API Endpoints

All endpoints are versioned under `/v1`:

### 1. Raw Time-Series Data
```http
GET /v1/ts/raw
```
**Parameters:**
- `city` (required): One of the metro cities
- `product` (required): "Petrol" or "Diesel"
- `from` (optional): Start date (YYYY-MM-DD)
- `to` (optional): End date (YYYY-MM-DD)

**Example:**
```bash
curl "http://localhost:8000/v1/ts/raw?city=Delhi&product=Petrol&from=2023-01-01&to=2023-01-31"
```

### 2. Moving Average
```http
GET /v1/ts/ma
```
**Parameters:**
- `city` (required): One of the metro cities
- `product` (required): "Petrol" or "Diesel"
- `from` (optional): Start date (YYYY-MM-DD)
- `to` (optional): End date (YYYY-MM-DD)
- `window` (optional): Window size (default: "7d", supports "7d", "14d", "30d", "1w", "2w", etc.)

**Example:**
```bash
curl "http://localhost:8000/v1/ts/ma?city=Mumbai&product=Diesel&window=14d"
```

### 3. Anomaly Detection
```http
GET /v1/ts/anomaly
```
**Parameters:**
- `city` (required): One of the metro cities
- `product` (required): "Petrol" or "Diesel"
- `from` (optional): Start date (YYYY-MM-DD)
- `to` (optional): End date (YYYY-MM-DD)
- `window` (optional): Window size for calculation (default: "7d")
- `z` (optional): Z-score threshold (default: 2.5)

**Example:**
```bash
curl "http://localhost:8000/v1/ts/anomaly?city=Chennai&product=Petrol&z=3.0&window=30d"
```

## Project Structure

```
.
├── data/
│   └── Retail Selling Price (RSP) of Petrol and Diesel in Metro Cities.csv
├── manufac_assignment/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1.py              # API routes (version 1)
│   ├── models/
│   │   ├── __init__.py
│   │   └── price.py           # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   └── price_service.py   # Business logic
│   └── utils/
│       ├── __init__.py
│       └── data_loader.py     # Data loading utilities
├── Dockerfile
├── pyproject.toml
├── poetry.lock
└── README.md
```

## Testing

The API can be tested using:

1. **Swagger UI**: Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive testing
2. **cURL**: Use the examples provided above
3. **Postman**: Import the OpenAPI specification from `/docs`

## Development

### Adding New Endpoints

1. Add route definitions in `manufac_assignment/api/v1.py`
2. Add business logic in `manufac_assignment/services/`
3. Add Pydantic models in `manufac_assignment/models/` if needed

### Code Quality

- Follow PEP 8 style guidelines
- Use type hints throughout the codebase
- Add docstrings for functions and classes

## License

This project is created for educational and evaluation purposes.

## Contributing

This is a project submission. For questions or issues, please refer to the task requirements.

---

**Note**: This API is designed to handle the specific dataset format provided by NITI Aayog. Ensure the CSV file is placed in the `data/` directory before running the application.
