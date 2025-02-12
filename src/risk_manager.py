"""
risk_manager.py

This module provides risk management functionality.
It includes methods for calculating key risk metrics such as maximum drawdown.
"""

import pandas as pd

class RiskManager:
    def __init__(self, max_drawdown: float = 0.2):
        """
        Initialize the RiskManager.
        
        :param max_drawdown: The maximum allowable drawdown as a fraction (e.g., 0.2 for 20%)
        """
        self.max_drawdown = max_drawdown

    def calculate_max_drawdown(self, portfolio_values: pd.Series) -> float:
        """
        Calculate the maximum drawdown of the portfolio.
        
        The drawdown is computed as the maximum percentage drop from a historical peak in portfolio value.
        
        :param portfolio_values: A pandas Series of portfolio values over time.
        :return: The maximum drawdown (a negative number, e.g., -0.15 for a 15% drawdown)
        """
        # Calculate the running maximum of the portfolio value
        roll_max = portfolio_values.cummax()
        # Calculate drawdown at each point in time
        drawdown = (portfolio_values - roll_max) / roll_max
        # The maximum drawdown is the minimum (most negative) drawdown observed
        max_dd = drawdown.min()
        return max_dd
