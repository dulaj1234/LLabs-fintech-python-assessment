import httpx
import os
from dotenv import load_dotenv

# Load the .env file to read ALPHAVANTAGE_API_KEY and ALPHAVANTAGE_API_URL
load_dotenv()

# Read the API key from the .env file
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

# The base URL for AlphaVantage read from .env file
BASE_URL = os.getenv("ALPHAVANTAGE_API_URL") 