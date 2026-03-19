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

### 1 — Create a Virtual Environment

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

### 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### 3 — Configure Environment Variables

Create a `.env` file in the root directory of the project:

**Windows:**
```bash
copy NUL .env
```

**Linux/MACOS:**
```bash
touch .env
```

Open the `.env` file and add your AlphaVantage API key:
```
ALPHAVANTAGE_API_URL=https://www.alphavantage.co/query
ALPHAVANTAGE_API_KEY=api_key
```

> Replace `api_key` with the actual key you copied
> from AlphaVantage and get the url from the docment and assign it 
> to ALPHAVANTAGE_API_URL. 

> No need of sharing or committing the `.env` file.
