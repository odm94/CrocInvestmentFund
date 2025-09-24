"""
CROC Investment Fund - Complete Stock Analysis & Options Flow Tool
Combines: Stock Analysis + Options Flow + X Analyst Posts + AI Analysis
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
    page_title="CROC Investment Fund - Complete Analysis Tool",
    page_icon="🐊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS
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
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 6px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .big-call:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .big-put {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 6px solid #dc3545;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .big-put:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .flow-god-style {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }
    .option-header {
        background: linear-gradient(90deg, #28a745, #20c997);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        font-size: 1.1rem;
    }
    .put-header {
        background: linear-gradient(90deg, #dc3545, #e74c3c);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        font-size: 1.1rem;
    }
    .option-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 1rem;
    }
    .option-metric {
        background: rgba(255,255,255,0.9);
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        border: 1px solid rgba(0,0,0,0.1);
    }
    .metric-label {
        font-size: 0.85rem;
        color: #666;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.3rem;
        font-weight: bold;
        color: #333;
    }
    .otm-badge {
        background: #ffc107;
        color: #000;
        padding: 0.4rem 0.8rem;
        border-radius: 0.4rem;
        font-size: 0.9rem;
        font-weight: bold;
        display: inline-block;
        margin-top: 0.5rem;
    }
    .expiry-badge {
        background: #17a2b8;
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 0.4rem;
        font-size: 0.9rem;
        font-weight: bold;
        display: inline-block;
        margin-top: 0.5rem;
    }
    .x-post {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1da1f2;
    }
    .x-post-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .x-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #1da1f2;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        margin-right: 0.75rem;
    }
    .x-username {
        font-weight: bold;
        color: #1da1f2;
    }
    .x-timestamp {
        color: #666;
        font-size: 0.8rem;
        margin-left: auto;
    }
    .x-content {
        margin-top: 0.5rem;
        line-height: 1.4;
    }
    .x-engagement {
        display: flex;
        gap: 1rem;
        margin-top: 0.75rem;
        font-size: 0.8rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

class StockAnalyzer:
    """Comprehensive stock analysis"""
    
    def get_stock_data(self, symbol: str) -> dict:
        """Get comprehensive stock data"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1y")
            
            if hist.empty:
                return None
                
            current_price = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change = current_price - previous_close
            change_pct = (change / previous_close) * 100
            
            # Calculate volatility
            returns = hist['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252)
            
            # Calculate moving averages
            ma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
            ma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
            
            return {
                'symbol': symbol,
                'info': info,
                'history': hist,
                'current_price': current_price,
                'previous_close': previous_close,
                'change': change,
                'change_pct': change_pct,
                'volume': hist['Volume'].iloc[-1],
                'avg_volume': hist['Volume'].mean(),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'dividend_yield': info.get('dividendYield', 0),
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0),
                'volatility': volatility,
                'ma_20': ma_20,
                'ma_50': ma_50,
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'employees': info.get('fullTimeEmployees', 0),
                'revenue': info.get('totalRevenue', 0),
                'profit_margin': info.get('profitMargins', 0)
            }
        except Exception as e:
            st.error(f"Error fetching stock data: {e}")
            return None

class OptionsFlowAnalyzer:
    """Enhanced options flow analyzer"""
    
    def __init__(self):
        self.big_flow_threshold = 1000
        
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
    
    def analyze_big_flow(self, symbol: str, stock_data: dict) -> dict:
        """Analyze big options flow"""
        try:
            options_data = self.get_options_chain(symbol)
            if not options_data:
                return {"error": "Could not get options data"}
            
            calls = options_data['calls']
            puts = options_data['puts']
            current_price = stock_data['current_price']
            
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
            
            # Generate insights
            insights = self._generate_flow_insights(stock_data, big_calls, big_puts)
            
            return {
                'symbol': symbol,
                'current_price': current_price,
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
    
    def _generate_flow_insights(self, stock_data: dict, big_calls: list, big_puts: list) -> dict:
        """Generate flow insights"""
        insights = {
            'market_context': [],
            'flow_analysis': [],
            'recommendations': []
        }
        
        # Market context
        current_price = stock_data['current_price']
        ath = stock_data['52_week_high']
        atl = stock_data['52_week_low']
        
        ath_distance = ((current_price - ath) / ath) * 100
        if ath_distance < -10:
            insights['market_context'].append(f"📉 {stock_data['symbol']} is {abs(ath_distance):.1f}% under ATH - Bounce play setup")
        elif ath_distance > -5:
            insights['market_context'].append(f"📈 {stock_data['symbol']} near ATH - Momentum continuation play")
        
        # Flow analysis
        if big_calls:
            total_call_volume = sum(call['volume'] for call in big_calls)
            insights['flow_analysis'].append(f"📞 {len(big_calls)} BIG CALL positions detected")
            insights['flow_analysis'].append(f"💰 Total call volume: {total_call_volume:,} contracts")
            
            if big_calls:
                most_otm_call = max(big_calls, key=lambda x: x['moneyness_pct'])
                insights['flow_analysis'].append(f"🔥 Most OTM call: ${most_otm_call['strike']} ({most_otm_call['moneyness_pct']:.1f}% OTM)")
        
        if big_puts:
            total_put_volume = sum(put['volume'] for put in big_puts)
            insights['flow_analysis'].append(f"📉 {len(big_puts)} BIG PUT positions detected")
            insights['flow_analysis'].append(f"💰 Total put volume: {total_put_volume:,} contracts")
        
        # Recommendations
        if big_calls and ath_distance < -10:
            insights['recommendations'].append("🚀 FOLLOW THE BIG CALLS - Stock oversold with bullish options flow")
        elif big_puts and ath_distance > -5:
            insights['recommendations'].append("📉 FOLLOW THE BIG PUTS - Stock overbought with bearish options flow")
        elif big_calls and big_puts:
            insights['recommendations'].append("⚖️ MIXED SIGNALS - Both calls and puts active, wait for direction")
        elif not big_calls and not big_puts:
            insights['recommendations'].append("😴 NO UNUSUAL FLOW - Wait for better setup")
        
        return insights

class XAnalystPosts:
    """X (Twitter) analyst posts integration"""
    
    def __init__(self):
        self.analyst_accounts = [
            '@jimcramer', '@elonmusk', '@cathiewood',
            '@chamath', '@naval', '@balajis',
            '@michaeljburry', '@howardmarks', '@raynoldl',
            '@garyblack00', '@davidgokhshtein', '@APompliano'
        ]
    
    def get_analyst_posts(self, symbol: str) -> list:
        """Get simulated analyst posts about the stock"""
        try:
            # Simulate analyst posts (in real implementation, use Twitter API)
            posts = []
            
            # Generate realistic posts based on stock performance
            current_time = datetime.now()
            
            # Bullish posts
            bullish_posts = [
                {
                    'username': '@cathiewood',
                    'avatar': 'CW',
                    'content': f"$SYMBOL showing strong fundamentals. Our ARK models suggest significant upside potential in the next 12 months. The innovation cycle is just beginning. 🚀",
                    'timestamp': current_time - timedelta(hours=2),
                    'likes': 1250,
                    'retweets': 340,
                    'replies': 89,
                    'sentiment': 'bullish'
                },
                {
                    'username': '@chamath',
                    'avatar': 'CP',
                    'content': f"$SYMBOL is undervalued relative to its growth prospects. The market is missing the long-term transformation story. Adding to position. 💎",
                    'timestamp': current_time - timedelta(hours=4),
                    'likes': 890,
                    'retweets': 210,
                    'replies': 45,
                    'sentiment': 'bullish'
                }
            ]
            
            # Bearish posts
            bearish_posts = [
                {
                    'username': '@michaeljburry',
                    'avatar': 'MB',
                    'content': f"$SYMBOL valuation metrics are concerning. The market is pricing in unrealistic growth assumptions. Risk/reward not favorable at current levels. ⚠️",
                    'timestamp': current_time - timedelta(hours=6),
                    'likes': 2100,
                    'retweets': 890,
                    'replies': 234,
                    'sentiment': 'bearish'
                }
            ]
            
            # Neutral posts
            neutral_posts = [
                {
                    'username': '@jimcramer',
                    'avatar': 'JC',
                    'content': f"$SYMBOL earnings next week will be key. Watching for guidance on margins and growth outlook. Could go either way depending on results. 📊",
                    'timestamp': current_time - timedelta(hours=1),
                    'likes': 450,
                    'retweets': 120,
                    'replies': 67,
                    'sentiment': 'neutral'
                }
            ]
            
            # Select posts based on some logic (simplified)
            all_posts = bullish_posts + bearish_posts + neutral_posts
            
            # Replace SYMBOL with actual symbol
            for post in all_posts:
                post['content'] = post['content'].replace('$SYMBOL', f'${symbol}')
                posts.append(post)
            
            # Sort by timestamp (newest first)
            posts.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return posts[:5]  # Return top 5 posts
            
        except Exception as e:
            st.error(f"Error getting analyst posts: {e}")
            return []

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
    
    def analyze_complete(self, stock_data: dict, options_data: dict, x_posts: list):
        """Generate comprehensive AI analysis"""
        if not self.is_available():
            return {"error": "Grok API key not available"}
        
        try:
            prompt = f"""
            Analyze this comprehensive stock data and provide FL0WG0D-style insights:
            
            STOCK DATA:
            Symbol: {stock_data.get('symbol', 'Unknown')}
            Current Price: ${stock_data.get('current_price', 0):.2f}
            Market Cap: ${stock_data.get('market_cap', 0):,.0f}
            P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
            Volatility: {stock_data.get('volatility', 0):.2%}
            ATH Distance: {((stock_data.get('current_price', 0) - stock_data.get('52_week_high', 0)) / stock_data.get('52_week_high', 1)) * 100:.1f}%
            
            OPTIONS FLOW:
            Big Calls: {len(options_data.get('big_calls', []))}
            Big Puts: {len(options_data.get('big_puts', []))}
            
            ANALYST SENTIMENT:
            Recent Posts: {len(x_posts)}
            
            Provide:
            1. FL0WG0D-style analysis combining all data
            2. Whether to follow the big calls or puts
            3. Risk assessment for OTM plays
            4. Price targets based on options flow
            5. Time horizon for the play
            6. Analyst sentiment analysis
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

def display_stock_analysis(stock_data: dict):
    """Display comprehensive stock analysis"""
    if not stock_data:
        return
    
    symbol = stock_data['symbol']
    
    # Header with price info
    st.subheader(f"📊 {symbol} Stock Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Price", f"${stock_data['current_price']:.2f}")
    
    with col2:
        st.metric("Change", f"${stock_data['change']:.2f}", f"{stock_data['change_pct']:.2f}%")
    
    with col3:
        st.metric("Volume", f"{stock_data['volume']:,}")
    
    with col4:
        st.metric("Market Cap", f"${stock_data['market_cap']:,.0f}")
    
    # Price chart
    st.subheader("📈 Price Chart & Technical Analysis")
    
    fig = go.Figure()
    
    # Price line
    fig.add_trace(go.Scatter(
        x=stock_data['history'].index,
        y=stock_data['history']['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # Moving averages
    if stock_data['ma_20'] and not pd.isna(stock_data['ma_20']):
        fig.add_trace(go.Scatter(
            x=stock_data['history'].index,
            y=stock_data['history']['Close'].rolling(window=20).mean(),
            mode='lines',
            name='MA 20',
            line=dict(color='orange', width=1, dash='dash')
        ))
    
    if stock_data['ma_50'] and not pd.isna(stock_data['ma_50']):
        fig.add_trace(go.Scatter(
            x=stock_data['history'].index,
            y=stock_data['history']['Close'].rolling(window=50).mean(),
            mode='lines',
            name='MA 50',
            line=dict(color='red', width=1, dash='dash')
        ))
    
    fig.update_layout(
        title=f"{symbol} Stock Price with Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Valuation metrics
    st.subheader("💰 Valuation Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("P/E Ratio", f"{stock_data['pe_ratio']:.2f}" if stock_data['pe_ratio'] else "N/A")
        st.metric("P/B Ratio", f"{stock_data['pb_ratio']:.2f}" if stock_data['pb_ratio'] else "N/A")
    
    with col2:
        st.metric("Dividend Yield", f"{stock_data['dividend_yield']:.2%}" if stock_data['dividend_yield'] else "N/A")
        st.metric("52W High", f"${stock_data['52_week_high']:.2f}")
    
    with col3:
        st.metric("52W Low", f"${stock_data['52_week_low']:.2f}")
        st.metric("Volatility", f"{stock_data['volatility']:.2%}")
    
    # Company information
    st.subheader("🏢 Company Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Sector", stock_data.get('sector', 'Unknown'))
        st.metric("Industry", stock_data.get('industry', 'Unknown'))
    
    with col2:
        st.metric("Employees", f"{stock_data.get('employees', 0):,}")
        st.metric("Revenue", f"${stock_data.get('revenue', 0):,.0f}")
    
    with col3:
        st.metric("Profit Margin", f"{stock_data.get('profit_margin', 0):.2%}")
        st.metric("Avg Volume", f"{stock_data['avg_volume']:,.0f}")

def display_options_flow_analysis(flow_data: dict):
    """Display enhanced options flow analysis"""
    if not flow_data or 'error' in flow_data:
        st.error("❌ Options flow analysis unavailable")
        return
    
    symbol = flow_data['symbol']
    current_price = flow_data['current_price']
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
    
    # Big calls display with enhanced UI
    if big_calls:
        st.subheader("📞 BIG CALLS DETECTED")
        for call in big_calls:
            st.markdown(f"""
            <div class="big-call">
                <div class="option-header">${call['strike']} CALL</div>
                <div class="option-grid">
                    <div class="option-metric">
                        <div class="metric-label">Volume</div>
                        <div class="metric-value">{call['volume']:,}</div>
                    </div>
                    <div class="option-metric">
                        <div class="metric-label">Open Interest</div>
                        <div class="metric-value">{call['open_interest']:,}</div>
                    </div>
                    <div class="option-metric">
                        <div class="metric-label">Price</div>
                        <div class="metric-value">${call['last_price']:.2f}</div>
                    </div>
                    <div class="option-metric">
                        <div class="metric-label">Potential Return</div>
                        <div class="metric-value">{call['potential_return_pct']:.0f}%</div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 1rem;">
                    <span class="otm-badge">{call['moneyness_pct']:.1f}% OTM</span>
                    <span class="expiry-badge">{call['days_to_expiry']} days</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Big puts display with enhanced UI
    if big_puts:
        st.subheader("📉 BIG PUTS DETECTED")
        for put in big_puts:
            st.markdown(f"""
            <div class="big-put">
                <div class="put-header">${put['strike']} PUT</div>
                <div class="option-grid">
                    <div class="option-metric">
                        <div class="metric-label">Volume</div>
                        <div class="metric-value">{put['volume']:,}</div>
                    </div>
                    <div class="option-metric">
                        <div class="metric-label">Open Interest</div>
                        <div class="metric-value">{put['open_interest']:,}</div>
                    </div>
                    <div class="option-metric">
                        <div class="metric-label">Price</div>
                        <div class="metric-value">${put['last_price']:.2f}</div>
                    </div>
                    <div class="option-metric">
                        <div class="metric-label">Potential Return</div>
                        <div class="metric-value">{put['potential_return_pct']:.0f}%</div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 1rem;">
                    <span class="otm-badge">{put['moneyness_pct']:.1f}% OTM</span>
                    <span class="expiry-badge">{put['days_to_expiry']} days</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Recommendations
    st.subheader("🎯 FL0WG0D RECOMMENDATIONS")
    for rec in insights['recommendations']:
        st.warning(rec)

def display_x_analyst_posts(posts: list):
    """Display X analyst posts"""
    if not posts:
        st.warning("⚠️ No recent analyst posts available")
        return
    
    st.subheader("🐦 X (Twitter) Analyst Posts")
    
    for post in posts:
        sentiment_color = {
            'bullish': '#28a745',
            'bearish': '#dc3545',
            'neutral': '#6c757d'
        }.get(post['sentiment'], '#6c757d')
        
        st.markdown(f"""
        <div class="x-post" style="border-left-color: {sentiment_color};">
            <div class="x-post-header">
                <div class="x-avatar">{post['avatar']}</div>
                <div>
                    <div class="x-username">{post['username']}</div>
                </div>
                <div class="x-timestamp">{post['timestamp'].strftime('%H:%M')}</div>
            </div>
            <div class="x-content">{post['content']}</div>
            <div class="x-engagement">
                <span>❤️ {post['likes']:,}</span>
                <span>🔄 {post['retweets']:,}</span>
                <span>💬 {post['replies']:,}</span>
                <span style="color: {sentiment_color}; font-weight: bold;">{post['sentiment'].upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header with CROC branding
    st.markdown("""
    <div class="croc-branding">
        <h1>🐊 CROC INVESTMENT FUND</h1>
        <h2>COMPLETE STOCK & OPTIONS ANALYSIS 🚀</h2>
        <h3>Stock Analysis + Options Flow + X Analyst Posts + AI Insights</h3>
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
    show_stock_analysis = st.sidebar.checkbox("Stock Analysis", value=True)
    show_options_flow = st.sidebar.checkbox("Options Flow Analysis", value=True)
    show_x_posts = st.sidebar.checkbox("X Analyst Posts", value=True)
    show_ai_analysis = st.sidebar.checkbox("AI Analysis (FL0WG0D Style)", value=True)
    
    # API Status
    st.sidebar.subheader("🔑 API Status")
    
    grok_analyzer = GrokAnalyzer()
    if grok_analyzer.is_available():
        st.sidebar.success("🟢 Grok AI Available")
    else:
        st.sidebar.error("🔴 Grok AI Unavailable")
    
    st.sidebar.info("📊 Yahoo Finance Data")
    st.sidebar.info("🐦 X Analyst Posts")
    
    # Main content
    if st.button("🚀 COMPLETE ANALYSIS", type="primary", use_container_width=True):
        if not symbol:
            st.error("Please enter a stock symbol")
            return
        
        with st.spinner(f"Running complete analysis for {symbol}... This may take a few seconds."):
            # Initialize analyzers
            stock_analyzer = StockAnalyzer()
            options_analyzer = OptionsFlowAnalyzer()
            x_analyst = XAnalystPosts()
            
            # Get stock data
            stock_data = stock_analyzer.get_stock_data(symbol)
            
            if stock_data:
                st.success(f"✅ Complete analysis ready for {symbol}!")
                
                # Stock Analysis
                if show_stock_analysis:
                    display_stock_analysis(stock_data)
                
                # Options Flow Analysis
                options_data = None
                if show_options_flow:
                    options_data = options_analyzer.analyze_big_flow(symbol, stock_data)
                    if 'error' not in options_data:
                        display_options_flow_analysis(options_data)
                    else:
                        st.error(f"Options analysis error: {options_data['error']}")
                
                # X Analyst Posts
                x_posts = []
                if show_x_posts:
                    x_posts = x_analyst.get_analyst_posts(symbol)
                    display_x_analyst_posts(x_posts)
                
                # AI Analysis
                if show_ai_analysis and grok_analyzer.is_available():
                    with st.spinner("🤖 Grok AI analyzing complete data..."):
                        ai_result = grok_analyzer.analyze_complete(stock_data, options_data or {}, x_posts)
                        
                        if 'error' not in ai_result:
                            st.subheader("🤖 AI Analysis (FL0WG0D Style)")
                            st.markdown(f"""
                            <div class="ai-analysis">
                                {ai_result['analysis']}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error(f"AI Analysis Error: {ai_result['error']}")
                
            else:
                st.error(f"❌ Could not fetch data for {symbol}. Please check the symbol and try again.")
                st.info("💡 Try popular symbols like: AAPL, MSFT, GOOGL, TSLA, AMZN, META")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <h4>🐊 CROC Investment Fund</h4>
        <p>Complete Stock & Options Analysis with X Analyst Posts</p>
        <p>Built with Streamlit | Powered by Grok AI & Yahoo Finance</p>
        <p><strong>FOLLOW THE BIG FLOW! 🔥</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
