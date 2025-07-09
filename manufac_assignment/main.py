from fastapi import FastAPI, Query
from typing import List, Optional
from pydantic import BaseModel
import pandas as pd
import os
from datetime import datetime, timedelta

app = FastAPI(title="India Metro Fuel-Price Time-Series API")

# Adjusted for actual CSV structure
CSV_PATH = os.path.join(os.path.dirname(__file__), '../data/Retail Selling Price (RSP) of Petrol and Diesel in Metro Cities.csv')
RAW_COLS = {
    'date': 'Calendar Day',
    'city': 'Metro Cities',
    'product': 'Products ',  
    'price': 'Retail Selling Price (Rsp) Of Petrol And Diesel (UOM:INR/L(IndianRupeesperLitre)), Scaling Factor:1'
}

# Load and standardize data
raw_df = pd.read_csv(CSV_PATH).fillna(0)
df = pd.DataFrame({
    'date': pd.to_datetime(raw_df[RAW_COLS['date']]),
    'city': raw_df[RAW_COLS['city']].str.strip(),
    'product': raw_df[RAW_COLS['product']].str.strip(),
    'price': pd.to_numeric(raw_df[RAW_COLS['price']], errors='coerce').fillna(0),
    'unit': 'INR/L',
})

CITIES = sorted(df['city'].unique())
PRODUCTS = sorted(df['product'].unique())

class PricePoint(BaseModel):
    date: str
    price: float
    unit: str

class MovingAveragePoint(PricePoint):
    ma: float

class AnomalyPoint(PricePoint):
    z: float
    isAnomaly: bool

def parse_window(window: str) -> int:
    if window.endswith('d'):
        return int(window[:-1])
    elif window.endswith('w'):
        return int(window[:-1]) * 7
    else:
        return 7  # default

@app.get("/ts/raw", response_model=List[PricePoint])
def get_raw(
    city: str = Query(..., enum=CITIES),
    product: str = Query(..., enum=PRODUCTS),
    from_: Optional[str] = Query(None, alias="from"),
    to: Optional[str] = Query(None)
):
    q = (df['city'].str.lower() == city.lower()) & (df['product'].str.lower() == product.lower())
    filtered = df[q].copy()
    if from_:
        filtered = filtered[filtered['date'] >= pd.to_datetime(from_)]
    if to:
        filtered = filtered[filtered['date'] <= pd.to_datetime(to)]
    filtered = filtered.sort_values('date', ascending=False)
    return [
        PricePoint(date=row['date'].strftime('%Y-%m-%d'), price=row['price'], unit=row['unit'])
        for _, row in filtered.iterrows()
    ]

@app.get("/ts/ma", response_model=List[MovingAveragePoint])
def get_ma(
    city: str = Query(..., enum=CITIES),
    product: str = Query(..., enum=PRODUCTS),
    from_: Optional[str] = Query(None, alias="from"),
    to: Optional[str] = Query(None),
    window: str = Query("7d")
):
    days = parse_window(window)
    q = (df['city'].str.lower() == city.lower()) & (df['product'].str.lower() == product.lower())
    filtered = df[q].copy()
    if from_:
        filtered = filtered[filtered['date'] >= pd.to_datetime(from_)]
    if to:
        filtered = filtered[filtered['date'] <= pd.to_datetime(to)]
    filtered = filtered.sort_values('date', ascending=False)
    filtered['ma'] = filtered['price'].rolling(window=days, min_periods=1).mean()
    return [
        MovingAveragePoint(date=row['date'].strftime('%Y-%m-%d'), price=row['price'], unit=row['unit'], ma=row['ma'])
        for _, row in filtered.iterrows()
    ]

@app.get("/ts/anomaly", response_model=List[AnomalyPoint])
def get_anomaly(
    city: str = Query(..., enum=CITIES),
    product: str = Query(..., enum=PRODUCTS),
    from_: Optional[str] = Query(None, alias="from"),
    to: Optional[str] = Query(None),
    window: str = Query("7d"),
    z: float = Query(2.5)
):
    days = parse_window(window)
    q = (df['city'].str.lower() == city.lower()) & (df['product'].str.lower() == product.lower())
    filtered = df[q].copy()
    if from_:
        filtered = filtered[filtered['date'] >= pd.to_datetime(from_)]
    if to:
        filtered = filtered[filtered['date'] <= pd.to_datetime(to)]
    filtered = filtered.sort_values('date', ascending=False)
    filtered['mean'] = filtered['price'].rolling(window=days, min_periods=1).mean()
    filtered['std'] = filtered['price'].rolling(window=days, min_periods=1).std(ddof=0).replace(0, 1e-9)
    filtered['z'] = ((filtered['price'] - filtered['mean']).abs() / filtered['std'])
    filtered['isAnomaly'] = filtered['z'] >= z
    return [
        AnomalyPoint(date=row['date'].strftime('%Y-%m-%d'), price=row['price'], unit=row['unit'], z=row['z'], isAnomaly=bool(row['isAnomaly']))
        for _, row in filtered.iterrows()
    ]

@app.get("/")
def read_root():
    return {"message": "India Metro Fuel-Price Time-Series API is running."} 