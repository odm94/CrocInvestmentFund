"""
Stock Data Fetcher Module
Handles fetching stock data from various sources
"""

import yfinance as yf
import pandas as pd
import requests
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class StockDataFetcher:
    """Fetches stock data from Yahoo Finance and other sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_stock_info(self, symbol: str) -> Dict:
        """Get basic stock information"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'current_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange', 'N/A')
            }
        except Exception as e:
            logger.error(f"Error fetching stock info for {symbol}: {e}")
            return {}
    
    def get_historical_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Get historical stock data"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            return data
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_financial_statements(self, symbol: str) -> Dict:
        """Get financial statements (income, balance sheet, cash flow)"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get financial statements
            income_stmt = ticker.financials
            balance_sheet = ticker.balance_sheet
            cash_flow = ticker.cashflow
            
            return {
                'income_statement': income_stmt,
                'balance_sheet': balance_sheet,
                'cash_flow': cash_flow
            }
        except Exception as e:
            logger.error(f"Error fetching financial statements for {symbol}: {e}")
            return {}
    
    def get_key_metrics(self, symbol: str) -> Dict:
        """Get key financial metrics"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'pe_ratio': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'peg_ratio': info.get('pegRatio', 0),
                'price_to_book': info.get('priceToBook', 0),
                'price_to_sales': info.get('priceToSalesTrailing12Months', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'return_on_equity': info.get('returnOnEquity', 0),
                'return_on_assets': info.get('returnOnAssets', 0),
                'profit_margin': info.get('profitMargins', 0),
                'revenue_growth': info.get('revenueGrowth', 0),
                'earnings_growth': info.get('earningsGrowth', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 0)
            }
        except Exception as e:
            logger.error(f"Error fetching key metrics for {symbol}: {e}")
            return {}
    
    def get_analyst_recommendations(self, symbol: str) -> Dict:
        """Get analyst recommendations and price targets"""
        try:
            ticker = yf.Ticker(symbol)
            recommendations = ticker.recommendations
            
            if recommendations is not None and not recommendations.empty:
                latest = recommendations.iloc[-1]
                return {
                    'recommendation': latest.get('To Grade', 'N/A'),
                    'target_price': latest.get('Target', 0),
                    'date': latest.name.strftime('%Y-%m-%d') if hasattr(latest.name, 'strftime') else str(latest.name)
                }
            return {}
        except Exception as e:
            logger.error(f"Error fetching analyst recommendations for {symbol}: {e}")
            return {}
