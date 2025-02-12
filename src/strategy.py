"""
strategy.py

This module implements a simple Moving Average Crossover strategy.
It calculates short-term and long-term moving averages on the close price and generates trading signals.
"""

import pandas as pd

class MovingAverageCrossoverStrategy:
    def __init__(self, short_window: int = 20, long_window: int = 50):
        """
        Initialize the strategy with short-term and long-term moving average window sizes.
        
        :param short_window: Window size for the short-term moving average.
        :param long_window: Window size for the long-term moving average.
        """
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on moving average crossovers.
        
        The method computes:
          - short_ma: Short-term moving average.
          - long_ma: Long-term moving average.
          - signal: +1 when short_ma > long_ma (bullish), -1 when short_ma < long_ma (bearish).
          - positions: The change in signal (used to indicate a trade entry/exit).
        
        :param data: DataFrame containing historical price data.
        :return: DataFrame with additional columns for moving averages and signals.
        """
        # Calculate the short-term moving average
        data['short_ma'] = data['Close'].rolling(window=self.short_window, min_periods=1).mean()
        # Calculate the long-term moving average
        data['long_ma'] = data['Close'].rolling(window=self.long_window, min_periods=1).mean()
        # Initialize the signal column to 0 (neutral)
        data['signal'] = 0
        # Set signal to +1 (buy) when short_ma > long_ma
        data.loc[data['short_ma'] > data['long_ma'], 'signal'] = 1
        # Set signal to -1 (sell) when short_ma < long_ma
        data.loc[data['short_ma'] < data['long_ma'], 'signal'] = -1
        # Determine when a change in signal occurs (i.e., when to enter or exit a trade)
        data['positions'] = data['signal'].diff()
        return data
