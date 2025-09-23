# 📈 Stock Valuation Tool

A comprehensive stock analysis and valuation tool that provides detailed financial analysis, multiple valuation models, and investment recommendations.

## 🚀 Features

### 📊 Comprehensive Analysis
- **Real-time Stock Data**: Fetches current stock information from Yahoo Finance
- **Financial Statements**: Income statement, balance sheet, and cash flow analysis
- **Key Metrics**: P/E, P/B, ROE, ROA, debt ratios, and more
- **Technical Analysis**: Moving averages, RSI, Bollinger Bands, volatility

### 💰 Multiple Valuation Models
- **Discounted Cash Flow (DCF)**: Future cash flow projections with terminal value
- **P/E Ratio Valuation**: Industry and growth-adjusted price-to-earnings analysis
- **Dividend Discount Model (DDM)**: Gordon Growth Model for dividend-paying stocks
- **Price-to-Book (P/B) Ratio**: Book value and ROE-adjusted valuations
- **Graham Valuation**: Benjamin Graham's intrinsic value formula

### 🎯 Investment Recommendations
- **Automated Scoring**: Multi-factor analysis with weighted scoring
- **Risk Assessment**: Comprehensive risk evaluation
- **Confidence Levels**: Statistical confidence in recommendations
- **Factor Analysis**: Detailed breakdown of recommendation factors

### 🖥️ Modern Web Interface
- **Streamlit Dashboard**: Beautiful, responsive web interface
- **Interactive Charts**: Real-time data visualization
- **Customizable Parameters**: Adjustable risk rates and growth assumptions
- **Export Capabilities**: Save analysis results

## 📋 Requirements

- Python 3.8+
- Internet connection for data fetching
- Required packages (see requirements.txt)

## 🛠️ Installation

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd stock_valuation_tool
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional):
   ```bash
   cp env_example.txt .env
   # Edit .env with your API keys if needed
   ```

## 🚀 Usage

### Web Application (Recommended)

1. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Enter a stock symbol** (e.g., AAPL, MSFT, GOOGL) in the sidebar

4. **Configure analysis parameters**:
   - Risk-free rate
   - Market risk premium
   - Terminal growth rate

5. **Click "Analyze Stock"** to run the analysis

### Command Line Usage

```python
from src.stock_analyzer import StockAnalyzer

# Initialize analyzer
analyzer = StockAnalyzer()

# Analyze a stock
results = analyzer.analyze_stock('AAPL')

# Access results
print(f"Recommendation: {results['recommendation']['recommendation']}")
print(f"Fair Value: ${results['valuation']['average_fair_value']:.2f}")
```

## 📊 Analysis Components

### 1. Stock Information
- Current price and market cap
- Company name, sector, and industry
- Exchange and currency information

### 2. Financial Metrics
- **Valuation Ratios**: P/E, P/B, P/S, PEG
- **Profitability**: ROE, ROA, profit margins
- **Growth**: Revenue and earnings growth rates
- **Leverage**: Debt-to-equity ratios
- **Dividend**: Dividend yield and payout ratios

### 3. Valuation Models

#### Discounted Cash Flow (DCF)
- Projects future free cash flows
- Calculates terminal value
- Applies appropriate discount rates
- Provides enterprise and equity values

#### P/E Ratio Analysis
- Compares current P/E to industry averages
- Adjusts for growth expectations (PEG ratio)
- Provides fair value estimates

#### Graham Valuation
- Uses Benjamin Graham's intrinsic value formula
- Incorporates earnings and growth assumptions
- Includes margin of safety calculations

### 4. Technical Analysis
- **Moving Averages**: 20, 50, and 200-day averages
- **RSI**: Relative Strength Index for momentum
- **Bollinger Bands**: Price volatility indicators
- **Volatility**: Annualized price volatility

### 5. Investment Recommendation
- **Scoring System**: Multi-factor weighted scoring
- **Recommendation Types**: Strong Buy, Buy, Hold, Sell, Strong Sell
- **Confidence Levels**: Statistical confidence in recommendations
- **Factor Breakdown**: Detailed explanation of recommendation factors

## ⚙️ Configuration

### Risk Parameters
- **Risk-Free Rate**: Default 4% (adjustable)
- **Market Risk Premium**: Default 6% (adjustable)
- **Terminal Growth Rate**: Default 3% (adjustable)

### Data Sources
- **Primary**: Yahoo Finance (yfinance library)
- **Backup**: Alpha Vantage (with API key)
- **Real-time**: Live market data

## 📁 Project Structure

```
stock_valuation_tool/
├── src/
│   ├── __init__.py
│   ├── stock_analyzer.py      # Main analysis engine
│   ├── data_fetcher.py        # Data retrieval
│   └── valuation_models.py    # Valuation calculations
├── data/                      # Data storage
├── tests/                     # Unit tests
├── docs/                      # Documentation
├── app.py                     # Streamlit web app
├── requirements.txt           # Dependencies
├── env_example.txt           # Environment variables template
└── README.md                 # This file
```

## 🔧 Customization

### Adding New Valuation Models

1. **Extend ValuationModels class**:
   ```python
   def new_valuation_model(self, parameters):
       # Your valuation logic here
       return results
   ```

2. **Update comprehensive_valuation method**:
   ```python
   results['new_model'] = self.new_valuation_model(params)
   ```

### Modifying Recommendation Logic

Edit the `_generate_recommendation` method in `stock_analyzer.py` to:
- Add new scoring factors
- Adjust weightings
- Modify recommendation thresholds

### Custom Data Sources

Extend `StockDataFetcher` class to:
- Add new data providers
- Implement custom data processing
- Handle different data formats

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 📈 Example Analysis

### Apple Inc. (AAPL) Analysis
- **Current Price**: $150.00
- **Fair Value**: $165.50
- **Upside Potential**: 10.3%
- **Recommendation**: BUY
- **Confidence**: 75%

**Key Factors**:
- Strong ROE (25.4%)
- Reasonable P/E ratio (18.2)
- Price above 200-day MA
- Low debt levels (0.3)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. It should not be considered as financial advice. Always consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results.

## 🆘 Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Check the documentation
- Review the code comments

## 🔄 Updates

### Version 1.0.0
- Initial release
- Core valuation models
- Streamlit web interface
- Comprehensive analysis features

---

**Happy Investing! 📈💰**
