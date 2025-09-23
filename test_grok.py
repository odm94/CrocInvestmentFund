#!/usr/bin/env python3
"""
Test script for Grok AI integration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.grok_analyzer import GrokAnalyzer
from config import GROK_API_KEY

def test_grok_integration():
    """Test Grok AI integration"""
    print("🤖 Testing Grok AI Integration...")
    
    # Initialize Grok analyzer
    grok = GrokAnalyzer(GROK_API_KEY)
    
    # Test data
    test_data = {
        'symbol': 'AAPL',
        'stock_info': {
            'name': 'Apple Inc.',
            'current_price': 175.50,
            'market_cap': 2800000000000,
            'sector': 'Technology'
        },
        'metrics': {
            'pe_ratio': 25.5,
            'return_on_equity': 0.15,
            'debt_to_equity': 0.3
        },
        'valuation': {
            'average_fair_value': 180.00,
            'upside_potential': 2.6
        },
        'recommendation': {
            'recommendation': 'BUY',
            'score': 7.5
        }
    }
    
    print("📊 Testing analysis report...")
    analysis = grok.generate_analysis_report(test_data)
    if 'error' in analysis:
        print(f"❌ Analysis failed: {analysis['error']}")
    else:
        print("✅ Analysis report generated successfully")
        print(f"Model used: {analysis.get('model_used', 'Unknown')}")
    
    print("\n💡 Testing investment thesis...")
    thesis = grok.generate_investment_thesis(test_data)
    if 'error' in thesis:
        print(f"❌ Investment thesis failed: {thesis['error']}")
    else:
        print("✅ Investment thesis generated successfully")
    
    print("\n⚠️ Testing risk assessment...")
    risk = grok.generate_risk_assessment(test_data)
    if 'error' in risk:
        print(f"❌ Risk assessment failed: {risk['error']}")
    else:
        print("✅ Risk assessment generated successfully")
    
    print("\n🎉 Grok AI integration test completed!")

if __name__ == "__main__":
    test_grok_integration()
