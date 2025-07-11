import os
import pandas as pd

"""
    @description Loads and standardizes the fuel price data from the CSV file into a pandas DataFrame.
    @returns: DataFrame with columns: date, city, product, price, unit. Missing values are filled with 0.
"""
def load_fuel_data():
    CSV_PATH = os.path.join(os.path.dirname(__file__), '../../data/Retail Selling Price (RSP) of Petrol and Diesel in Metro Cities.csv')
    RAW_COLS = {
        'date': 'Calendar Day',
        'city': 'Metro Cities',
        'product': 'Products ',  
        'price': 'Retail Selling Price (Rsp) Of Petrol And Diesel (UOM:INR/L(IndianRupeesperLitre)), Scaling Factor:1'
    }
    raw_df = pd.read_csv(CSV_PATH).fillna(0)
    df = pd.DataFrame({
        'date': pd.to_datetime(raw_df[RAW_COLS['date']]),
        'city': raw_df[RAW_COLS['city']].str.strip(),
        'product': raw_df[RAW_COLS['product']].str.strip(),
        'price': pd.to_numeric(raw_df[RAW_COLS['price']], errors='coerce').fillna(0),
        'unit': 'INR/L',
    })
    return df 