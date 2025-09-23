"""
CROC Investment Fund - AI-Powered Stock Analysis with Options Flow
Enhanced with Big Calls/Puts Detection and FL0WG0D-style Analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="CROC Investment Fund - Options Flow Analysis",
    page_icon="🐊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .croc-branding {
        background: linear-gradient(90deg, #00ff00, #00cc00);
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        font-weight: bold;
    }
    .ai-analysis {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .options-flow {
        background-color: #fff3cd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .big-call {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .big-put {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }
    .flow-god-style {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

class OptionsFlowAnalyzer:
    """FL0WG0D-style options flow analyzer"""
    
    def __init__(self):
        self.big_flow_threshold = 1000
        self.unusual_activity_multiplier = 5
        
    def get_stock_context(self, symbol: str) -> dict:
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
            
            # Recent performance
            recent_performance = {}
            periods = {'1M': 30, '3M': 90, '6M': 180, '1Y': 365}
            
            for period_name, days in periods.items():
                if len(hist) >= days:
                    old_price = hist['Close'].iloc[-days]
                    performance = ((current_price - old_price) / old_price) * 100
                    recent_performance[period_name] = performance
            
            # Volatility and volume analysis
            returns = hist['Close'].pct_change().dropna()
            volatility_30d = returns.tail(30).std() * np.sqrt(252) * 100
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
                'avg_volume_30d': avg_volume_30d,
                'current_volume': current_volume,
                'volume_ratio': volume_ratio,
                'market_cap': info.get('marketCap', 0),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown')
            }
            
        except Exception as e:
            st.error(f"Error getting stock context: {e}")
            return {}
    
    def get_options_chain(self, symbol: str) -> dict:
        """Get options chain data"""
        try:
            ticker = yf.Ticker(symbol)
            expirations = ticker.options
            
            if not expirations:
                return {}
            
            # Get options for nearest expiration
            nearest_exp = expirations[0]
            options_chain = ticker.option_chain(nearest_exp)
            
            return {
                'expiration': nearest_exp,
                'calls': options_chain.calls,
                'puts': options_chain.puts,
                'all_expirations': expirations
            }
            
        except Exception as e:
            st.error(f"Error getting options chain: {e}")
            return {}
    
    def analyze_big_flow(self, symbol: str) -> dict:
        """Analyze big options flow with FL0WG0D-style insights"""
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
            
            # Analyze big calls (OTM)
            big_calls = []
            if not calls.empty:
                otm_calls = calls[calls['strike'] > current_price]
                
                for _, call in otm_calls.iterrows():
                    volume = call.get('volume', 0)
                    open_interest = call.get('openInterest', 0)
                    last_price = call.get('lastPrice', 0)
                    strike = call.get('strike', 0)
                    
                    if volume >= self.big_flow_threshold or open_interest >= self.big_flow_threshold:
                        moneyness = ((strike - current_price) / current_price) * 100
                        potential_return = ((strike - current_price) / last_price) * 100 if last_price > 0 else 0
                        
                        big_calls.append({
                            'strike': strike,
                            'expiration': options_data['expiration'],
                            'volume': volume,
                            'open_interest': open_interest,
                            'last_price': last_price,
                            'moneyness_pct': moneyness,
                            'potential_return_pct': potential_return,
                            'days_to_expiry': self._days_to_expiry(options_data['expiration'])
                        })
            
            # Analyze big puts (OTM)
            big_puts = []
            if not puts.empty:
                otm_puts = puts[puts['strike'] < current_price]
                
                for _, put in otm_puts.iterrows():
                    volume = put.get('volume', 0)
                    open_interest = put.get('openInterest', 0)
                    last_price = put.get('lastPrice', 0)
                    strike = put.get('strike', 0)
                    
                    if volume >= self.big_flow_threshold or open_interest >= self.big_flow_threshold:
                        moneyness = ((current_price - strike) / current_price) * 100
                        potential_return = ((current_price - strike) / last_price) * 100 if last_price > 0 else 0
                        
                        big_puts.append({
                            'strike': strike,
                            'expiration': options_data['expiration'],
                            'volume': volume,
                            'open_interest': open_interest,
                            'last_price': last_price,
                            'moneyness_pct': moneyness,
                            'potential_return_pct': potential_return,
                            'days_to_expiry': self._days_to_expiry(options_data['expiration'])
                        })
            
            # Generate FL0WG0D-style insights
            insights = self._generate_flow_insights(context, big_calls, big_puts)
            
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
    
    def _generate_flow_insights(self, context: dict, big_calls: list, big_puts: list) -> dict:
        """Generate FL0WG0D-style insights"""
        insights = {
            'market_context': [],
            'flow_analysis': [],
            'contract_analysis': [],
            'recommendations': []
        }
        
        # Market context
        ath_distance = context.get('ath_distance_pct', 0)
        if ath_distance < -10:
            insights['market_context'].append(f"📉 {context['symbol']} is {abs(ath_distance):.1f}% under ATH - Bounce play setup")
        elif ath_distance > -5:
            insights['market_context'].append(f"📈 {context['symbol']} near ATH - Momentum continuation play")
        
        # Recent performance context
        recent_perf = context.get('recent_performance', {})
        if '1M' in recent_perf:
            perf_1m = recent_perf['1M']
            if perf_1m > 50:
                insights['market_context'].append(f"🚀 {context['symbol']} up {perf_1m:.1f}% in 1M - High momentum, watch for continuation")
            elif perf_1m < -20:
                insights['market_context'].append(f"📉 {context['symbol']} down {abs(perf_1m):.1f}% in 1M - Oversold bounce potential")
        
        # Volume context
        volume_ratio = context.get('volume_ratio', 1)
        if volume_ratio > 2:
            insights['market_context'].append(f"📊 Volume {volume_ratio:.1f}x average - Unusual activity detected")
        
        # Options flow analysis
        if big_calls:
            total_call_volume = sum(call['volume'] for call in big_calls)
            avg_call_moneyness = np.mean([call['moneyness_pct'] for call in big_calls])
            
            insights['flow_analysis'].append(f"📞 {len(big_calls)} BIG CALL positions detected")
            insights['flow_analysis'].append(f"💰 Total call volume: {total_call_volume:,} contracts")
            insights['flow_analysis'].append(f"🎯 Average OTM: {avg_call_moneyness:.1f}%")
            
            # Most interesting calls
            if big_calls:
                most_otm_call = max(big_calls, key=lambda x: x['moneyness_pct'])
                insights['flow_analysis'].append(f"🔥 Most OTM call: ${most_otm_call['strike']} ({most_otm_call['moneyness_pct']:.1f}% OTM)")
        
        if big_puts:
            total_put_volume = sum(put['volume'] for put in big_puts)
            avg_put_moneyness = np.mean([put['moneyness_pct'] for put in big_puts])
            
            insights['flow_analysis'].append(f"📉 {len(big_puts)} BIG PUT positions detected")
            insights['flow_analysis'].append(f"💰 Total put volume: {total_put_volume:,} contracts")
            insights['flow_analysis'].append(f"🎯 Average OTM: {avg_put_moneyness:.1f}%")
        
        # Contract price analysis
        if big_calls:
            for call in big_calls[:3]:  # Show top 3
                insights['contract_analysis'].append(
                    f"📞 ${call['strike']} call: ${call['last_price']:.2f} "
                    f"({call['moneyness_pct']:.1f}% OTM, {call['days_to_expiry']}d)"
                )
        
        if big_puts:
            for put in big_puts[:3]:  # Show top 3
                insights['contract_analysis'].append(
                    f"📉 ${put['strike']} put: ${put['last_price']:.2f} "
                    f"({put['moneyness_pct']:.1f}% OTM, {put['days_to_expiry']}d)"
                )
        
        # FL0WG0D-style recommendations
        if big_calls and ath_distance < -10:
            insights['recommendations'].append("🚀 FOLLOW THE BIG CALLS - Stock oversold with bullish options flow")
        elif big_puts and ath_distance > -5:
            insights['recommendations'].append("📉 FOLLOW THE BIG PUTS - Stock overbought with bearish options flow")
        elif big_calls and big_puts:
            insights['recommendations'].append("⚖️ MIXED SIGNALS - Both calls and puts active, wait for direction")
        elif not big_calls and not big_puts:
            insights['recommendations'].append("😴 NO UNUSUAL FLOW - Wait for better setup")
        
        return insights

class GrokAnalyzer:
    """Grok AI-powered analysis"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GROK_API_KEY')
        self.base_url = "https://api.x.ai/v1"
        self.model = "grok-3"
        self.max_tokens = 1000
        self.temperature = 0.7
    
    def is_available(self):
        return bool(self.api_key)
    
    def analyze_options_flow(self, flow_data):
        """Generate AI analysis for options flow"""
        if not self.is_available():
            return {"error": "Grok API key not available"}
        
        try:
            prompt = f"""
            Analyze this options flow data and provide FL0WG0D-style insights:
            
            Symbol: {flow_data.get('symbol', 'Unknown')}
            Current Price: ${flow_data.get('current_price', 0):.2f}
            ATH Distance: {flow_data.get('context', {}).get('ath_distance_pct', 0):.1f}%
            Big Calls: {len(flow_data.get('big_calls', []))}
            Big Puts: {len(flow_data.get('big_puts', []))}
            
            Provide:
            1. FL0WG0D-style analysis of the flow
            2. Whether to follow the big calls or puts
            3. Risk assessment for OTM plays
            4. Price targets based on options flow
            5. Time horizon for the play
            """
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are FL0WG0D, an expert options flow analyst. Provide sharp, actionable insights about big calls and puts with specific recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "analysis": result['choices'][0]['message']['content'],
                    "model": self.model,
                    "provider": "Grok AI (FL0WG0D Style)"
                }
            else:
                return {"error": f"Grok API error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Error calling Grok API: {str(e)}"}

def display_options_flow_analysis(flow_data):
    """Display options flow analysis in FL0WG0D style"""
    if not flow_data or 'error' in flow_data:
        st.error("❌ Options flow analysis unavailable")
        return
    
    symbol = flow_data['symbol']
    current_price = flow_data['current_price']
    context = flow_data['context']
    big_calls = flow_data['big_calls']
    big_puts = flow_data['big_puts']
    insights = flow_data['insights']
    
    # FL0WG0D-style header
    st.markdown(f"""
    <div class="flow-god-style">
        <h2>🔥 FL0WG0D OPTIONS FLOW ANALYSIS 🔥</h2>
        <h3>{symbol} - ${current_price:.2f}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Market context
    st.subheader("📊 Market Context")
    for insight in insights['market_context']:
        st.info(insight)
    
    # Flow analysis
    st.subheader("💰 Options Flow Analysis")
    for insight in insights['flow_analysis']:
        st.success(insight)
    
    # Contract analysis
    st.subheader("📋 Contract Analysis")
    for insight in insights['contract_analysis']:
        st.info(insight)
    
    # Big calls display
    if big_calls:
        st.subheader("📞 BIG CALLS DETECTED")
        for call in big_calls:
            st.markdown(f"""
            <div class="big-call">
                <strong>${call['strike']} CALL</strong><br>
                Volume: {call['volume']:,} | OI: {call['open_interest']:,}<br>
                Price: ${call['last_price']:.2f} | {call['moneyness_pct']:.1f}% OTM<br>
                Expiry: {call['days_to_expiry']} days
            </div>
            """, unsafe_allow_html=True)
    
    # Big puts display
    if big_puts:
        st.subheader("📉 BIG PUTS DETECTED")
        for put in big_puts:
            st.markdown(f"""
            <div class="big-put">
                <strong>${put['strike']} PUT</strong><br>
                Volume: {put['volume']:,} | OI: {put['open_interest']:,}<br>
                Price: ${put['last_price']:.2f} | {put['moneyness_pct']:.1f}% OTM<br>
                Expiry: {put['days_to_expiry']} days
            </div>
            """, unsafe_allow_html=True)
    
    # Recommendations
    st.subheader("🎯 FL0WG0D RECOMMENDATIONS")
    for rec in insights['recommendations']:
        st.warning(rec)

def main():
    """Main application function"""
    
    # Header with CROC branding
    st.markdown("""
    <div class="croc-branding">
        <h1>🐊 CROC INVESTMENT FUND</h1>
        <h2>FL0WG0D OPTIONS FLOW ANALYSIS 🚀</h2>
        <h3>Big Calls & Puts Detection with AI Insights</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("🔧 Analysis Settings")
    
    # Stock symbol input
    symbol = st.sidebar.text_input(
        "Enter Stock Symbol",
        value="AAPL",
        help="Enter a valid stock symbol (e.g., AAPL, MSFT, GOOGL, TSLA)"
    ).upper()
    
    # Analysis options
    st.sidebar.subheader("📊 Analysis Options")
    show_options_flow = st.sidebar.checkbox("Options Flow Analysis", value=True)
    show_ai_analysis = st.sidebar.checkbox("AI Analysis (FL0WG0D Style)", value=True)
    show_context = st.sidebar.checkbox("Market Context", value=True)
    
    # API Status
    st.sidebar.subheader("🔑 API Status")
    
    grok_analyzer = GrokAnalyzer()
    if grok_analyzer.is_available():
        st.sidebar.success("🟢 Grok AI Available")
    else:
        st.sidebar.error("🔴 Grok AI Unavailable")
    
    st.sidebar.info("📊 Yahoo Finance Data")
    
    # Main content
    if st.button("🔥 ANALYZE OPTIONS FLOW", type="primary", use_container_width=True):
        if not symbol:
            st.error("Please enter a stock symbol")
            return
        
        with st.spinner(f"Analyzing {symbol} options flow... This may take a few seconds."):
            # Initialize options flow analyzer
            flow_analyzer = OptionsFlowAnalyzer()
            
            # Get options flow analysis
            flow_data = flow_analyzer.analyze_big_flow(symbol)
            
            if 'error' not in flow_data:
                st.success(f"✅ Options flow analysis complete for {symbol}!")
                
                # Display options flow analysis
                if show_options_flow:
                    display_options_flow_analysis(flow_data)
                
                # AI Analysis
                if show_ai_analysis and grok_analyzer.is_available():
                    with st.spinner("🤖 Grok AI analyzing options flow..."):
                        ai_result = grok_analyzer.analyze_options_flow(flow_data)
                        
                        if 'error' not in ai_result:
                            st.subheader("🤖 AI Analysis (FL0WG0D Style)")
                            st.markdown(f"""
                            <div class="ai-analysis">
                                {ai_result['analysis']}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error(f"AI Analysis Error: {ai_result['error']}")
                
                # Market context
                if show_context:
                    st.subheader("📈 Market Context")
                    context = flow_data['context']
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Current Price", f"${context['current_price']:.2f}")
                        st.metric("ATH Distance", f"{context['ath_distance_pct']:.1f}%")
                    
                    with col2:
                        st.metric("Market Cap", f"${context['market_cap']:,.0f}")
                        st.metric("Volume Ratio", f"{context['volume_ratio']:.1f}x")
                    
                    with col3:
                        st.metric("Volatility (30d)", f"{context['volatility_30d']:.1f}%")
                        st.metric("Sector", context['sector'])
                    
                    with col4:
                        recent_perf = context['recent_performance']
                        if '1M' in recent_perf:
                            st.metric("1M Performance", f"{recent_perf['1M']:.1f}%")
                        if '3M' in recent_perf:
                            st.metric("3M Performance", f"{recent_perf['3M']:.1f}%")
                
            else:
                st.error(f"❌ Error analyzing {symbol}: {flow_data['error']}")
                st.info("💡 Try popular symbols like: AAPL, MSFT, GOOGL, TSLA, AMZN, META")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <h4>🐊 CROC Investment Fund</h4>
        <p>FL0WG0D-Style Options Flow Analysis</p>
        <p>Built with Streamlit | Powered by Grok AI & Yahoo Finance</p>
        <p><strong>FOLLOW THE BIG FLOW! 🔥</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
