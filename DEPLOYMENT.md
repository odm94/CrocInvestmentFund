# 🚀 CROC Investment Fund - Deployment Guide

## Streamlit Cloud Deployment

### Step 1: Prepare Your Repository
1. Ensure all files are committed to GitHub
2. Make sure `requirements.txt` is up to date
3. Verify `app.py` is in the root directory

### Step 2: Deploy to Streamlit Cloud
1. Go to [Streamlit Cloud](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Select the repository: `odm94/CrocInvestmentFund`
5. Set main file path: `app.py`

### Step 3: Configure Environment Variables
In Streamlit Cloud dashboard:
1. Go to your app settings
2. Add these secrets:
```
OPENAI_API_KEY = YOUR_OPENAI_API_KEY_HERE
GROK_API_KEY = YOUR_GROK_API_KEY_HERE
```

### Step 4: Your Public URL
After deployment, you'll get a URL like:
```
https://croc-investment-fund.streamlit.app
```

### Step 5: Test Your App
1. Open the public URL
2. Enter a stock symbol (e.g., AAPL)
3. Select analysis mode
4. View comprehensive analysis results

## Local Development

### Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `env_local.txt` to `.env`
4. Add your API keys to `.env`
5. Run: `streamlit run app.py`

### Features
- 🤖 Multi-AI Analysis (Grok, OpenAI, Claude, Gemini, Llama)
- 📊 Advanced Stock Analysis
- 🐦 X (Twitter) Analyst Feeds
- 📈 Technical Indicators
- 💰 Valuation Models
- 🎯 Risk Assessment
- 🌍 ESG Analysis