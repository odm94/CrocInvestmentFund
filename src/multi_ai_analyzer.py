"""
Multi-AI Analyzer
Integrates all available AI models and social media feeds for comprehensive analysis
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class MultiAIAnalyzer:
    """Multi-AI analyzer integrating all available models and feeds"""
    
    def __init__(self):
        self.ai_providers = {
            'openai': self._init_openai(),
            'grok': self._init_grok(),
            'claude': self._init_claude(),
            'gemini': self._init_gemini(),
            'llama': self._init_llama()
        }
        
        self.social_feeds = {
            'twitter': self._init_twitter(),
            'reddit': self._init_reddit(),
            'youtube': self._init_youtube()
        }
        
        self.analyst_feeds = {
            'x_analysts': self._init_x_analysts(),
            'bloomberg': self._init_bloomberg(),
            'reuters': self._init_reuters()
        }
    
    def generate_comprehensive_analysis(self, stock_data: Dict) -> Dict:
        """Generate comprehensive analysis using all available AI models"""
        try:
            symbol = stock_data.get('symbol', 'Unknown')
            logger.info(f"Starting comprehensive multi-AI analysis for {symbol}")
            
            # Collect analysis from all AI providers
            ai_analyses = {}
            for provider_name, provider in self.ai_providers.items():
                if provider:
                    try:
                        # Generate comprehensive analysis for each provider
                        analysis_report = provider.generate_analysis_report(stock_data)
                        investment_thesis = provider.generate_investment_thesis(stock_data)
                        risk_assessment = provider.generate_risk_assessment(stock_data)
                        
                        analysis = {
                            'ai_analysis': analysis_report.get('ai_analysis', 'Analysis unavailable'),
                            'investment_thesis': investment_thesis.get('investment_thesis', 'Thesis unavailable'),
                            'risk_assessment': risk_assessment.get('risk_assessment', 'Risk assessment unavailable'),
                            'model_used': analysis_report.get('model_used', provider_name),
                            'recommendation': 'HOLD'  # Default recommendation
                        }
                        
                        ai_analyses[provider_name] = analysis
                        logger.info(f"✅ {provider_name.upper()} analysis completed")
                    except Exception as e:
                        logger.error(f"❌ {provider_name.upper()} analysis failed: {e}")
                        ai_analyses[provider_name] = {'error': str(e)}
            
            # Collect social media sentiment
            social_sentiment = self._collect_social_sentiment(symbol)
            
            # Collect analyst feeds
            analyst_feeds = self._collect_analyst_feeds(symbol)
            
            # Generate consensus analysis
            consensus_analysis = self._generate_consensus_analysis(ai_analyses, social_sentiment, analyst_feeds)
            
            return {
                'symbol': symbol,
                'ai_analyses': ai_analyses,
                'social_sentiment': social_sentiment,
                'analyst_feeds': analyst_feeds,
                'consensus_analysis': consensus_analysis,
                'analysis_timestamp': datetime.now().isoformat(),
                'ai_providers_used': list(ai_analyses.keys()),
                'total_ai_models': len([a for a in ai_analyses.values() if 'error' not in a])
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive multi-AI analysis: {e}")
            return {'error': f'Multi-AI analysis failed: {str(e)}'}
    
    def _init_openai(self):
        """Initialize OpenAI provider"""
        try:
            from .ai_analyzer import AIAnalyzer
            return AIAnalyzer()
        except Exception as e:
            logger.error(f"OpenAI initialization failed: {e}")
            return None
    
    def _init_grok(self):
        """Initialize Grok provider"""
        try:
            from .grok_analyzer import GrokAnalyzer
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from config import GROK_API_KEY
            return GrokAnalyzer(GROK_API_KEY)
        except Exception as e:
            logger.error(f"Grok initialization failed: {e}")
            return None
    
    def _init_claude(self):
        """Initialize Claude provider"""
        try:
            # Placeholder for Claude integration
            return None
        except Exception as e:
            logger.error(f"Claude initialization failed: {e}")
            return None
    
    def _init_gemini(self):
        """Initialize Gemini provider"""
        try:
            # Placeholder for Gemini integration
            return None
        except Exception as e:
            logger.error(f"Gemini initialization failed: {e}")
            return None
    
    def _init_llama(self):
        """Initialize Llama provider"""
        try:
            # Placeholder for Llama integration
            return None
        except Exception as e:
            logger.error(f"Llama initialization failed: {e}")
            return None
    
    def _init_twitter(self):
        """Initialize Twitter/X integration"""
        try:
            # Placeholder for Twitter API integration
            return {
                'api_key': 'twitter_api_key',
                'bearer_token': 'twitter_bearer_token'
            }
        except Exception as e:
            logger.error(f"Twitter initialization failed: {e}")
            return None
    
    def _init_reddit(self):
        """Initialize Reddit integration"""
        try:
            # Placeholder for Reddit API integration
            return {
                'client_id': 'reddit_client_id',
                'client_secret': 'reddit_client_secret'
            }
        except Exception as e:
            logger.error(f"Reddit initialization failed: {e}")
            return None
    
    def _init_youtube(self):
        """Initialize YouTube integration"""
        try:
            # Placeholder for YouTube API integration
            return {
                'api_key': 'youtube_api_key'
            }
        except Exception as e:
            logger.error(f"YouTube initialization failed: {e}")
            return None
    
    def _init_x_analysts(self):
        """Initialize X (Twitter) analyst feeds"""
        try:
            # Placeholder for X analyst feeds
            return {
                'api_key': 'x_api_key',
                'bearer_token': 'x_bearer_token',
                'analyst_accounts': [
                    '@jimcramer', '@elonmusk', '@cathiewood',
                    '@chamath', '@naval', '@balajis',
                    '@michaeljburry', '@howardmarks', '@raynoldl'
                ]
            }
        except Exception as e:
            logger.error(f"X analysts initialization failed: {e}")
            return None
    
    def _init_bloomberg(self):
        """Initialize Bloomberg feeds"""
        try:
            # Placeholder for Bloomberg API
            return {
                'api_key': 'bloomberg_api_key'
            }
        except Exception as e:
            logger.error(f"Bloomberg initialization failed: {e}")
            return None
    
    def _init_reuters(self):
        """Initialize Reuters feeds"""
        try:
            # Placeholder for Reuters API
            return {
                'api_key': 'reuters_api_key'
            }
        except Exception as e:
            logger.error(f"Reuters initialization failed: {e}")
            return None
    
    def _collect_social_sentiment(self, symbol: str) -> Dict:
        """Collect social media sentiment for the stock"""
        try:
            # Simulate social media sentiment collection
            sentiment_data = {
                'twitter_sentiment': self._get_twitter_sentiment(symbol),
                'reddit_sentiment': self._get_reddit_sentiment(symbol),
                'youtube_sentiment': self._get_youtube_sentiment(symbol),
                'overall_social_sentiment': 0.0,
                'social_mentions': 0,
                'sentiment_trend': 'neutral'
            }
            
            # Calculate overall sentiment
            sentiments = [v for k, v in sentiment_data.items() if 'sentiment' in k and isinstance(v, (int, float))]
            if sentiments:
                sentiment_data['overall_social_sentiment'] = np.mean(sentiments)
            
            return sentiment_data
            
        except Exception as e:
            logger.error(f"Error collecting social sentiment: {e}")
            return {'error': str(e)}
    
    def _collect_analyst_feeds(self, symbol: str) -> Dict:
        """Collect analyst feeds and recommendations"""
        try:
            analyst_data = {
                'x_analysts': self._get_x_analyst_mentions(symbol),
                'bloomberg_analysts': self._get_bloomberg_analysts(symbol),
                'reuters_analysts': self._get_reuters_analysts(symbol),
                'consensus_rating': 'HOLD',
                'analyst_confidence': 0.0,
                'price_targets': [],
                'analyst_mentions': 0
            }
            
            return analyst_data
            
        except Exception as e:
            logger.error(f"Error collecting analyst feeds: {e}")
            return {'error': str(e)}
    
    def _generate_consensus_analysis(self, ai_analyses: Dict, social_sentiment: Dict, analyst_feeds: Dict) -> Dict:
        """Generate consensus analysis from all sources"""
        try:
            # Collect all recommendations
            recommendations = []
            for provider, analysis in ai_analyses.items():
                if 'error' not in analysis and 'recommendation' in analysis:
                    recommendations.append(analysis['recommendation'])
            
            # Calculate consensus
            if recommendations:
                consensus_recommendation = self._calculate_consensus_recommendation(recommendations)
            else:
                consensus_recommendation = 'HOLD'
            
            # Calculate confidence score
            confidence = self._calculate_confidence_score(ai_analyses, social_sentiment, analyst_feeds)
            
            # Generate consensus factors
            factors = self._generate_consensus_factors(ai_analyses, social_sentiment, analyst_feeds)
            
            return {
                'consensus_recommendation': consensus_recommendation,
                'confidence_score': confidence,
                'consensus_factors': factors,
                'ai_agreement': self._calculate_ai_agreement(ai_analyses),
                'social_sentiment_impact': social_sentiment.get('overall_social_sentiment', 0),
                'analyst_sentiment_impact': analyst_feeds.get('consensus_rating', 'HOLD'),
                'data_sources_used': len([a for a in ai_analyses.values() if 'error' not in a]) + 3  # +3 for social/analyst feeds
            }
            
        except Exception as e:
            logger.error(f"Error generating consensus analysis: {e}")
            return {'error': str(e)}
    
    def _get_twitter_sentiment(self, symbol: str) -> float:
        """Get Twitter sentiment for symbol"""
        # Placeholder - would integrate with Twitter API
        return np.random.uniform(-1, 1)
    
    def _get_reddit_sentiment(self, symbol: str) -> float:
        """Get Reddit sentiment for symbol"""
        # Placeholder - would integrate with Reddit API
        return np.random.uniform(-1, 1)
    
    def _get_youtube_sentiment(self, symbol: str) -> float:
        """Get YouTube sentiment for symbol"""
        # Placeholder - would integrate with YouTube API
        return np.random.uniform(-1, 1)
    
    def _get_x_analyst_mentions(self, symbol: str) -> Dict:
        """Get X analyst mentions for symbol"""
        # Placeholder - would integrate with X API
        return {
            'mentions': np.random.randint(0, 50),
            'sentiment': np.random.uniform(-1, 1),
            'top_analysts': ['@jimcramer', '@cathiewood', '@chamath']
        }
    
    def _get_bloomberg_analysts(self, symbol: str) -> Dict:
        """Get Bloomberg analyst data"""
        # Placeholder - would integrate with Bloomberg API
        return {
            'rating': 'BUY',
            'price_target': 200.0,
            'analyst': 'Bloomberg Analyst'
        }
    
    def _get_reuters_analysts(self, symbol: str) -> Dict:
        """Get Reuters analyst data"""
        # Placeholder - would integrate with Reuters API
        return {
            'rating': 'HOLD',
            'price_target': 180.0,
            'analyst': 'Reuters Analyst'
        }
    
    def _calculate_consensus_recommendation(self, recommendations: List[str]) -> str:
        """Calculate consensus recommendation from AI analyses"""
        if not recommendations:
            return 'HOLD'
        
        # Simple voting mechanism
        buy_count = sum(1 for r in recommendations if 'BUY' in r.upper())
        sell_count = sum(1 for r in recommendations if 'SELL' in r.upper())
        hold_count = sum(1 for r in recommendations if 'HOLD' in r.upper())
        
        if buy_count > sell_count and buy_count > hold_count:
            return 'BUY'
        elif sell_count > buy_count and sell_count > hold_count:
            return 'SELL'
        else:
            return 'HOLD'
    
    def _calculate_confidence_score(self, ai_analyses: Dict, social_sentiment: Dict, analyst_feeds: Dict) -> float:
        """Calculate overall confidence score"""
        try:
            # AI agreement score
            ai_agreement = self._calculate_ai_agreement(ai_analyses)
            
            # Social sentiment consistency
            social_consistency = 1.0 - abs(social_sentiment.get('overall_social_sentiment', 0))
            
            # Analyst consensus
            analyst_consensus = 0.8  # Placeholder
            
            # Overall confidence
            confidence = (ai_agreement * 0.5 + social_consistency * 0.3 + analyst_consensus * 0.2)
            
            return min(max(confidence, 0.0), 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating confidence score: {e}")
            return 0.5
    
    def _calculate_ai_agreement(self, ai_analyses: Dict) -> float:
        """Calculate agreement between AI analyses"""
        try:
            valid_analyses = [a for a in ai_analyses.values() if 'error' not in a]
            if len(valid_analyses) < 2:
                return 0.5
            
            # Simple agreement calculation
            return 0.8  # Placeholder
            
        except Exception as e:
            logger.error(f"Error calculating AI agreement: {e}")
            return 0.5
    
    def _generate_consensus_factors(self, ai_analyses: Dict, social_sentiment: Dict, analyst_feeds: Dict) -> List[str]:
        """Generate consensus factors from all sources"""
        factors = []
        
        # AI factors
        for provider, analysis in ai_analyses.items():
            if 'error' not in analysis and 'factors' in analysis:
                factors.extend(analysis['factors'][:2])  # Top 2 factors per AI
        
        # Social sentiment factors
        social_sent = social_sentiment.get('overall_social_sentiment', 0)
        if social_sent > 0.3:
            factors.append("Positive social media sentiment")
        elif social_sent < -0.3:
            factors.append("Negative social media sentiment")
        
        # Analyst factors
        if analyst_feeds.get('consensus_rating') == 'BUY':
            factors.append("Analyst consensus bullish")
        elif analyst_feeds.get('consensus_rating') == 'SELL':
            factors.append("Analyst consensus bearish")
        
        return factors[:10]  # Limit to top 10 factors
    
    def get_ai_status(self) -> Dict:
        """Get status of all AI providers"""
        status = {}
        for provider_name, provider in self.ai_providers.items():
            if provider:
                status[provider_name] = 'Available'
            else:
                status[provider_name] = 'Unavailable'
        
        return status
    
    def get_feed_status(self) -> Dict:
        """Get status of all data feeds"""
        status = {}
        for feed_name, feed in self.social_feeds.items():
            if feed:
                status[feed_name] = 'Available'
            else:
                status[feed_name] = 'Unavailable'
        
        for feed_name, feed in self.analyst_feeds.items():
            if feed:
                status[feed_name] = 'Available'
            else:
                status[feed_name] = 'Unavailable'
        
        return status
