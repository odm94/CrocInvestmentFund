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
from src.enhanced_analyzer import EnhancedStockAnalyzer
from src.ultimate_analyzer import UltimateStockAnalyzer
from src.multi_ai_analyzer import MultiAIAnalyzer
from src.x_analyst_feed import XAnalystFeed

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
        
        # AI Status
        st.subheader("🤖 AI Status")
        try:
            from src.hybrid_ai_analyzer import HybridAIAnalyzer
            ai_status = HybridAIAnalyzer().get_ai_status()
            
            col1, col2 = st.columns(2)
            with col1:
                if ai_status['grok_available']:
                    st.success("🟢 Grok AI")
                else:
                    st.error("🔴 Grok AI")
            
            with col2:
                if ai_status['openai_available']:
                    st.warning("🟡 OpenAI (Quota)")
                else:
                    st.error("🔴 OpenAI")
            
            st.caption(f"Current: {ai_status['current_ai']}")
        except:
            st.info("AI Status: Checking...")
        
        st.markdown("---")
        
        # Stock symbol input
        symbol = st.text_input(
            "Stock Symbol", 
            value="AAPL", 
            help="Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
        ).upper()
        
        # Analysis options
        st.subheader("Analysis Options")
        analysis_mode = st.selectbox(
            "Analysis Mode",
            ["Basic Analysis", "Enhanced Analysis", "Ultimate Analysis", "Multi-AI Analysis (All Models + X Feeds)"],
            index=3
        )
        
        show_technical = st.checkbox("Show Technical Analysis", value=True)
        show_valuation = st.checkbox("Show Valuation Models", value=True)
        show_financials = st.checkbox("Show Financial Metrics", value=True)
        show_ai_analysis = st.checkbox("Show AI Analysis", value=True)
        
        # Initialize all variables
        show_analyst_data = False
        show_options_flow = False
        show_institutional = False
        show_sentiment = False
        show_advanced_technical = False
        show_sector_analysis = False
        show_peer_comparison = False
        show_earnings_analysis = False
        show_risk_analysis = False
        show_esg_analysis = False
        show_x_feeds = False
        show_social_sentiment = False
        show_multi_ai_consensus = False
        
        if analysis_mode in ["Enhanced Analysis", "Ultimate Analysis", "Multi-AI Analysis (All Models + X Feeds)"]:
            show_analyst_data = st.checkbox("Show Analyst Ratings & Price Targets", value=True)
            show_options_flow = st.checkbox("Show Options Flow & Unusual Activity", value=True)
            show_institutional = st.checkbox("Show Institutional Holdings", value=True)
            show_sentiment = st.checkbox("Show News Sentiment", value=True)
            show_advanced_technical = st.checkbox("Show Advanced Technical Indicators", value=True)
        
        if analysis_mode == "Ultimate Analysis":
            show_sector_analysis = st.checkbox("Show Sector & Industry Analysis", value=True)
            show_peer_comparison = st.checkbox("Show Peer Company Comparison", value=True)
            show_earnings_analysis = st.checkbox("Show Earnings Analysis & Guidance", value=True)
            show_risk_analysis = st.checkbox("Show Advanced Risk Metrics", value=True)
            show_esg_analysis = st.checkbox("Show ESG Analysis", value=True)
        
        if analysis_mode == "Multi-AI Analysis (All Models + X Feeds)":
            show_sector_analysis = st.checkbox("Show Sector & Industry Analysis", value=True)
            show_peer_comparison = st.checkbox("Show Peer Company Comparison", value=True)
            show_earnings_analysis = st.checkbox("Show Earnings Analysis & Guidance", value=True)
            show_risk_analysis = st.checkbox("Show Advanced Risk Metrics", value=True)
            show_esg_analysis = st.checkbox("Show ESG Analysis", value=True)
            show_x_feeds = st.checkbox("Show X (Twitter) Analyst Feeds", value=True)
            show_social_sentiment = st.checkbox("Show Social Media Sentiment", value=True)
            show_multi_ai_consensus = st.checkbox("Show Multi-AI Consensus", value=True)
        
        # AI Provider Selection
        st.subheader("🤖 AI Analysis Provider")
        ai_provider = st.selectbox(
            "Choose AI Provider",
            ["Grok AI (Recommended)", "OpenAI GPT", "Auto (Best Available)"],
            index=0,
            help="Grok AI provides unique insights and analysis style"
        )
        
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
                    # Initialize analyzer based on mode
                    if analysis_mode == "Multi-AI Analysis (All Models + X Feeds)":
                        # Use multi-AI analyzer for comprehensive analysis
                        analyzer = MultiAIAnalyzer()
                        # Get basic stock data first
                        basic_analyzer = StockAnalyzer()
                        basic_data = basic_analyzer.analyze_stock(symbol)
                        # Perform multi-AI analysis
                        results = analyzer.generate_comprehensive_analysis(basic_data)
                    elif analysis_mode == "Ultimate Analysis":
                        analyzer = UltimateStockAnalyzer()
                        # Update model parameters
                        analyzer.valuation_models.risk_free_rate = risk_free_rate / 100
                        analyzer.valuation_models.market_risk_premium = market_risk_premium / 100
                        # Configure AI provider
                        if ai_provider == "Grok AI (Recommended)":
                            analyzer.ai_analyzer.set_ai_preference(use_grok=True)
                        elif ai_provider == "OpenAI GPT":
                            analyzer.ai_analyzer.set_ai_preference(use_grok=False)
                        # Perform ultimate analysis
                        results = analyzer.analyze_stock_ultimate(symbol)
                    elif analysis_mode == "Enhanced Analysis":
                        analyzer = EnhancedStockAnalyzer()
                        # Update model parameters
                        analyzer.valuation_models.risk_free_rate = risk_free_rate / 100
                        analyzer.valuation_models.market_risk_premium = market_risk_premium / 100
                        # Configure AI provider
                        if ai_provider == "Grok AI (Recommended)":
                            analyzer.ai_analyzer.set_ai_preference(use_grok=True)
                        elif ai_provider == "OpenAI GPT":
                            analyzer.ai_analyzer.set_ai_preference(use_grok=False)
                        # Perform enhanced analysis
                        results = analyzer.analyze_stock_enhanced(symbol)
                    else:
                        analyzer = StockAnalyzer()
                        # Update model parameters
                        analyzer.valuation_models.risk_free_rate = risk_free_rate / 100
                        analyzer.valuation_models.market_risk_premium = market_risk_premium / 100
                        # Configure AI provider
                        if ai_provider == "Grok AI (Recommended)":
                            analyzer.ai_analyzer.set_ai_preference(use_grok=True)
                        elif ai_provider == "OpenAI GPT":
                            analyzer.ai_analyzer.set_ai_preference(use_grok=False)
                        # Perform basic analysis
                        results = analyzer.analyze_stock(symbol)
                    
                    if 'error' in results:
                        st.error(f"Error: {results['error']}")
                        return
                    
                    # Display results
                    if analysis_mode == "Multi-AI Analysis (All Models + X Feeds)":
                        display_multi_ai_analysis_results(
                            results, show_technical, show_valuation, show_financials, show_ai_analysis,
                            show_analyst_data, show_options_flow, show_institutional, show_sentiment, show_advanced_technical,
                            show_sector_analysis, show_peer_comparison, show_earnings_analysis, show_risk_analysis, show_esg_analysis,
                            show_x_feeds, show_social_sentiment, show_multi_ai_consensus
                        )
                    elif analysis_mode == "Ultimate Analysis":
                        display_ultimate_analysis_results(
                            results, show_technical, show_valuation, show_financials, show_ai_analysis,
                            show_analyst_data, show_options_flow, show_institutional, show_sentiment, show_advanced_technical,
                            show_sector_analysis, show_peer_comparison, show_earnings_analysis, show_risk_analysis, show_esg_analysis
                        )
                    elif analysis_mode == "Enhanced Analysis":
                        display_enhanced_analysis_results(
                            results, show_technical, show_valuation, show_financials, show_ai_analysis,
                            show_analyst_data, show_options_flow, show_institutional, show_sentiment, show_advanced_technical
                        )
                    else:
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

def display_enhanced_analysis_results(results, show_technical, show_valuation, show_financials, show_ai_analysis,
                                    show_analyst_data, show_options_flow, show_institutional, show_sentiment, show_advanced_technical):
    """Display enhanced analysis results with all new features"""
    
    symbol = results['symbol']
    stock_info = results['stock_info']
    metrics = results['metrics']
    valuation = results['valuation']
    technical = results['technical_analysis']
    recommendation = results.get('enhanced_recommendation', results.get('recommendation', {}))
    
    # Enhanced recommendation display
    st.markdown("---")
    st.subheader("🎯 Enhanced Investment Recommendation")
    
    rec_type = recommendation.get('enhanced_recommendation', recommendation.get('recommendation', 'HOLD'))
    rec_score = recommendation.get('enhanced_score', recommendation.get('score', 0))
    confidence = recommendation.get('confidence_level', recommendation.get('confidence', 0))
    
    if 'BUY' in rec_type:
        st.markdown(f'<div class="recommendation-buy">', unsafe_allow_html=True)
    elif 'SELL' in rec_type:
        st.markdown(f'<div class="recommendation-sell">', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="recommendation-hold">', unsafe_allow_html=True)
    
    st.markdown(f"""
    **{rec_type}** (Enhanced Score: {rec_score:.1f}, Confidence: {confidence:.1%})
    
    **Enhanced Analysis Factors:**
    """)
    
    for factor in recommendation.get('enhanced_factors', recommendation.get('factors', [])):
        st.markdown(f"• {factor}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data sources used
    data_sources = recommendation.get('data_sources_used', [])
    if data_sources:
        st.markdown(f"**Data Sources:** {', '.join(data_sources)}")
    
    # Analyst Data Section
    if show_analyst_data and 'analyst_insights' in results:
        st.markdown("---")
        st.subheader("📊 Analyst Ratings & Price Targets")
        
        analyst_insights = results['analyst_insights']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Consensus Rating", analyst_insights.get('consensus_rating', 'N/A'))
        with col2:
            st.metric("Consensus Score", f"{analyst_insights.get('consensus_score', 0):.1f}/5")
        with col3:
            st.metric("Price Target Upside", f"{analyst_insights.get('price_target_upside', 0):.1f}%")
        with col4:
            st.metric("Analyst Confidence", f"{analyst_insights.get('analyst_confidence', 0):.1%}")
    
    # Options Flow Section
    if show_options_flow and 'options_insights' in results:
        st.markdown("---")
        st.subheader("📈 Options Flow & Unusual Activity")
        
        options_insights = results['options_insights']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Put/Call Ratio", f"{options_insights.get('put_call_ratio', 0):.2f}")
        with col2:
            st.metric("Options Sentiment", options_insights.get('options_sentiment', 'N/A'))
        with col3:
            st.metric("Unusual Activity", options_insights.get('unusual_activity', 0))
        with col4:
            st.metric("Options Signal", options_insights.get('options_flow_signal', 'N/A'))
    
    # Institutional Data Section
    if show_institutional and 'institutional_insights' in results:
        st.markdown("---")
        st.subheader("🏛️ Institutional Holdings & Smart Money")
        
        institutional_insights = results['institutional_insights']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Institutional Ownership", f"{institutional_insights.get('institutional_ownership', 0):.1f}%")
        with col2:
            st.metric("Institutional Support", institutional_insights.get('institutional_support', 'N/A'))
        with col3:
            st.metric("Smart Money Signal", institutional_insights.get('smart_money_signal', 'N/A'))
        with col4:
            st.metric("Number of Institutions", institutional_insights.get('number_of_institutions', 0))
    
    # Sentiment Analysis Section
    if show_sentiment and 'sentiment_insights' in results:
        st.markdown("---")
        st.subheader("📰 News Sentiment & Media Buzz")
        
        sentiment_insights = results['sentiment_insights']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("News Sentiment", f"{sentiment_insights.get('news_sentiment', 0):.2f}")
        with col2:
            st.metric("Sentiment Trend", sentiment_insights.get('sentiment_trend', 'N/A'))
        with col3:
            st.metric("Media Buzz", sentiment_insights.get('media_buzz', 0))
        with col4:
            st.metric("Sentiment Signal", sentiment_insights.get('sentiment_signal', 'N/A'))
    
    # Advanced Technical Section
    if show_advanced_technical and 'advanced_technical_insights' in results:
        st.markdown("---")
        st.subheader("📊 Advanced Technical Indicators")
        
        technical_insights = results['advanced_technical_insights']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("MACD Signal", technical_insights.get('macd_signal', 'N/A'))
        with col2:
            st.metric("Stochastic Signal", technical_insights.get('stochastic_signal', 'N/A'))
        with col3:
            st.metric("Volume Signal", technical_insights.get('volume_signal', 'N/A'))
        with col4:
            st.metric("Technical Momentum", f"{technical_insights.get('technical_momentum', 0):.2f}")
    
    # Call the basic display function for remaining sections
    display_analysis_results(results, show_technical, show_valuation, show_financials, show_ai_analysis)

def display_ultimate_analysis_results(results, show_technical, show_valuation, show_financials, show_ai_analysis,
                                    show_analyst_data, show_options_flow, show_institutional, show_sentiment, show_advanced_technical,
                                    show_sector_analysis, show_peer_comparison, show_earnings_analysis, show_risk_analysis, show_esg_analysis):
    """Display ultimate analysis results with all advanced features"""
    
    symbol = results['symbol']
    stock_info = results['stock_info']
    recommendation = results.get('ultimate_recommendation', results.get('enhanced_recommendation', results.get('recommendation', {})))
    
    # Ultimate recommendation display
    st.markdown("---")
    st.subheader("🎯 ULTIMATE Investment Recommendation")
    
    rec_type = recommendation.get('ultimate_recommendation', recommendation.get('enhanced_recommendation', recommendation.get('recommendation', 'HOLD')))
    rec_score = recommendation.get('ultimate_score', recommendation.get('enhanced_score', recommendation.get('score', 0)))
    confidence = recommendation.get('confidence_level', recommendation.get('confidence', 0))
    
    if 'BUY' in rec_type:
        st.markdown(f'<div class="recommendation-buy">', unsafe_allow_html=True)
    elif 'SELL' in rec_type:
        st.markdown(f'<div class="recommendation-sell">', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="recommendation-hold">', unsafe_allow_html=True)
    
    st.markdown(f"""
    **{rec_type}** (Ultimate Score: {rec_score:.1f}, Confidence: {confidence:.1%})
    
    **Ultimate Analysis Factors:**
    """)
    
    for factor in recommendation.get('ultimate_factors', recommendation.get('enhanced_factors', recommendation.get('factors', []))):
        st.markdown(f"• {factor}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data sources used
    data_sources = recommendation.get('data_sources_used', [])
    if data_sources:
        st.markdown(f"**Data Sources:** {', '.join(data_sources)}")
        st.markdown(f"**Analysis Depth:** {recommendation.get('analysis_depth', 'Ultimate Comprehensive')}")
    
    # Sector Analysis Section
    if show_sector_analysis and 'sector_analysis' in results:
        st.markdown("---")
        st.subheader("🏭 Sector & Industry Analysis")
        
        sector_analysis = results['sector_analysis']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Sector", sector_analysis.get('sector', 'N/A'))
        with col2:
            st.metric("vs Sector Performance", f"{sector_analysis.get('vs_sector_performance', 0):.1f}%")
        with col3:
            st.metric("vs Market Performance", f"{sector_analysis.get('vs_market_performance', 0):.1f}%")
        with col4:
            st.metric("Relative Volatility", f"{sector_analysis.get('relative_volatility', 0):.2f}")
    
    # Peer Comparison Section
    if show_peer_comparison and 'peer_analysis' in results:
        st.markdown("---")
        st.subheader("👥 Peer Company Comparison")
        
        peer_analysis = results['peer_analysis']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Peer Count", peer_analysis.get('peer_count', 0))
        with col2:
            st.metric("Average P/E Ratio", f"{peer_analysis.get('average_pe_ratio', 0):.1f}")
        with col3:
            st.metric("Average Return 1Y", f"{peer_analysis.get('average_return_1y', 0):.1f}%")
        with col4:
            st.metric("Peer Analysis", peer_analysis.get('peer_analysis', 'N/A'))
    
    # Earnings Analysis Section
    if show_earnings_analysis and 'earnings_analysis' in results:
        st.markdown("---")
        st.subheader("📊 Earnings Analysis & Guidance")
        
        earnings_analysis = results['earnings_analysis']
        earnings_guidance = results.get('earnings_guidance', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            surprises = earnings_analysis.get('earnings_surprises', {})
            st.metric("Avg Surprise %", f"{surprises.get('average_surprise_pct', 0):.1f}%")
        with col2:
            st.metric("Surprise Consistency", f"{surprises.get('surprise_consistency', 0):.1%}")
        with col3:
            st.metric("Earnings Quality", earnings_analysis.get('earnings_quality', 'N/A'))
        with col4:
            st.metric("Guidance Sentiment", earnings_guidance.get('guidance_sentiment', 'N/A'))
    
    # Risk Analysis Section
    if show_risk_analysis and 'risk_analysis' in results:
        st.markdown("---")
        st.subheader("⚠️ Advanced Risk Metrics")
        
        risk_analysis = results['risk_analysis']
        var_metrics = risk_analysis.get('var_metrics', {})
        risk_adjusted = risk_analysis.get('risk_adjusted_returns', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("VaR 95%", f"{var_metrics.get('var_95_historical', 0):.2%}")
        with col2:
            st.metric("Max Drawdown", f"{var_metrics.get('maximum_drawdown', 0):.2%}")
        with col3:
            st.metric("Sharpe Ratio", f"{risk_adjusted.get('sharpe_ratio', 0):.2f}")
        with col4:
            st.metric("Risk Rating", risk_adjusted.get('risk_adjusted_rating', 'N/A'))
    
    # ESG Analysis Section
    if show_esg_analysis and 'risk_analysis' in results:
        st.markdown("---")
        st.subheader("🌱 ESG Analysis")
        
        esg_analysis = results['risk_analysis'].get('esg_analysis', {})
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("ESG Rating", esg_analysis.get('esg_rating', 'N/A'))
        with col2:
            st.metric("Environmental Score", esg_analysis.get('environmental_score', 0))
        with col3:
            st.metric("Social Score", esg_analysis.get('social_score', 0))
        with col4:
            st.metric("Governance Score", esg_analysis.get('governance_score', 0))
    
    # Call the enhanced display function for remaining sections
    display_enhanced_analysis_results(
        results, show_technical, show_valuation, show_financials, show_ai_analysis,
        show_analyst_data, show_options_flow, show_institutional, show_sentiment, show_advanced_technical
    )

def display_multi_ai_analysis_results(results, show_technical, show_valuation, show_financials, show_ai_analysis,
                                    show_analyst_data, show_options_flow, show_institutional, show_sentiment, show_advanced_technical,
                                    show_sector_analysis, show_peer_comparison, show_earnings_analysis, show_risk_analysis, show_esg_analysis,
                                    show_x_feeds, show_social_sentiment, show_multi_ai_consensus):
    """Display multi-AI analysis results with all AI models and X feeds"""
    
    symbol = results.get('symbol', 'Unknown')
    
    # Multi-AI Consensus Analysis
    if show_multi_ai_consensus and 'consensus_analysis' in results:
        st.markdown("---")
        st.subheader("🤖 Multi-AI Consensus Analysis")
        
        consensus = results['consensus_analysis']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Consensus Recommendation", consensus.get('consensus_recommendation', 'N/A'))
        with col2:
            st.metric("Confidence Score", f"{consensus.get('confidence_score', 0):.1%}")
        with col3:
            st.metric("AI Agreement", f"{consensus.get('ai_agreement', 0):.1%}")
        with col4:
            st.metric("Data Sources", consensus.get('data_sources_used', 0))
        
        # Display consensus factors
        factors = consensus.get('consensus_factors', [])
        if factors:
            st.markdown("**Consensus Factors:**")
            for factor in factors:
                st.markdown(f"• {factor}")
    
    # Individual AI Analyses
    if 'ai_analyses' in results:
        st.markdown("---")
        st.subheader("🤖 Individual AI Model Analyses")
        
        ai_analyses = results['ai_analyses']
        for provider, analysis in ai_analyses.items():
            if 'error' not in analysis:
                with st.expander(f"{provider.upper()} Analysis"):
                    if 'ai_analysis' in analysis:
                        st.markdown(analysis['ai_analysis'])
                    if 'investment_thesis' in analysis:
                        st.markdown("**Investment Thesis:**")
                        st.markdown(analysis['investment_thesis'])
                    if 'risk_assessment' in analysis:
                        st.markdown("**Risk Assessment:**")
                        st.markdown(analysis['risk_assessment'])
    
    # X (Twitter) Feeds
    if show_x_feeds and 'analyst_feeds' in results:
        st.markdown("---")
        st.subheader("🐦 X (Twitter) Analyst Feeds")
        
        analyst_feeds = results['analyst_feeds']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("X Mentions", analyst_feeds.get('x_analysts', {}).get('mentions', 0))
        with col2:
            st.metric("Analyst Sentiment", analyst_feeds.get('consensus_rating', 'N/A'))
        with col3:
            st.metric("Analyst Confidence", f"{analyst_feeds.get('analyst_confidence', 0):.1%}")
        with col4:
            st.metric("Price Targets", len(analyst_feeds.get('price_targets', [])))
    
    # Social Media Sentiment
    if show_social_sentiment and 'social_sentiment' in results:
        st.markdown("---")
        st.subheader("📱 Social Media Sentiment")
        
        social_sentiment = results['social_sentiment']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Overall Sentiment", f"{social_sentiment.get('overall_social_sentiment', 0):.2f}")
        with col2:
            st.metric("Twitter Sentiment", f"{social_sentiment.get('twitter_sentiment', 0):.2f}")
        with col3:
            st.metric("Reddit Sentiment", f"{social_sentiment.get('reddit_sentiment', 0):.2f}")
        with col4:
            st.metric("YouTube Sentiment", f"{social_sentiment.get('youtube_sentiment', 0):.2f}")
    
    # AI Provider Status
    st.markdown("---")
    st.subheader("🤖 AI Provider Status")
    
    try:
        multi_analyzer = MultiAIAnalyzer()
        ai_status = multi_analyzer.get_ai_status()
        feed_status = multi_analyzer.get_feed_status()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**AI Models:**")
            for provider, status in ai_status.items():
                if status == 'Available':
                    st.success(f"🟢 {provider.upper()}")
                else:
                    st.error(f"🔴 {provider.upper()}")
        
        with col2:
            st.markdown("**Data Feeds:**")
            for feed, status in feed_status.items():
                if status == 'Available':
                    st.success(f"🟢 {feed.upper()}")
                else:
                    st.error(f"🔴 {feed.upper()}")
    
    except Exception as e:
        st.error(f"Error getting AI status: {e}")
    
    # Call the ultimate display function for remaining sections
    display_ultimate_analysis_results(
        results, show_technical, show_valuation, show_financials, show_ai_analysis,
        show_analyst_data, show_options_flow, show_institutional, show_sentiment, show_advanced_technical,
        show_sector_analysis, show_peer_comparison, show_earnings_analysis, show_risk_analysis, show_esg_analysis
    )

if __name__ == "__main__":
    main()
