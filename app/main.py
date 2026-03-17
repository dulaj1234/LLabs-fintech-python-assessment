from fastapi import FastAPI
from app.database import initialize_db
from app.routers import router

# Create the FastAPI app instance
app = FastAPI(
    title="Liquid Labs Market Data API",
    description="Fetches and caches stock market data from AlphaVantage",
    version="1.0.0"
)

# This runs automatically when the app starts up
@app.on_event("startup")
async def startup_event():
    """
    Initializes the database when the app starts.
    Creates the table if it doesn't exist yet.
    """
    initialize_db()

# Register the router so FastAPI knows the endpoint
app.include_router(router)