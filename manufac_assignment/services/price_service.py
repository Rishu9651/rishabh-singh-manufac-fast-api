import pandas as pd
from typing import Optional

def get_cities_products(df):
    return sorted(df['city'].unique()), sorted(df['product'].unique())

def filter_data(df, city, product, from_=None, to=None):
    q = (df['city'].str.lower() == city.lower()) & (df['product'].str.lower() == product.lower())
    filtered = df[q].copy()
    if from_:
        filtered = filtered[filtered['date'] >= pd.to_datetime(from_)]
    if to:
        filtered = filtered[filtered['date'] <= pd.to_datetime(to)]
    filtered = filtered.sort_values('date', ascending=False)
    return filtered

def get_raw_points(filtered):
    return [
        {
            'date': row['date'].strftime('%Y-%m-%d'),
            'price': row['price'],
            'unit': row['unit']
        }
        for _, row in filtered.iterrows()
    ]

def get_moving_average(filtered, window_days):
    filtered['ma'] = filtered['price'].rolling(window=window_days, min_periods=1).mean()
    return [
        {
            'date': row['date'].strftime('%Y-%m-%d'),
            'price': row['price'],
            # 'unit': row['unit'],
            'ma': row['ma']
        }
        for _, row in filtered.iterrows()
    ]

def get_anomalies(filtered, window_days, z_thresh):
    filtered['mean'] = filtered['price'].rolling(window=window_days, min_periods=1).mean()
    filtered['std'] = filtered['price'].rolling(window=window_days, min_periods=1).std(ddof=0).replace(0, 1e-9)
    filtered['z'] = ((filtered['price'] - filtered['mean']).abs() / filtered['std'])
    filtered['isAnomaly'] = filtered['z'] >= z_thresh
    return [
        {
            'date': row['date'].strftime('%Y-%m-%d'),
            'price': row['price'],
            # 'unit': row['unit'],
            'z': row['z'],
            'isAnomaly': bool(row['isAnomaly'])
        }
        for _, row in filtered.iterrows()
    ]

def parse_window(window: str) -> int:
    if window.endswith('d'):
        return int(window[:-1])
    elif window.endswith('w'):
        return int(window[:-1]) * 7
    else:
        return 7  # default 