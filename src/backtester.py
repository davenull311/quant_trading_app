"""
backtester.py

This module implements a backtesting engine. It simulates trading using the generated signals,
updates portfolio values over time, accounts for transaction costs, and provides a method to plot results.
"""

import pandas as pd
import matplotlib.pyplot as plt

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
        self.data['holdings'] = 0.0                    # Value of the asset held
        self.data['cash'] = self.initial_capital       # Remaining cash

        # Variable to track the number of shares currently held (position)
        position = 0

        # Loop through each time period (skip the first row as there is no previous signal)
        for i in range(1, len(self.data)):
            # Retrieve the trade signal (position change)
            pos_change = self.data['positions'].iloc[i]
            
            # Check for a BUY signal (signal changes from 0 or -1 to +1)
            if pos_change == 1:
                # Buy: use available cash to purchase as many shares as possible
                buy_price = self.data['Open'].iloc[i]  # Assume buying at the opening price
                # Calculate the number of shares to purchase accounting for transaction costs
                position = self.data['cash'].iloc[i-1] / (buy_price * (1 + self.transaction_cost))
                # Update holdings value based on the closing price of the day
                self.data.at[self.data.index[i], 'holdings'] = position * self.data['Close'].iloc[i]
                # All cash is used up for the purchase
                self.data.at[self.data.index[i], 'cash'] = 0.0

            # Check for a SELL signal (signal changes from +1 or 0 to -1)
            elif pos_change == -1:
                # Sell: liquidate all holdings
                sell_price = self.data['Open'].iloc[i]  # Assume selling at the opening price
                # Update cash with the proceeds of the sale minus transaction costs
                self.data.at[self.data.index[i], 'cash'] = position * sell_price * (1 - self.transaction_cost)
                # Reset holdings to zero as all shares are sold
                self.data.at[self.data.index[i], 'holdings'] = 0.0
                # Reset position count
                position = 0

            else:
                # No trade executed; update holdings value if in a position
                if position != 0:
                    self.data.at[self.data.index[i], 'holdings'] = position * self.data['Close'].iloc[i]
                    # Cash remains the same as the previous time step
                    self.data.at[self.data.index[i], 'cash'] = self.data['cash'].iloc[i-1]
                else:
                    # If not in a position, both cash and holdings remain unchanged
                    self.data.at[self.data.index[i], 'holdings'] = 0.0
                    self.data.at[self.data.index[i], 'cash'] = self.data['cash'].iloc[i-1]

            # Update the total portfolio value (cash + holdings)
            self.data.at[self.data.index[i], 'portfolio'] = \
                self.data.at[self.data.index[i], 'cash'] + self.data.at[self.data.index[i], 'holdings']

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
