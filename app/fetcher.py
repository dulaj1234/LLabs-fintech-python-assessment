from symtable import Symbol

import httpx
import os
from dotenv import load_dotenv

# Load the .env file to read ALPHAVANTAGE_API_KEY and ALPHAVANTAGE_API_URL
load_dotenv()

# Read the API key from the .env file
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

# The base URL for AlphaVantage read from .env file
BASE_URL = os.getenv("ALPHAVANTAGE_API_URL")

async def get_monthly_mkt_data(symbol: str) -> dict:
    """
    Calls the AlphaVantage API and return all monthly data for given symbol as a data set.
    """
    # create params for the URL
    params = {
        "function": "TIME_SERISE_MONTHLY",
        "symbol": symbol.upper(),
        "apikey": API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

    if "Error Message" in data:
        raise ValueError(f"Invalid Symbol '{symbol}': {data['Error Message']}")
    
    if "Information" in data:
        raise ValueError(f"API limit reached: {data['Information']}")
    
    monthly_time_series = data.get("Monthly Time Series")

    if not monthly_time_series:
        raise ValueError(f"No data returned for the symbol '{symbol}'")
    
    return monthly_time_series

def filter_data_by_year(monthly_time_series: dict, year: str) -> dict:
    """
    AlphaVantage returns all historical data for the given symbol.
    """
    filtered = {
        date: values
        for date, values in monthly_time_series.items()
        if date.startswith(year)
    }

    if not filtered:
        raise ValueError(f"No data found for the given yeat '{year}'")
    
    return filtered
    
