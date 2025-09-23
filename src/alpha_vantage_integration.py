"""
Alpha Vantage Integration for CROC Investment Fund
Example of adding a new data source
"""

import requests
import pandas as pd
import os
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()

class AlphaVantageIntegration:
    """Alpha Vantage API integration for enhanced financial data"""
    
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.base_url = "https://www.alphavantage.co/query"
        self.rate_limit_delay = 12  # Alpha Vantage free tier: 5 calls per minute
    
    def is_available(self) -> bool:
        """Check if Alpha Vantage API is available"""
        return bool(self.api_key)
    
    def get_company_overview(self, symbol: str) -> Dict:
        """Get comprehensive company overview"""
        if not self.is_available():
            return {"error": "Alpha Vantage API key not available"}
        
        try:
            params = {
                'function': 'OVERVIEW',
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if 'Error Message' in data:
                return {"error": data['Error Message']}
            
            return {
                "symbol": data.get('Symbol', symbol),
                "name": data.get('Name', ''),
                "description": data.get('Description', ''),
                "sector": data.get('Sector', ''),
                "industry": data.get('Industry', ''),
                "market_cap": data.get('MarketCapitalization', ''),
                "pe_ratio": data.get('PERatio', ''),
                "peg_ratio": data.get('PEGRatio', ''),
                "book_value": data.get('BookValue', ''),
                "dividend_per_share": data.get('DividendPerShare', ''),
                "dividend_yield": data.get('DividendYield', ''),
                "eps": data.get('EPS', ''),
                "revenue_per_share": data.get('RevenuePerShareTTM', ''),
                "profit_margin": data.get('ProfitMargin', ''),
                "operating_margin": data.get('OperatingMarginTTM', ''),
                "return_on_assets": data.get('ReturnOnAssetsTTM', ''),
                "return_on_equity": data.get('ReturnOnEquityTTM', ''),
                "revenue_ttm": data.get('RevenueTTM', ''),
                "gross_profit_ttm": data.get('GrossProfitTTM', ''),
                "diluted_eps_ttm": data.get('DilutedEPSTTM', ''),
                "quarterly_earnings_growth": data.get('QuarterlyEarningsGrowthYOY', ''),
                "quarterly_revenue_growth": data.get('QuarterlyRevenueGrowthYOY', ''),
                "analyst_target_price": data.get('AnalystTargetPrice', ''),
                "trailing_pe": data.get('TrailingPE', ''),
                "forward_pe": data.get('ForwardPE', ''),
                "price_to_sales_ratio": data.get('PriceToSalesRatioTTM', ''),
                "price_to_book_ratio": data.get('PriceToBookRatio', ''),
                "ev_to_revenue": data.get('EVToRevenue', ''),
                "ev_to_ebitda": data.get('EVToEBITDA', ''),
                "beta": data.get('Beta', ''),
                "52_week_high": data.get('52WeekHigh', ''),
                "52_week_low": data.get('52WeekLow', ''),
                "50_day_moving_average": data.get('50DayMovingAverage', ''),
                "200_day_moving_average": data.get('200DayMovingAverage', ''),
                "shares_outstanding": data.get('SharesOutstanding', ''),
                "dividend_date": data.get('DividendDate', ''),
                "ex_dividend_date": data.get('ExDividendDate', '')
            }
            
        except Exception as e:
            return {"error": f"Alpha Vantage API error: {str(e)}"}
    
    def get_earnings_data(self, symbol: str) -> Dict:
        """Get earnings data and estimates"""
        if not self.is_available():
            return {"error": "Alpha Vantage API key not available"}
        
        try:
            params = {
                'function': 'EARNINGS',
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if 'Error Message' in data:
                return {"error": data['Error Message']}
            
            return {
                "annual_earnings": data.get('annualEarnings', []),
                "quarterly_earnings": data.get('quarterlyEarnings', [])
            }
            
        except Exception as e:
            return {"error": f"Alpha Vantage API error: {str(e)}"}
    
    def get_income_statement(self, symbol: str) -> Dict:
        """Get income statement data"""
        if not self.is_available():
            return {"error": "Alpha Vantage API key not available"}
        
        try:
            params = {
                'function': 'INCOME_STATEMENT',
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if 'Error Message' in data:
                return {"error": data['Error Message']}
            
            return {
                "annual_reports": data.get('annualReports', []),
                "quarterly_reports": data.get('quarterlyReports', [])
            }
            
        except Exception as e:
            return {"error": f"Alpha Vantage API error: {str(e)}"}
    
    def get_balance_sheet(self, symbol: str) -> Dict:
        """Get balance sheet data"""
        if not self.is_available():
            return {"error": "Alpha Vantage API key not available"}
        
        try:
            params = {
                'function': 'BALANCE_SHEET',
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if 'Error Message' in data:
                return {"error": data['Error Message']}
            
            return {
                "annual_reports": data.get('annualReports', []),
                "quarterly_reports": data.get('quarterlyReports', [])
            }
            
        except Exception as e:
            return {"error": f"Alpha Vantage API error: {str(e)}"}
    
    def get_cash_flow(self, symbol: str) -> Dict:
        """Get cash flow data"""
        if not self.is_available():
            return {"error": "Alpha Vantage API key not available"}
        
        try:
            params = {
                'function': 'CASH_FLOW',
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if 'Error Message' in data:
                return {"error": data['Error Message']}
            
            return {
                "annual_reports": data.get('annualReports', []),
                "quarterly_reports": data.get('quarterlyReports', [])
            }
            
        except Exception as e:
            return {"error": f"Alpha Vantage API error: {str(e)}"}

def display_alpha_vantage_data(data: Dict, st):
    """Display Alpha Vantage data in Streamlit"""
    if 'error' in data:
        st.error(f"Alpha Vantage Error: {data['error']}")
        return
    
    st.subheader("📊 Alpha Vantage Enhanced Data")
    
    # Company Overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("PEG Ratio", data.get('peg_ratio', 'N/A'))
        st.metric("Book Value", f"${data.get('book_value', 'N/A')}")
        st.metric("EPS", data.get('eps', 'N/A'))
    
    with col2:
        st.metric("Operating Margin", f"{data.get('operating_margin', 'N/A')}%")
        st.metric("ROA", f"{data.get('return_on_assets', 'N/A')}%")
        st.metric("ROE", f"{data.get('return_on_equity', 'N/A')}%")
    
    with col3:
        st.metric("Forward P/E", data.get('forward_pe', 'N/A'))
        st.metric("Price/Sales", data.get('price_to_sales_ratio', 'N/A'))
        st.metric("EV/EBITDA", data.get('ev_to_ebitda', 'N/A'))
    
    # Growth Metrics
    st.subheader("📈 Growth Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Quarterly Earnings Growth", f"{data.get('quarterly_earnings_growth', 'N/A')}%")
    
    with col2:
        st.metric("Quarterly Revenue Growth", f"{data.get('quarterly_revenue_growth', 'N/A')}%")
    
    with col3:
        st.metric("Revenue TTM", f"${data.get('revenue_ttm', 'N/A')}")
    
    with col4:
        st.metric("Gross Profit TTM", f"${data.get('gross_profit_ttm', 'N/A')}")
    
    # Analyst Data
    st.subheader("🎯 Analyst Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Target Price", f"${data.get('analyst_target_price', 'N/A')}")
    
    with col2:
        st.metric("Beta", data.get('beta', 'N/A'))
    
    with col3:
        st.metric("Shares Outstanding", f"{data.get('shares_outstanding', 'N/A'):,}")

# Example usage
if __name__ == "__main__":
    # Test Alpha Vantage integration
    av = AlphaVantageIntegration()
    
    if av.is_available():
        print("Alpha Vantage API is available!")
        
        # Get company overview
        overview = av.get_company_overview("AAPL")
        if 'error' not in overview:
            print(f"Company: {overview['name']}")
            print(f"Sector: {overview['sector']}")
            print(f"Market Cap: {overview['market_cap']}")
        else:
            print(f"Error: {overview['error']}")
    else:
        print("Alpha Vantage API key not found. Add ALPHA_VANTAGE_API_KEY to .env file")
