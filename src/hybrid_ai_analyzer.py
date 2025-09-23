"""
Hybrid AI Analyzer
Combines OpenAI and Grok AI for comprehensive analysis
"""

import logging
from typing import Dict, Optional
from .ai_analyzer import AIAnalyzer
from .grok_analyzer import GrokAnalyzer
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, GROK_API_KEY

logger = logging.getLogger(__name__)

class HybridAIAnalyzer:
    """Hybrid AI analyzer using both OpenAI and Grok"""
    
    def __init__(self):
        self.openai_analyzer = AIAnalyzer()
        self.grok_analyzer = GrokAnalyzer(GROK_API_KEY)
        self.use_grok = True  # Default to Grok since OpenAI quota is exceeded
    
    def generate_analysis_report(self, stock_data: Dict) -> Dict:
        """Generate analysis using available AI"""
        try:
            if self.use_grok:
                logger.info("Using Grok AI for analysis")
                return self.grok_analyzer.generate_analysis_report(stock_data)
            else:
                logger.info("Using OpenAI for analysis")
                return self.openai_analyzer.generate_analysis_report(stock_data)
        except Exception as e:
            logger.error(f"Error in hybrid AI analysis: {e}")
            # Fallback to Grok if OpenAI fails
            if self.use_grok:
                return self.grok_analyzer.generate_analysis_report(stock_data)
            else:
                return self.openai_analyzer.generate_analysis_report(stock_data)
    
    def generate_investment_thesis(self, stock_data: Dict) -> Dict:
        """Generate investment thesis using available AI"""
        try:
            if self.use_grok:
                logger.info("Using Grok AI for investment thesis")
                return self.grok_analyzer.generate_investment_thesis(stock_data)
            else:
                logger.info("Using OpenAI for investment thesis")
                return self.openai_analyzer.generate_investment_thesis(stock_data)
        except Exception as e:
            logger.error(f"Error in hybrid AI investment thesis: {e}")
            # Fallback to Grok if OpenAI fails
            if self.use_grok:
                return self.grok_analyzer.generate_investment_thesis(stock_data)
            else:
                return self.openai_analyzer.generate_investment_thesis(stock_data)
    
    def generate_risk_assessment(self, stock_data: Dict) -> Dict:
        """Generate risk assessment using available AI"""
        try:
            if self.use_grok:
                logger.info("Using Grok AI for risk assessment")
                return self.grok_analyzer.generate_risk_assessment(stock_data)
            else:
                logger.info("Using OpenAI for risk assessment")
                return self.openai_analyzer.generate_risk_assessment(stock_data)
        except Exception as e:
            logger.error(f"Error in hybrid AI risk assessment: {e}")
            # Fallback to Grok if OpenAI fails
            if self.use_grok:
                return self.grok_analyzer.generate_risk_assessment(stock_data)
            else:
                return self.openai_analyzer.generate_risk_assessment(stock_data)
    
    def set_ai_preference(self, use_grok: bool = True):
        """Set which AI to use primarily"""
        self.use_grok = use_grok
        logger.info(f"AI preference set to: {'Grok' if use_grok else 'OpenAI'}")
    
    def get_ai_status(self) -> Dict:
        """Get status of both AI services"""
        return {
            'grok_available': True,  # Grok is always available
            'openai_available': True,  # OpenAI is available but quota exceeded
            'current_ai': 'Grok' if self.use_grok else 'OpenAI',
            'grok_api_key': 'Configured' if GROK_API_KEY else 'Not configured',
            'openai_api_key': 'Configured' if OPENAI_API_KEY else 'Not configured'
        }
