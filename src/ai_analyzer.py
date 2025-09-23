"""
AI-Powered Stock Analysis using OpenAI GPT
"""

import openai
import json
from typing import Dict, List, Optional
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE

logger = logging.getLogger(__name__)

class AIAnalyzer:
    """AI-powered stock analysis using OpenAI GPT models"""
    
    def __init__(self):
        # Set up OpenAI client
        openai.api_key = OPENAI_API_KEY
        self.model = DEFAULT_MODEL
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
    
    def generate_analysis_report(self, stock_data: Dict) -> Dict:
        """
        Generate comprehensive AI analysis report
        
        Args:
            stock_data: Complete stock analysis data
        """
        try:
            # Prepare the prompt
            prompt = self._create_analysis_prompt(stock_data)
            
            # Call OpenAI API
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional financial analyst with expertise in stock valuation and investment analysis. Provide detailed, accurate, and actionable insights."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the response
            ai_analysis = response.choices[0].message.content
            
            return {
                'ai_analysis': ai_analysis,
                'model_used': self.model,
                'analysis_type': 'comprehensive_report'
            }
            
        except Exception as e:
            logger.error(f"Error generating AI analysis: {e}")
            return {
                'error': f'AI analysis failed: {str(e)}',
                'ai_analysis': 'AI analysis unavailable due to technical issues.'
            }
    
    def generate_investment_thesis(self, stock_data: Dict) -> Dict:
        """
        Generate investment thesis using AI
        
        Args:
            stock_data: Stock analysis data
        """
        try:
            symbol = stock_data.get('symbol', 'Unknown')
            stock_info = stock_data.get('stock_info', {})
            metrics = stock_data.get('metrics', {})
            valuation = stock_data.get('valuation', {})
            
            prompt = f"""
            Generate a comprehensive investment thesis for {symbol} ({stock_info.get('name', 'Unknown Company')}).
            
            Key Data:
            - Current Price: ${stock_info.get('current_price', 0):.2f}
            - Market Cap: ${stock_info.get('market_cap', 0):,.0f}
            - Sector: {stock_info.get('sector', 'N/A')}
            - P/E Ratio: {metrics.get('pe_ratio', 0):.1f}
            - ROE: {metrics.get('return_on_equity', 0):.1%}
            - Debt/Equity: {metrics.get('debt_to_equity', 0):.1f}
            - Fair Value: ${valuation.get('average_fair_value', 0):.2f}
            - Upside Potential: {valuation.get('upside_potential', 0):.1f}%
            
            Please provide:
            1. Executive Summary
            2. Investment Thesis (Bull Case)
            3. Key Risks (Bear Case)
            4. Valuation Assessment
            5. Investment Recommendation with Time Horizon
            6. Key Catalysts to Watch
            
            Format as a professional investment report.
            """
            
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior investment analyst at a top-tier investment firm. Write professional, detailed investment theses that institutional investors would find valuable."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return {
                'investment_thesis': response.choices[0].message.content,
                'model_used': self.model,
                'analysis_type': 'investment_thesis'
            }
            
        except Exception as e:
            logger.error(f"Error generating investment thesis: {e}")
            return {
                'error': f'Investment thesis generation failed: {str(e)}',
                'investment_thesis': 'Investment thesis unavailable due to technical issues.'
            }
    
    def generate_risk_assessment(self, stock_data: Dict) -> Dict:
        """
        Generate AI-powered risk assessment
        
        Args:
            stock_data: Stock analysis data
        """
        try:
            symbol = stock_data.get('symbol', 'Unknown')
            metrics = stock_data.get('metrics', {})
            technical = stock_data.get('technical_analysis', {})
            
            prompt = f"""
            Provide a comprehensive risk assessment for {symbol}.
            
            Financial Metrics:
            - P/E Ratio: {metrics.get('pe_ratio', 0):.1f}
            - Debt/Equity: {metrics.get('debt_to_equity', 0):.1f}
            - Beta: {metrics.get('beta', 0):.1f}
            - Volatility: {technical.get('volatility', 0):.1%}
            - RSI: {technical.get('rsi', 0):.1f}
            
            Please assess:
            1. Market Risk
            2. Financial Risk
            3. Operational Risk
            4. Regulatory Risk
            5. Liquidity Risk
            6. Overall Risk Score (1-10)
            7. Risk Mitigation Strategies
            
            Provide specific, actionable insights.
            """
            
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a risk management expert specializing in equity analysis. Provide detailed, quantitative risk assessments with specific mitigation strategies."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return {
                'risk_assessment': response.choices[0].message.content,
                'model_used': self.model,
                'analysis_type': 'risk_assessment'
            }
            
        except Exception as e:
            logger.error(f"Error generating risk assessment: {e}")
            return {
                'error': f'Risk assessment generation failed: {str(e)}',
                'risk_assessment': 'Risk assessment unavailable due to technical issues.'
            }
    
    def _create_analysis_prompt(self, stock_data: Dict) -> str:
        """Create comprehensive analysis prompt"""
        
        symbol = stock_data.get('symbol', 'Unknown')
        stock_info = stock_data.get('stock_info', {})
        metrics = stock_data.get('metrics', {})
        valuation = stock_data.get('valuation', {})
        technical = stock_data.get('technical_analysis', {})
        recommendation = stock_data.get('recommendation', {})
        
        prompt = f"""
        Analyze {symbol} ({stock_info.get('name', 'Unknown Company')}) and provide a comprehensive investment analysis.
        
        COMPANY OVERVIEW:
        - Current Price: ${stock_info.get('current_price', 0):.2f}
        - Market Cap: ${stock_info.get('market_cap', 0):,.0f}
        - Sector: {stock_info.get('sector', 'N/A')}
        - Industry: {stock_info.get('industry', 'N/A')}
        
        FINANCIAL METRICS:
        - P/E Ratio: {metrics.get('pe_ratio', 0):.1f}
        - P/B Ratio: {metrics.get('price_to_book', 0):.1f}
        - ROE: {metrics.get('return_on_equity', 0):.1%}
        - ROA: {metrics.get('return_on_assets', 0):.1%}
        - Debt/Equity: {metrics.get('debt_to_equity', 0):.1f}
        - Profit Margin: {metrics.get('profit_margin', 0):.1%}
        - Revenue Growth: {metrics.get('revenue_growth', 0):.1%}
        - Earnings Growth: {metrics.get('earnings_growth', 0):.1%}
        
        VALUATION:
        - Fair Value: ${valuation.get('average_fair_value', 0):.2f}
        - Upside/Downside: {valuation.get('upside_potential', 0):.1f}%
        
        TECHNICAL ANALYSIS:
        - RSI: {technical.get('rsi', 0):.1f}
        - Volatility: {technical.get('volatility', 0):.1%}
        - Price vs 200-day MA: {technical.get('price_vs_ma', {}).get('vs_ma_200', 0):.1f}%
        
        RECOMMENDATION: {recommendation.get('recommendation', 'N/A')} (Score: {recommendation.get('score', 0)})
        
        Please provide:
        1. Executive Summary
        2. Strengths and Opportunities
        3. Weaknesses and Threats
        4. Valuation Analysis
        5. Technical Outlook
        6. Investment Recommendation with Rationale
        7. Key Risks and Mitigation
        8. Price Targets and Time Horizon
        
        Format as a professional investment research report.
        """
        
        return prompt
