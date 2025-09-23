# 📊 How to Add More Data Sources to CROC Investment Fund

## 🎯 **Quick Start Guide**

### **Step 1: Choose Your Data Source**
Popular options:
- **Alpha Vantage** - Financial fundamentals, earnings, income statements
- **Polygon.io** - Real-time trades, quotes, news
- **Finnhub** - Company profiles, recommendations, sentiment
- **News API** - Financial news and headlines
- **Reddit API** - Social sentiment from r/investing, r/stocks
- **Twitter API** - Real-time social sentiment
- **SEC EDGAR** - Official SEC filings (10-K, 10-Q, 8-K)
- **FRED** - Economic data (interest rates, inflation)

### **Step 2: Get API Key**
1. Sign up for the service
2. Get your API key
3. Add to your `.env` file:
```bash
ALPHA_VANTAGE_API_KEY=your_key_here
POLYGON_API_KEY=your_key_here
FINNHUB_API_KEY=your_key_here
```

### **Step 3: Add to Streamlit Secrets**
For production deployment:
1. Go to Streamlit Cloud
2. Add secrets:
```toml
ALPHA_VANTAGE_API_KEY = "your_key_here"
POLYGON_API_KEY = "your_key_here"
FINNHUB_API_KEY = "your_key_here"
```

## 🔧 **Implementation Examples**

### **Example 1: Alpha Vantage Integration**

#### **1. Create the Integration Class**
```python
# src/alpha_vantage_integration.py
class AlphaVantageIntegration:
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.base_url = "https://www.alphavantage.co/query"
    
    def get_company_overview(self, symbol: str):
        # Implementation here
        pass
```

#### **2. Add to Your Main App**
```python
# app.py
from src.alpha_vantage_integration import AlphaVantageIntegration

# In your main function:
av = AlphaVantageIntegration()
if av.is_available():
    av_data = av.get_company_overview(symbol)
    display_alpha_vantage_data(av_data, st)
```

#### **3. Add UI Components**
```python
def display_alpha_vantage_data(data, st):
    st.subheader("📊 Alpha Vantage Data")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("PEG Ratio", data.get('peg_ratio', 'N/A'))
    # More metrics...
```

### **Example 2: News API Integration**

#### **1. Create News Source**
```python
class NewsAPISource:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"
    
    def get_news(self, symbol: str):
        params = {
            'q': symbol,
            'apiKey': self.api_key,
            'sortBy': 'publishedAt'
        }
        response = requests.get(f"{self.base_url}/everything", params=params)
        return response.json()
```

#### **2. Display News**
```python
def display_news(news_data, st):
    st.subheader("📰 Latest News")
    for article in news_data['articles'][:5]:
        st.markdown(f"**{article['title']}**")
        st.markdown(f"*{article['source']['name']} - {article['publishedAt']}*")
        st.markdown(article['description'])
        st.markdown("---")
```

## 🚀 **Advanced Data Sources**

### **Real-Time Data Sources**

#### **Polygon.io - Real-Time Trades**
```python
class PolygonRealTime:
    def get_latest_trades(self, symbol: str):
        url = f"https://api.polygon.io/v3/trades/{symbol}"
        params = {'apikey': self.api_key}
        response = requests.get(url, params=params)
        return response.json()
```

#### **Finnhub - Real-Time Quotes**
```python
class FinnhubRealTime:
    def get_quote(self, symbol: str):
        url = f"https://finnhub.io/api/v1/quote"
        params = {'symbol': symbol, 'token': self.api_key}
        response = requests.get(url, params=params)
        return response.json()
```

### **Social Sentiment Sources**

#### **Reddit API Integration**
```python
class RedditSentiment:
    def get_stock_mentions(self, symbol: str):
        # Search r/investing, r/stocks, r/SecurityAnalysis
        # Analyze sentiment of posts
        return {
            "sentiment": "bullish",
            "mentions": 150,
            "top_posts": []
        }
```

#### **Twitter API Integration**
```python
class TwitterSentiment:
    def get_tweets(self, symbol: str):
        # Search for $SYMBOL tweets
        # Analyze sentiment
        return {
            "tweets": [],
            "sentiment": "neutral",
            "volume": 0
        }
```

### **Fundamental Data Sources**

#### **SEC EDGAR - Official Filings**
```python
class SECEdgar:
    def get_recent_filings(self, symbol: str):
        # Get 10-K, 10-Q, 8-K filings
        return {
            "recent_filings": [],
            "10k": None,
            "10q": None
        }
```

#### **FRED - Economic Data**
```python
class FREDData:
    def get_interest_rates(self):
        # Get Fed funds rate, 10-year treasury
        return {
            "fed_funds_rate": 5.25,
            "10_year_treasury": 4.5
        }
```

## 📋 **Step-by-Step Implementation**

### **1. Plan Your Data Source**
- What data do you want?
- How often will you call the API?
- What's the cost/rate limit?
- How will you display it?

### **2. Create the Integration**
```python
# src/your_data_source.py
class YourDataSource:
    def __init__(self):
        self.api_key = os.getenv('YOUR_API_KEY')
        self.base_url = "https://api.yourservice.com"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def get_data(self, symbol: str, data_type: str):
        # Your implementation
        pass
```

### **3. Add to Main App**
```python
# app.py
from src.your_data_source import YourDataSource

# In sidebar:
your_source = YourDataSource()
if your_source.is_available():
    st.sidebar.success("🟢 Your Data Source Available")
else:
    st.sidebar.error("🔴 Your Data Source Unavailable")

# In main analysis:
if show_your_data:
    data = your_source.get_data(symbol, "your_data_type")
    display_your_data(data, st)
```

### **4. Create Display Function**
```python
def display_your_data(data, st):
    if 'error' in data:
        st.error(f"Error: {data['error']}")
        return
    
    st.subheader("📊 Your Data Source")
    # Display your data here
```

### **5. Update Requirements**
```bash
# requirements.txt
requests>=2.28.0
pandas>=1.5.0
# Add any new dependencies
```

### **6. Test Locally**
```bash
# Test your integration
python src/your_data_source.py
```

### **7. Deploy to Streamlit Cloud**
1. Add API key to Streamlit Secrets
2. Push to GitHub
3. Redeploy

## 🎯 **Popular Data Source Combinations**

### **For Fundamental Analysis:**
- Yahoo Finance (basic data)
- Alpha Vantage (detailed fundamentals)
- SEC EDGAR (official filings)
- FRED (economic context)

### **For Technical Analysis:**
- Yahoo Finance (price data)
- Polygon.io (real-time trades)
- Finnhub (technical indicators)

### **For Sentiment Analysis:**
- News API (news sentiment)
- Reddit API (social sentiment)
- Twitter API (real-time sentiment)

### **For Options Analysis:**
- Yahoo Finance (options chains)
- Polygon.io (options trades)
- CBOE (volatility data)

## 💡 **Pro Tips**

### **1. Rate Limiting**
```python
import time

class RateLimitedSource:
    def __init__(self):
        self.last_call = 0
        self.min_interval = 1  # 1 second between calls
    
    def make_request(self):
        now = time.time()
        if now - self.last_call < self.min_interval:
            time.sleep(self.min_interval - (now - self.last_call))
        self.last_call = time.time()
        # Make your API call
```

### **2. Error Handling**
```python
def safe_api_call(self, url, params):
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API call failed: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON response: {str(e)}"}
```

### **3. Caching**
```python
import functools
import time

@functools.lru_cache(maxsize=128)
def cached_api_call(symbol, timestamp):
    # Your API call here
    # Use timestamp to invalidate cache
    pass
```

### **4. Data Validation**
```python
def validate_data(data):
    required_fields = ['symbol', 'price', 'volume']
    for field in required_fields:
        if field not in data:
            return False
    return True
```

## 🚨 **Common Issues & Solutions**

### **Issue 1: API Key Not Working**
- Check if key is correctly added to `.env`
- Verify key is active and has credits
- Check rate limits

### **Issue 2: Rate Limiting**
- Implement delays between calls
- Use caching to reduce API calls
- Consider upgrading to paid tier

### **Issue 3: Data Format Issues**
- Validate API responses
- Handle missing fields gracefully
- Use try/catch blocks

### **Issue 4: Streamlit Cloud Issues**
- Add API keys to Streamlit Secrets
- Check if service is accessible from Streamlit Cloud
- Test locally first

## 🎉 **Ready to Add Data Sources!**

Your CROC Investment Fund is now ready to integrate with any data source. Start with one source, test it thoroughly, then add more!

**Next Steps:**
1. Choose your first data source
2. Get an API key
3. Follow the implementation guide
4. Test and deploy

Happy coding! 🐊🚀
