"""
Options Flow Analyzer for CROC Investment Fund
Analyzes big calls/puts with contextual insights
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json
from typing import Dict, List, Optional

class OptionsFlowAnalyzer:
    """Analyzes options flow for big calls/puts with contextual insights"""
    
    def __init__(self):
        self.big_flow_threshold = 1000  # Minimum contracts for "big" flow
        self.unusual_activity_multiplier = 5  # 5x average volume
        
    def get_stock_context(self, symbol: str) -> Dict:
        """Get contextual information about the stock"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="2y")
            
            if hist.empty:
                return {}
            
            current_price = hist['Close'].iloc[-1]
            all_time_high = hist['High'].max()
            all_time_low = hist['Low'].min()
            
            # Calculate distances from ATH and ATL
            ath_distance = ((current_price - all_time_high) / all_time_high) * 100
            atl_distance = ((current_price - all_time_low) / all_time_low) * 100
            
            # Recent performance (1 month, 3 months, 6 months, 1 year)
            recent_performance = {}
            periods = {
                '1M': 30,
                '3M': 90,
                '6M': 180,
                '1Y': 365
            }
            
            for period_name, days in periods.items():
                if len(hist) >= days:
                    old_price = hist['Close'].iloc[-days]
                    performance = ((current_price - old_price) / old_price) * 100
                    recent_performance[period_name] = performance
            
            # Volatility analysis
            returns = hist['Close'].pct_change().dropna()
            volatility_30d = returns.tail(30).std() * np.sqrt(252) * 100
            volatility_90d = returns.tail(90).std() * np.sqrt(252) * 100
            
            # Volume analysis
            avg_volume_30d = hist['Volume'].tail(30).mean()
            current_volume = hist['Volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume_30d if avg_volume_30d > 0 else 1
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'all_time_high': all_time_high,
                'all_time_low': all_time_low,
                'ath_distance_pct': ath_distance,
                'atl_distance_pct': atl_distance,
                'recent_performance': recent_performance,
                'volatility_30d': volatility_30d,
                'volatility_90d': volatility_90d,
                'avg_volume_30d': avg_volume_30d,
                'current_volume': current_volume,
                'volume_ratio': volume_ratio,
                'market_cap': info.get('marketCap', 0),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown')
            }
            
        except Exception as e:
            print(f"Error getting stock context: {e}")
            return {}
    
    def get_options_chain(self, symbol: str) -> Dict:
        """Get options chain data"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get expiration dates
            expirations = ticker.options
            if not expirations:
                return {}
            
            # Get options for nearest expiration
            nearest_exp = expirations[0]
            options_chain = ticker.option_chain(nearest_exp)
            
            calls = options_chain.calls
            puts = options_chain.puts
            
            return {
                'expiration': nearest_exp,
                'calls': calls,
                'puts': puts,
                'all_expirations': expirations
            }
            
        except Exception as e:
            print(f"Error getting options chain: {e}")
            return {}
    
    def analyze_big_flow(self, symbol: str) -> Dict:
        """Analyze big options flow with contextual insights"""
        try:
            # Get stock context
            context = self.get_stock_context(symbol)
            if not context:
                return {"error": "Could not get stock context"}
            
            # Get options chain
            options_data = self.get_options_chain(symbol)
            if not options_data:
                return {"error": "Could not get options data"}
            
            calls = options_data['calls']
            puts = options_data['puts']
            current_price = context['current_price']
            
            # Analyze calls for big flow
            big_calls = []
            if not calls.empty:
                # Filter for OTM calls (strike > current price)
                otm_calls = calls[calls['strike'] > current_price]
                
                for _, call in otm_calls.iterrows():
                    volume = call.get('volume', 0)
                    open_interest = call.get('openInterest', 0)
                    last_price = call.get('lastPrice', 0)
                    strike = call.get('strike', 0)
                    
                    # Check for big volume or unusual activity
                    if volume >= self.big_flow_threshold or open_interest >= self.big_flow_threshold:
                        # Calculate moneyness
                        moneyness = ((strike - current_price) / current_price) * 100
                        
                        # Calculate potential return if ITM
                        potential_return = ((strike - current_price) / last_price) * 100 if last_price > 0 else 0
                        
                        big_calls.append({
                            'type': 'CALL',
                            'strike': strike,
                            'expiration': options_data['expiration'],
                            'volume': volume,
                            'open_interest': open_interest,
                            'last_price': last_price,
                            'moneyness_pct': moneyness,
                            'potential_return_pct': potential_return,
                            'is_otm': True,
                            'days_to_expiry': self._days_to_expiry(options_data['expiration'])
                        })
            
            # Analyze puts for big flow
            big_puts = []
            if not puts.empty:
                # Filter for OTM puts (strike < current price)
                otm_puts = puts[puts['strike'] < current_price]
                
                for _, put in otm_puts.iterrows():
                    volume = put.get('volume', 0)
                    open_interest = put.get('openInterest', 0)
                    last_price = put.get('lastPrice', 0)
                    strike = put.get('strike', 0)
                    
                    # Check for big volume or unusual activity
                    if volume >= self.big_flow_threshold or open_interest >= self.big_flow_threshold:
                        # Calculate moneyness
                        moneyness = ((current_price - strike) / current_price) * 100
                        
                        # Calculate potential return if ITM
                        potential_return = ((current_price - strike) / last_price) * 100 if last_price > 0 else 0
                        
                        big_puts.append({
                            'type': 'PUT',
                            'strike': strike,
                            'expiration': options_data['expiration'],
                            'volume': volume,
                            'open_interest': open_interest,
                            'last_price': last_price,
                            'moneyness_pct': moneyness,
                            'potential_return_pct': potential_return,
                            'is_otm': True,
                            'days_to_expiry': self._days_to_expiry(options_data['expiration'])
                        })
            
            # Generate insights
            insights = self._generate_insights(context, big_calls, big_puts)
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'context': context,
                'big_calls': big_calls,
                'big_puts': big_puts,
                'insights': insights,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Error analyzing options flow: {str(e)}"}
    
    def _days_to_expiry(self, expiration_date: str) -> int:
        """Calculate days to expiration"""
        try:
            exp_date = datetime.strptime(expiration_date, '%Y-%m-%d')
            return (exp_date - datetime.now()).days
        except:
            return 0
    
    def _generate_insights(self, context: Dict, big_calls: List, big_puts: List) -> Dict:
        """Generate contextual insights about the options flow"""
        insights = {
            'market_context': [],
            'options_flow_analysis': [],
            'risk_assessment': [],
            'recommendations': []
        }
        
        # Market context insights
        ath_distance = context.get('ath_distance_pct', 0)
        if ath_distance < -10:
            insights['market_context'].append(f"📉 Stock is {abs(ath_distance):.1f}% below all-time high - potential bounce play")
        elif ath_distance > -5:
            insights['market_context'].append(f"📈 Stock is near all-time high - momentum play")
        
        # Recent performance insights
        recent_perf = context.get('recent_performance', {})
        if '1M' in recent_perf:
            perf_1m = recent_perf['1M']
            if perf_1m > 50:
                insights['market_context'].append(f"🚀 Stock up {perf_1m:.1f}% in 1 month - high momentum")
            elif perf_1m < -20:
                insights['market_context'].append(f"📉 Stock down {abs(perf_1m):.1f}% in 1 month - oversold bounce potential")
        
        # Volume insights
        volume_ratio = context.get('volume_ratio', 1)
        if volume_ratio > 2:
            insights['market_context'].append(f"📊 Volume {volume_ratio:.1f}x average - unusual activity")
        
        # Options flow analysis
        if big_calls:
            total_call_volume = sum(call['volume'] for call in big_calls)
            avg_call_moneyness = np.mean([call['moneyness_pct'] for call in big_calls])
            
            insights['options_flow_analysis'].append(f"📞 {len(big_calls)} big call positions detected")
            insights['options_flow_analysis'].append(f"💰 Total call volume: {total_call_volume:,} contracts")
            insights['options_flow_analysis'].append(f"🎯 Average OTM: {avg_call_moneyness:.1f}%")
            
            # Find most interesting calls
            if big_calls:
                most_otm_call = max(big_calls, key=lambda x: x['moneyness_pct'])
                insights['options_flow_analysis'].append(f"🔥 Most OTM call: ${most_otm_call['strike']} ({most_otm_call['moneyness_pct']:.1f}% OTM)")
        
        if big_puts:
            total_put_volume = sum(put['volume'] for put in big_puts)
            avg_put_moneyness = np.mean([put['moneyness_pct'] for put in big_puts])
            
            insights['options_flow_analysis'].append(f"📉 {len(big_puts)} big put positions detected")
            insights['options_flow_analysis'].append(f"💰 Total put volume: {total_put_volume:,} contracts")
            insights['options_flow_analysis'].append(f"🎯 Average OTM: {avg_put_moneyness:.1f}%")
        
        # Risk assessment
        volatility = context.get('volatility_30d', 0)
        if volatility > 50:
            insights['risk_assessment'].append(f"⚠️ High volatility ({volatility:.1f}%) - options are expensive")
        elif volatility < 20:
            insights['risk_assessment'].append(f"✅ Low volatility ({volatility:.1f}%) - options are cheap")
        
        # Recommendations
        if big_calls and ath_distance < -10:
            insights['recommendations'].append("🚀 Consider following big call flow - stock oversold with bullish options activity")
        
        if big_puts and ath_distance > -5:
            insights['recommendations'].append("📉 Consider following big put flow - stock overbought with bearish options activity")
        
        if not big_calls and not big_puts:
            insights['recommendations'].append("😴 No unusual options activity detected - wait for better setup")
        
        return insights
    
    def get_flow_summary(self, symbol: str) -> Dict:
        """Get a summary of options flow for quick analysis"""
        try:
            analysis = self.analyze_big_flow(symbol)
            if 'error' in analysis:
                return analysis
            
            big_calls = analysis.get('big_calls', [])
            big_puts = analysis.get('big_puts', [])
            
            # Calculate flow ratios
            total_call_volume = sum(call['volume'] for call in big_calls)
            total_put_volume = sum(put['volume'] for put in big_puts)
            
            put_call_ratio = total_put_volume / total_call_volume if total_call_volume > 0 else 0
            
            return {
                'symbol': symbol,
                'current_price': analysis['current_price'],
                'big_calls_count': len(big_calls),
                'big_puts_count': len(big_puts),
                'total_call_volume': total_call_volume,
                'total_put_volume': total_put_volume,
                'put_call_ratio': put_call_ratio,
                'flow_sentiment': 'Bullish' if put_call_ratio < 0.7 else 'Bearish' if put_call_ratio > 1.3 else 'Neutral',
                'context': analysis['context'],
                'insights': analysis['insights']
            }
            
        except Exception as e:
            return {"error": f"Error getting flow summary: {str(e)}"}

# Example usage and testing
if __name__ == "__main__":
    analyzer = OptionsFlowAnalyzer()
    
    # Test with a popular stock
    symbol = "AAPL"
    print(f"Analyzing options flow for {symbol}...")
    
    summary = analyzer.get_flow_summary(symbol)
    if 'error' not in summary:
        print(f"\n📊 Options Flow Summary for {symbol}:")
        print(f"Current Price: ${summary['current_price']:.2f}")
        print(f"Big Calls: {summary['big_calls_count']}")
        print(f"Big Puts: {summary['big_puts_count']}")
        print(f"Flow Sentiment: {summary['flow_sentiment']}")
        print(f"Put/Call Ratio: {summary['put_call_ratio']:.2f}")
        
        print(f"\n🎯 Key Insights:")
        for insight in summary['insights']['market_context']:
            print(f"  {insight}")
        for insight in summary['insights']['options_flow_analysis']:
            print(f"  {insight}")
        for insight in summary['insights']['recommendations']:
            print(f"  {insight}")
    else:
        print(f"Error: {summary['error']}")
