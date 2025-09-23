"""
Earnings Analysis Module
Comprehensive earnings analysis including surprises, guidance, and forecasts
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class EarningsAnalyzer:
    """Comprehensive earnings analysis and forecasting"""
    
    def __init__(self):
        pass
    
    def get_earnings_history(self, symbol: str) -> Dict:
        """Get comprehensive earnings history and surprises"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get earnings data
            earnings = ticker.earnings
            quarterly_earnings = ticker.quarterly_earnings
            
            if earnings.empty and quarterly_earnings.empty:
                return {}
            
            # Analyze earnings surprises
            surprises = self._analyze_earnings_surprises(ticker)
            
            # Calculate earnings growth
            growth_metrics = self._calculate_earnings_growth(earnings, quarterly_earnings)
            
            # Get earnings estimates
            estimates = self._get_earnings_estimates(ticker)
            
            return {
                'annual_earnings': earnings.to_dict() if not earnings.empty else {},
                'quarterly_earnings': quarterly_earnings.to_dict() if not quarterly_earnings.empty else {},
                'earnings_surprises': surprises,
                'growth_metrics': growth_metrics,
                'estimates': estimates,
                'earnings_quality': self._assess_earnings_quality(earnings, quarterly_earnings)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing earnings for {symbol}: {e}")
            return {}
    
    def get_earnings_guidance(self, symbol: str) -> Dict:
        """Get earnings guidance and management commentary"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get forward-looking metrics
            forward_pe = info.get('forwardPE', 0)
            peg_ratio = info.get('pegRatio', 0)
            earnings_growth = info.get('earningsGrowth', 0)
            revenue_growth = info.get('revenueGrowth', 0)
            
            # Get analyst estimates
            estimates = self._get_analyst_estimates(ticker)
            
            # Analyze guidance trends
            guidance_analysis = self._analyze_guidance_trends(estimates)
            
            return {
                'forward_pe': forward_pe,
                'peg_ratio': peg_ratio,
                'earnings_growth_estimate': earnings_growth,
                'revenue_growth_estimate': revenue_growth,
                'analyst_estimates': estimates,
                'guidance_analysis': guidance_analysis,
                'guidance_sentiment': self._assess_guidance_sentiment(estimates, earnings_growth, revenue_growth)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing earnings guidance for {symbol}: {e}")
            return {}
    
    def get_earnings_calendar(self, symbol: str) -> Dict:
        """Get upcoming earnings dates and expectations"""
        try:
            ticker = yf.Ticker(symbol)
            calendar = ticker.calendar
            
            if calendar is None or calendar.empty:
                return {}
            
            # Get next earnings date
            next_earnings = calendar.iloc[0] if not calendar.empty else None
            
            # Get earnings estimates for next quarter
            estimates = self._get_next_earnings_estimates(ticker)
            
            return {
                'next_earnings_date': next_earnings.name if next_earnings is not None else None,
                'earnings_calendar': calendar.to_dict() if not calendar.empty else {},
                'next_quarter_estimates': estimates,
                'earnings_volatility_risk': self._assess_earnings_volatility_risk(estimates)
            }
            
        except Exception as e:
            logger.error(f"Error getting earnings calendar for {symbol}: {e}")
            return {}
    
    def _analyze_earnings_surprises(self, ticker) -> Dict:
        """Analyze earnings surprises"""
        try:
            # Get earnings surprises data
            surprises = ticker.earnings_dates
            
            if surprises is None or surprises.empty:
                return {}
            
            # Calculate surprise statistics
            actual_eps = surprises['Actual'].dropna()
            estimated_eps = surprises['Estimate'].dropna()
            
            if len(actual_eps) == 0 or len(estimated_eps) == 0:
                return {}
            
            # Calculate surprise percentages
            surprise_pct = ((actual_eps - estimated_eps) / estimated_eps * 100).dropna()
            
            if len(surprise_pct) == 0:
                return {}
            
            # Calculate statistics
            avg_surprise = surprise_pct.mean()
            positive_surprises = (surprise_pct > 0).sum()
            negative_surprises = (surprise_pct < 0).sum()
            total_quarters = len(surprise_pct)
            
            # Calculate surprise consistency
            surprise_consistency = positive_surprises / total_quarters if total_quarters > 0 else 0
            
            return {
                'average_surprise_pct': avg_surprise,
                'positive_surprises': positive_surprises,
                'negative_surprises': negative_surprises,
                'total_quarters': total_quarters,
                'surprise_consistency': surprise_consistency,
                'last_surprise': surprise_pct.iloc[-1] if len(surprise_pct) > 0 else 0,
                'surprise_trend': self._calculate_surprise_trend(surprise_pct)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing earnings surprises: {e}")
            return {}
    
    def _calculate_earnings_growth(self, annual_earnings, quarterly_earnings) -> Dict:
        """Calculate earnings growth metrics"""
        try:
            growth_metrics = {}
            
            # Annual earnings growth
            if not annual_earnings.empty and len(annual_earnings) >= 2:
                annual_growth = ((annual_earnings.iloc[-1] / annual_earnings.iloc[-2]) - 1) * 100
                growth_metrics['annual_earnings_growth'] = annual_growth
            
            # Quarterly earnings growth
            if not quarterly_earnings.empty and len(quarterly_earnings) >= 2:
                quarterly_growth = ((quarterly_earnings.iloc[-1] / quarterly_earnings.iloc[-2]) - 1) * 100
                growth_metrics['quarterly_earnings_growth'] = quarterly_growth
            
            # Calculate growth consistency
            if not quarterly_earnings.empty and len(quarterly_earnings) >= 4:
                quarterly_changes = quarterly_earnings.pct_change().dropna()
                positive_growth_quarters = (quarterly_changes > 0).sum()
                total_quarters = len(quarterly_changes)
                growth_consistency = positive_growth_quarters / total_quarters if total_quarters > 0 else 0
                growth_metrics['growth_consistency'] = growth_consistency
            
            return growth_metrics
            
        except Exception as e:
            logger.error(f"Error calculating earnings growth: {e}")
            return {}
    
    def _get_earnings_estimates(self, ticker) -> Dict:
        """Get earnings estimates from analysts"""
        try:
            # Get analyst estimates
            estimates = ticker.analyst_price_targets
            
            if estimates is None or estimates.empty:
                return {}
            
            # Get current estimates
            current_estimate = estimates.iloc[0] if not estimates.empty else None
            
            return {
                'current_estimate': current_estimate.to_dict() if current_estimate is not None else {},
                'estimate_trend': self._analyze_estimate_trend(estimates),
                'estimate_consensus': self._calculate_estimate_consensus(estimates)
            }
            
        except Exception as e:
            logger.error(f"Error getting earnings estimates: {e}")
            return {}
    
    def _get_analyst_estimates(self, ticker) -> Dict:
        """Get detailed analyst estimates"""
        try:
            info = ticker.info
            
            return {
                'eps_estimate_current_year': info.get('epsEstimateCurrentYear', 0),
                'eps_estimate_next_year': info.get('epsEstimateNextYear', 0),
                'eps_estimate_next_quarter': info.get('epsEstimateNextQuarter', 0),
                'revenue_estimate_current_year': info.get('revenueEstimateCurrentYear', 0),
                'revenue_estimate_next_year': info.get('revenueEstimateNextYear', 0),
                'revenue_estimate_next_quarter': info.get('revenueEstimateNextQuarter', 0)
            }
            
        except Exception as e:
            logger.error(f"Error getting analyst estimates: {e}")
            return {}
    
    def _analyze_guidance_trends(self, estimates: Dict) -> str:
        """Analyze guidance trends"""
        try:
            current_year_eps = estimates.get('eps_estimate_current_year', 0)
            next_year_eps = estimates.get('eps_estimate_next_year', 0)
            
            if current_year_eps > 0 and next_year_eps > 0:
                growth_rate = ((next_year_eps - current_year_eps) / current_year_eps) * 100
                
                if growth_rate > 20:
                    return "Very Positive Guidance"
                elif growth_rate > 10:
                    return "Positive Guidance"
                elif growth_rate > 0:
                    return "Moderate Growth Guidance"
                elif growth_rate > -10:
                    return "Flat Guidance"
                else:
                    return "Negative Guidance"
            
            return "Insufficient Data"
            
        except Exception as e:
            logger.error(f"Error analyzing guidance trends: {e}")
            return "Analysis Error"
    
    def _assess_guidance_sentiment(self, estimates: Dict, earnings_growth: float, revenue_growth: float) -> str:
        """Assess overall guidance sentiment"""
        try:
            score = 0
            
            # Earnings growth
            if earnings_growth > 20:
                score += 3
            elif earnings_growth > 10:
                score += 2
            elif earnings_growth > 0:
                score += 1
            elif earnings_growth < -20:
                score -= 3
            elif earnings_growth < -10:
                score -= 2
            elif earnings_growth < 0:
                score -= 1
            
            # Revenue growth
            if revenue_growth > 15:
                score += 2
            elif revenue_growth > 5:
                score += 1
            elif revenue_growth < -15:
                score -= 2
            elif revenue_growth < -5:
                score -= 1
            
            if score >= 4:
                return "Very Bullish"
            elif score >= 2:
                return "Bullish"
            elif score >= 0:
                return "Neutral"
            elif score >= -2:
                return "Bearish"
            else:
                return "Very Bearish"
                
        except Exception as e:
            logger.error(f"Error assessing guidance sentiment: {e}")
            return "Analysis Error"
    
    def _get_next_earnings_estimates(self, ticker) -> Dict:
        """Get estimates for next earnings report"""
        try:
            info = ticker.info
            
            return {
                'next_eps_estimate': info.get('epsEstimateNextQuarter', 0),
                'next_revenue_estimate': info.get('revenueEstimateNextQuarter', 0),
                'estimate_accuracy': self._calculate_estimate_accuracy(ticker)
            }
            
        except Exception as e:
            logger.error(f"Error getting next earnings estimates: {e}")
            return {}
    
    def _assess_earnings_volatility_risk(self, estimates: Dict) -> str:
        """Assess earnings volatility risk"""
        try:
            # This is a simplified assessment
            # In a real implementation, you'd analyze historical volatility
            
            estimate_accuracy = estimates.get('estimate_accuracy', 0)
            
            if estimate_accuracy > 0.8:
                return "Low Volatility Risk"
            elif estimate_accuracy > 0.6:
                return "Moderate Volatility Risk"
            else:
                return "High Volatility Risk"
                
        except Exception as e:
            logger.error(f"Error assessing earnings volatility risk: {e}")
            return "Analysis Error"
    
    def _calculate_surprise_trend(self, surprise_pct: pd.Series) -> str:
        """Calculate surprise trend"""
        try:
            if len(surprise_pct) < 2:
                return "Insufficient Data"
            
            recent_avg = surprise_pct.tail(2).mean()
            older_avg = surprise_pct.head(-2).mean() if len(surprise_pct) > 2 else surprise_pct.iloc[0]
            
            if recent_avg > older_avg + 2:
                return "Improving Surprises"
            elif recent_avg < older_avg - 2:
                return "Declining Surprises"
            else:
                return "Stable Surprises"
                
        except Exception as e:
            logger.error(f"Error calculating surprise trend: {e}")
            return "Analysis Error"
    
    def _analyze_estimate_trend(self, estimates: pd.DataFrame) -> str:
        """Analyze estimate trend"""
        try:
            if estimates.empty or len(estimates) < 2:
                return "Insufficient Data"
            
            # This is a simplified analysis
            return "Stable Estimates"
            
        except Exception as e:
            logger.error(f"Error analyzing estimate trend: {e}")
            return "Analysis Error"
    
    def _calculate_estimate_consensus(self, estimates: pd.DataFrame) -> float:
        """Calculate estimate consensus"""
        try:
            if estimates.empty:
                return 0.0
            
            # This is a simplified calculation
            return 0.75  # Placeholder
            
        except Exception as e:
            logger.error(f"Error calculating estimate consensus: {e}")
            return 0.0
    
    def _calculate_estimate_accuracy(self, ticker) -> float:
        """Calculate historical estimate accuracy"""
        try:
            # This is a simplified calculation
            # In a real implementation, you'd compare historical estimates vs actuals
            return 0.7  # Placeholder
            
        except Exception as e:
            logger.error(f"Error calculating estimate accuracy: {e}")
            return 0.0
    
    def _assess_earnings_quality(self, annual_earnings, quarterly_earnings) -> str:
        """Assess earnings quality"""
        try:
            if annual_earnings.empty and quarterly_earnings.empty:
                return "Insufficient Data"
            
            # Simple quality assessment based on consistency
            if not quarterly_earnings.empty and len(quarterly_earnings) >= 4:
                quarterly_changes = quarterly_earnings.pct_change().dropna()
                volatility = quarterly_changes.std()
                
                if volatility < 0.1:
                    return "High Quality (Stable)"
                elif volatility < 0.2:
                    return "Good Quality (Moderate Stability)"
                else:
                    return "Variable Quality (High Volatility)"
            
            return "Moderate Quality"
            
        except Exception as e:
            logger.error(f"Error assessing earnings quality: {e}")
            return "Analysis Error"
