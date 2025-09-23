#!/usr/bin/env python3
"""
Test script for AI integration
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.stock_analyzer import StockAnalyzer

def test_ai_analysis():
    """Test AI analysis functionality"""
    
    print("🤖 Testing AI-Powered Stock Analysis...")
    print("="*50)
    
    # Initialize analyzer
    analyzer = StockAnalyzer()
    
    # Test with Apple stock
    symbol = "AAPL"
    print(f"Analyzing {symbol} with AI...")
    
    try:
        # Perform analysis
        results = analyzer.analyze_stock(symbol)
        
        if 'error' in results:
            print(f"❌ Error: {results['error']}")
            return
        
        print("✅ Analysis completed successfully!")
        print(f"📊 Symbol: {results['symbol']}")
        print(f"💰 Current Price: ${results['stock_info'].get('current_price', 0):.2f}")
        print(f"🎯 Recommendation: {results['recommendation']['recommendation']}")
        
        # Check AI analysis results
        if 'ai_analysis' in results:
            ai_result = results['ai_analysis']
            if 'ai_analysis' in ai_result:
                print("\n🤖 AI Analysis Preview:")
                print("-" * 30)
                # Show first 200 characters
                preview = ai_result['ai_analysis'][:200] + "..." if len(ai_result['ai_analysis']) > 200 else ai_result['ai_analysis']
                print(preview)
            else:
                print("⚠️ AI analysis content not found")
        else:
            print("⚠️ AI analysis not available")
        
        if 'investment_thesis' in results:
            thesis_result = results['investment_thesis']
            if 'investment_thesis' in thesis_result:
                print("\n💡 Investment Thesis Available")
            else:
                print("⚠️ Investment thesis content not found")
        
        if 'risk_assessment' in results:
            risk_result = results['risk_assessment']
            if 'risk_assessment' in risk_result:
                print("⚠️ Risk Assessment Available")
            else:
                print("⚠️ Risk assessment content not found")
        
        print("\n🎉 AI integration test completed!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_analysis()
