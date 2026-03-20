# Liquid Labs Market Data API

A REST API built with **FastAPI** and **SQLite** that fetches stock market data
from AlphaVantage, caches it locally, and serves aggregated annual summaries.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

| Tool | Version | Download |
|---|---|---|
| Python | 3.14+ | https://www.python.org/downloads/ |
| Git | Latest | https://git-scm.com/downloads |

You will also need a free AlphaVantage API key:
1. Go to https://www.alphavantage.co/support/#api-key
2. Fill in your details and select **"Student"** as your role
3. The API key will be displayed on the screen, copy and save it

## Clone the Repository

Open your terminal and run the following commands:
```bash
git clone https://github.com/dulaj1234/LLabs-fintech-python-assessment.git
cd LLabs-fintech-python-assessment
```

## Environment Setup

### 1. Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
source venv/Scripts/activate
```

**Linux/MACOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> It is neccessary to open a new terminal window and 
> activate the virtual environment every time before running the app.

To confirm the virtual eviroment is active, `(venv)` appear at the start of the terminal line.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory of the project:

**Windows:**
```bash
copy NUL .env
```

**Linux/MACOS:**
```bash
touch .env
```

Open the `.env` file and add your AlphaVantage API key and URL:
```
ALPHAVANTAGE_API_URL=https://www.alphavantage.co/query
ALPHAVANTAGE_API_KEY=api_key
```

> Replace `api_key` with the actual key you copied
> from AlphaVantage and get the url from the docment and assign it 
> to ALPHAVANTAGE_API_URL. 

> No need of sharing or committing the `.env` file.

## Database Setup

The SQLite database is created **automatically** when the
application starts. No manual database setup is required.

The database file `market_data.db` will be created in the
root directory of the project on first run.

The following table will be created automatically:
```sql
CREATE TABLE IF NOT EXISTS monthly_stock_prices (
    symbol  TEXT NOT NULL,
    date    TEXT NOT NULL,
    open    TEXT,
    high    TEXT NOT NULL,
    low     TEXT NOT NULL,
    volume  TEXT NOT NULL,
    PRIMARY KEY (symbol, date)
);
```

## Run the Application

### Development Mode
The following command reloads automatically

```bash
uvicorn app.main:app --reload
```


Once running, you will see the following output:
```
>    Uvicorn running on http://127.0.0.1:8000
>    Application startup complete.
```

The API is now up at:
```
http://127.0.0.1:8000
```

### API Documentation

Since FastAPI automatically generates interactive documentation.
Open the browser and go to:
```
http://127.0.0.1:8000/docs
```

You can test all endpoints directly from this page
without needing any extra tools.

## API Endpoint

### `GET /symbols/{symbol}/annual/{year}`

Returns the highest price, lowest price and total trading
volume for a given stock symbol or the given year.

#### URL Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `symbol` | string | Yes | Stock symbol/code like `IBM`, `AAPL`, `MSFT` |
| `year` | string | Yes | 4 digit year like `2005`. Must be 1900 or later. |

#### Example Request
```bash
GET "http://127.0.0.1:8000/symbols/IBM/annual/2005"
```

Or simply open this URL in your browser:
```
http://127.0.0.1:8000/symbols/IBM/annual/2005
```

#### Error Responses

| ErrorCode | Reason |
|---|---|
| `400` | Invalid symbol format |
| `400` | Invalid year format |
| `400` | Year in the future |
| `400` | Year too old |
| `404` | Symbol not found |
| `404` | No data for year |
| `500` | Internal server error |
| `502` | External API error |
| `503` | Cannot reach API |

#### Example Error Response
```json
{
  "detail": "Year cannot be in the future. Current year is 2026."
}
> This is for error code  `400` - Year in the future
```

## Libraries Used

| Library | Version | Rationale |
|---|---|---|
| **fastapi** | Latest | Required by assignment. Modern async-native REST framework with automatic documentation generation |
| **uvicorn** | Latest | ASGI server required to run FastAPI applications |
| **httpx** | Latest | Async HTTP client that works natively with FastAPI's async architecture. Preferred over `requests` which is synchronous only |
| **python-dotenv** | Latest | Safely loads the API key from `.env` file keeping secrets out of source code |
| **pytest** | Latest | Industry standard Python testing framework |
| **pytest-asyncio** | Latest | Enables pytest to handle async functions used throughout the FastAPI application |

> SQLite is used via Python's built-in `sqlite3` module, no additional installation required.