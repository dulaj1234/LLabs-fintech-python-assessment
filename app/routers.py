from fastapi import APIRouter, HTTPException
from app.database import insert_monthly_mkt_data, get_annual_mkt_data, is_data_available_for_year
from app.fetcher import get_monthly_mkt_data, filter_data_by_year
import httpx
import datetime

router = APIRouter()

def input_validations(symbol: str, year: str):
    """
    Raises the exceptions immediately when validating the symbol and year
    """

    #validate symbol
    if not symbol or not symbol.isalpha():
        raise HTTPException(
            status_code=400,
            detail="Symbol must contain letters only like 'AAPL', 'IBM'."
        )
    
    if len(symbol) > 4:
        raise HTTPException(
            status_code=400,
            detail="Symbol is too long. Max: 4 characters."
        )
    
    #validate year
    if not year.isdigit() or len(year) != 4:
        raise HTTPException(
            status_code=400,
            detail="Year must be a 4 digit number like 2005, 2010, 2022."
        )
    
    current_year = datetime.now().year
    year_int = int(year)

    if year_int > current_year:
        raise HTTPException(
            status_code=400,
            detail=f"Future year cannot be checked. Current year is {current_year}."
        )
    
    if year_int < 1900:
        raise HTTPException(
            status_code=400,
            detail="Year must be 1900 or later. No data exists before that."
        )

@router.get("/symbols/{symbol}/annual/{year}")
async def get_annual_data_summary(symbol: str, year: str):
    """
    Returns high, low and total volume
    for a given stock symbol and year.
    """

    #Input validations
    input_validations(symbol, year)

    # Check if data exists in the db
    if not is_data_available_for_year(symbol, year):

        # If not, fetch from AlphaVantage
        try:
            monthly_series = await get_monthly_mkt_data(symbol)
            filtered = filter_data_by_year(monthly_series, year)
            insert_monthly_mkt_data(symbol, filtered)

        except ValueError as e:
            raise HTTPException(
                status_code=404, 
                detail=str(e)
            )

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to fetch data from external API: {str(e)}"
            )
        
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Couldn't reach the API due to connection lost."
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error occured: {str(e)}"
            )

    # Query the database and aggregate
    rows = get_annual_mkt_data(symbol, year)

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for symbol '{symbol}' in year '{year}'"
        )

    # Calculate high, low and total volume
    try:
        highest = max(float(row["high"]) for row in rows)
        lowest = min(float(row["low"]) for row in rows)
        total_volume = sum(int(row["volume"]) for row in rows)

    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while processing data: {str(e)}"
        )    

    return {
        "high": f"{highest:.4f}",
        "low": f"{lowest:.4f}",
        "volume": str(total_volume)
    }