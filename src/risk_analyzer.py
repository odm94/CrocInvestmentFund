"""
Advanced Risk Analysis Module
Comprehensive risk metrics including VaR, Beta, Correlation, and ESG analysis
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
from scipy import stats

logger = logging.getLogger(__name__)

class RiskAnalyzer:
    """Advanced risk analysis and metrics"""
    
    def __init__(self):
        pass
    
    def get_comprehensive_risk_metrics(self, symbol: str) -> Dict:
        """Get comprehensive risk analysis"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            hist = ticker.history(period="2y")
            if hist.empty:
                return {}
            
            # Calculate various risk metrics
            risk_metrics = {
                'volatility_metrics': self._calculate_volatility_metrics(hist),
                'beta_analysis': self._calculate_beta_analysis(symbol, hist),
                'var_metrics': self._calculate_var_metrics(hist),
                'correlation_analysis': self._calculate_correlation_analysis(symbol, hist),
                'drawdown_analysis': self._calculate_drawdown_analysis(hist),
                'risk_adjusted_returns': self._calculate_risk_adjusted_returns(hist),
                'esg_analysis': self._get_esg_analysis(ticker),
                'liquidity_risk': self._assess_liquidity_risk(ticker, hist)
            }
            
            return risk_metrics
            
        except Exception as e:
            logger.error(f"Error calculating risk metrics for {symbol}: {e}")
            return {}
    
    def _calculate_volatility_metrics(self, hist: pd.DataFrame) -> Dict:
        """Calculate various volatility metrics"""
        try:
            returns = hist['Close'].pct_change().dropna()
            
            # Annualized volatility
            annual_vol = returns.std() * np.sqrt(252)
            
            # Rolling volatility (30-day)
            rolling_vol = returns.rolling(window=30).std() * np.sqrt(252)
            current_vol = rolling_vol.iloc[-1] if not rolling_vol.empty else 0
            avg_vol = rolling_vol.mean()
            
            # Volatility of volatility
            vol_of_vol = rolling_vol.std()
            
            # GARCH-like volatility clustering
            vol_clustering = self._calculate_volatility_clustering(returns)
            
            return {
                'annual_volatility': annual_vol,
                'current_volatility': current_vol,
                'average_volatility': avg_vol,
                'volatility_of_volatility': vol_of_vol,
                'volatility_clustering': vol_clustering,
                'volatility_percentile': self._calculate_volatility_percentile(current_vol, rolling_vol)
            }
            
        except Exception as e:
            logger.error(f"Error calculating volatility metrics: {e}")
            return {}
    
    def _calculate_beta_analysis(self, symbol: str, hist: pd.DataFrame) -> Dict:
        """Calculate beta and market correlation"""
        try:
            # Get market data (SPY)
            market = yf.Ticker('SPY').history(period="2y")
            if market.empty:
                return {}
            
            # Align dates
            common_dates = hist.index.intersection(market.index)
            stock_returns = hist.loc[common_dates, 'Close'].pct_change().dropna()
            market_returns = market.loc[common_dates, 'Close'].pct_change().dropna()
            
            # Calculate beta
            covariance = np.cov(stock_returns, market_returns)[0, 1]
            market_variance = np.var(market_returns)
            beta = covariance / market_variance if market_variance > 0 else 0
            
            # Calculate correlation
            correlation = np.corrcoef(stock_returns, market_returns)[0, 1]
            
            # Calculate rolling beta
            rolling_beta = self._calculate_rolling_beta(stock_returns, market_returns)
            
            return {
                'beta': beta,
                'market_correlation': correlation,
                'current_rolling_beta': rolling_beta.iloc[-1] if not rolling_beta.empty else beta,
                'beta_stability': self._assess_beta_stability(rolling_beta),
                'systematic_risk': beta * 0.15,  # Assuming 15% market volatility
                'unsystematic_risk': self._calculate_unsystematic_risk(stock_returns, market_returns, beta)
            }
            
        except Exception as e:
            logger.error(f"Error calculating beta analysis: {e}")
            return {}
    
    def _calculate_var_metrics(self, hist: pd.DataFrame) -> Dict:
        """Calculate Value at Risk (VaR) metrics"""
        try:
            returns = hist['Close'].pct_change().dropna()
            
            # Historical VaR
            var_95 = np.percentile(returns, 5)
            var_99 = np.percentile(returns, 1)
            
            # Parametric VaR (assuming normal distribution)
            mean_return = returns.mean()
            std_return = returns.std()
            var_95_param = mean_return - 1.645 * std_return
            var_99_param = mean_return - 2.326 * std_return
            
            # Expected Shortfall (Conditional VaR)
            es_95 = returns[returns <= var_95].mean()
            es_99 = returns[returns <= var_99].mean()
            
            # Maximum Drawdown
            cumulative_returns = (1 + returns).cumprod()
            running_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - running_max) / running_max
            max_drawdown = drawdown.min()
            
            return {
                'var_95_historical': var_95,
                'var_99_historical': var_99,
                'var_95_parametric': var_95_param,
                'var_99_parametric': var_99_param,
                'expected_shortfall_95': es_95,
                'expected_shortfall_99': es_99,
                'maximum_drawdown': max_drawdown,
                'var_percentile_rank': self._calculate_var_percentile_rank(var_95)
            }
            
        except Exception as e:
            logger.error(f"Error calculating VaR metrics: {e}")
            return {}
    
    def _calculate_correlation_analysis(self, symbol: str, hist: pd.DataFrame) -> Dict:
        """Calculate correlation with various assets and sectors"""
        try:
            # Get sector ETFs
            sector_etfs = {
                'Technology': 'XLK',
                'Healthcare': 'XLV',
                'Financial': 'XLF',
                'Consumer Discretionary': 'XLY',
                'Communication': 'XLC',
                'Industrials': 'XLI',
                'Consumer Staples': 'XLP',
                'Energy': 'XLE',
                'Utilities': 'XLU',
                'Real Estate': 'XLRE',
                'Materials': 'XLB'
            }
            
            stock_returns = hist['Close'].pct_change().dropna()
            correlations = {}
            
            for sector, etf in sector_etfs.items():
                try:
                    etf_data = yf.Ticker(etf).history(period="2y")
                    if not etf_data.empty:
                        common_dates = hist.index.intersection(etf_data.index)
                        etf_returns = etf_data.loc[common_dates, 'Close'].pct_change().dropna()
                        stock_returns_aligned = stock_returns.loc[common_dates].dropna()
                        
                        if len(stock_returns_aligned) > 10 and len(etf_returns) > 10:
                            correlation = np.corrcoef(stock_returns_aligned, etf_returns)[0, 1]
                            correlations[sector] = correlation
                except:
                    continue
            
            # Find highest correlation
            if correlations:
                max_correlation = max(correlations.items(), key=lambda x: abs(x[1]))
                avg_correlation = np.mean(list(correlations.values()))
            else:
                max_correlation = ("None", 0)
                avg_correlation = 0
            
            return {
                'sector_correlations': correlations,
                'highest_correlation': max_correlation,
                'average_correlation': avg_correlation,
                'correlation_diversification': self._assess_correlation_diversification(correlations)
            }
            
        except Exception as e:
            logger.error(f"Error calculating correlation analysis: {e}")
            return {}
    
    def _calculate_drawdown_analysis(self, hist: pd.DataFrame) -> Dict:
        """Calculate drawdown analysis"""
        try:
            returns = hist['Close'].pct_change().dropna()
            cumulative_returns = (1 + returns).cumprod()
            
            # Calculate drawdowns
            running_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - running_max) / running_max
            
            # Drawdown statistics
            max_drawdown = drawdown.min()
            current_drawdown = drawdown.iloc[-1]
            avg_drawdown = drawdown[drawdown < 0].mean()
            
            # Recovery analysis
            recovery_analysis = self._analyze_recovery_periods(drawdown)
            
            return {
                'maximum_drawdown': max_drawdown,
                'current_drawdown': current_drawdown,
                'average_drawdown': avg_drawdown,
                'drawdown_frequency': (drawdown < -0.05).sum(),  # Count of 5%+ drawdowns
                'recovery_analysis': recovery_analysis,
                'drawdown_risk_level': self._assess_drawdown_risk(max_drawdown, avg_drawdown)
            }
            
        except Exception as e:
            logger.error(f"Error calculating drawdown analysis: {e}")
            return {}
    
    def _calculate_risk_adjusted_returns(self, hist: pd.DataFrame) -> Dict:
        """Calculate risk-adjusted return metrics"""
        try:
            returns = hist['Close'].pct_change().dropna()
            
            # Sharpe Ratio (assuming 2% risk-free rate)
            risk_free_rate = 0.02 / 252  # Daily risk-free rate
            excess_returns = returns - risk_free_rate
            sharpe_ratio = excess_returns.mean() / returns.std() * np.sqrt(252)
            
            # Sortino Ratio (downside deviation)
            downside_returns = returns[returns < 0]
            downside_deviation = downside_returns.std() * np.sqrt(252)
            sortino_ratio = excess_returns.mean() / downside_deviation * np.sqrt(252) if downside_deviation > 0 else 0
            
            # Calmar Ratio (return / max drawdown)
            cumulative_returns = (1 + returns).cumprod()
            running_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - running_max) / running_max
            max_drawdown = abs(drawdown.min())
            annual_return = (cumulative_returns.iloc[-1] ** (252 / len(returns))) - 1
            calmar_ratio = annual_return / max_drawdown if max_drawdown > 0 else 0
            
            # Information Ratio (vs market)
            market = yf.Ticker('SPY').history(period="2y")
            if not market.empty:
                common_dates = hist.index.intersection(market.index)
                market_returns = market.loc[common_dates, 'Close'].pct_change().dropna()
                stock_returns_aligned = returns.loc[common_dates].dropna()
                
                if len(stock_returns_aligned) > 10 and len(market_returns) > 10:
                    active_returns = stock_returns_aligned - market_returns
                    tracking_error = active_returns.std() * np.sqrt(252)
                    information_ratio = active_returns.mean() / tracking_error * np.sqrt(252) if tracking_error > 0 else 0
                else:
                    information_ratio = 0
            else:
                information_ratio = 0
            
            return {
                'sharpe_ratio': sharpe_ratio,
                'sortino_ratio': sortino_ratio,
                'calmar_ratio': calmar_ratio,
                'information_ratio': information_ratio,
                'risk_adjusted_rating': self._rate_risk_adjusted_performance(sharpe_ratio, sortino_ratio, calmar_ratio)
            }
            
        except Exception as e:
            logger.error(f"Error calculating risk-adjusted returns: {e}")
            return {}
    
    def _get_esg_analysis(self, ticker) -> Dict:
        """Get ESG (Environmental, Social, Governance) analysis"""
        try:
            info = ticker.info
            
            # ESG scores (if available)
            esg_scores = {
                'environmental_score': info.get('environmentalScore', 0),
                'social_score': info.get('socialScore', 0),
                'governance_score': info.get('governanceScore', 0),
                'esg_risk_score': info.get('esgRiskScore', 0)
            }
            
            # Calculate overall ESG rating
            if all(score > 0 for score in esg_scores.values() if score > 0):
                avg_esg = np.mean([score for score in esg_scores.values() if score > 0])
                esg_rating = self._calculate_esg_rating(avg_esg)
            else:
                esg_rating = "Not Available"
            
            return {
                **esg_scores,
                'esg_rating': esg_rating,
                'esg_risk_level': self._assess_esg_risk(esg_scores.get('esg_risk_score', 0))
            }
            
        except Exception as e:
            logger.error(f"Error getting ESG analysis: {e}")
            return {}
    
    def _assess_liquidity_risk(self, ticker, hist: pd.DataFrame) -> Dict:
        """Assess liquidity risk"""
        try:
            info = ticker.info
            
            # Volume analysis
            avg_volume = hist['Volume'].mean()
            current_volume = hist['Volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            # Bid-ask spread (approximation using high-low)
            daily_spread = ((hist['High'] - hist['Low']) / hist['Close']).mean()
            
            # Market cap
            market_cap = info.get('marketCap', 0)
            
            return {
                'average_volume': avg_volume,
                'current_volume': current_volume,
                'volume_ratio': volume_ratio,
                'daily_spread': daily_spread,
                'market_cap': market_cap,
                'liquidity_rating': self._rate_liquidity(volume_ratio, daily_spread, market_cap)
            }
            
        except Exception as e:
            logger.error(f"Error assessing liquidity risk: {e}")
            return {}
    
    # Helper methods
    def _calculate_volatility_clustering(self, returns: pd.Series) -> float:
        """Calculate volatility clustering (GARCH-like)"""
        try:
            squared_returns = returns ** 2
            return squared_returns.autocorr(lag=1) if len(squared_returns) > 1 else 0
        except:
            return 0
    
    def _calculate_volatility_percentile(self, current_vol: float, rolling_vol: pd.Series) -> float:
        """Calculate current volatility percentile"""
        try:
            if rolling_vol.empty:
                return 50
            return (rolling_vol < current_vol).sum() / len(rolling_vol) * 100
        except:
            return 50
    
    def _calculate_rolling_beta(self, stock_returns: pd.Series, market_returns: pd.Series) -> pd.Series:
        """Calculate rolling beta"""
        try:
            window = 60  # 60-day rolling window
            rolling_beta = stock_returns.rolling(window=window).cov(market_returns) / market_returns.rolling(window=window).var()
            return rolling_beta
        except:
            return pd.Series()
    
    def _assess_beta_stability(self, rolling_beta: pd.Series) -> str:
        """Assess beta stability"""
        try:
            if rolling_beta.empty:
                return "Unknown"
            
            beta_std = rolling_beta.std()
            if beta_std < 0.1:
                return "Very Stable"
            elif beta_std < 0.2:
                return "Stable"
            elif beta_std < 0.3:
                return "Moderate"
            else:
                return "Volatile"
        except:
            return "Unknown"
    
    def _calculate_unsystematic_risk(self, stock_returns: pd.Series, market_returns: pd.Series, beta: float) -> float:
        """Calculate unsystematic risk"""
        try:
            predicted_returns = beta * market_returns
            residuals = stock_returns - predicted_returns
            return residuals.var() * 252  # Annualized
        except:
            return 0
    
    def _calculate_var_percentile_rank(self, var_95: float) -> float:
        """Calculate VaR percentile rank"""
        # This is a simplified calculation
        return 50.0  # Placeholder
    
    def _assess_correlation_diversification(self, correlations: Dict) -> str:
        """Assess correlation diversification"""
        try:
            if not correlations:
                return "Unknown"
            
            avg_correlation = np.mean(list(correlations.values()))
            if avg_correlation < 0.3:
                return "High Diversification"
            elif avg_correlation < 0.6:
                return "Moderate Diversification"
            else:
                return "Low Diversification"
        except:
            return "Unknown"
    
    def _analyze_recovery_periods(self, drawdown: pd.Series) -> Dict:
        """Analyze recovery periods from drawdowns"""
        try:
            # This is a simplified analysis
            return {
                'average_recovery_days': 30,  # Placeholder
                'longest_recovery_days': 90,  # Placeholder
                'recovery_success_rate': 0.8  # Placeholder
            }
        except:
            return {}
    
    def _assess_drawdown_risk(self, max_drawdown: float, avg_drawdown: float) -> str:
        """Assess drawdown risk level"""
        try:
            if max_drawdown < -0.3:
                return "High Risk"
            elif max_drawdown < -0.2:
                return "Moderate Risk"
            elif max_drawdown < -0.1:
                return "Low Risk"
            else:
                return "Very Low Risk"
        except:
            return "Unknown"
    
    def _rate_risk_adjusted_performance(self, sharpe: float, sortino: float, calmar: float) -> str:
        """Rate risk-adjusted performance"""
        try:
            score = 0
            if sharpe > 1.5:
                score += 3
            elif sharpe > 1.0:
                score += 2
            elif sharpe > 0.5:
                score += 1
            
            if sortino > 2.0:
                score += 2
            elif sortino > 1.0:
                score += 1
            
            if calmar > 1.0:
                score += 2
            elif calmar > 0.5:
                score += 1
            
            if score >= 6:
                return "Excellent"
            elif score >= 4:
                return "Good"
            elif score >= 2:
                return "Average"
            else:
                return "Poor"
        except:
            return "Unknown"
    
    def _calculate_esg_rating(self, avg_esg: float) -> str:
        """Calculate ESG rating"""
        try:
            if avg_esg >= 80:
                return "AAA"
            elif avg_esg >= 70:
                return "AA"
            elif avg_esg >= 60:
                return "A"
            elif avg_esg >= 50:
                return "BBB"
            elif avg_esg >= 40:
                return "BB"
            elif avg_esg >= 30:
                return "B"
            else:
                return "CCC"
        except:
            return "Not Rated"
    
    def _assess_esg_risk(self, esg_risk_score: float) -> str:
        """Assess ESG risk level"""
        try:
            if esg_risk_score <= 10:
                return "Low Risk"
            elif esg_risk_score <= 20:
                return "Moderate Risk"
            elif esg_risk_score <= 30:
                return "High Risk"
            else:
                return "Very High Risk"
        except:
            return "Unknown"
    
    def _rate_liquidity(self, volume_ratio: float, daily_spread: float, market_cap: float) -> str:
        """Rate liquidity"""
        try:
            score = 0
            
            if volume_ratio > 1.5:
                score += 2
            elif volume_ratio > 1.0:
                score += 1
            
            if daily_spread < 0.01:
                score += 2
            elif daily_spread < 0.02:
                score += 1
            
            if market_cap > 10e9:  # > $10B
                score += 2
            elif market_cap > 1e9:  # > $1B
                score += 1
            
            if score >= 5:
                return "High Liquidity"
            elif score >= 3:
                return "Good Liquidity"
            elif score >= 1:
                return "Moderate Liquidity"
            else:
                return "Low Liquidity"
        except:
            return "Unknown"
