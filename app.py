"""
CROC Investment Fund - Simplified Stock Valuation Tool
Streamlit Cloud Compatible Version
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

# Page configuration
st.set_page_config(
    page_title="CROC Investment Fund - Stock Valuation Tool",
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
</style>
""", unsafe_allow_html=True)

def get_stock_data(symbol):
    """Get basic stock data using yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="1y")
        
        if hist.empty:
            return None
            
        return {
            'symbol': symbol,
            'info': info,
            'history': hist,
            'current_price': hist['Close'].iloc[-1],
            'previous_close': hist['Close'].iloc[-2] if len(hist) > 1 else hist['Close'].iloc[-1],
            'volume': hist['Volume'].iloc[-1],
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'pb_ratio': info.get('priceToBook', 0),
            'dividend_yield': info.get('dividendYield', 0),
            '52_week_high': info.get('fiftyTwoWeekHigh', 0),
            '52_week_low': info.get('fiftyTwoWeekLow', 0),
            'avg_volume': hist['Volume'].mean(),
            'volatility': hist['Close'].pct_change().std() * np.sqrt(252)
        }
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

def calculate_valuation_metrics(data):
    """Calculate basic valuation metrics"""
    if not data:
        return {}
    
    current_price = data['current_price']
    pe_ratio = data['pe_ratio']
    pb_ratio = data['pb_ratio']
    dividend_yield = data['dividend_yield']
    
    # Basic valuation calculations
    metrics = {}
    
    if pe_ratio and pe_ratio > 0:
        # P/E based valuation (simplified)
        fair_value_pe = 15  # Conservative P/E
        metrics['pe_fair_value'] = current_price * (fair_value_pe / pe_ratio)
        metrics['pe_undervalued'] = current_price < metrics['pe_fair_value']
    
    if pb_ratio and pb_ratio > 0:
        # P/B based valuation
        fair_value_pb = 1.5  # Conservative P/B
        metrics['pb_fair_value'] = current_price * (fair_value_pb / pb_ratio)
        metrics['pb_undervalued'] = current_price < metrics['pb_fair_value']
    
    # Overall recommendation
    undervalued_count = sum([metrics.get('pe_undervalued', False), metrics.get('pb_undervalued', False)])
    if undervalued_count >= 1:
        metrics['recommendation'] = 'BUY'
        metrics['confidence'] = 'High' if undervalued_count == 2 else 'Medium'
    else:
        metrics['recommendation'] = 'HOLD'
        metrics['confidence'] = 'Low'
    
    return metrics

def display_stock_analysis(data, metrics):
    """Display stock analysis results"""
    if not data:
        st.error("No data available for analysis")
        return
    
    symbol = data['symbol']
    current_price = data['current_price']
    previous_close = data['previous_close']
    change = current_price - previous_close
    change_pct = (change / previous_close) * 100
    
    # Header with price info
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Price", f"${current_price:.2f}")
    
    with col2:
        st.metric("Change", f"${change:.2f}", f"{change_pct:.2f}%")
    
    with col3:
        st.metric("Volume", f"{data['volume']:,}")
    
    with col4:
        st.metric("Market Cap", f"${data['market_cap']:,.0f}")
    
    # Price chart
    st.subheader("📈 Price Chart (1 Year)")
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
    
    # Valuation metrics
    st.subheader("💰 Valuation Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("P/E Ratio", f"{data['pe_ratio']:.2f}" if data['pe_ratio'] else "N/A")
        st.metric("P/B Ratio", f"{data['pb_ratio']:.2f}" if data['pb_ratio'] else "N/A")
    
    with col2:
        st.metric("Dividend Yield", f"{data['dividend_yield']:.2%}" if data['dividend_yield'] else "N/A")
        st.metric("52W High", f"${data['52_week_high']:.2f}")
    
    with col3:
        st.metric("52W Low", f"${data['52_week_low']:.2f}")
        st.metric("Volatility", f"{data['volatility']:.2%}")
    
    # Investment recommendation
    if metrics:
        st.subheader("🎯 Investment Recommendation")
        
        recommendation = metrics.get('recommendation', 'HOLD')
        confidence = metrics.get('confidence', 'Low')
        
        if recommendation == 'BUY':
            st.success(f"🟢 **{recommendation}** - Confidence: {confidence}")
        elif recommendation == 'SELL':
            st.error(f"🔴 **{recommendation}** - Confidence: {confidence}")
        else:
            st.warning(f"🟡 **{recommendation}** - Confidence: {confidence}")
        
        # Fair value estimates
        if 'pe_fair_value' in metrics:
            st.info(f"P/E Fair Value: ${metrics['pe_fair_value']:.2f}")
        if 'pb_fair_value' in metrics:
            st.info(f"P/B Fair Value: ${metrics['pb_fair_value']:.2f}")

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🐊 CROC Investment Fund</h1>', unsafe_allow_html=True)
    st.markdown("### Advanced Stock Valuation & Analysis Tool")
    
    # Sidebar
    st.sidebar.header("🔧 Analysis Settings")
    
    # Stock symbol input
    symbol = st.sidebar.text_input(
        "Enter Stock Symbol",
        value="AAPL",
        help="Enter a valid stock symbol (e.g., AAPL, MSFT, GOOGL)"
    ).upper()
    
    # Analysis options
    st.sidebar.subheader("📊 Analysis Options")
    show_technical = st.sidebar.checkbox("Technical Analysis", value=True)
    show_valuation = st.sidebar.checkbox("Valuation Metrics", value=True)
    show_financials = st.sidebar.checkbox("Financial Ratios", value=True)
    
    # API Status
    st.sidebar.subheader("🔑 API Status")
    st.sidebar.info("✅ Basic Analysis Available")
    st.sidebar.warning("⚠️ AI Analysis Requires API Keys")
    
    # Main content
    if st.button("🚀 Analyze Stock", type="primary"):
        if not symbol:
            st.error("Please enter a stock symbol")
            return
        
        with st.spinner(f"Analyzing {symbol}..."):
            # Get stock data
            data = get_stock_data(symbol)
            
            if data:
                # Calculate valuation metrics
                metrics = calculate_valuation_metrics(data)
                
                # Display analysis
                display_stock_analysis(data, metrics)
                
                # Additional analysis sections
                if show_technical:
                    st.subheader("📊 Technical Analysis")
                    st.info("Technical analysis features coming soon!")
                
                if show_valuation:
                    st.subheader("💰 Advanced Valuation")
                    st.info("Advanced valuation models coming soon!")
                
                if show_financials:
                    st.subheader("📋 Financial Ratios")
                    st.info("Detailed financial ratios coming soon!")
            else:
                st.error(f"Could not fetch data for {symbol}. Please check the symbol and try again.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🐊 CROC Investment Fund - Professional Stock Analysis Tool</p>
        <p>Built with Streamlit | Powered by Yahoo Finance</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
