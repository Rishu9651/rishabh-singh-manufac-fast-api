from fastapi import APIRouter, Query
from typing import List, Optional
from manufac_assignment.models.price import PricePoint, MovingAveragePoint, AnomalyPoint
from manufac_assignment.utils.data_loader import load_fuel_data
from manufac_assignment.services.price_service import (
    get_cities_products, filter_data, get_raw_points, get_moving_average, get_anomalies, parse_window
)

router = APIRouter()

df = load_fuel_data()
CITIES, PRODUCTS = get_cities_products(df)

# Returns raw price data for a given city, product, and optional date range
@router.get("/ts/raw", response_model=List[PricePoint])
def get_raw(
    city: str = Query(..., enum=CITIES),
    product: str = Query(..., enum=PRODUCTS),
    from_: Optional[str] = Query(None, alias="from"),
    to: Optional[str] = Query(None)
):
    filtered = filter_data(df, city, product, from_, to)
    return get_raw_points(filtered)

# Returns moving average price data for a given city, product, and window size
@router.get("/ts/ma", response_model=List[MovingAveragePoint])
def get_ma(
    city: str = Query(..., enum=CITIES),
    product: str = Query(..., enum=PRODUCTS),
    from_: Optional[str] = Query(None, alias="from"),
    to: Optional[str] = Query(None),
    window: str = Query("7d")
):
    days = parse_window(window)
    filtered = filter_data(df, city, product, from_, to)
    return get_moving_average(filtered, days)

# Returns anomaly-flagged price data for a given city, product, window size, and z-score threshold
@router.get("/ts/anomaly", response_model=List[AnomalyPoint])
def get_anomaly(
    city: str = Query(..., enum=CITIES),
    product: str = Query(..., enum=PRODUCTS),
    from_: Optional[str] = Query(None, alias="from"),
    to: Optional[str] = Query(None),
    window: str = Query("7d"),
    z: float = Query(2.5)
):
    days = parse_window(window)
    filtered = filter_data(df, city, product, from_, to)
    return get_anomalies(filtered, days, z) 