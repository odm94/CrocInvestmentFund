"""
Grok AI Analyzer for Stock Analysis
Alternative AI analysis using Grok API
"""

import requests
import json
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class GrokAnalyzer:
    """Grok AI-powered stock analysis"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1"
        self.model = "grok-3"
        self.max_tokens = 1000
        self.temperature = 0.7
    
    def generate_analysis_report(self, stock_data: Dict) -> Dict:
        """
        Generate comprehensive AI analysis report using Grok
        
        Args:
            stock_data: Complete stock analysis data
        """
        try:
            # Prepare the prompt
            prompt = self._create_analysis_prompt(stock_data)
            
            # Call Grok API
            response = self._call_grok_api(prompt)
            
            if response:
                return {
                    'ai_analysis': response,
                    'model_used': self.model,
                    'analysis_type': 'grok_comprehensive_report'
                }
            else:
                return {
                    'error': 'Grok analysis failed',
                    'ai_analysis': 'Grok analysis unavailable due to technical issues.'
                }
            
        except Exception as e:
            logger.error(f"Error generating Grok analysis: {e}")
            return {
                'error': f'Grok analysis failed: {str(e)}',
                'ai_analysis': 'Grok analysis unavailable due to technical issues.'
            }
    
    def generate_investment_thesis(self, stock_data: Dict) -> Dict:
        """
        Generate investment thesis using Grok
        
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
            
            Format as a professional investment report with Grok's unique insights and analysis style.
            """
            
            response = self._call_grok_api(prompt)
            
            if response:
                return {
                    'investment_thesis': response,
                    'model_used': self.model,
                    'analysis_type': 'grok_investment_thesis'
                }
            else:
                return {
                    'error': 'Grok investment thesis generation failed',
                    'investment_thesis': 'Grok investment thesis unavailable due to technical issues.'
                }
            
        except Exception as e:
            logger.error(f"Error generating Grok investment thesis: {e}")
            return {
                'error': f'Grok investment thesis generation failed: {str(e)}',
                'investment_thesis': 'Grok investment thesis unavailable due to technical issues.'
            }
    
    def generate_risk_assessment(self, stock_data: Dict) -> Dict:
        """
        Generate AI-powered risk assessment using Grok
        
        Args:
            stock_data: Stock analysis data
        """
        try:
            symbol = stock_data.get('symbol', 'Unknown')
            metrics = stock_data.get('metrics', {})
            technical = stock_data.get('technical_analysis', {})
            
            prompt = f"""
            Provide a comprehensive risk assessment for {symbol} using Grok's analytical capabilities.
            
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
            
            Provide specific, actionable insights with Grok's unique perspective on risk analysis.
            """
            
            response = self._call_grok_api(prompt)
            
            if response:
                return {
                    'risk_assessment': response,
                    'model_used': self.model,
                    'analysis_type': 'grok_risk_assessment'
                }
            else:
                return {
                    'error': 'Grok risk assessment generation failed',
                    'risk_assessment': 'Grok risk assessment unavailable due to technical issues.'
                }
            
        except Exception as e:
            logger.error(f"Error generating Grok risk assessment: {e}")
            return {
                'error': f'Grok risk assessment generation failed: {str(e)}',
                'risk_assessment': 'Grok risk assessment unavailable due to technical issues.'
            }
    
    def _call_grok_api(self, prompt: str) -> Optional[str]:
        """Call Grok API with the given prompt"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': self.model,
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are Grok, an AI assistant with a unique perspective on financial analysis. Provide insightful, comprehensive, and sometimes unconventional analysis of stocks and investments. Be direct, analytical, and offer unique insights that other AI might miss.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': self.max_tokens,
                'temperature': self.temperature
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"Grok API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling Grok API: {e}")
            return None
    
    def _create_analysis_prompt(self, stock_data: Dict) -> str:
        """Create comprehensive analysis prompt for Grok"""
        
        symbol = stock_data.get('symbol', 'Unknown')
        stock_info = stock_data.get('stock_info', {})
        metrics = stock_data.get('metrics', {})
        valuation = stock_data.get('valuation', {})
        technical = stock_data.get('technical_analysis', {})
        recommendation = stock_data.get('recommendation', {})
        
        prompt = f"""
        Analyze {symbol} ({stock_info.get('name', 'Unknown Company')}) using Grok's unique analytical approach.
        
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
        
        Please provide Grok's unique analysis including:
        1. Executive Summary with Grok's perspective
        2. Strengths and Opportunities (what others might miss)
        3. Weaknesses and Threats (unconventional risks)
        4. Valuation Analysis (Grok's take on fair value)
        5. Technical Outlook (market dynamics)
        6. Investment Recommendation with Grok's reasoning
        7. Key Risks and Mitigation (unique insights)
        8. Price Targets and Time Horizon (Grok's forecast)
        9. What the market is missing (Grok's edge)
        
        Format as a professional investment research report with Grok's distinctive analytical style.
        """
        
        return prompt
