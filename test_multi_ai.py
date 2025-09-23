#!/usr/bin/env python3
"""
Test script for Multi-AI Analysis
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.multi_ai_analyzer import MultiAIAnalyzer
from src.x_analyst_feed import XAnalystFeed

def test_multi_ai_system():
    """Test the multi-AI analysis system"""
    print("🤖 Testing Multi-AI Analysis System...")
    
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
    
    # Test Multi-AI Analyzer
    print("\n📊 Testing Multi-AI Analyzer...")
    multi_analyzer = MultiAIAnalyzer()
    
    # Get AI status
    ai_status = multi_analyzer.get_ai_status()
    print("AI Provider Status:")
    for provider, status in ai_status.items():
        print(f"  {provider.upper()}: {status}")
    
    # Get feed status
    feed_status = multi_analyzer.get_feed_status()
    print("\nData Feed Status:")
    for feed, status in feed_status.items():
        print(f"  {feed.upper()}: {status}")
    
    # Test comprehensive analysis
    print("\n🔍 Testing comprehensive analysis...")
    try:
        results = multi_analyzer.generate_comprehensive_analysis(test_data)
        if 'error' in results:
            print(f"❌ Analysis failed: {results['error']}")
        else:
            print("✅ Multi-AI analysis completed successfully")
            print(f"AI providers used: {results.get('ai_providers_used', [])}")
            print(f"Total AI models: {results.get('total_ai_models', 0)}")
            
            # Show consensus analysis
            consensus = results.get('consensus_analysis', {})
            if consensus:
                print(f"Consensus recommendation: {consensus.get('consensus_recommendation', 'N/A')}")
                print(f"Confidence score: {consensus.get('confidence_score', 0):.1%}")
    except Exception as e:
        print(f"❌ Multi-AI analysis error: {e}")
    
    # Test X Analyst Feed
    print("\n🐦 Testing X Analyst Feed...")
    x_feed = XAnalystFeed()
    
    try:
        x_analysis = x_feed.get_comprehensive_x_analysis('AAPL')
        if 'error' in x_analysis:
            print(f"❌ X analysis failed: {x_analysis['error']}")
        else:
            print("✅ X analysis completed successfully")
            print(f"Overall X score: {x_analysis.get('overall_x_score', 0):.2f}")
            print(f"X recommendation: {x_analysis.get('x_recommendation', 'N/A')}")
    except Exception as e:
        print(f"❌ X analysis error: {e}")
    
    print("\n🎉 Multi-AI system test completed!")

if __name__ == "__main__":
    test_multi_ai_system()
