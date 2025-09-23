"""
Stock Valuation Models
Implements various valuation methodologies
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class ValuationModels:
    """Implements various stock valuation models"""
    
    def __init__(self):
        self.risk_free_rate = 0.04  # 4% default risk-free rate
        self.market_risk_premium = 0.06  # 6% market risk premium
    
    def dcf_valuation(self, 
                     free_cash_flows: List[float],
                     terminal_growth_rate: float = 0.03,
                     discount_rate: float = 0.10,
                     current_shares_outstanding: int = 1000000) -> Dict:
        """
        Discounted Cash Flow (DCF) Valuation
        
        Args:
            free_cash_flows: List of projected free cash flows
            terminal_growth_rate: Long-term growth rate (default 3%)
            discount_rate: Required rate of return (default 10%)
            current_shares_outstanding: Number of shares outstanding
        """
        try:
            # Calculate present value of projected cash flows
            pv_cash_flows = []
            for i, fcf in enumerate(free_cash_flows):
                pv = fcf / ((1 + discount_rate) ** (i + 1))
                pv_cash_flows.append(pv)
            
            # Calculate terminal value
            terminal_fcf = free_cash_flows[-1] * (1 + terminal_growth_rate)
            terminal_value = terminal_fcf / (discount_rate - terminal_growth_rate)
            pv_terminal_value = terminal_value / ((1 + discount_rate) ** len(free_cash_flows))
            
            # Calculate enterprise value
            enterprise_value = sum(pv_cash_flows) + pv_terminal_value
            
            # Calculate equity value per share
            equity_value_per_share = enterprise_value / current_shares_outstanding
            
            return {
                'enterprise_value': enterprise_value,
                'equity_value_per_share': equity_value_per_share,
                'terminal_value': terminal_value,
                'pv_terminal_value': pv_terminal_value,
                'pv_cash_flows': pv_cash_flows,
                'discount_rate': discount_rate,
                'terminal_growth_rate': terminal_growth_rate
            }
        except Exception as e:
            logger.error(f"Error in DCF valuation: {e}")
            return {}
    
    def pe_ratio_valuation(self, 
                          current_price: float,
                          earnings_per_share: float,
                          industry_pe: float = 20.0,
                          growth_rate: float = 0.05) -> Dict:
        """
        Price-to-Earnings (P/E) Ratio Valuation
        
        Args:
            current_price: Current stock price
            earnings_per_share: Current EPS
            industry_pe: Industry average P/E ratio
            growth_rate: Expected earnings growth rate
        """
        try:
            # Calculate current P/E ratio
            current_pe = current_price / earnings_per_share if earnings_per_share > 0 else 0
            
            # PEG ratio (P/E to Growth ratio)
            peg_ratio = current_pe / (growth_rate * 100) if growth_rate > 0 else 0
            
            # Fair value based on industry P/E
            fair_value_industry = earnings_per_share * industry_pe
            
            # Fair value based on growth-adjusted P/E
            growth_adjusted_pe = industry_pe * (1 + growth_rate)
            fair_value_growth = earnings_per_share * growth_adjusted_pe
            
            return {
                'current_pe': current_pe,
                'industry_pe': industry_pe,
                'peg_ratio': peg_ratio,
                'fair_value_industry': fair_value_industry,
                'fair_value_growth': fair_value_growth,
                'upside_downside': {
                    'industry': ((fair_value_industry - current_price) / current_price) * 100,
                    'growth': ((fair_value_growth - current_price) / current_price) * 100
                }
            }
        except Exception as e:
            logger.error(f"Error in P/E ratio valuation: {e}")
            return {}
    
    def ddm_valuation(self,
                     current_dividend: float,
                     dividend_growth_rate: float,
                     required_return: float = 0.10) -> Dict:
        """
        Dividend Discount Model (DDM) Valuation
        
        Args:
            current_dividend: Current annual dividend per share
            dividend_growth_rate: Expected dividend growth rate
            required_return: Required rate of return
        """
        try:
            if required_return <= dividend_growth_rate:
                return {'error': 'Required return must be greater than dividend growth rate'}
            
            # Gordon Growth Model
            fair_value = current_dividend * (1 + dividend_growth_rate) / (required_return - dividend_growth_rate)
            
            return {
                'fair_value': fair_value,
                'dividend_yield': current_dividend / fair_value if fair_value > 0 else 0,
                'total_return': dividend_growth_rate + (current_dividend / fair_value) if fair_value > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error in DDM valuation: {e}")
            return {}
    
    def pb_ratio_valuation(self,
                          current_price: float,
                          book_value_per_share: float,
                          industry_pb: float = 2.0,
                          roe: float = 0.15) -> Dict:
        """
        Price-to-Book (P/B) Ratio Valuation
        
        Args:
            current_price: Current stock price
            book_value_per_share: Book value per share
            industry_pb: Industry average P/B ratio
            roe: Return on equity
        """
        try:
            # Calculate current P/B ratio
            current_pb = current_price / book_value_per_share if book_value_per_share > 0 else 0
            
            # Fair value based on industry P/B
            fair_value_industry = book_value_per_share * industry_pb
            
            # Fair value based on ROE-adjusted P/B
            roe_adjusted_pb = industry_pb * (roe / 0.15)  # Assuming 15% as benchmark ROE
            fair_value_roe = book_value_per_share * roe_adjusted_pb
            
            return {
                'current_pb': current_pb,
                'industry_pb': industry_pb,
                'roe_adjusted_pb': roe_adjusted_pb,
                'fair_value_industry': fair_value_industry,
                'fair_value_roe': fair_value_roe,
                'upside_downside': {
                    'industry': ((fair_value_industry - current_price) / current_price) * 100,
                    'roe': ((fair_value_roe - current_price) / current_price) * 100
                }
            }
        except Exception as e:
            logger.error(f"Error in P/B ratio valuation: {e}")
            return {}
    
    def graham_valuation(self,
                        earnings_per_share: float,
                        book_value_per_share: float,
                        growth_rate: float = 0.05) -> Dict:
        """
        Benjamin Graham's Intrinsic Value Formula
        
        Args:
            earnings_per_share: Current EPS
            book_value_per_share: Book value per share
            growth_rate: Expected earnings growth rate
        """
        try:
            # Graham's formula: V = EPS × (8.5 + 2g) × 4.4 / Y
            # Where g = growth rate, Y = current yield on AAA corporate bonds (assumed 4.4%)
            
            intrinsic_value = earnings_per_share * (8.5 + 2 * growth_rate * 100) * 4.4 / 4.4
            
            # Simplified version: V = EPS × (8.5 + 2g)
            simplified_value = earnings_per_share * (8.5 + 2 * growth_rate * 100)
            
            return {
                'intrinsic_value': intrinsic_value,
                'simplified_value': simplified_value,
                'margin_of_safety_price': simplified_value * 0.7  # 30% margin of safety
            }
        except Exception as e:
            logger.error(f"Error in Graham valuation: {e}")
            return {}
    
    def calculate_wacc(self,
                      equity_value: float,
                      debt_value: float,
                      cost_of_equity: float,
                      cost_of_debt: float,
                      tax_rate: float = 0.25) -> float:
        """
        Calculate Weighted Average Cost of Capital (WACC)
        """
        try:
            total_value = equity_value + debt_value
            equity_weight = equity_value / total_value
            debt_weight = debt_value / total_value
            
            wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
            return wacc
        except Exception as e:
            logger.error(f"Error calculating WACC: {e}")
            return 0.10  # Default 10%
    
    def comprehensive_valuation(self, stock_data: Dict, financial_data: Dict) -> Dict:
        """
        Perform comprehensive valuation using multiple models
        """
        try:
            results = {}
            
            # Extract key data
            current_price = stock_data.get('current_price', 0)
            market_cap = stock_data.get('market_cap', 0)
            shares_outstanding = market_cap / current_price if current_price > 0 else 1000000
            
            # Get financial metrics
            metrics = financial_data.get('metrics', {})
            eps = metrics.get('earnings_per_share', 0)
            book_value = metrics.get('book_value_per_share', 0)
            dividend = metrics.get('dividend_per_share', 0)
            growth_rate = metrics.get('earnings_growth', 0.05)
            
            # Run different valuation models
            if eps > 0:
                results['pe_valuation'] = self.pe_ratio_valuation(
                    current_price, eps, growth_rate=growth_rate
                )
                
                results['graham_valuation'] = self.graham_valuation(
                    eps, book_value, growth_rate
                )
            
            if book_value > 0:
                results['pb_valuation'] = self.pb_ratio_valuation(
                    current_price, book_value, roe=metrics.get('return_on_equity', 0.15)
                )
            
            if dividend > 0:
                results['ddm_valuation'] = self.ddm_valuation(
                    dividend, growth_rate
                )
            
            # Calculate average fair value
            fair_values = []
            for model, result in results.items():
                if 'fair_value' in result:
                    fair_values.append(result['fair_value'])
                elif 'intrinsic_value' in result:
                    fair_values.append(result['intrinsic_value'])
                elif 'simplified_value' in result:
                    fair_values.append(result['simplified_value'])
            
            if fair_values:
                results['average_fair_value'] = sum(fair_values) / len(fair_values)
                results['current_price'] = current_price
                results['upside_potential'] = ((results['average_fair_value'] - current_price) / current_price) * 100
            
            return results
            
        except Exception as e:
            logger.error(f"Error in comprehensive valuation: {e}")
            return {}
