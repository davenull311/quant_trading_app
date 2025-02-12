"""
main.py

This is the main driver script that ties together all modules:
- It fetches historical market data.
- It generates trading signals using a Moving Average Crossover strategy.
- It runs a backtest simulation.
- It calculates risk metrics.
- It plots the portfolio performance.
- It demonstrates simulated order execution.
"""

import pandas as pd
from data_fetcher import DataFetcher
from strategy import MovingAverageCrossoverStrategy
from backtester import Backtester
from risk_manager import RiskManager
from execution_engine import ExecutionEngine

def main():
    # ===============================
    # STEP 1: Configuration Parameters
    # ===============================
    ticker = 'AAPL'                   # Stock ticker to analyze (e.g., Apple Inc.)
    start_date = '2020-01-01'           # Start date for historical data
    end_date = '2023-01-01'             # End date for historical data
    initial_capital = 100000.0          # Starting portfolio capital in USD

    # ===============================
    # STEP 2: Data Fetching
    # ===============================
    print("Fetching historical data for ticker:", ticker)
    try:
        fetcher = DataFetcher(ticker, start_date, end_date)
        data = fetcher.fetch()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # ===============================
    # STEP 3: Signal Generation via Strategy
    # ===============================
    print("Generating trading signals using Moving Average Crossover Strategy...")
    strategy = MovingAverageCrossoverStrategy(short_window=20, long_window=50)
    # Generate signals and add them to the data DataFrame
    data_with_signals = strategy.generate_signals(data.copy())

    # ===============================
    # STEP 4: Backtesting the Strategy
    # ===============================
    print("Running backtest simulation...")
    backtester = Backtester(data_with_signals, initial_capital=initial_capital)
    results = backtester.run_backtest()

    # ===============================
    # STEP 5: Risk Management Evaluation
    # ===============================
    risk_manager = RiskManager(max_drawdown=0.2)
    max_dd = risk_manager.calculate_max_drawdown(results['portfolio'])
    print(f"Maximum Drawdown during backtest: {max_dd*100:.2f}%")

    # ===============================
    # STEP 6: Visualizing Results
    # ===============================
    print("Plotting portfolio performance...")
    backtester.plot_results()

    # ===============================
    # STEP 7: Simulated Order Execution
    # ===============================
    execution_engine = ExecutionEngine()
    # Create a sample order (for demonstration; in a live system, orders would be dynamic)
    sample_order = {
        'ticker': ticker,
        'action': 'BUY',
        'quantity': 10,
        'price': float(results['Open'].iloc[-1])  # Convert the last available open price to a float
    }
    execution_engine.execute_order(sample_order)

if __name__ == "__main__":
    main()
