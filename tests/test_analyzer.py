"""
Unit tests for Stock Analyzer
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.stock_analyzer import StockAnalyzer
from src.valuation_models import ValuationModels
from src.data_fetcher import StockDataFetcher

class TestValuationModels(unittest.TestCase):
    """Test valuation models"""
    
    def setUp(self):
        self.valuation = ValuationModels()
    
    def test_dcf_valuation(self):
        """Test DCF valuation calculation"""
        fcf = [1000000, 1100000, 1200000, 1300000, 1400000]
        result = self.valuation.dcf_valuation(fcf, terminal_growth_rate=0.03, discount_rate=0.10)
        
        self.assertIn('enterprise_value', result)
        self.assertIn('equity_value_per_share', result)
        self.assertGreater(result['enterprise_value'], 0)
    
    def test_pe_ratio_valuation(self):
        """Test P/E ratio valuation"""
        result = self.valuation.pe_ratio_valuation(
            current_price=100,
            earnings_per_share=5,
            industry_pe=20
        )
        
        self.assertIn('current_pe', result)
        self.assertIn('fair_value_industry', result)
        self.assertEqual(result['current_pe'], 20.0)
        self.assertEqual(result['fair_value_industry'], 100.0)
    
    def test_graham_valuation(self):
        """Test Graham valuation"""
        result = self.valuation.graham_valuation(
            earnings_per_share=5,
            book_value_per_share=20,
            growth_rate=0.05
        )
        
        self.assertIn('intrinsic_value', result)
        self.assertIn('simplified_value', result)
        self.assertGreater(result['intrinsic_value'], 0)
    
    def test_wacc_calculation(self):
        """Test WACC calculation"""
        wacc = self.valuation.calculate_wacc(
            equity_value=8000000,
            debt_value=2000000,
            cost_of_equity=0.12,
            cost_of_debt=0.06,
            tax_rate=0.25
        )
        
        self.assertGreater(wacc, 0)
        self.assertLess(wacc, 1)

class TestDataFetcher(unittest.TestCase):
    """Test data fetcher"""
    
    def setUp(self):
        self.fetcher = StockDataFetcher()
    
    def test_get_stock_info(self):
        """Test stock info fetching"""
        # This test requires internet connection
        result = self.fetcher.get_stock_info('AAPL')
        
        if result:  # Only test if data is available
            self.assertIn('symbol', result)
            self.assertIn('name', result)
            self.assertIn('current_price', result)

class TestStockAnalyzer(unittest.TestCase):
    """Test main stock analyzer"""
    
    def setUp(self):
        self.analyzer = StockAnalyzer()
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        self.assertIsNotNone(self.analyzer.data_fetcher)
        self.assertIsNotNone(self.analyzer.valuation_models)
    
    def test_calculate_technical_indicators(self):
        """Test technical indicators calculation"""
        import pandas as pd
        import numpy as np
        
        # Create sample data
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        prices = 100 + np.cumsum(np.random.randn(100) * 0.5)
        
        data = pd.DataFrame({
            'Close': prices
        }, index=dates)
        
        result = self.analyzer._calculate_technical_indicators(data)
        
        self.assertIn('moving_averages', result)
        self.assertIn('rsi', result)
        self.assertIn('volatility', result)

if __name__ == '__main__':
    unittest.main()
