import pandas as pd
from typing import Optional

"""
    @description Returns sorted lists of unique city names and product names from the DataFrame.
    @param df: The pandas DataFrame containing the fuel price data.
    @returns: (cities, products) - two sorted lists of unique city and product names.
"""
def get_cities_products(df):
    return sorted(df['city'].unique()), sorted(df['product'].unique())


"""
    @description Filters the DataFrame for a specific city, product, and optional date range.
    @param df: The pandas DataFrame containing the fuel price data.
    @param city: The city to filter by.
    @param product: The product to filter by.
    @param from_: Optional start date (YYYY-MM-DD).
    @param to: Optional end date (YYYY-MM-DD).
    @returns: Filtered DataFrame sorted by date descending.
"""
def filter_data(df, city, product, from_=None, to=None):
    q = (df['city'].str.lower() == city.lower()) & (df['product'].str.lower() == product.lower())
    filtered = df[q].copy()
    if from_:
        filtered = filtered[filtered['date'] >= pd.to_datetime(from_)]
    if to:
        filtered = filtered[filtered['date'] <= pd.to_datetime(to)]
    filtered = filtered.sort_values('date', ascending=False)
    return filtered


"""
    @description Converts filtered DataFrame rows to a list of raw price point dicts.
    @param filtered: The filtered DataFrame.
    @returns: List of dicts with date, price, and unit for each record.
"""
def get_raw_points(filtered):
    return [
        {
            'date': row['date'].strftime('%Y-%m-%d'),
            'price': row['price'],
            'unit': row['unit']
        }
        for _, row in filtered.iterrows()
    ]


"""
    @description Calculates moving average for the filtered data and returns as list of dicts.
    @param filtered: The filtered DataFrame.
    @param window_days: The window size in days for the moving average.
    @returns: List of dicts with date, price, unit, and moving average (ma).
"""
def get_moving_average(filtered, window_days):
    filtered['ma'] = filtered['price'].rolling(window=window_days, min_periods=1).mean()
    return [
        {
            'date': row['date'].strftime('%Y-%m-%d'),
            'price': row['price'],
            'unit': row['unit'],
            'ma': row['ma']
        }
        for _, row in filtered.iterrows()
    ]


"""
    @description Calculates Z-score anomalies for the filtered data and returns as list of dicts.
    @param filtered: The filtered DataFrame.
    @param window_days: The window size in days for rolling calculations.
    @param z_thresh: The Z-score threshold for anomaly detection.
    @returns: List of dicts with date, price, unit, z-score, and anomaly flag.
"""
def get_anomalies(filtered, window_days, z_thresh):
    filtered['mean'] = filtered['price'].rolling(window=window_days, min_periods=1).mean()
    filtered['std'] = filtered['price'].rolling(window=window_days, min_periods=1).std(ddof=0).replace(0, 1e-9)
    filtered['z'] = ((filtered['price'] - filtered['mean']).abs() / filtered['std'])
    filtered['isAnomaly'] = filtered['z'] >= z_thresh
    return [
        {
            'date': row['date'].strftime('%Y-%m-%d'),
            'price': row['price'],
            'unit': row['unit'],
            'z': row['z'],
            'isAnomaly': bool(row['isAnomaly'])
        }
        for _, row in filtered.iterrows()
    ]


"""
    @description Parses a window string (e.g., '7d', '2w') into an integer number of days.
    @param window: The window string to parse.
    @returns: The window size in days as an integer.
"""
def parse_window(window: str) -> int:
    if window.endswith('d'):
        return int(window[:-1])
    elif window.endswith('w'):
        return int(window[:-1]) * 7
    else:
        return 7  # default 