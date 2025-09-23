"""
Data Sources Integration Guide for CROC Investment Fund
How to add more data sources and APIs
"""

import requests
import pandas as pd
import yfinance as yf
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class DataSourceManager:
    """Manages multiple data sources for comprehensive analysis"""
    
    def __init__(self):
        self.sources = {
            'yahoo_finance': YahooFinanceSource(),
            'alpha_vantage': AlphaVantageSource(),
            'polygon': PolygonSource(),
            'quandl': QuandlSource(),
            'finnhub': FinnhubSource(),
            'news_api': NewsAPISource(),
            'reddit_api': RedditAPISource(),
            'twitter_api': TwitterAPISource(),
            'sec_edgar': SECEdgarSource(),
            'fred': FREDSource()
        }
    
    def get_available_sources(self) -> List[str]:
        """Get list of available data sources"""
        return list(self.sources.keys())
    
    def get_data(self, source: str, symbol: str, data_type: str) -> Dict:
        """Get data from specified source"""
        if source in self.sources:
            return self.sources[source].get_data(symbol, data_type)
        return {"error": f"Source {source} not available"}

class YahooFinanceSource:
    """Yahoo Finance data source (already implemented)"""
    
    def get_data(self, symbol: str, data_type: str) -> Dict:
        """Get data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            
            if data_type == "basic":
                info = ticker.info
                hist = ticker.history(period="1y")
                return {"info": info, "history": hist}
            
            elif data_type == "options":
                expirations = ticker.options
                if expirations:
                    options_chain = ticker.option_chain(expirations[0])
                    return {"calls": options_chain.calls, "puts": options_chain.puts}
                return {"error": "No options data"}
            
            elif data_type == "news":
                news = ticker.news
                return {"news": news}
            
            elif data_type == "recommendations":
                recommendations = ticker.recommendations
                return {"recommendations": recommendations}
            
            else:
                return {"error": f"Data type {data_type} not supported"}
                
        except Exception as e:
            return {"error": f"Yahoo Finance error: {str(e)}"}

class AlphaVantageSource:
    """Alpha Vantage API data source"""
    
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.base_url = "https://www.alphavantage.co/query"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def get_data(self, symbol: str, data_type: str) -> Dict:
        """Get data from Alpha Vantage"""
        if not self.is_available():
            return {"error": "Alpha Vantage API key not available"}
        
        try:
            if data_type == "fundamental":
                params = {
                    'function': 'OVERVIEW',
                    'symbol': symbol,
                    'apikey': self.api_key
                }
                response = requests.get(self.base_url, params=params)
                return response.json()
            
            elif data_type == "earnings":
                params = {
                    'function': 'EARNINGS',
                    'symbol': symbol,
                    'apikey': self.api_key
                }
                response = requests.get(self.base_url, params=params)
                return response.json()
            
            elif data_type == "income_statement":
                params = {
                    'function': 'INCOME_STATEMENT',
                    'symbol': symbol,
                    'apikey': self.api_key
                }
                response = requests.get(self.base_url, params=params)
                return response.json()
            
            else:
                return {"error": f"Data type {data_type} not supported"}
                
        except Exception as e:
            return {"error": f"Alpha Vantage error: {str(e)}"}

class PolygonSource:
    """Polygon.io API data source"""
    
    def __init__(self):
        self.api_key = os.getenv('POLYGON_API_KEY')
        self.base_url = "https://api.polygon.io"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def get_data(self, symbol: str, data_type: str) -> Dict:
        """Get data from Polygon.io"""
        if not self.is_available():
            return {"error": "Polygon API key not available"}
        
        try:
            if data_type == "trades":
                url = f"{self.base_url}/v3/trades/{symbol}"
                params = {'apikey': self.api_key}
                response = requests.get(url, params=params)
                return response.json()
            
            elif data_type == "quotes":
                url = f"{self.base_url}/v3/quotes/{symbol}"
                params = {'apikey': self.api_key}
                response = requests.get(url, params=params)
                return response.json()
            
            elif data_type == "news":
                url = f"{self.base_url}/v2/reference/news"
                params = {'ticker': symbol, 'apikey': self.api_key}
                response = requests.get(url, params=params)
                return response.json()
            
            else:
                return {"error": f"Data type {data_type} not supported"}
                
        except Exception as e:
            return {"error": f"Polygon error: {str(e)}"}

class FinnhubSource:
    """Finnhub API data source"""
    
    def __init__(self):
        self.api_key = os.getenv('FINNHUB_API_KEY')
        self.base_url = "https://finnhub.io/api/v1"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def get_data(self, symbol: str, data_type: str) -> Dict:
        """Get data from Finnhub"""
        if not self.is_available():
            return {"error": "Finnhub API key not available"}
        
        try:
            if data_type == "profile":
                url = f"{self.base_url}/stock/profile2"
                params = {'symbol': symbol, 'token': self.api_key}
                response = requests.get(url, params=params)
                return response.json()
            
            elif data_type == "recommendations":
                url = f"{self.base_url}/stock/recommendation"
                params = {'symbol': symbol, 'token': self.api_key}
                response = requests.get(url, params=params)
                return response.json()
            
            elif data_type == "sentiment":
                url = f"{self.base_url}/news-sentiment"
                params = {'symbol': symbol, 'token': self.api_key}
                response = requests.get(url, params=params)
                return response.json()
            
            else:
                return {"error": f"Data type {data_type} not supported"}
                
        except Exception as e:
            return {"error": f"Finnhub error: {str(e)}"}

class NewsAPISource:
    """News API data source"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def get_data(self, symbol: str, data_type: str) -> Dict:
        """Get news data"""
        if not self.is_available():
            return {"error": "News API key not available"}
        
        try:
            if data_type == "headlines":
                url = f"{self.base_url}/everything"
                params = {
                    'q': symbol,
                    'apiKey': self.api_key,
                    'sortBy': 'publishedAt',
                    'pageSize': 20
                }
                response = requests.get(url, params=params)
                return response.json()
            
            else:
                return {"error": f"Data type {data_type} not supported"}
                
        except Exception as e:
            return {"error": f"News API error: {str(e)}"}

class RedditAPISource:
    """Reddit API data source"""
    
    def __init__(self):
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = "CROC Investment Fund Bot"
    
    def is_available(self) -> bool:
        return bool(self.client_id and self.client_secret)
    
    def get_data(self, symbol: str, data_type: str) -> Dict:
        """Get Reddit sentiment data"""
        if not self.is_available():
            return {"error": "Reddit API credentials not available"}
        
        try:
            # Reddit API implementation would go here
            # This is a simplified version
            return {
                "sentiment": "bullish",
                "mentions": 150,
                "subreddits": ["investing", "stocks", "SecurityAnalysis"],
                "top_posts": []
            }
            
        except Exception as e:
            return {"error": f"Reddit API error: {str(e)}"}

class TwitterAPISource:
    """Twitter API data source"""
    
    def __init__(self):
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        self.base_url = "https://api.twitter.com/2"
    
    def is_available(self) -> bool:
        return bool(self.bearer_token)
    
    def get_data(self, symbol: str, data_type: str) -> Dict:
        """Get Twitter data"""
        if not self.is_available():
            return {"error": "Twitter API credentials not available"}
        
        try:
            # Twitter API v2 implementation would go here
            return {
                "tweets": [],
                "sentiment": "neutral",
                "volume": 0
            }
            
        except Exception as e:
            return {"error": f"Twitter API error: {str(e)}"}

class SECEdgarSource:
    """SEC EDGAR data source"""
    
    def __init__(self):
        self.base_url = "https://data.sec.gov"
        self.user_agent = "CROC Investment Fund contact@example.com"
    
    def get_data(self, symbol: str, data_type: str) -> Dict:
        """Get SEC filings data"""
        try:
            if data_type == "filings":
                # SEC EDGAR API implementation
                return {
                    "recent_filings": [],
                    "10k": None,
                    "10q": None,
                    "8k": []
                }
            
            else:
                return {"error": f"Data type {data_type} not supported"}
                
        except Exception as e:
            return {"error": f"SEC EDGAR error: {str(e)}"}

class FREDSource:
    """Federal Reserve Economic Data source"""
    
    def __init__(self):
        self.api_key = os.getenv('FRED_API_KEY')
        self.base_url = "https://api.stlouisfed.org/fred"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def get_data(self, symbol: str, data_type: str) -> Dict:
        """Get economic data"""
        if not self.is_available():
            return {"error": "FRED API key not available"}
        
        try:
            if data_type == "interest_rates":
                # FRED API implementation
                return {
                    "fed_funds_rate": 5.25,
                    "10_year_treasury": 4.5,
                    "inflation_rate": 3.2
                }
            
            else:
                return {"error": f"Data type {data_type} not supported"}
                
        except Exception as e:
            return {"error": f"FRED error: {str(e)}"}

# Example usage and integration guide
def add_data_source_to_app():
    """
    How to add a new data source to your CROC Investment Fund app:
    
    1. Create a new class inheriting from a base data source
    2. Implement the get_data method
    3. Add API key to .env file
    4. Update the DataSourceManager
    5. Add UI components to display the data
    """
    
    # Example: Adding a new data source
    class CustomDataSource:
        def __init__(self):
            self.api_key = os.getenv('CUSTOM_API_KEY')
        
        def is_available(self) -> bool:
            return bool(self.api_key)
        
        def get_data(self, symbol: str, data_type: str) -> Dict:
            # Your custom data fetching logic here
            return {"data": "custom_data"}
    
    return CustomDataSource()

# Integration examples
def integrate_alpha_vantage():
    """Example: How to integrate Alpha Vantage"""
    
    # 1. Add to requirements.txt
    # requests>=2.28.0
    
    # 2. Add API key to .env
    # ALPHA_VANTAGE_API_KEY=your_key_here
    
    # 3. Use in your app
    source = AlphaVantageSource()
    if source.is_available():
        data = source.get_data("AAPL", "fundamental")
        print(f"Alpha Vantage data: {data}")
    else:
        print("Alpha Vantage not available")

def integrate_polygon():
    """Example: How to integrate Polygon.io"""
    
    # 1. Add API key to .env
    # POLYGON_API_KEY=your_key_here
    
    # 2. Use in your app
    source = PolygonSource()
    if source.is_available():
        data = source.get_data("AAPL", "trades")
        print(f"Polygon data: {data}")
    else:
        print("Polygon not available")

if __name__ == "__main__":
    # Test data sources
    manager = DataSourceManager()
    
    print("Available data sources:")
    for source in manager.get_available_sources():
        print(f"- {source}")
    
    # Test Yahoo Finance (should work)
    yahoo_data = manager.get_data("yahoo_finance", "AAPL", "basic")
    print(f"Yahoo Finance test: {'Success' if 'error' not in yahoo_data else 'Failed'}")
    
    # Test Alpha Vantage (requires API key)
    av_data = manager.get_data("alpha_vantage", "AAPL", "fundamental")
    print(f"Alpha Vantage test: {'Success' if 'error' not in av_data else 'Failed'}")
