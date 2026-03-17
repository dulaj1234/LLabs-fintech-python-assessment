from fastapi import APIRouter, HTTPException
from app.database import insert_monthly_mkt_data, get_annual_mkt_data, is_data_available_for_year
from app.fetcher import get_monthly_mkt_data, filter_data_by_year

