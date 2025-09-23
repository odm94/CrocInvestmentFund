"""
Ultimate Stock Analyzer - The Most Comprehensive Stock Analysis Tool
Combines all analysis modules for institutional-grade analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from .enhanced_analyzer import EnhancedStockAnalyzer
from .sector_analyzer import SectorAnalyzer
from .earnings_analyzer import EarningsAnalyzer
from .risk_analyzer import RiskAnalyzer

logger = logging.getLogger(__name__)

class UltimateStockAnalyzer(EnhancedStockAnalyzer):
    """Ultimate stock analyzer with all advanced features"""
    
    def __init__(self):
        super().__init__()
        self.sector_analyzer = SectorAnalyzer()
        self.earnings_analyzer = EarningsAnalyzer()
        self.risk_analyzer = RiskAnalyzer()
    
    def analyze_stock_ultimate(self, symbol: str) -> Dict:
        """
        Perform ultimate comprehensive stock analysis
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        """
        try:
            logger.info(f"Starting ULTIMATE analysis for {symbol}")
            
            # Get enhanced analysis from parent class
            enhanced_analysis = self.analyze_stock_enhanced(symbol)
            
            if 'error' in enhanced_analysis:
                return enhanced_analysis
            
            # Get additional analysis modules
            sector_analysis = self.sector_analyzer.get_sector_performance(symbol)
            peer_analysis = self.sector_analyzer.get_peer_comparison(symbol)
            industry_trends = self.sector_analyzer.get_industry_trends(symbol)
            
            earnings_analysis = self.earnings_analyzer.get_earnings_history(symbol)
            earnings_guidance = self.earnings_analyzer.get_earnings_guidance(symbol)
            earnings_calendar = self.earnings_analyzer.get_earnings_calendar(symbol)
            
            risk_analysis = self.risk_analyzer.get_comprehensive_risk_metrics(symbol)
            
            # Combine all analysis
            ultimate_analysis = self._combine_all_analysis(
                enhanced_analysis, sector_analysis, peer_analysis, industry_trends,
                earnings_analysis, earnings_guidance, earnings_calendar, risk_analysis
            )
            
            # Generate ultimate recommendation
            ultimate_recommendation = self._generate_ultimate_recommendation(ultimate_analysis)
            
            # Add ultimate data to results
            ultimate_analysis.update({
                'sector_analysis': sector_analysis,
                'peer_analysis': peer_analysis,
                'industry_trends': industry_trends,
                'earnings_analysis': earnings_analysis,
                'earnings_guidance': earnings_guidance,
                'earnings_calendar': earnings_calendar,
                'risk_analysis': risk_analysis,
                'ultimate_recommendation': ultimate_recommendation,
                'analysis_type': 'ultimate_comprehensive',
                'total_data_sources': 15  # Count of all data sources used
            })
            
            return ultimate_analysis
            
        except Exception as e:
            logger.error(f"Error in ultimate analysis for {symbol}: {e}")
            return {'error': f'Ultimate analysis failed for {symbol}: {str(e)}'}
    
    def _combine_all_analysis(self, enhanced_analysis: Dict, sector_analysis: Dict, 
                            peer_analysis: Dict, industry_trends: Dict,
                            earnings_analysis: Dict, earnings_guidance: Dict, 
                            earnings_calendar: Dict, risk_analysis: Dict) -> Dict:
        """Combine all analysis modules into comprehensive insights"""
        try:
            combined_insights = {}
            
            # Sector and Industry Insights
            if sector_analysis:
                combined_insights['sector_insights'] = {
                    'sector_performance': sector_analysis.get('vs_sector_performance', 0),
                    'market_performance': sector_analysis.get('vs_market_performance', 0),
                    'sector_ranking': self._calculate_sector_ranking(sector_analysis),
                    'sector_momentum': self._assess_sector_momentum(sector_analysis)
                }
            
            # Peer Comparison Insights
            if peer_analysis:
                combined_insights['peer_insights'] = {
                    'peer_performance_rank': self._calculate_peer_rank(peer_analysis),
                    'valuation_vs_peers': self._compare_valuation_to_peers(enhanced_analysis, peer_analysis),
                    'competitive_position': self._assess_competitive_position(peer_analysis)
                }
            
            # Industry Trends Insights
            if industry_trends:
                combined_insights['industry_insights'] = {
                    'industry_trend': industry_trends.get('industry_trend', 'Unknown'),
                    'industry_strength': industry_trends.get('industry_strength', 'Unknown'),
                    'momentum_alignment': self._assess_momentum_alignment(enhanced_analysis, industry_trends)
                }
            
            # Earnings Insights
            if earnings_analysis:
                combined_insights['earnings_insights'] = {
                    'earnings_quality': earnings_analysis.get('earnings_quality', 'Unknown'),
                    'surprise_consistency': earnings_analysis.get('earnings_surprises', {}).get('surprise_consistency', 0),
                    'growth_trend': self._assess_earnings_growth_trend(earnings_analysis)
                }
            
            # Risk Insights
            if risk_analysis:
                combined_insights['risk_insights'] = {
                    'overall_risk_level': self._calculate_overall_risk_level(risk_analysis),
                    'risk_adjusted_performance': risk_analysis.get('risk_adjusted_returns', {}).get('risk_adjusted_rating', 'Unknown'),
                    'esg_rating': risk_analysis.get('esg_analysis', {}).get('esg_rating', 'Not Rated'),
                    'liquidity_rating': risk_analysis.get('liquidity_risk', {}).get('liquidity_rating', 'Unknown')
                }
            
            return combined_insights
            
        except Exception as e:
            logger.error(f"Error combining analysis: {e}")
            return {}
    
    def _generate_ultimate_recommendation(self, ultimate_analysis: Dict) -> Dict:
        """Generate ultimate investment recommendation using all data sources"""
        try:
            # Start with enhanced recommendation
            enhanced_rec = ultimate_analysis.get('enhanced_recommendation', {})
            base_score = enhanced_rec.get('enhanced_score', 0)
            base_factors = enhanced_rec.get('enhanced_factors', [])
            
            ultimate_score = base_score
            ultimate_factors = base_factors.copy()
            
            # Sector analysis impact
            sector_insights = ultimate_analysis.get('sector_insights', {})
            if sector_insights:
                sector_performance = sector_insights.get('sector_performance', 0)
                sector_ranking = sector_insights.get('sector_ranking', 'Average')
                
                if sector_performance > 10:
                    ultimate_score += 1
                    ultimate_factors.append(f"Outperforming sector by {sector_performance:.1f}%")
                elif sector_performance < -10:
                    ultimate_score -= 1
                    ultimate_factors.append(f"Underperforming sector by {abs(sector_performance):.1f}%")
                
                if sector_ranking == "Top Quartile":
                    ultimate_score += 0.5
                    ultimate_factors.append("Top quartile sector performance")
                elif sector_ranking == "Bottom Quartile":
                    ultimate_score -= 0.5
                    ultimate_factors.append("Bottom quartile sector performance")
            
            # Peer comparison impact
            peer_insights = ultimate_analysis.get('peer_insights', {})
            if peer_insights:
                peer_rank = peer_insights.get('peer_performance_rank', 'Average')
                competitive_position = peer_insights.get('competitive_position', 'Average')
                
                if peer_rank == "Top Performer":
                    ultimate_score += 1
                    ultimate_factors.append("Top performer among peers")
                elif peer_rank == "Underperformer":
                    ultimate_score -= 1
                    ultimate_factors.append("Underperforming peers")
                
                if competitive_position == "Strong":
                    ultimate_score += 0.5
                    ultimate_factors.append("Strong competitive position")
                elif competitive_position == "Weak":
                    ultimate_score -= 0.5
                    ultimate_factors.append("Weak competitive position")
            
            # Industry trends impact
            industry_insights = ultimate_analysis.get('industry_insights', {})
            if industry_insights:
                industry_trend = industry_insights.get('industry_trend', 'Unknown')
                industry_strength = industry_insights.get('industry_strength', 'Unknown')
                
                if industry_trend in ["Strong Uptrend", "Uptrend"]:
                    ultimate_score += 0.5
                    ultimate_factors.append(f"Favorable industry trend: {industry_trend}")
                elif industry_trend in ["Strong Downtrend", "Downtrend"]:
                    ultimate_score -= 0.5
                    ultimate_factors.append(f"Unfavorable industry trend: {industry_trend}")
                
                if industry_strength in ["Very Strong", "Strong"]:
                    ultimate_score += 0.5
                    ultimate_factors.append(f"Strong industry fundamentals: {industry_strength}")
                elif industry_strength in ["Very Weak", "Weak"]:
                    ultimate_score -= 0.5
                    ultimate_factors.append(f"Weak industry fundamentals: {industry_strength}")
            
            # Earnings quality impact
            earnings_insights = ultimate_analysis.get('earnings_insights', {})
            if earnings_insights:
                earnings_quality = earnings_insights.get('earnings_quality', 'Unknown')
                surprise_consistency = earnings_insights.get('surprise_consistency', 0)
                
                if earnings_quality == "High Quality (Stable)":
                    ultimate_score += 1
                    ultimate_factors.append("High quality, stable earnings")
                elif earnings_quality == "Variable Quality (High Volatility)":
                    ultimate_score -= 0.5
                    ultimate_factors.append("Variable earnings quality")
                
                if surprise_consistency > 0.7:
                    ultimate_score += 0.5
                    ultimate_factors.append("Consistent positive earnings surprises")
                elif surprise_consistency < 0.3:
                    ultimate_score -= 0.5
                    ultimate_factors.append("Inconsistent earnings surprises")
            
            # Risk assessment impact
            risk_insights = ultimate_analysis.get('risk_insights', {})
            if risk_insights:
                overall_risk = risk_insights.get('overall_risk_level', 'Moderate')
                risk_adjusted_perf = risk_insights.get('risk_adjusted_performance', 'Average')
                esg_rating = risk_insights.get('esg_rating', 'Not Rated')
                
                if overall_risk == "Low Risk":
                    ultimate_score += 0.5
                    ultimate_factors.append("Low overall risk profile")
                elif overall_risk == "High Risk":
                    ultimate_score -= 0.5
                    ultimate_factors.append("High risk profile")
                
                if risk_adjusted_perf in ["Excellent", "Good"]:
                    ultimate_score += 0.5
                    ultimate_factors.append(f"Strong risk-adjusted performance: {risk_adjusted_perf}")
                elif risk_adjusted_perf == "Poor":
                    ultimate_score -= 0.5
                    ultimate_factors.append("Poor risk-adjusted performance")
                
                if esg_rating in ["AAA", "AA", "A"]:
                    ultimate_score += 0.5
                    ultimate_factors.append(f"Strong ESG rating: {esg_rating}")
                elif esg_rating in ["CCC", "CC", "C"]:
                    ultimate_score -= 0.5
                    ultimate_factors.append(f"Weak ESG rating: {esg_rating}")
            
            # Determine ultimate recommendation
            if ultimate_score >= 5:
                ultimate_recommendation = "STRONG BUY"
            elif ultimate_score >= 3:
                ultimate_recommendation = "BUY"
            elif ultimate_score >= 1:
                ultimate_recommendation = "HOLD"
            elif ultimate_score >= -1:
                ultimate_recommendation = "SELL"
            else:
                ultimate_recommendation = "STRONG SELL"
            
            return {
                'ultimate_recommendation': ultimate_recommendation,
                'ultimate_score': ultimate_score,
                'ultimate_factors': ultimate_factors,
                'confidence_level': min(abs(ultimate_score) / 8, 1.0),  # Adjusted for higher max score
                'data_sources_used': [
                    'Traditional Analysis', 'Analyst Ratings', 'Options Flow', 
                    'Institutional Data', 'News Sentiment', 'Advanced Technical',
                    'Sector Analysis', 'Peer Comparison', 'Industry Trends',
                    'Earnings Analysis', 'Earnings Guidance', 'Risk Metrics',
                    'ESG Analysis', 'Liquidity Analysis', 'Correlation Analysis'
                ],
                'analysis_depth': 'Ultimate Comprehensive'
            }
            
        except Exception as e:
            logger.error(f"Error generating ultimate recommendation: {e}")
            return {
                'ultimate_recommendation': 'HOLD',
                'ultimate_score': 0,
                'ultimate_factors': ['Analysis error'],
                'confidence_level': 0.0,
                'data_sources_used': [],
                'analysis_depth': 'Error'
            }
    
    # Helper methods for analysis combination
    def _calculate_sector_ranking(self, sector_analysis: Dict) -> str:
        """Calculate sector ranking"""
        try:
            vs_sector = sector_analysis.get('vs_sector_performance', 0)
            if vs_sector > 15:
                return "Top Quartile"
            elif vs_sector > 5:
                return "Above Average"
            elif vs_sector > -5:
                return "Average"
            elif vs_sector > -15:
                return "Below Average"
            else:
                return "Bottom Quartile"
        except:
            return "Unknown"
    
    def _assess_sector_momentum(self, sector_analysis: Dict) -> str:
        """Assess sector momentum"""
        try:
            vs_sector = sector_analysis.get('vs_sector_performance', 0)
            if vs_sector > 10:
                return "Strong Positive Momentum"
            elif vs_sector > 0:
                return "Positive Momentum"
            elif vs_sector > -10:
                return "Negative Momentum"
            else:
                return "Strong Negative Momentum"
        except:
            return "Unknown"
    
    def _calculate_peer_rank(self, peer_analysis: Dict) -> str:
        """Calculate peer performance rank"""
        try:
            peer_analysis_text = peer_analysis.get('peer_analysis', '')
            if 'Top Quartile' in peer_analysis_text:
                return "Top Performer"
            elif 'Above Average' in peer_analysis_text:
                return "Above Average"
            elif 'Below Average' in peer_analysis_text:
                return "Below Average"
            elif 'Bottom Quartile' in peer_analysis_text:
                return "Underperformer"
            else:
                return "Average"
        except:
            return "Unknown"
    
    def _compare_valuation_to_peers(self, enhanced_analysis: Dict, peer_analysis: Dict) -> str:
        """Compare valuation to peers"""
        try:
            # This is a simplified comparison
            return "Fairly Valued"  # Placeholder
        except:
            return "Unknown"
    
    def _assess_competitive_position(self, peer_analysis: Dict) -> str:
        """Assess competitive position"""
        try:
            peer_analysis_text = peer_analysis.get('peer_analysis', '')
            if 'Top Quartile' in peer_analysis_text:
                return "Strong"
            elif 'Bottom Quartile' in peer_analysis_text:
                return "Weak"
            else:
                return "Average"
        except:
            return "Unknown"
    
    def _assess_momentum_alignment(self, enhanced_analysis: Dict, industry_trends: Dict) -> str:
        """Assess momentum alignment with industry"""
        try:
            # This is a simplified assessment
            return "Aligned"  # Placeholder
        except:
            return "Unknown"
    
    def _assess_earnings_growth_trend(self, earnings_analysis: Dict) -> str:
        """Assess earnings growth trend"""
        try:
            growth_metrics = earnings_analysis.get('growth_metrics', {})
            annual_growth = growth_metrics.get('annual_earnings_growth', 0)
            
            if annual_growth > 20:
                return "Strong Growth"
            elif annual_growth > 10:
                return "Moderate Growth"
            elif annual_growth > 0:
                return "Slow Growth"
            else:
                return "Declining"
        except:
            return "Unknown"
    
    def _calculate_overall_risk_level(self, risk_analysis: Dict) -> str:
        """Calculate overall risk level"""
        try:
            # Combine various risk metrics
            var_metrics = risk_analysis.get('var_metrics', {})
            drawdown_analysis = risk_analysis.get('drawdown_analysis', {})
            volatility_metrics = risk_analysis.get('volatility_metrics', {})
            
            risk_score = 0
            
            # VaR impact
            var_95 = var_metrics.get('var_95_historical', 0)
            if var_95 < -0.05:  # 5% daily VaR
                risk_score += 2
            elif var_95 < -0.03:
                risk_score += 1
            
            # Drawdown impact
            max_drawdown = drawdown_analysis.get('maximum_drawdown', 0)
            if max_drawdown < -0.3:
                risk_score += 2
            elif max_drawdown < -0.2:
                risk_score += 1
            
            # Volatility impact
            annual_vol = volatility_metrics.get('annual_volatility', 0)
            if annual_vol > 0.4:
                risk_score += 1
            
            if risk_score >= 4:
                return "High Risk"
            elif risk_score >= 2:
                return "Moderate Risk"
            else:
                return "Low Risk"
        except:
            return "Unknown"
