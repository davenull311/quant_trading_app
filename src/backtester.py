"""
backtester.py

This module implements a backtesting engine. It simulates trading using the generated signals,
updates portfolio values over time, accounts for transaction costs, and provides a method to plot results.
"""

import pandas as pd
import matplotlib.pyplot as plt

def to_scalar(x):
    """
    Helper function to convert a value to a plain Python scalar.
    
    If x is a single-element Series or a NumPy scalar, this function returns the scalar value.
    Otherwise, it returns x unchanged.
    """
    try:
        return x.item()
    except AttributeError:
        return x

class Backtester:
    def __init__(self, data: pd.DataFrame, initial_capital: float = 100000.0, transaction_cost: float = 0.001):
        """
        Initialize the backtester.
        
        :param data: DataFrame containing historical data with signals.
        :param initial_capital: The starting capital for the portfolio.
        :param transaction_cost: The fractional cost per transaction (e.g., 0.001 for 0.1% per trade).
        """
        self.data = data.copy()  # Work on a copy to avoid modifying the original DataFrame
        self.initial_capital = initial_capital
        self.transaction_cost = transaction_cost

    def run_backtest(self) -> pd.DataFrame:
        """
        Run the backtest simulation.
        
        For each time step, this method checks if a new trading signal (position change) is generated.
        It then "executes" trades by allocating or de-allocating the portfolio to the asset.
        The portfolio value is updated by considering both cash and holdings.
        
        :return: DataFrame with updated portfolio, cash, and holdings over time.
        """
        # Initialize columns to track portfolio performance
        self.data['portfolio'] = self.initial_capital  # Total portfolio value
        self.data['holdings'] = 0.0                     # Value of the asset held
        self.data['cash'] = self.initial_capital        # Remaining cash

        # Variable to track the number of shares currently held (position)
        position = 0.0

        # Get the column positions for easier updating with .iloc
        cash_idx = self.data.columns.get_loc('cash')
        holdings_idx = self.data.columns.get_loc('holdings')
        portfolio_idx = self.data.columns.get_loc('portfolio')

        # Loop through each time period (skip the first row as there is no previous signal)
        for i in range(1, len(self.data)):
            # Retrieve the trade signal (position change) using integer indexing
            pos_change = self.data['positions'].iloc[i]

            if pos_change == 1:
                # BUY signal: use available cash to purchase as many shares as possible
                buy_price = self.data['Open'].iloc[i]  # Assume buying at the opening price
                # Convert previous cash to a scalar value
                cash_prev = to_scalar(self.data['cash'].iloc[i - 1])
                # Calculate the number of shares to purchase accounting for transaction costs
                position = float(cash_prev) / (buy_price * (1 + self.transaction_cost))
                # Update holdings value based on the closing price of the day
                self.data.iloc[i, holdings_idx] = position * self.data['Close'].iloc[i]
                # All cash is used up for the purchase
                self.data.iloc[i, cash_idx] = 0.0

            elif pos_change == -1:
                # SELL signal: liquidate all holdings
                sell_price = self.data['Open'].iloc[i]  # Assume selling at the opening price
                # Update cash with the proceeds of the sale minus transaction costs
                self.data.iloc[i, cash_idx] = position * sell_price * (1 - self.transaction_cost)
                # Reset holdings to zero as all shares are sold
                self.data.iloc[i, holdings_idx] = 0.0
                # Reset position count
                position = 0.0

            else:
                # No trade executed; update holdings value if in a position
                # Ensure that position is a float so that the comparison is unambiguous
                if float(position) != 0:
                    self.data.iloc[i, holdings_idx] = position * self.data['Close'].iloc[i]
                    # Cash remains the same as the previous time step
                    self.data.iloc[i, cash_idx] = self.data['cash'].iloc[i - 1]
                else:
                    # If not in a position, both cash and holdings remain unchanged
                    self.data.iloc[i, holdings_idx] = 0.0
                    self.data.iloc[i, cash_idx] = self.data['cash'].iloc[i - 1]

            # Update the total portfolio value (cash + holdings)
            cash_now = to_scalar(self.data.iloc[i, cash_idx])
            holdings_now = to_scalar(self.data.iloc[i, holdings_idx])
            total_value = float(cash_now) + float(holdings_now)
            self.data.iloc[i, portfolio_idx] = total_value

        return self.data

    def plot_results(self):
        """
        Plot the portfolio performance over time.
        
        This method creates a matplotlib plot showing the evolution of the portfolio value.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data['portfolio'], label='Portfolio Value')
        plt.title('Portfolio Value Over Time')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value ($)')
        plt.legend()
        plt.grid(True)
        plt.show()
