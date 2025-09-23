"""
Stock Valuation Tool - Streamlit Web Application
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import logging
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.stock_analyzer import StockAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .recommendation-buy {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .recommendation-sell {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
    .recommendation-hold {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # CROC Logo and Header
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <div style="display: inline-block; background: linear-gradient(135deg, #2d5016, #1a3009); padding: 20px; border-radius: 15px; box-shadow: 0 8px 32px rgba(0,0,0,0.3);">
            <div style="color: #c0c0c0; font-family: 'Arial', sans-serif; font-weight: bold;">
                <div style="font-size: 48px; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                    🐊 CROC
                </div>
                <div style="font-size: 18px; color: #e6e6e6; margin-bottom: 15px;">
                    TO THE MOON
                </div>
                <div style="font-size: 16px; color: #b8b8b8;">
                    INVESTMENT FUND
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">📈 Stock Valuation Tool</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Analysis Parameters")
        
        # Stock symbol input
        symbol = st.text_input(
            "Stock Symbol", 
            value="AAPL", 
            help="Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
        ).upper()
        
        # Analysis options
        st.subheader("Analysis Options")
        show_technical = st.checkbox("Show Technical Analysis", value=True)
        show_valuation = st.checkbox("Show Valuation Models", value=True)
        show_financials = st.checkbox("Show Financial Metrics", value=True)
        show_ai_analysis = st.checkbox("Show AI Analysis", value=True)
        
        # Advanced parameters
        with st.expander("Advanced Parameters"):
            risk_free_rate = st.slider("Risk-Free Rate (%)", 0.0, 10.0, 4.0, 0.1)
            market_risk_premium = st.slider("Market Risk Premium (%)", 0.0, 15.0, 6.0, 0.1)
            terminal_growth = st.slider("Terminal Growth Rate (%)", 0.0, 10.0, 3.0, 0.1)
    
    # Main content area
    if st.button("🚀 Analyze Stock", type="primary"):
        if symbol:
            with st.spinner(f"Analyzing {symbol}..."):
                try:
                    # Initialize analyzer
                    analyzer = StockAnalyzer()
                    
                    # Update model parameters
                    analyzer.valuation_models.risk_free_rate = risk_free_rate / 100
                    analyzer.valuation_models.market_risk_premium = market_risk_premium / 100
                    
                    # Perform analysis
                    results = analyzer.analyze_stock(symbol)
                    
                    if 'error' in results:
                        st.error(f"Error: {results['error']}")
                        return
                    
                    # Display results
                    display_analysis_results(results, show_technical, show_valuation, show_financials, show_ai_analysis)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    logger.error(f"Error in main analysis: {e}")
        else:
            st.warning("Please enter a stock symbol")

def display_analysis_results(results, show_technical, show_valuation, show_financials, show_ai_analysis):
    """Display the analysis results"""
    
    symbol = results['symbol']
    stock_info = results['stock_info']
    metrics = results['metrics']
    valuation = results['valuation']
    technical = results['technical_analysis']
    recommendation = results['recommendation']
    
    # Stock overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Price", f"${stock_info.get('current_price', 0):.2f}")
    with col2:
        st.metric("Market Cap", f"${stock_info.get('market_cap', 0):,.0f}")
    with col3:
        st.metric("Sector", stock_info.get('sector', 'N/A'))
    with col4:
        st.metric("Exchange", stock_info.get('exchange', 'N/A'))
    
    # Investment recommendation
    st.markdown("---")
    st.subheader("🎯 Investment Recommendation")
    
    rec_type = recommendation['recommendation']
    rec_score = recommendation['score']
    confidence = recommendation['confidence']
    
    if 'BUY' in rec_type:
        st.markdown(f'<div class="recommendation-buy">', unsafe_allow_html=True)
    elif 'SELL' in rec_type:
        st.markdown(f'<div class="recommendation-sell">', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="recommendation-hold">', unsafe_allow_html=True)
    
    st.markdown(f"""
    **{rec_type}** (Score: {rec_score}, Confidence: {confidence:.1%})
    
    **Key Factors:**
    """)
    
    for factor in recommendation['factors']:
        st.markdown(f"• {factor}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Valuation results
    if show_valuation and valuation:
        st.markdown("---")
        st.subheader("💰 Valuation Analysis")
        
        if 'average_fair_value' in valuation:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Fair Value", 
                    f"${valuation['average_fair_value']:.2f}",
                    delta=f"{valuation.get('upside_potential', 0):.1f}%"
                )
            
            with col2:
                current_price = valuation.get('current_price', 0)
                fair_value = valuation['average_fair_value']
                if current_price > 0:
                    st.metric(
                        "Current Price", 
                        f"${current_price:.2f}",
                        delta=f"{((current_price - fair_value) / fair_value) * 100:.1f}%"
                    )
            
            with col3:
                upside = valuation.get('upside_potential', 0)
                if upside > 0:
                    st.metric("Upside Potential", f"{upside:.1f}%", delta="Positive")
                else:
                    st.metric("Downside Risk", f"{abs(upside):.1f}%", delta="Negative")
        
        # Individual valuation models
        valuation_cols = st.columns(2)
        
        with valuation_cols[0]:
            if 'pe_valuation' in valuation:
                pe_val = valuation['pe_valuation']
                st.subheader("P/E Ratio Valuation")
                st.metric("Current P/E", f"{pe_val.get('current_pe', 0):.1f}")
                st.metric("Fair Value (Industry)", f"${pe_val.get('fair_value_industry', 0):.2f}")
                st.metric("Fair Value (Growth)", f"${pe_val.get('fair_value_growth', 0):.2f}")
        
        with valuation_cols[1]:
            if 'graham_valuation' in valuation:
                graham_val = valuation['graham_valuation']
                st.subheader("Graham Valuation")
                st.metric("Intrinsic Value", f"${graham_val.get('intrinsic_value', 0):.2f}")
                st.metric("Simplified Value", f"${graham_val.get('simplified_value', 0):.2f}")
                st.metric("Margin of Safety Price", f"${graham_val.get('margin_of_safety_price', 0):.2f}")
    
    # Financial metrics
    if show_financials and metrics:
        st.markdown("---")
        st.subheader("📊 Financial Metrics")
        
        # Key ratios
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("P/E Ratio", f"{metrics.get('pe_ratio', 0):.1f}")
            st.metric("PEG Ratio", f"{metrics.get('peg_ratio', 0):.1f}")
        
        with col2:
            st.metric("P/B Ratio", f"{metrics.get('price_to_book', 0):.1f}")
            st.metric("P/S Ratio", f"{metrics.get('price_to_sales', 0):.1f}")
        
        with col3:
            st.metric("ROE", f"{metrics.get('return_on_equity', 0):.1%}")
            st.metric("ROA", f"{metrics.get('return_on_assets', 0):.1%}")
        
        with col4:
            st.metric("Debt/Equity", f"{metrics.get('debt_to_equity', 0):.1f}")
            st.metric("Profit Margin", f"{metrics.get('profit_margin', 0):.1%}")
        
        # Growth metrics
        st.subheader("Growth Metrics")
        growth_cols = st.columns(3)
        
        with growth_cols[0]:
            st.metric("Revenue Growth", f"{metrics.get('revenue_growth', 0):.1%}")
        with growth_cols[1]:
            st.metric("Earnings Growth", f"{metrics.get('earnings_growth', 0):.1%}")
        with growth_cols[2]:
            st.metric("Dividend Yield", f"{metrics.get('dividend_yield', 0):.1%}")
    
    # Technical analysis
    if show_technical and technical:
        st.markdown("---")
        st.subheader("📈 Technical Analysis")
        
        # Technical indicators
        tech_cols = st.columns(4)
        
        with tech_cols[0]:
            st.metric("RSI", f"{technical.get('rsi', 0):.1f}")
        with tech_cols[1]:
            st.metric("Volatility", f"{technical.get('volatility', 0):.1%}")
        with tech_cols[2]:
            ma_20 = technical.get('moving_averages', {}).get('ma_20', 0)
            st.metric("20-day MA", f"${ma_20:.2f}")
        with tech_cols[3]:
            ma_200 = technical.get('moving_averages', {}).get('ma_200', 0)
            st.metric("200-day MA", f"${ma_200:.2f}")
        
        # Price vs Moving Averages
        price_vs_ma = technical.get('price_vs_ma', {})
        if price_vs_ma:
            st.subheader("Price vs Moving Averages")
            ma_cols = st.columns(3)
            
            with ma_cols[0]:
                vs_ma_20 = price_vs_ma.get('vs_ma_20', 0)
                st.metric("vs 20-day MA", f"{vs_ma_20:.1f}%")
            with ma_cols[1]:
                vs_ma_50 = price_vs_ma.get('vs_ma_50', 0)
                st.metric("vs 50-day MA", f"{vs_ma_50:.1f}%")
            with ma_cols[2]:
                vs_ma_200 = price_vs_ma.get('vs_ma_200', 0)
                st.metric("vs 200-day MA", f"{vs_ma_200:.1f}%")
    
    # AI Analysis
    if show_ai_analysis:
        st.markdown("---")
        st.subheader("🤖 AI-Powered Analysis")
        
        # AI Analysis Report
        if 'ai_analysis' in results and 'ai_analysis' in results['ai_analysis']:
            with st.expander("📊 Comprehensive AI Analysis Report", expanded=True):
                st.markdown(results['ai_analysis']['ai_analysis'])
        
        # Investment Thesis
        if 'investment_thesis' in results and 'investment_thesis' in results['investment_thesis']:
            with st.expander("💡 Investment Thesis", expanded=False):
                st.markdown(results['investment_thesis']['investment_thesis'])
        
        # Risk Assessment
        if 'risk_assessment' in results and 'risk_assessment' in results['risk_assessment']:
            with st.expander("⚠️ Risk Assessment", expanded=False):
                st.markdown(results['risk_assessment']['risk_assessment'])
    
    # Analysis summary
    st.markdown("---")
    st.subheader("📋 Analysis Summary")
    
    summary_data = {
        'Metric': [
            'Stock Symbol',
            'Company Name',
            'Current Price',
            'Fair Value',
            'Upside/Downside',
            'Recommendation',
            'Confidence Level',
            'Analysis Date'
        ],
        'Value': [
            symbol,
            stock_info.get('name', 'N/A'),
            f"${stock_info.get('current_price', 0):.2f}",
            f"${valuation.get('average_fair_value', 0):.2f}" if 'average_fair_value' in valuation else 'N/A',
            f"{valuation.get('upside_potential', 0):.1f}%" if 'upside_potential' in valuation else 'N/A',
            recommendation['recommendation'],
            f"{recommendation['confidence']:.1%}",
            results.get('analysis_date', 'N/A')
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
