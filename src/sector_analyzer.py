"""
Sector and Industry Analysis Module
Provides comprehensive sector analysis and peer comparisons
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
import requests
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SectorAnalyzer:
    """Comprehensive sector and industry analysis"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_sector_performance(self, symbol: str) -> Dict:
        """Get sector performance and ranking"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            sector = info.get('sector', 'Unknown')
            industry = info.get('industry', 'Unknown')
            
            # Get sector ETFs for comparison
            sector_etfs = {
                'Technology': 'XLK',
                'Healthcare': 'XLV',
                'Financial Services': 'XLF',
                'Consumer Discretionary': 'XLY',
                'Communication Services': 'XLC',
                'Industrials': 'XLI',
                'Consumer Staples': 'XLP',
                'Energy': 'XLE',
                'Utilities': 'XLU',
                'Real Estate': 'XLRE',
                'Materials': 'XLB'
            }
            
            sector_etf = sector_etfs.get(sector, 'SPY')  # Default to SPY if sector not found
            
            # Get performance data
            stock_data = ticker.history(period="1y")
            sector_data = yf.Ticker(sector_etf).history(period="1y")
            market_data = yf.Ticker('SPY').history(period="1y")
            
            if stock_data.empty or sector_data.empty or market_data.empty:
                return {}
            
            # Calculate returns
            stock_return = ((stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[0]) - 1) * 100
            sector_return = ((sector_data['Close'].iloc[-1] / sector_data['Close'].iloc[0]) - 1) * 100
            market_return = ((market_data['Close'].iloc[-1] / market_data['Close'].iloc[0]) - 1) * 100
            
            # Calculate relative performance
            vs_sector = stock_return - sector_return
            vs_market = stock_return - market_return
            
            # Calculate volatility
            stock_vol = stock_data['Close'].pct_change().std() * np.sqrt(252) * 100
            sector_vol = sector_data['Close'].pct_change().std() * np.sqrt(252) * 100
            
            return {
                'sector': sector,
                'industry': industry,
                'sector_etf': sector_etf,
                'stock_return_1y': stock_return,
                'sector_return_1y': sector_return,
                'market_return_1y': market_return,
                'vs_sector_performance': vs_sector,
                'vs_market_performance': vs_market,
                'stock_volatility': stock_vol,
                'sector_volatility': sector_vol,
                'relative_volatility': stock_vol / sector_vol if sector_vol > 0 else 1
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sector performance for {symbol}: {e}")
            return {}
    
    def get_peer_comparison(self, symbol: str) -> Dict:
        """Get peer company comparison"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get peer companies (simplified - in real implementation, use more sophisticated matching)
            peers = self._get_peer_companies(symbol, info.get('sector', ''), info.get('industry', ''))
            
            if not peers:
                return {}
            
            # Get peer data
            peer_data = {}
            for peer in peers[:5]:  # Limit to top 5 peers
                try:
                    peer_ticker = yf.Ticker(peer)
                    peer_info = peer_ticker.info
                    peer_hist = peer_ticker.history(period="1y")
                    
                    if not peer_hist.empty:
                        peer_return = ((peer_hist['Close'].iloc[-1] / peer_hist['Close'].iloc[0]) - 1) * 100
                        peer_vol = peer_hist['Close'].pct_change().std() * np.sqrt(252) * 100
                        
                        peer_data[peer] = {
                            'name': peer_info.get('longName', peer),
                            'market_cap': peer_info.get('marketCap', 0),
                            'pe_ratio': peer_info.get('trailingPE', 0),
                            'return_1y': peer_return,
                            'volatility': peer_vol,
                            'current_price': peer_info.get('currentPrice', 0)
                        }
                except:
                    continue
            
            # Calculate peer averages
            if peer_data:
                avg_pe = np.mean([data['pe_ratio'] for data in peer_data.values() if data['pe_ratio'] > 0])
                avg_return = np.mean([data['return_1y'] for data in peer_data.values()])
                avg_vol = np.mean([data['volatility'] for data in peer_data.values()])
                
                return {
                    'peers': peer_data,
                    'peer_count': len(peer_data),
                    'average_pe_ratio': avg_pe,
                    'average_return_1y': avg_return,
                    'average_volatility': avg_vol,
                    'peer_analysis': self._analyze_peer_position(symbol, peer_data)
                }
            
            return {}
            
        except Exception as e:
            logger.error(f"Error getting peer comparison for {symbol}: {e}")
            return {}
    
    def get_industry_trends(self, symbol: str) -> Dict:
        """Get industry trends and outlook"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            sector = info.get('sector', '')
            industry = info.get('industry', '')
            
            # Get industry-specific ETFs and indices
            industry_etfs = {
                'Technology': ['XLK', 'QQQ', 'VGT'],
                'Healthcare': ['XLV', 'VHT', 'IBB'],
                'Financial Services': ['XLF', 'VFH', 'KBE'],
                'Energy': ['XLE', 'VDE', 'OIH'],
                'Consumer Discretionary': ['XLY', 'VCR', 'FDIS']
            }
            
            etfs = industry_etfs.get(sector, ['SPY'])
            
            # Analyze industry momentum
            industry_momentum = {}
            for etf in etfs:
                try:
                    etf_data = yf.Ticker(etf).history(period="6mo")
                    if not etf_data.empty:
                        momentum_1m = ((etf_data['Close'].iloc[-1] / etf_data['Close'].iloc[-22]) - 1) * 100
                        momentum_3m = ((etf_data['Close'].iloc[-1] / etf_data['Close'].iloc[-66]) - 1) * 100
                        momentum_6m = ((etf_data['Close'].iloc[-1] / etf_data['Close'].iloc[0]) - 1) * 100
                        
                        industry_momentum[etf] = {
                            'momentum_1m': momentum_1m,
                            'momentum_3m': momentum_3m,
                            'momentum_6m': momentum_6m
                        }
                except:
                    continue
            
            # Calculate industry strength
            avg_momentum_1m = np.mean([data['momentum_1m'] for data in industry_momentum.values()])
            avg_momentum_3m = np.mean([data['momentum_3m'] for data in industry_momentum.values()])
            avg_momentum_6m = np.mean([data['momentum_6m'] for data in industry_momentum.values()])
            
            # Determine trend
            if avg_momentum_1m > 5 and avg_momentum_3m > 10:
                trend = "Strong Uptrend"
            elif avg_momentum_1m > 2 and avg_momentum_3m > 5:
                trend = "Uptrend"
            elif avg_momentum_1m < -5 and avg_momentum_3m < -10:
                trend = "Strong Downtrend"
            elif avg_momentum_1m < -2 and avg_momentum_3m < -5:
                trend = "Downtrend"
            else:
                trend = "Sideways"
            
            return {
                'sector': sector,
                'industry': industry,
                'industry_trend': trend,
                'momentum_1m': avg_momentum_1m,
                'momentum_3m': avg_momentum_3m,
                'momentum_6m': avg_momentum_6m,
                'industry_strength': self._calculate_industry_strength(avg_momentum_1m, avg_momentum_3m, avg_momentum_6m),
                'etf_performance': industry_momentum
            }
            
        except Exception as e:
            logger.error(f"Error analyzing industry trends for {symbol}: {e}")
            return {}
    
    def _get_peer_companies(self, symbol: str, sector: str, industry: str) -> List[str]:
        """Get peer companies (simplified implementation)"""
        # This is a simplified implementation. In a real system, you'd use more sophisticated matching
        peer_mapping = {
            'AAPL': ['MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA'],
            'MSFT': ['AAPL', 'GOOGL', 'AMZN', 'META', 'ORCL'],
            'GOOGL': ['AAPL', 'MSFT', 'AMZN', 'META', 'NFLX'],
            'AMZN': ['AAPL', 'MSFT', 'GOOGL', 'META', 'TSLA'],
            'TSLA': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META'],
            'META': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NFLX'],
            'NVDA': ['AMD', 'INTC', 'MSFT', 'GOOGL', 'AMZN'],
            'AMD': ['NVDA', 'INTC', 'MSFT', 'GOOGL', 'AMZN'],
            'INTC': ['NVDA', 'AMD', 'MSFT', 'GOOGL', 'AMZN']
        }
        
        return peer_mapping.get(symbol, [])
    
    def _analyze_peer_position(self, symbol: str, peer_data: Dict) -> str:
        """Analyze position relative to peers"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1y")
            
            if hist.empty:
                return "Insufficient data"
            
            stock_return = ((hist['Close'].iloc[-1] / hist['Close'].iloc[0]) - 1) * 100
            stock_pe = info.get('trailingPE', 0)
            
            peer_returns = [data['return_1y'] for data in peer_data.values()]
            peer_pes = [data['pe_ratio'] for data in peer_data.values() if data['pe_ratio'] > 0]
            
            if not peer_returns or not peer_pes:
                return "Insufficient peer data"
            
            # Compare performance
            if stock_return > np.percentile(peer_returns, 75):
                performance_rank = "Top Quartile"
            elif stock_return > np.percentile(peer_returns, 50):
                performance_rank = "Above Average"
            elif stock_return > np.percentile(peer_returns, 25):
                performance_rank = "Below Average"
            else:
                performance_rank = "Bottom Quartile"
            
            # Compare valuation
            if stock_pe > 0:
                if stock_pe < np.percentile(peer_pes, 25):
                    valuation_rank = "Undervalued"
                elif stock_pe < np.percentile(peer_pes, 75):
                    valuation_rank = "Fairly Valued"
                else:
                    valuation_rank = "Overvalued"
            else:
                valuation_rank = "N/A"
            
            return f"{performance_rank} Performance, {valuation_rank} Valuation"
            
        except Exception as e:
            logger.error(f"Error analyzing peer position: {e}")
            return "Analysis Error"
    
    def _calculate_industry_strength(self, momentum_1m: float, momentum_3m: float, momentum_6m: float) -> str:
        """Calculate overall industry strength"""
        score = 0
        
        if momentum_1m > 5:
            score += 3
        elif momentum_1m > 2:
            score += 2
        elif momentum_1m > 0:
            score += 1
        elif momentum_1m < -5:
            score -= 3
        elif momentum_1m < -2:
            score -= 2
        elif momentum_1m < 0:
            score -= 1
        
        if momentum_3m > 10:
            score += 2
        elif momentum_3m > 5:
            score += 1
        elif momentum_3m < -10:
            score -= 2
        elif momentum_3m < -5:
            score -= 1
        
        if momentum_6m > 15:
            score += 1
        elif momentum_6m < -15:
            score -= 1
        
        if score >= 5:
            return "Very Strong"
        elif score >= 3:
            return "Strong"
        elif score >= 1:
            return "Moderate"
        elif score >= -1:
            return "Weak"
        else:
            return "Very Weak"
