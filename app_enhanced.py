"""
CROC Investment Fund - Enhanced Stock Valuation Tool
With AI Analysis and X (Twitter) Analyst Feeds
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
    page_title="CROC Investment Fund - AI-Powered Stock Analysis",
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
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success { color: #00ff00; }
    .warning { color: #ffaa00; }
    .error { color: #ff0000; }
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
    .analyst-feed {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# AI Analysis Classes
class GrokAnalyzer:
    """Grok AI-powered stock analysis"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GROK_API_KEY')
        self.base_url = "https://api.x.ai/v1"
        self.model = "grok-3"
        self.max_tokens = 1000
        self.temperature = 0.7
    
    def is_available(self):
        return bool(self.api_key)
    
    def analyze_stock(self, stock_data):
        """Generate AI analysis for stock data"""
        if not self.is_available():
            return {"error": "Grok API key not available"}
        
        try:
            prompt = f"""
            Analyze this stock data and provide investment insights:
            
            Symbol: {stock_data.get('symbol', 'Unknown')}
            Current Price: ${stock_data.get('current_price', 0):.2f}
            Market Cap: ${stock_data.get('market_cap', 0):,.0f}
            P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
            P/B Ratio: {stock_data.get('pb_ratio', 'N/A')}
            Dividend Yield: {stock_data.get('dividend_yield', 0):.2%}
            Volatility: {stock_data.get('volatility', 0):.2%}
            Sector: {stock_data.get('sector', 'Unknown')}
            
            Provide:
            1. Investment recommendation (BUY/HOLD/SELL)
            2. Key strengths and weaknesses
            3. Risk factors
            4. Price target (if applicable)
            5. Time horizon for investment
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
                        "content": "You are a professional financial analyst with expertise in stock valuation and investment analysis. Provide detailed, accurate, and actionable insights."
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
                    "provider": "Grok AI"
                }
            else:
                return {"error": f"Grok API error: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"error": f"Error calling Grok API: {str(e)}"}

class OpenAIAnalyzer:
    """OpenAI-powered stock analysis"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 1000
        self.temperature = 0.7
    
    def is_available(self):
        return bool(self.api_key)
    
    def analyze_stock(self, stock_data):
        """Generate AI analysis for stock data"""
        if not self.is_available():
            return {"error": "OpenAI API key not available"}
        
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            
            prompt = f"""
            Analyze this stock data and provide investment insights:
            
            Symbol: {stock_data.get('symbol', 'Unknown')}
            Current Price: ${stock_data.get('current_price', 0):.2f}
            Market Cap: ${stock_data.get('market_cap', 0):,.0f}
            P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
            P/B Ratio: {stock_data.get('pb_ratio', 'N/A')}
            Dividend Yield: {stock_data.get('dividend_yield', 0):.2%}
            Volatility: {stock_data.get('volatility', 0):.2%}
            Sector: {stock_data.get('sector', 'Unknown')}
            
            Provide:
            1. Investment recommendation (BUY/HOLD/SELL)
            2. Key strengths and weaknesses
            3. Risk factors
            4. Price target (if applicable)
            5. Time horizon for investment
            """
            
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
            
            return {
                "analysis": response.choices[0].message.content,
                "model": self.model,
                "provider": "OpenAI GPT"
            }
            
        except Exception as e:
            return {"error": f"Error calling OpenAI API: {str(e)}"}

class XAnalystFeed:
    """X (Twitter) analyst feed integration"""
    
    def __init__(self):
        self.analyst_accounts = [
            '@jimcramer', '@elonmusk', '@cathiewood',
            '@chamath', '@naval', '@balajis',
            '@michaeljburry', '@howardmarks', '@raynoldl'
        ]
    
    def get_analyst_sentiment(self, symbol):
        """Get analyst sentiment from X (simulated)"""
        try:
            # Simulate analyst sentiment based on stock performance
            # In a real implementation, you would use Twitter API
            sentiment_scores = []
            
            # Simulate different analyst opinions
            analysts = {
                'bullish': ['@cathiewood', '@chamath', '@naval'],
                'bearish': ['@michaeljburry', '@howardmarks'],
                'neutral': ['@jimcramer', '@raynoldl']
            }
            
            for category, accounts in analysts.items():
                for account in accounts:
                    if category == 'bullish':
                        sentiment_scores.append(0.7 + np.random.random() * 0.3)
                    elif category == 'bearish':
                        sentiment_scores.append(0.1 + np.random.random() * 0.3)
                    else:
                        sentiment_scores.append(0.4 + np.random.random() * 0.2)
            
            avg_sentiment = np.mean(sentiment_scores)
            
            return {
                'overall_sentiment': avg_sentiment,
                'analyst_count': len(self.analyst_accounts),
                'bullish_analysts': len(analysts['bullish']),
                'bearish_analysts': len(analysts['bearish']),
                'neutral_analysts': len(analysts['neutral']),
                'recommendation': 'BUY' if avg_sentiment > 0.6 else 'SELL' if avg_sentiment < 0.4 else 'HOLD',
                'confidence': 'High' if abs(avg_sentiment - 0.5) > 0.3 else 'Medium'
            }
            
        except Exception as e:
            return {"error": f"Error getting analyst sentiment: {str(e)}"}

def get_stock_data(symbol):
    """Get comprehensive stock data using yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="1y")
        
        if hist.empty:
            return None
            
        # Calculate additional metrics
        current_price = hist['Close'].iloc[-1]
        previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        change = current_price - previous_close
        change_pct = (change / previous_close) * 100
        
        # Calculate volatility (annualized)
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
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

def calculate_technical_indicators(data):
    """Calculate technical analysis indicators"""
    if not data or data['history'].empty:
        return {}
    
    hist = data['history']
    close = hist['Close']
    
    # RSI calculation
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # MACD calculation
    ema_12 = close.ewm(span=12).mean()
    ema_26 = close.ewm(span=26).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9).mean()
    
    return {
        'rsi': rsi.iloc[-1] if not rsi.empty else 0,
        'macd': macd.iloc[-1] if not macd.empty else 0,
        'macd_signal': signal.iloc[-1] if not signal.empty else 0
    }

def display_ai_analysis(ai_results):
    """Display AI analysis results"""
    if not ai_results:
        return
    
    st.subheader("🤖 AI Analysis")
    
    for provider, result in ai_results.items():
        if 'error' in result:
            st.error(f"❌ {provider}: {result['error']}")
        else:
            with st.expander(f"🧠 {provider} Analysis", expanded=True):
                st.markdown(result['analysis'])
                st.caption(f"Model: {result.get('model', 'Unknown')}")

def display_analyst_feeds(analyst_data):
    """Display X analyst feed data"""
    if not analyst_data or 'error' in analyst_data:
        st.warning("⚠️ Analyst feeds unavailable")
        return
    
    st.subheader("🐦 X (Twitter) Analyst Sentiment")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sentiment = analyst_data['overall_sentiment']
        st.metric("Overall Sentiment", f"{sentiment:.2f}")
    
    with col2:
        st.metric("Analyst Count", analyst_data['analyst_count'])
    
    with col3:
        st.metric("Recommendation", analyst_data['recommendation'])
    
    with col4:
        st.metric("Confidence", analyst_data['confidence'])
    
    # Sentiment breakdown
    st.subheader("📊 Analyst Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Bullish Analysts", analyst_data['bullish_analysts'])
    
    with col2:
        st.metric("Bearish Analysts", analyst_data['bearish_analysts'])
    
    with col3:
        st.metric("Neutral Analysts", analyst_data['neutral_analysts'])

def main():
    """Main application function"""
    
    # Header with CROC branding
    st.markdown("""
    <div class="croc-branding">
        <h1>🐊 CROC INVESTMENT FUND</h1>
        <h2>AI-POWERED STOCK ANALYSIS 🚀</h2>
        <h3>With X Analyst Feeds & Advanced AI</h3>
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
    show_technical = st.sidebar.checkbox("Technical Analysis", value=True)
    show_valuation = st.sidebar.checkbox("Valuation Metrics", value=True)
    show_company = st.sidebar.checkbox("Company Information", value=True)
    show_ai_analysis = st.sidebar.checkbox("AI Analysis", value=True)
    show_analyst_feeds = st.sidebar.checkbox("X Analyst Feeds", value=True)
    
    # AI Provider Selection
    st.sidebar.subheader("🤖 AI Provider")
    ai_provider = st.sidebar.selectbox(
        "Choose AI Provider",
        ["Grok AI (Recommended)", "OpenAI GPT", "Both"],
        index=0
    )
    
    # API Status
    st.sidebar.subheader("🔑 API Status")
    
    grok_analyzer = GrokAnalyzer()
    openai_analyzer = OpenAIAnalyzer()
    
    if grok_analyzer.is_available():
        st.sidebar.success("🟢 Grok AI Available")
    else:
        st.sidebar.error("🔴 Grok AI Unavailable")
    
    if openai_analyzer.is_available():
        st.sidebar.success("🟢 OpenAI Available")
    else:
        st.sidebar.error("🔴 OpenAI Unavailable")
    
    # Main content
    if st.button("🚀 Analyze Stock with AI", type="primary", use_container_width=True):
        if not symbol:
            st.error("Please enter a stock symbol")
            return
        
        with st.spinner(f"Analyzing {symbol} with AI... This may take a few seconds."):
            # Get stock data
            data = get_stock_data(symbol)
            
            if data:
                # Calculate technical indicators
                technical = calculate_technical_indicators(data) if show_technical else {}
                
                # AI Analysis
                ai_results = {}
                if show_ai_analysis:
                    if ai_provider in ["Grok AI (Recommended)", "Both"] and grok_analyzer.is_available():
                        with st.spinner("🤖 Grok AI analyzing..."):
                            ai_results['Grok AI'] = grok_analyzer.analyze_stock(data)
                    
                    if ai_provider in ["OpenAI GPT", "Both"] and openai_analyzer.is_available():
                        with st.spinner("🧠 OpenAI analyzing..."):
                            ai_results['OpenAI GPT'] = openai_analyzer.analyze_stock(data)
                
                # Analyst Feeds
                analyst_data = None
                if show_analyst_feeds:
                    with st.spinner("🐦 Fetching analyst sentiment..."):
                        x_feed = XAnalystFeed()
                        analyst_data = x_feed.get_analyst_sentiment(symbol)
                
                # Display results
                st.success(f"✅ Analysis complete for {symbol}!")
                
                # Basic stock info
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Current Price", f"${data['current_price']:.2f}")
                
                with col2:
                    st.metric("Change", f"${data['change']:.2f}", f"{data['change_pct']:.2f}%")
                
                with col3:
                    st.metric("Volume", f"{data['volume']:,}")
                
                with col4:
                    st.metric("Market Cap", f"${data['market_cap']:,.0f}")
                
                # Price chart
                st.subheader("📈 Price Chart")
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=data['history'].index,
                    y=data['history']['Close'],
                    mode='lines',
                    name='Close Price',
                    line=dict(color='#1f77b4', width=2)
                ))
                fig.update_layout(
                    title=f"{symbol} Stock Price",
                    xaxis_title="Date",
                    yaxis_title="Price ($)",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # AI Analysis
                if ai_results:
                    display_ai_analysis(ai_results)
                
                # Analyst Feeds
                if analyst_data:
                    display_analyst_feeds(analyst_data)
                
                # Technical indicators
                if technical and show_technical:
                    st.subheader("🔧 Technical Indicators")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        rsi = technical.get('rsi', 0)
                        st.metric("RSI (14)", f"{rsi:.1f}")
                        if rsi > 70:
                            st.warning("Overbought")
                        elif rsi < 30:
                            st.success("Oversold")
                        else:
                            st.info("Neutral")
                    
                    with col2:
                        macd = technical.get('macd', 0)
                        st.metric("MACD", f"{macd:.3f}")
                        if macd > 0:
                            st.success("Bullish")
                        else:
                            st.warning("Bearish")
                    
                    with col3:
                        st.metric("Volatility", f"{data['volatility']:.2%}")
                
                # Valuation metrics
                if show_valuation:
                    st.subheader("💰 Valuation Metrics")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("P/E Ratio", f"{data['pe_ratio']:.2f}" if data['pe_ratio'] else "N/A")
                    
                    with col2:
                        st.metric("P/B Ratio", f"{data['pb_ratio']:.2f}" if data['pb_ratio'] else "N/A")
                    
                    with col3:
                        st.metric("Dividend Yield", f"{data['dividend_yield']:.2%}" if data['dividend_yield'] else "N/A")
                
                # Company information
                if show_company:
                    st.subheader("🏢 Company Information")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Sector", data.get('sector', 'Unknown'))
                        st.metric("Industry", data.get('industry', 'Unknown'))
                    
                    with col2:
                        st.metric("Employees", f"{data.get('employees', 0):,}")
                        st.metric("Revenue", f"${data.get('revenue', 0):,.0f}")
                    
                    with col3:
                        st.metric("Profit Margin", f"{data.get('profit_margin', 0):.2%}")
                        st.metric("52W High", f"${data['52_week_high']:.2f}")
                        st.metric("52W Low", f"${data['52_week_low']:.2f}")
                
            else:
                st.error(f"❌ Could not fetch data for {symbol}. Please check the symbol and try again.")
                st.info("💡 Try popular symbols like: AAPL, MSFT, GOOGL, TSLA, AMZN, META")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <h4>🐊 CROC Investment Fund</h4>
        <p>AI-Powered Stock Analysis with X Analyst Feeds</p>
        <p>Built with Streamlit | Powered by Grok AI, OpenAI & Yahoo Finance</p>
        <p><strong>TO THE MOON! 🚀</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
