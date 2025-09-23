"""
Advanced Data Fetcher for Enhanced Stock Analysis
Includes analyst ratings, options flow, institutional data, and more
"""

import yfinance as yf
import pandas as pd
import requests
import json
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)

class AdvancedDataFetcher:
    """Enhanced data fetcher with advanced market data"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # API endpoints for additional data
        self.alpha_vantage_key = None  # Add your Alpha Vantage key
        self.polygon_key = None  # Add your Polygon.io key
        self.quandl_key = None  # Add your Quandl key
    
    def get_comprehensive_analyst_data(self, symbol: str) -> Dict:
        """Get comprehensive analyst ratings and price targets"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get analyst recommendations
            recommendations = ticker.recommendations
            analyst_data = {}
            
            if recommendations is not None and not recommendations.empty:
                # Get latest recommendations
                latest_recs = recommendations.tail(10)
                
                # Calculate consensus
                rating_counts = latest_recs['To Grade'].value_counts()
                total_ratings = len(latest_recs)
                
                # Map ratings to scores
                rating_scores = {
                    'Strong Buy': 5, 'Buy': 4, 'Hold': 3, 
                    'Underperform': 2, 'Sell': 1, 'Strong Sell': 0
                }
                
                consensus_score = 0
                for rating, count in rating_counts.items():
                    if rating in rating_scores:
                        consensus_score += rating_scores[rating] * count
                
                consensus_score = consensus_score / total_ratings if total_ratings > 0 else 3
                
                # Get price targets
                price_targets = latest_recs['Target'].dropna()
                avg_target = price_targets.mean() if not price_targets.empty else 0
                high_target = price_targets.max() if not price_targets.empty else 0
                low_target = price_targets.min() if not price_targets.empty else 0
                
                analyst_data = {
                    'consensus_rating': self._score_to_rating(consensus_score),
                    'consensus_score': consensus_score,
                    'total_analysts': total_ratings,
                    'rating_distribution': rating_counts.to_dict(),
                    'average_price_target': avg_target,
                    'high_price_target': high_target,
                    'low_price_target': low_target,
                    'latest_recommendations': latest_recs.to_dict('records')
                }
            
            # Get institutional holdings
            institutional_data = self._get_institutional_holdings(symbol)
            analyst_data.update(institutional_data)
            
            return analyst_data
            
        except Exception as e:
            logger.error(f"Error fetching analyst data for {symbol}: {e}")
            return {}
    
    def get_options_flow_data(self, symbol: str) -> Dict:
        """Get options flow and unusual activity data"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get options data
            options_data = {}
            
            # Get expiration dates
            expirations = ticker.options
            if expirations:
                # Get nearest expiration
                nearest_exp = expirations[0]
                options_chain = ticker.option_chain(nearest_exp)
                
                # Analyze calls and puts
                calls = options_chain.calls
                puts = options_chain.puts
                
                # Calculate put/call ratio
                total_call_volume = calls['volume'].sum() if 'volume' in calls.columns else 0
                total_put_volume = puts['volume'].sum() if 'volume' in puts.columns else 0
                put_call_ratio = total_put_volume / total_call_volume if total_call_volume > 0 else 0
                
                # Find unusual activity (high volume, low open interest)
                if not calls.empty:
                    unusual_calls = calls[
                        (calls['volume'] > calls['openInterest'] * 2) & 
                        (calls['volume'] > 100)
                    ]
                    
                    unusual_puts = puts[
                        (puts['volume'] > puts['openInterest'] * 2) & 
                        (puts['volume'] > 100)
                    ]
                
                options_data = {
                    'put_call_ratio': put_call_ratio,
                    'total_call_volume': total_call_volume,
                    'total_put_volume': total_put_volume,
                    'unusual_calls_count': len(unusual_calls) if 'unusual_calls' in locals() else 0,
                    'unusual_puts_count': len(unusual_puts) if 'unusual_puts' in locals() else 0,
                    'nearest_expiration': nearest_exp,
                    'options_available': len(expirations) > 0
                }
            
            return options_data
            
        except Exception as e:
            logger.error(f"Error fetching options data for {symbol}: {e}")
            return {}
    
    def get_insider_trading_data(self, symbol: str) -> Dict:
        """Get insider trading and institutional activity"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get insider transactions
            insider_data = {}
            
            # Get institutional holders
            institutional_holders = ticker.institutional_holders
            if institutional_holders is not None and not institutional_holders.empty:
                # Calculate institutional ownership percentage
                total_shares = institutional_holders['Shares'].sum()
                institutional_ownership = (total_shares / ticker.info.get('sharesOutstanding', 1)) * 100
                
                # Get top holders
                top_holders = institutional_holders.head(5)
                
                insider_data = {
                    'institutional_ownership_pct': institutional_ownership,
                    'total_institutional_shares': total_shares,
                    'top_institutional_holders': top_holders.to_dict('records'),
                    'number_of_institutions': len(institutional_holders)
                }
            
            # Get major holders
            major_holders = ticker.major_holders
            if major_holders is not None and not major_holders.empty:
                insider_data['major_holders'] = major_holders.to_dict('records')
            
            return insider_data
            
        except Exception as e:
            logger.error(f"Error fetching insider data for {symbol}: {e}")
            return {}
    
    def get_news_sentiment_data(self, symbol: str) -> Dict:
        """Get news sentiment and social media buzz"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get news
            news = ticker.news
            sentiment_data = {}
            
            if news:
                # Analyze news sentiment (simplified)
                positive_keywords = ['beat', 'exceed', 'growth', 'strong', 'positive', 'bullish', 'upgrade']
                negative_keywords = ['miss', 'decline', 'weak', 'negative', 'bearish', 'downgrade', 'cut']
                
                positive_count = 0
                negative_count = 0
                
                for article in news[:10]:  # Analyze last 10 articles
                    title = article.get('title', '').lower()
                    summary = article.get('summary', '').lower()
                    text = title + ' ' + summary
                    
                    for keyword in positive_keywords:
                        if keyword in text:
                            positive_count += 1
                    
                    for keyword in negative_keywords:
                        if keyword in text:
                            negative_count += 1
                
                total_articles = len(news[:10])
                sentiment_score = (positive_count - negative_count) / total_articles if total_articles > 0 else 0
                
                sentiment_data = {
                    'news_sentiment_score': sentiment_score,
                    'positive_news_count': positive_count,
                    'negative_news_count': negative_count,
                    'total_articles_analyzed': total_articles,
                    'latest_news': news[:5]  # Latest 5 articles
                }
            
            return sentiment_data
            
        except Exception as e:
            logger.error(f"Error fetching news sentiment for {symbol}: {e}")
            return {}
    
    def get_advanced_technical_indicators(self, symbol: str) -> Dict:
        """Get advanced technical indicators"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1y")
            
            if hist.empty:
                return {}
            
            # Calculate advanced indicators
            close = hist['Close']
            high = hist['High']
            low = hist['Low']
            volume = hist['Volume']
            
            # MACD
            exp1 = close.ewm(span=12).mean()
            exp2 = close.ewm(span=26).mean()
            macd = exp1 - exp2
            macd_signal = macd.ewm(span=9).mean()
            macd_histogram = macd - macd_signal
            
            # Stochastic Oscillator
            lowest_low = low.rolling(window=14).min()
            highest_high = high.rolling(window=14).max()
            k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
            d_percent = k_percent.rolling(window=3).mean()
            
            # Williams %R
            williams_r = -100 * ((highest_high - close) / (highest_high - lowest_low))
            
            # Average True Range (ATR)
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = true_range.rolling(window=14).mean()
            
            # Volume indicators
            volume_sma = volume.rolling(window=20).mean()
            volume_ratio = volume.iloc[-1] / volume_sma.iloc[-1] if volume_sma.iloc[-1] > 0 else 1
            
            return {
                'macd': macd.iloc[-1],
                'macd_signal': macd_signal.iloc[-1],
                'macd_histogram': macd_histogram.iloc[-1],
                'stochastic_k': k_percent.iloc[-1],
                'stochastic_d': d_percent.iloc[-1],
                'williams_r': williams_r.iloc[-1],
                'atr': atr.iloc[-1],
                'volume_ratio': volume_ratio,
                'current_volume': volume.iloc[-1],
                'avg_volume_20d': volume_sma.iloc[-1]
            }
            
        except Exception as e:
            logger.error(f"Error calculating advanced technical indicators for {symbol}: {e}")
            return {}
    
    def _get_institutional_holdings(self, symbol: str) -> Dict:
        """Get institutional holdings data"""
        try:
            ticker = yf.Ticker(symbol)
            institutional_holders = ticker.institutional_holders
            
            if institutional_holders is None or institutional_holders.empty:
                return {}
            
            # Calculate institutional ownership
            total_shares = institutional_holders['Shares'].sum()
            shares_outstanding = ticker.info.get('sharesOutstanding', 1)
            institutional_ownership_pct = (total_shares / shares_outstanding) * 100
            
            return {
                'institutional_ownership_pct': institutional_ownership_pct,
                'total_institutional_shares': total_shares,
                'number_of_institutions': len(institutional_holders),
                'top_institutional_holders': institutional_holders.head(5).to_dict('records')
            }
            
        except Exception as e:
            logger.error(f"Error fetching institutional holdings for {symbol}: {e}")
            return {}
    
    def _score_to_rating(self, score: float) -> str:
        """Convert numerical score to rating"""
        if score >= 4.5:
            return "Strong Buy"
        elif score >= 3.5:
            return "Buy"
        elif score >= 2.5:
            return "Hold"
        elif score >= 1.5:
            return "Underperform"
        else:
            return "Sell"
    
    def get_comprehensive_market_data(self, symbol: str) -> Dict:
        """Get all comprehensive market data"""
        try:
            logger.info(f"Fetching comprehensive market data for {symbol}")
            
            # Fetch all data types
            analyst_data = self.get_comprehensive_analyst_data(symbol)
            options_data = self.get_options_flow_data(symbol)
            insider_data = self.get_insider_trading_data(symbol)
            sentiment_data = self.get_news_sentiment_data(symbol)
            technical_data = self.get_advanced_technical_indicators(symbol)
            
            return {
                'analyst_data': analyst_data,
                'options_data': options_data,
                'insider_data': insider_data,
                'sentiment_data': sentiment_data,
                'advanced_technical': technical_data,
                'data_fetch_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching comprehensive market data for {symbol}: {e}")
            return {}
