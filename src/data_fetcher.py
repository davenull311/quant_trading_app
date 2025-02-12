"""
data_fetcher.py

This module is responsible for fetching historical market data using the yfinance library.
It downloads the data for a given ticker symbol over a specified date range.
"""

import yfinance as yf
import pandas as pd

class DataFetcher:
    def __init__(self, ticker: str, start_date: str, end_date: str):
        """
        Initialize the DataFetcher with the desired ticker and date range.
        
        :param ticker: The stock ticker symbol (e.g., "AAPL")
        :param start_date: The start date for data in 'YYYY-MM-DD' format
        :param end_date: The end date for data in 'YYYY-MM-DD' format
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def fetch(self) -> pd.DataFrame:
        """
        Fetch historical market data using yfinance.
        
        :return: A pandas DataFrame containing historical price data.
        """
        # Download data from Yahoo Finance
        data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        # Ensure that the DataFrame is not empty
        if data.empty:
            raise ValueError("No data fetched. Check the ticker symbol or date range.")
        return data
