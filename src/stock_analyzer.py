"""
Main Stock Analyzer Class
Combines data fetching and valuation models
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from .data_fetcher import StockDataFetcher
from .valuation_models import ValuationModels
from .ai_analyzer import AIAnalyzer
from .hybrid_ai_analyzer import HybridAIAnalyzer

logger = logging.getLogger(__name__)

class StockAnalyzer:
    """Main class for stock analysis and valuation"""
    
    def __init__(self):
        self.data_fetcher = StockDataFetcher()
        self.valuation_models = ValuationModels()
        self.ai_analyzer = HybridAIAnalyzer()  # Use hybrid AI analyzer
    
    def analyze_stock(self, symbol: str) -> Dict:
        """
        Perform comprehensive stock analysis
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        """
        try:
            logger.info(f"Starting analysis for {symbol}")
            
            # Fetch all required data
            stock_info = self.data_fetcher.get_stock_info(symbol)
            if not stock_info:
                return {'error': f'Could not fetch data for {symbol}'}
            
            key_metrics = self.data_fetcher.get_key_metrics(symbol)
            financial_statements = self.data_fetcher.get_financial_statements(symbol)
            analyst_recommendations = self.data_fetcher.get_analyst_recommendations(symbol)
            historical_data = self.data_fetcher.get_historical_data(symbol)
            
            # Calculate additional metrics from financial statements
            additional_metrics = self._calculate_additional_metrics(financial_statements)
            
            # Combine all metrics
            all_metrics = {**key_metrics, **additional_metrics}
            
            # Perform valuations
            valuation_results = self.valuation_models.comprehensive_valuation(
                stock_info, {'metrics': all_metrics}
            )
            
            # Calculate technical indicators
            technical_analysis = self._calculate_technical_indicators(historical_data)
            
            # Generate investment recommendation
            recommendation = self._generate_recommendation(
                stock_info, all_metrics, valuation_results, technical_analysis
            )
            
            # Prepare data for AI analysis
            analysis_data = {
                'symbol': symbol,
                'stock_info': stock_info,
                'metrics': all_metrics,
                'valuation': valuation_results,
                'technical_analysis': technical_analysis,
                'recommendation': recommendation
            }
            
            # Generate AI analysis
            ai_analysis = self.ai_analyzer.generate_analysis_report(analysis_data)
            investment_thesis = self.ai_analyzer.generate_investment_thesis(analysis_data)
            risk_assessment = self.ai_analyzer.generate_risk_assessment(analysis_data)
            
            return {
                'symbol': symbol,
                'stock_info': stock_info,
                'metrics': all_metrics,
                'valuation': valuation_results,
                'technical_analysis': technical_analysis,
                'analyst_recommendations': analyst_recommendations,
                'recommendation': recommendation,
                'ai_analysis': ai_analysis,
                'investment_thesis': investment_thesis,
                'risk_assessment': risk_assessment,
                'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            logger.error(f"Error analyzing stock {symbol}: {e}")
            return {'error': f'Analysis failed for {symbol}: {str(e)}'}
    
    def _calculate_additional_metrics(self, financial_statements: Dict) -> Dict:
        """Calculate additional financial metrics from statements"""
        try:
            metrics = {}
            
            if not financial_statements:
                return metrics
            
            income_stmt = financial_statements.get('income_statement', pd.DataFrame())
            balance_sheet = financial_statements.get('balance_sheet', pd.DataFrame())
            cash_flow = financial_statements.get('cash_flow', pd.DataFrame())
            
            if not income_stmt.empty:
                # Get latest year data
                latest_year = income_stmt.columns[0]
                
                # Revenue and earnings
                revenue = income_stmt.loc['Total Revenue', latest_year] if 'Total Revenue' in income_stmt.index else 0
                net_income = income_stmt.loc['Net Income', latest_year] if 'Net Income' in income_stmt.index else 0
                
                metrics['revenue'] = revenue
                metrics['net_income'] = net_income
                metrics['earnings_per_share'] = net_income / 1000000  # Simplified calculation
            
            if not balance_sheet.empty:
                latest_year = balance_sheet.columns[0]
                
                # Balance sheet items
                total_assets = balance_sheet.loc['Total Assets', latest_year] if 'Total Assets' in balance_sheet.index else 0
                total_liabilities = balance_sheet.loc['Total Liab', latest_year] if 'Total Liab' in balance_sheet.index else 0
                shareholders_equity = balance_sheet.loc['Stockholders Equity', latest_year] if 'Stockholders Equity' in balance_sheet.index else 0
                
                metrics['total_assets'] = total_assets
                metrics['total_liabilities'] = total_liabilities
                metrics['shareholders_equity'] = shareholders_equity
                metrics['book_value_per_share'] = shareholders_equity / 1000000  # Simplified calculation
            
            if not cash_flow.empty:
                latest_year = cash_flow.columns[0]
                
                # Cash flow items
                operating_cash_flow = cash_flow.loc['Total Cash From Operating Activities', latest_year] if 'Total Cash From Operating Activities' in cash_flow.index else 0
                capex = cash_flow.loc['Capital Expenditures', latest_year] if 'Capital Expenditures' in cash_flow.index else 0
                
                metrics['operating_cash_flow'] = operating_cash_flow
                metrics['capital_expenditures'] = capex
                metrics['free_cash_flow'] = operating_cash_flow - capex
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating additional metrics: {e}")
            return {}
    
    def _calculate_technical_indicators(self, historical_data: pd.DataFrame) -> Dict:
        """Calculate technical analysis indicators"""
        try:
            if historical_data.empty:
                return {}
            
            # Calculate moving averages
            ma_20 = historical_data['Close'].rolling(window=20).mean().iloc[-1]
            ma_50 = historical_data['Close'].rolling(window=50).mean().iloc[-1]
            ma_200 = historical_data['Close'].rolling(window=200).mean().iloc[-1]
            
            current_price = historical_data['Close'].iloc[-1]
            
            # Calculate RSI
            delta = historical_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1]
            
            # Calculate Bollinger Bands
            bb_period = 20
            bb_std = 2
            bb_middle = historical_data['Close'].rolling(window=bb_period).mean()
            bb_std_dev = historical_data['Close'].rolling(window=bb_period).std()
            bb_upper = bb_middle + (bb_std_dev * bb_std)
            bb_lower = bb_middle - (bb_std_dev * bb_std)
            
            bb_upper_current = bb_upper.iloc[-1]
            bb_lower_current = bb_lower.iloc[-1]
            bb_middle_current = bb_middle.iloc[-1]
            
            # Calculate volatility
            returns = historical_data['Close'].pct_change()
            volatility = returns.std() * np.sqrt(252)  # Annualized volatility
            
            return {
                'moving_averages': {
                    'ma_20': ma_20,
                    'ma_50': ma_50,
                    'ma_200': ma_200
                },
                'current_price': current_price,
                'rsi': rsi,
                'bollinger_bands': {
                    'upper': bb_upper_current,
                    'middle': bb_middle_current,
                    'lower': bb_lower_current
                },
                'volatility': volatility,
                'price_vs_ma': {
                    'vs_ma_20': ((current_price - ma_20) / ma_20) * 100,
                    'vs_ma_50': ((current_price - ma_50) / ma_50) * 100,
                    'vs_ma_200': ((current_price - ma_200) / ma_200) * 100
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {e}")
            return {}
    
    def _generate_recommendation(self, 
                               stock_info: Dict, 
                               metrics: Dict, 
                               valuation: Dict, 
                               technical: Dict) -> Dict:
        """Generate investment recommendation based on analysis"""
        try:
            recommendation_score = 0
            factors = []
            
            # Valuation factors
            if 'upside_potential' in valuation:
                upside = valuation['upside_potential']
                if upside > 20:
                    recommendation_score += 2
                    factors.append(f"Strong upside potential: {upside:.1f}%")
                elif upside > 10:
                    recommendation_score += 1
                    factors.append(f"Moderate upside potential: {upside:.1f}%")
                elif upside < -20:
                    recommendation_score -= 2
                    factors.append(f"Significant downside risk: {upside:.1f}%")
                elif upside < -10:
                    recommendation_score -= 1
                    factors.append(f"Moderate downside risk: {upside:.1f}%")
            
            # Financial health factors
            pe_ratio = metrics.get('pe_ratio', 0)
            if 10 <= pe_ratio <= 25:
                recommendation_score += 1
                factors.append(f"Reasonable P/E ratio: {pe_ratio:.1f}")
            elif pe_ratio > 30:
                recommendation_score -= 1
                factors.append(f"High P/E ratio: {pe_ratio:.1f}")
            
            # Profitability
            roe = metrics.get('return_on_equity', 0)
            if roe > 0.15:
                recommendation_score += 1
                factors.append(f"Strong ROE: {roe:.1%}")
            elif roe < 0.05:
                recommendation_score -= 1
                factors.append(f"Low ROE: {roe:.1%}")
            
            # Debt levels
            debt_to_equity = metrics.get('debt_to_equity', 0)
            if debt_to_equity < 0.5:
                recommendation_score += 1
                factors.append(f"Low debt levels: {debt_to_equity:.1f}")
            elif debt_to_equity > 1.0:
                recommendation_score -= 1
                factors.append(f"High debt levels: {debt_to_equity:.1f}")
            
            # Technical factors
            if technical:
                rsi = technical.get('rsi', 50)
                if rsi < 30:
                    recommendation_score += 1
                    factors.append("Oversold conditions (RSI < 30)")
                elif rsi > 70:
                    recommendation_score -= 1
                    factors.append("Overbought conditions (RSI > 70)")
                
                price_vs_ma = technical.get('price_vs_ma', {})
                if price_vs_ma.get('vs_ma_200', 0) > 0:
                    recommendation_score += 1
                    factors.append("Price above 200-day MA")
                else:
                    recommendation_score -= 1
                    factors.append("Price below 200-day MA")
            
            # Determine recommendation
            if recommendation_score >= 3:
                recommendation = "STRONG BUY"
            elif recommendation_score >= 1:
                recommendation = "BUY"
            elif recommendation_score >= -1:
                recommendation = "HOLD"
            elif recommendation_score >= -3:
                recommendation = "SELL"
            else:
                recommendation = "STRONG SELL"
            
            return {
                'recommendation': recommendation,
                'score': recommendation_score,
                'factors': factors,
                'confidence': min(abs(recommendation_score) / 5, 1.0)  # Confidence level 0-1
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendation: {e}")
            return {
                'recommendation': 'HOLD',
                'score': 0,
                'factors': ['Analysis error'],
                'confidence': 0.0
            }
