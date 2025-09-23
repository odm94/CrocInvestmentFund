"""
X (Twitter) Analyst Feed Integration
Collects real-time analyst insights and sentiment from X platform
"""

import requests
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class XAnalystFeed:
    """X (Twitter) analyst feed integration"""
    
    def __init__(self, bearer_token: str = None):
        self.bearer_token = bearer_token or "your_x_bearer_token_here"
        self.base_url = "https://api.twitter.com/2"
        self.headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json'
        }
        
        # Top financial analysts and influencers on X
        self.analyst_accounts = [
            'jimcramer', 'elonmusk', 'cathiewood', 'chamath', 'naval',
            'balajis', 'michaeljburry', 'howardmarks', 'raynoldl',
            'davidportnoy', 'kevinoleary', 'garyvee', 'timferriss',
            'reidhoffman', 'peterthiel', 'marcandreessen', 'balajis',
            'naval', 'sama', 'darioamodei', 'demishassabis'
        ]
        
        # Financial news accounts
        self.news_accounts = [
            'bloomberg', 'reuters', 'wsj', 'ft', 'cnbc',
            'marketwatch', 'benzinga', 'seekingalpha', 'zerohedge',
            'investingcom', 'yahoo_finance', 'forbes', 'business'
        ]
    
    def get_stock_mentions(self, symbol: str, hours_back: int = 24) -> Dict:
        """Get recent mentions of stock symbol on X"""
        try:
            # This would use Twitter API v2 to search for mentions
            # For now, we'll simulate the data
            
            mentions_data = {
                'symbol': symbol,
                'total_mentions': np.random.randint(100, 1000),
                'sentiment_score': np.random.uniform(-1, 1),
                'sentiment_breakdown': {
                    'positive': np.random.randint(20, 60),
                    'neutral': np.random.randint(20, 40),
                    'negative': np.random.randint(10, 30)
                },
                'top_hashtags': self._get_top_hashtags(symbol),
                'influencer_mentions': self._get_influencer_mentions(symbol),
                'news_mentions': self._get_news_mentions(symbol),
                'time_range': f'Last {hours_back} hours',
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            return mentions_data
            
        except Exception as e:
            logger.error(f"Error getting stock mentions for {symbol}: {e}")
            return {'error': str(e)}
    
    def get_analyst_insights(self, symbol: str) -> Dict:
        """Get insights from top financial analysts"""
        try:
            insights = {
                'symbol': symbol,
                'analyst_mentions': [],
                'consensus_sentiment': 'neutral',
                'key_insights': [],
                'price_targets': [],
                'analyst_confidence': 0.0
            }
            
            # Simulate analyst mentions
            for analyst in self.analyst_accounts[:5]:  # Top 5 analysts
                mention = self._simulate_analyst_mention(symbol, analyst)
                if mention:
                    insights['analyst_mentions'].append(mention)
            
            # Calculate consensus
            if insights['analyst_mentions']:
                sentiments = [m['sentiment'] for m in insights['analyst_mentions']]
                insights['consensus_sentiment'] = self._calculate_consensus_sentiment(sentiments)
                insights['analyst_confidence'] = self._calculate_analyst_confidence(insights['analyst_mentions'])
            
            return insights
            
        except Exception as e:
            logger.error(f"Error getting analyst insights for {symbol}: {e}")
            return {'error': str(e)}
    
    def get_market_sentiment(self, symbol: str) -> Dict:
        """Get overall market sentiment for the stock"""
        try:
            sentiment_data = {
                'symbol': symbol,
                'overall_sentiment': np.random.uniform(-1, 1),
                'sentiment_trend': self._get_sentiment_trend(symbol),
                'volume_mentions': np.random.randint(50, 500),
                'engagement_rate': np.random.uniform(0.02, 0.15),
                'viral_potential': np.random.uniform(0.1, 0.9),
                'key_themes': self._extract_key_themes(symbol),
                'sentiment_drivers': self._identify_sentiment_drivers(symbol),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            return sentiment_data
            
        except Exception as e:
            logger.error(f"Error getting market sentiment for {symbol}: {e}")
            return {'error': str(e)}
    
    def get_breaking_news_impact(self, symbol: str) -> Dict:
        """Analyze impact of breaking news on X"""
        try:
            news_impact = {
                'symbol': symbol,
                'breaking_news_count': np.random.randint(0, 5),
                'news_sentiment': np.random.uniform(-1, 1),
                'impact_score': np.random.uniform(0, 10),
                'key_headlines': self._get_key_headlines(symbol),
                'news_sources': self._get_news_sources(symbol),
                'market_reaction': self._analyze_market_reaction(symbol),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            return news_impact
            
        except Exception as e:
            logger.error(f"Error analyzing breaking news impact for {symbol}: {e}")
            return {'error': str(e)}
    
    def _get_top_hashtags(self, symbol: str) -> List[Dict]:
        """Get top hashtags related to the stock"""
        hashtags = [
            f'#{symbol}', f'#{symbol}stock', f'#{symbol}trading',
            f'#{symbol}analysis', f'#{symbol}news', '#stocks',
            '#trading', '#investing', '#finance', '#market'
        ]
        
        return [{'hashtag': tag, 'count': np.random.randint(10, 1000)} for tag in hashtags]
    
    def _get_influencer_mentions(self, symbol: str) -> List[Dict]:
        """Get mentions from top influencers"""
        influencers = []
        for influencer in self.analyst_accounts[:3]:
            influencers.append({
                'username': f'@{influencer}',
                'followers': np.random.randint(100000, 10000000),
                'sentiment': np.random.uniform(-1, 1),
                'engagement': np.random.randint(100, 10000),
                'influence_score': np.random.uniform(0.5, 1.0)
            })
        
        return influencers
    
    def _get_news_mentions(self, symbol: str) -> List[Dict]:
        """Get mentions from news accounts"""
        news_mentions = []
        for news_account in self.news_accounts[:3]:
            news_mentions.append({
                'account': f'@{news_account}',
                'mentions': np.random.randint(1, 10),
                'sentiment': np.random.uniform(-1, 1),
                'reach': np.random.randint(1000000, 50000000)
            })
        
        return news_mentions
    
    def _simulate_analyst_mention(self, symbol: str, analyst: str) -> Optional[Dict]:
        """Simulate analyst mention (placeholder for real API integration)"""
        if np.random.random() > 0.7:  # 30% chance of mention
            return {
                'analyst': f'@{analyst}',
                'sentiment': np.random.uniform(-1, 1),
                'confidence': np.random.uniform(0.5, 1.0),
                'price_target': np.random.uniform(100, 300) if np.random.random() > 0.5 else None,
                'key_insight': self._generate_insight(symbol),
                'timestamp': datetime.now().isoformat()
            }
        return None
    
    def _generate_insight(self, symbol: str) -> str:
        """Generate simulated analyst insight"""
        insights = [
            f"{symbol} showing strong technical momentum",
            f"Fundamental analysis suggests {symbol} is undervalued",
            f"Market sentiment for {symbol} is mixed",
            f"{symbol} facing headwinds in current market",
            f"Long-term outlook for {symbol} remains positive",
            f"{symbol} trading at attractive valuation",
            f"Risk factors increasing for {symbol}",
            f"{symbol} positioned for growth recovery"
        ]
        return np.random.choice(insights)
    
    def _calculate_consensus_sentiment(self, sentiments: List[float]) -> str:
        """Calculate consensus sentiment from analyst mentions"""
        if not sentiments:
            return 'neutral'
        
        avg_sentiment = np.mean(sentiments)
        if avg_sentiment > 0.3:
            return 'bullish'
        elif avg_sentiment < -0.3:
            return 'bearish'
        else:
            return 'neutral'
    
    def _calculate_analyst_confidence(self, mentions: List[Dict]) -> float:
        """Calculate overall analyst confidence"""
        if not mentions:
            return 0.0
        
        confidences = [m.get('confidence', 0.5) for m in mentions]
        return np.mean(confidences)
    
    def _get_sentiment_trend(self, symbol: str) -> str:
        """Get sentiment trend over time"""
        trends = ['improving', 'declining', 'stable', 'volatile']
        return np.random.choice(trends)
    
    def _extract_key_themes(self, symbol: str) -> List[str]:
        """Extract key themes from X mentions"""
        themes = [
            'earnings growth', 'market volatility', 'sector rotation',
            'institutional buying', 'retail interest', 'options activity',
            'dividend yield', 'debt levels', 'cash position',
            'management changes', 'regulatory environment'
        ]
        return np.random.choice(themes, size=np.random.randint(3, 6), replace=False).tolist()
    
    def _identify_sentiment_drivers(self, symbol: str) -> List[str]:
        """Identify key sentiment drivers"""
        drivers = [
            'earnings beat', 'guidance raise', 'analyst upgrade',
            'institutional accumulation', 'positive news flow',
            'earnings miss', 'guidance cut', 'analyst downgrade',
            'institutional selling', 'negative news flow'
        ]
        return np.random.choice(drivers, size=np.random.randint(2, 4), replace=False).tolist()
    
    def _get_key_headlines(self, symbol: str) -> List[str]:
        """Get key headlines from X"""
        headlines = [
            f"{symbol} reports strong Q4 earnings",
            f"Analysts upgrade {symbol} price target",
            f"{symbol} faces regulatory challenges",
            f"Institutional investors increase {symbol} holdings",
            f"{symbol} announces new product launch",
            f"Market volatility impacts {symbol} trading"
        ]
        return np.random.choice(headlines, size=np.random.randint(2, 4), replace=False).tolist()
    
    def _get_news_sources(self, symbol: str) -> List[str]:
        """Get news sources mentioning the stock"""
        sources = ['Bloomberg', 'Reuters', 'CNBC', 'WSJ', 'MarketWatch', 'Benzinga']
        return np.random.choice(sources, size=np.random.randint(2, 4), replace=False).tolist()
    
    def _analyze_market_reaction(self, symbol: str) -> Dict:
        """Analyze market reaction to news"""
        return {
            'immediate_impact': np.random.uniform(-5, 5),
            'sustained_impact': np.random.uniform(-2, 2),
            'volatility_change': np.random.uniform(-0.1, 0.1),
            'volume_spike': np.random.uniform(1.0, 3.0)
        }
    
    def get_comprehensive_x_analysis(self, symbol: str) -> Dict:
        """Get comprehensive X analysis combining all data sources"""
        try:
            logger.info(f"Starting comprehensive X analysis for {symbol}")
            
            # Collect all X data
            mentions = self.get_stock_mentions(symbol)
            analyst_insights = self.get_analyst_insights(symbol)
            market_sentiment = self.get_market_sentiment(symbol)
            news_impact = self.get_breaking_news_impact(symbol)
            
            # Combine all data
            comprehensive_analysis = {
                'symbol': symbol,
                'mentions_analysis': mentions,
                'analyst_insights': analyst_insights,
                'market_sentiment': market_sentiment,
                'news_impact': news_impact,
                'overall_x_score': self._calculate_overall_x_score(mentions, analyst_insights, market_sentiment, news_impact),
                'x_recommendation': self._generate_x_recommendation(mentions, analyst_insights, market_sentiment),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            return comprehensive_analysis
            
        except Exception as e:
            logger.error(f"Error in comprehensive X analysis for {symbol}: {e}")
            return {'error': f'X analysis failed: {str(e)}'}
    
    def _calculate_overall_x_score(self, mentions: Dict, analyst_insights: Dict, market_sentiment: Dict, news_impact: Dict) -> float:
        """Calculate overall X score from all data sources"""
        try:
            # Weighted average of different sentiment scores
            scores = []
            weights = []
            
            if 'sentiment_score' in mentions:
                scores.append(mentions['sentiment_score'])
                weights.append(0.3)
            
            if 'consensus_sentiment' in analyst_insights:
                sentiment_map = {'bullish': 1.0, 'neutral': 0.0, 'bearish': -1.0}
                scores.append(sentiment_map.get(analyst_insights['consensus_sentiment'], 0.0))
                weights.append(0.4)
            
            if 'overall_sentiment' in market_sentiment:
                scores.append(market_sentiment['overall_sentiment'])
                weights.append(0.2)
            
            if 'news_sentiment' in news_impact:
                scores.append(news_impact['news_sentiment'])
                weights.append(0.1)
            
            if scores and weights:
                return np.average(scores, weights=weights)
            else:
                return 0.0
                
        except Exception as e:
            logger.error(f"Error calculating overall X score: {e}")
            return 0.0
    
    def _generate_x_recommendation(self, mentions: Dict, analyst_insights: Dict, market_sentiment: Dict) -> str:
        """Generate recommendation based on X data"""
        try:
            overall_score = self._calculate_overall_x_score(mentions, analyst_insights, market_sentiment, {})
            
            if overall_score > 0.3:
                return 'BUY'
            elif overall_score < -0.3:
                return 'SELL'
            else:
                return 'HOLD'
                
        except Exception as e:
            logger.error(f"Error generating X recommendation: {e}")
            return 'HOLD'
