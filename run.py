#!/usr/bin/env python3
"""
Stock Valuation Tool - Command Line Runner
"""

import sys
import os
import argparse
import json
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.stock_analyzer import StockAnalyzer

def main():
    """Command line interface for stock analysis"""
    
    parser = argparse.ArgumentParser(
        description="Stock Valuation Tool - Analyze stocks from command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py AAPL                    # Analyze Apple stock
  python run.py MSFT --output results.json  # Save results to file
  python run.py GOOGL --verbose         # Detailed output
        """
    )
    
    parser.add_argument(
        'symbol',
        help='Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file to save results (JSON format)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed analysis output'
    )
    
    parser.add_argument(
        '--risk-free-rate',
        type=float,
        default=4.0,
        help='Risk-free rate percentage (default: 4.0)'
    )
    
    parser.add_argument(
        '--market-risk-premium',
        type=float,
        default=6.0,
        help='Market risk premium percentage (default: 6.0)'
    )
    
    parser.add_argument(
        '--terminal-growth',
        type=float,
        default=3.0,
        help='Terminal growth rate percentage (default: 3.0)'
    )
    
    args = parser.parse_args()
    
    # Initialize analyzer
    print(f"🔍 Analyzing {args.symbol.upper()}...")
    analyzer = StockAnalyzer()
    
    # Update model parameters
    analyzer.valuation_models.risk_free_rate = args.risk_free_rate / 100
    analyzer.valuation_models.market_risk_premium = args.market_risk_premium / 100
    
    try:
        # Perform analysis
        results = analyzer.analyze_stock(args.symbol.upper())
        
        if 'error' in results:
            print(f"❌ Error: {results['error']}")
            sys.exit(1)
        
        # Display results
        display_results(results, args.verbose)
        
        # Save to file if requested
        if args.output:
            save_results(results, args.output)
            print(f"💾 Results saved to {args.output}")
        
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        sys.exit(1)

def display_results(results, verbose=False):
    """Display analysis results in a formatted way"""
    
    symbol = results['symbol']
    stock_info = results['stock_info']
    metrics = results['metrics']
    valuation = results['valuation']
    recommendation = results['recommendation']
    
    print("\n" + "="*60)
    print(f"📈 STOCK ANALYSIS: {symbol}")
    print("="*60)
    
    # Stock overview
    print(f"\n🏢 Company: {stock_info.get('name', 'N/A')}")
    print(f"💰 Current Price: ${stock_info.get('current_price', 0):.2f}")
    print(f"📊 Market Cap: ${stock_info.get('market_cap', 0):,.0f}")
    print(f"🏭 Sector: {stock_info.get('sector', 'N/A')}")
    print(f"🏛️ Exchange: {stock_info.get('exchange', 'N/A')}")
    
    # Investment recommendation
    print(f"\n🎯 RECOMMENDATION: {recommendation['recommendation']}")
    print(f"📊 Score: {recommendation['score']}")
    print(f"🎲 Confidence: {recommendation['confidence']:.1%}")
    
    print("\n📋 Key Factors:")
    for factor in recommendation['factors']:
        print(f"  • {factor}")
    
    # Valuation summary
    if 'average_fair_value' in valuation:
        print(f"\n💰 VALUATION SUMMARY:")
        print(f"  Fair Value: ${valuation['average_fair_value']:.2f}")
        print(f"  Current Price: ${valuation.get('current_price', 0):.2f}")
        print(f"  Upside/Downside: {valuation.get('upside_potential', 0):.1f}%")
    
    # Key metrics
    print(f"\n📊 KEY METRICS:")
    print(f"  P/E Ratio: {metrics.get('pe_ratio', 0):.1f}")
    print(f"  P/B Ratio: {metrics.get('price_to_book', 0):.1f}")
    print(f"  ROE: {metrics.get('return_on_equity', 0):.1%}")
    print(f"  Debt/Equity: {metrics.get('debt_to_equity', 0):.1f}")
    print(f"  Profit Margin: {metrics.get('profit_margin', 0):.1%}")
    
    if verbose:
        # Detailed valuation models
        print(f"\n🔍 DETAILED VALUATION MODELS:")
        
        if 'pe_valuation' in valuation:
            pe_val = valuation['pe_valuation']
            print(f"  P/E Valuation:")
            print(f"    Current P/E: {pe_val.get('current_pe', 0):.1f}")
            print(f"    Fair Value (Industry): ${pe_val.get('fair_value_industry', 0):.2f}")
            print(f"    Fair Value (Growth): ${pe_val.get('fair_value_growth', 0):.2f}")
        
        if 'graham_valuation' in valuation:
            graham_val = valuation['graham_valuation']
            print(f"  Graham Valuation:")
            print(f"    Intrinsic Value: ${graham_val.get('intrinsic_value', 0):.2f}")
            print(f"    Simplified Value: ${graham_val.get('simplified_value', 0):.2f}")
            print(f"    Margin of Safety: ${graham_val.get('margin_of_safety_price', 0):.2f}")
        
        # Technical analysis
        technical = results.get('technical_analysis', {})
        if technical:
            print(f"\n📈 TECHNICAL ANALYSIS:")
            print(f"  RSI: {technical.get('rsi', 0):.1f}")
            print(f"  Volatility: {technical.get('volatility', 0):.1%}")
            
            ma = technical.get('moving_averages', {})
            if ma:
                print(f"  20-day MA: ${ma.get('ma_20', 0):.2f}")
                print(f"  50-day MA: ${ma.get('ma_50', 0):.2f}")
                print(f"  200-day MA: ${ma.get('ma_200', 0):.2f}")
    
    print(f"\n⏰ Analysis completed at: {results.get('analysis_date', 'N/A')}")
    print("="*60)

def save_results(results, filename):
    """Save results to JSON file"""
    
    # Convert numpy types to native Python types for JSON serialization
    def convert_types(obj):
        if isinstance(obj, dict):
            return {key: convert_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_types(item) for item in obj]
        elif hasattr(obj, 'item'):  # numpy scalar
            return obj.item()
        elif hasattr(obj, 'tolist'):  # numpy array
            return obj.tolist()
        else:
            return obj
    
    # Convert results
    json_results = convert_types(results)
    
    # Add metadata
    json_results['metadata'] = {
        'tool_version': '1.0.0',
        'export_date': datetime.now().isoformat(),
        'export_format': 'json'
    }
    
    # Save to file
    with open(filename, 'w') as f:
        json.dump(json_results, f, indent=2, default=str)

if __name__ == "__main__":
    main()
