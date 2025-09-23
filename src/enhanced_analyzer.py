"""
Enhanced Stock Analyzer with Advanced Market Data
Combines traditional analysis with analyst ratings, options flow, and institutional data
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from .stock_analyzer import StockAnalyzer
from .advanced_data_fetcher import AdvancedDataFetcher

logger = logging.getLogger(__name__)

class EnhancedStockAnalyzer(StockAnalyzer):
    """Enhanced stock analyzer with advanced market data"""
    
    def __init__(self):
        super().__init__()
        self.advanced_fetcher = AdvancedDataFetcher()
    
    def analyze_stock_enhanced(self, symbol: str) -> Dict:
        """
        Perform comprehensive enhanced stock analysis
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        """
        try:
            logger.info(f"Starting enhanced analysis for {symbol}")
            
            # Get basic analysis from parent class
            basic_analysis = self.analyze_stock(symbol)
            
            if 'error' in basic_analysis:
                return basic_analysis
            
            # Get advanced market data
            advanced_data = self.advanced_fetcher.get_comprehensive_market_data(symbol)
            
            # Enhance the analysis with advanced data
            enhanced_analysis = self._enhance_analysis_with_advanced_data(basic_analysis, advanced_data)
            
            # Generate enhanced recommendation
            enhanced_recommendation = self._generate_enhanced_recommendation(enhanced_analysis)
            
            # Add enhanced data to results
            enhanced_analysis.update({
                'advanced_market_data': advanced_data,
                'enhanced_recommendation': enhanced_recommendation,
                'analysis_type': 'enhanced_comprehensive'
            })
            
            return enhanced_analysis
            
        except Exception as e:
            logger.error(f"Error in enhanced analysis for {symbol}: {e}")
            return {'error': f'Enhanced analysis failed for {symbol}: {str(e)}'}
    
    def _enhance_analysis_with_advanced_data(self, basic_analysis: Dict, advanced_data: Dict) -> Dict:
        """Enhance basic analysis with advanced market data"""
        try:
            # Add analyst data insights
            analyst_data = advanced_data.get('analyst_data', {})
            if analyst_data:
                basic_analysis['analyst_insights'] = {
                    'consensus_rating': analyst_data.get('consensus_rating', 'N/A'),
                    'consensus_score': analyst_data.get('consensus_score', 0),
                    'price_target_upside': self._calculate_price_target_upside(
                        basic_analysis.get('stock_info', {}).get('current_price', 0),
                        analyst_data.get('average_price_target', 0)
                    ),
                    'analyst_confidence': self._calculate_analyst_confidence(analyst_data)
                }
            
            # Add options flow insights
            options_data = advanced_data.get('options_data', {})
            if options_data:
                basic_analysis['options_insights'] = {
                    'put_call_ratio': options_data.get('put_call_ratio', 0),
                    'options_sentiment': self._interpret_put_call_ratio(options_data.get('put_call_ratio', 0)),
                    'unusual_activity': options_data.get('unusual_calls_count', 0) + options_data.get('unusual_puts_count', 0),
                    'options_flow_signal': self._generate_options_signal(options_data)
                }
            
            # Add institutional insights
            insider_data = advanced_data.get('insider_data', {})
            if insider_data:
                basic_analysis['institutional_insights'] = {
                    'institutional_ownership': insider_data.get('institutional_ownership_pct', 0),
                    'institutional_support': self._assess_institutional_support(insider_data),
                    'smart_money_signal': self._generate_smart_money_signal(insider_data)
                }
            
            # Add sentiment insights
            sentiment_data = advanced_data.get('sentiment_data', {})
            if sentiment_data:
                basic_analysis['sentiment_insights'] = {
                    'news_sentiment': sentiment_data.get('news_sentiment_score', 0),
                    'sentiment_trend': self._interpret_sentiment_score(sentiment_data.get('news_sentiment_score', 0)),
                    'media_buzz': len(sentiment_data.get('latest_news', [])),
                    'sentiment_signal': self._generate_sentiment_signal(sentiment_data)
                }
            
            # Add advanced technical insights
            technical_data = advanced_data.get('advanced_technical', {})
            if technical_data:
                basic_analysis['advanced_technical_insights'] = {
                    'macd_signal': self._interpret_macd(technical_data),
                    'stochastic_signal': self._interpret_stochastic(technical_data),
                    'volume_signal': self._interpret_volume(technical_data),
                    'technical_momentum': self._calculate_technical_momentum(technical_data)
                }
            
            return basic_analysis
            
        except Exception as e:
            logger.error(f"Error enhancing analysis: {e}")
            return basic_analysis
    
    def _generate_enhanced_recommendation(self, enhanced_analysis: Dict) -> Dict:
        """Generate enhanced investment recommendation using all data sources"""
        try:
            # Start with basic recommendation score
            basic_rec = enhanced_analysis.get('recommendation', {})
            base_score = basic_rec.get('score', 0)
            base_factors = basic_rec.get('factors', [])
            
            enhanced_score = base_score
            enhanced_factors = base_factors.copy()
            
            # Analyst data impact
            analyst_insights = enhanced_analysis.get('analyst_insights', {})
            if analyst_insights:
                consensus_score = analyst_insights.get('consensus_score', 3)
                price_target_upside = analyst_insights.get('price_target_upside', 0)
                
                # Adjust score based on analyst consensus
                if consensus_score > 4:
                    enhanced_score += 1
                    enhanced_factors.append(f"Strong analyst consensus: {analyst_insights.get('consensus_rating', 'N/A')}")
                elif consensus_score < 2:
                    enhanced_score -= 1
                    enhanced_factors.append(f"Weak analyst consensus: {analyst_insights.get('consensus_rating', 'N/A')}")
                
                # Price target impact
                if price_target_upside > 20:
                    enhanced_score += 1
                    enhanced_factors.append(f"Significant upside potential: {price_target_upside:.1f}%")
                elif price_target_upside < -20:
                    enhanced_score -= 1
                    enhanced_factors.append(f"Downside risk: {price_target_upside:.1f}%")
            
            # Options flow impact
            options_insights = enhanced_analysis.get('options_insights', {})
            if options_insights:
                put_call_ratio = options_insights.get('put_call_ratio', 0)
                unusual_activity = options_insights.get('unusual_activity', 0)
                
                # Put/call ratio interpretation
                if put_call_ratio < 0.7:  # More calls than puts
                    enhanced_score += 0.5
                    enhanced_factors.append("Bullish options flow (low put/call ratio)")
                elif put_call_ratio > 1.3:  # More puts than calls
                    enhanced_score -= 0.5
                    enhanced_factors.append("Bearish options flow (high put/call ratio)")
                
                # Unusual activity
                if unusual_activity > 5:
                    enhanced_factors.append(f"High unusual options activity: {unusual_activity} contracts")
            
            # Institutional data impact
            institutional_insights = enhanced_analysis.get('institutional_insights', {})
            if institutional_insights:
                institutional_ownership = institutional_insights.get('institutional_ownership', 0)
                
                if institutional_ownership > 70:
                    enhanced_score += 0.5
                    enhanced_factors.append(f"High institutional ownership: {institutional_ownership:.1f}%")
                elif institutional_ownership < 30:
                    enhanced_score -= 0.5
                    enhanced_factors.append(f"Low institutional ownership: {institutional_ownership:.1f}%")
            
            # Sentiment impact
            sentiment_insights = enhanced_analysis.get('sentiment_insights', {})
            if sentiment_insights:
                sentiment_score = sentiment_insights.get('news_sentiment', 0)
                
                if sentiment_score > 0.3:
                    enhanced_score += 0.5
                    enhanced_factors.append("Positive news sentiment")
                elif sentiment_score < -0.3:
                    enhanced_score -= 0.5
                    enhanced_factors.append("Negative news sentiment")
            
            # Advanced technical impact
            technical_insights = enhanced_analysis.get('advanced_technical_insights', {})
            if technical_insights:
                technical_momentum = technical_insights.get('technical_momentum', 0)
                
                if technical_momentum > 0.7:
                    enhanced_score += 0.5
                    enhanced_factors.append("Strong technical momentum")
                elif technical_momentum < -0.7:
                    enhanced_score -= 0.5
                    enhanced_factors.append("Weak technical momentum")
            
            # Determine enhanced recommendation
            if enhanced_score >= 4:
                enhanced_recommendation = "STRONG BUY"
            elif enhanced_score >= 2:
                enhanced_recommendation = "BUY"
            elif enhanced_score >= -1:
                enhanced_recommendation = "HOLD"
            elif enhanced_score >= -3:
                enhanced_recommendation = "SELL"
            else:
                enhanced_recommendation = "STRONG SELL"
            
            return {
                'enhanced_recommendation': enhanced_recommendation,
                'enhanced_score': enhanced_score,
                'enhanced_factors': enhanced_factors,
                'confidence_level': min(abs(enhanced_score) / 6, 1.0),  # Adjusted for higher max score
                'data_sources_used': [
                    'Traditional Analysis', 'Analyst Ratings', 'Options Flow', 
                    'Institutional Data', 'News Sentiment', 'Advanced Technical'
                ]
            }
            
        except Exception as e:
            logger.error(f"Error generating enhanced recommendation: {e}")
            return {
                'enhanced_recommendation': 'HOLD',
                'enhanced_score': 0,
                'enhanced_factors': ['Analysis error'],
                'confidence_level': 0.0,
                'data_sources_used': []
            }
    
    # Helper methods for data interpretation
    def _calculate_price_target_upside(self, current_price: float, target_price: float) -> float:
        """Calculate upside potential from price target"""
        if current_price > 0 and target_price > 0:
            return ((target_price - current_price) / current_price) * 100
        return 0
    
    def _calculate_analyst_confidence(self, analyst_data: Dict) -> float:
        """Calculate analyst confidence based on consensus and distribution"""
        total_analysts = analyst_data.get('total_analysts', 0)
        rating_dist = analyst_data.get('rating_distribution', {})
        
        if total_analysts == 0:
            return 0.0
        
        # Higher confidence if more analysts agree
        max_rating_count = max(rating_dist.values()) if rating_dist else 0
        return max_rating_count / total_analysts
    
    def _interpret_put_call_ratio(self, ratio: float) -> str:
        """Interpret put/call ratio"""
        if ratio < 0.7:
            return "Bullish (More calls than puts)"
        elif ratio > 1.3:
            return "Bearish (More puts than calls)"
        else:
            return "Neutral"
    
    def _generate_options_signal(self, options_data: Dict) -> str:
        """Generate options flow signal"""
        put_call_ratio = options_data.get('put_call_ratio', 1)
        unusual_activity = options_data.get('unusual_calls_count', 0) + options_data.get('unusual_puts_count', 0)
        
        if put_call_ratio < 0.7 and unusual_activity > 3:
            return "Strong Bullish"
        elif put_call_ratio > 1.3 and unusual_activity > 3:
            return "Strong Bearish"
        elif put_call_ratio < 0.7:
            return "Bullish"
        elif put_call_ratio > 1.3:
            return "Bearish"
        else:
            return "Neutral"
    
    def _assess_institutional_support(self, insider_data: Dict) -> str:
        """Assess institutional support level"""
        ownership = insider_data.get('institutional_ownership_pct', 0)
        
        if ownership > 70:
            return "Very High"
        elif ownership > 50:
            return "High"
        elif ownership > 30:
            return "Moderate"
        else:
            return "Low"
    
    def _generate_smart_money_signal(self, insider_data: Dict) -> str:
        """Generate smart money signal"""
        ownership = insider_data.get('institutional_ownership_pct', 0)
        num_institutions = insider_data.get('number_of_institutions', 0)
        
        if ownership > 60 and num_institutions > 100:
            return "Strong Smart Money Support"
        elif ownership > 40 and num_institutions > 50:
            return "Moderate Smart Money Support"
        else:
            return "Limited Smart Money Support"
    
    def _interpret_sentiment_score(self, score: float) -> str:
        """Interpret sentiment score"""
        if score > 0.3:
            return "Very Positive"
        elif score > 0.1:
            return "Positive"
        elif score > -0.1:
            return "Neutral"
        elif score > -0.3:
            return "Negative"
        else:
            return "Very Negative"
    
    def _generate_sentiment_signal(self, sentiment_data: Dict) -> str:
        """Generate sentiment signal"""
        score = sentiment_data.get('news_sentiment_score', 0)
        buzz = len(sentiment_data.get('latest_news', []))
        
        if score > 0.3 and buzz > 5:
            return "Strong Positive Buzz"
        elif score < -0.3 and buzz > 5:
            return "Strong Negative Buzz"
        elif score > 0.1:
            return "Positive Sentiment"
        elif score < -0.1:
            return "Negative Sentiment"
        else:
            return "Neutral Sentiment"
    
    def _interpret_macd(self, technical_data: Dict) -> str:
        """Interpret MACD signal"""
        macd = technical_data.get('macd', 0)
        signal = technical_data.get('macd_signal', 0)
        histogram = technical_data.get('macd_histogram', 0)
        
        if macd > signal and histogram > 0:
            return "Bullish MACD"
        elif macd < signal and histogram < 0:
            return "Bearish MACD"
        else:
            return "Neutral MACD"
    
    def _interpret_stochastic(self, technical_data: Dict) -> str:
        """Interpret Stochastic Oscillator"""
        k = technical_data.get('stochastic_k', 50)
        d = technical_data.get('stochastic_d', 50)
        
        if k > 80 and d > 80:
            return "Overbought"
        elif k < 20 and d < 20:
            return "Oversold"
        elif k > d:
            return "Bullish Momentum"
        else:
            return "Bearish Momentum"
    
    def _interpret_volume(self, technical_data: Dict) -> str:
        """Interpret volume signal"""
        volume_ratio = technical_data.get('volume_ratio', 1)
        
        if volume_ratio > 2:
            return "Very High Volume"
        elif volume_ratio > 1.5:
            return "High Volume"
        elif volume_ratio < 0.5:
            return "Low Volume"
        else:
            return "Normal Volume"
    
    def _calculate_technical_momentum(self, technical_data: Dict) -> float:
        """Calculate overall technical momentum score"""
        macd_signal = 1 if technical_data.get('macd', 0) > technical_data.get('macd_signal', 0) else -1
        stochastic_signal = 1 if technical_data.get('stochastic_k', 50) > 50 else -1
        volume_signal = 1 if technical_data.get('volume_ratio', 1) > 1.2 else 0
        
        return (macd_signal + stochastic_signal + volume_signal) / 3
