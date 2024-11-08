"""
Requirements:
3.1 Visualize the closing price and daily returns using line plots.
3.2 Calculate and plot basic summary statistics like mean, median, variance, and standard deviation for stock prices and returns.
3.3 Create a correlation matrix to see the relationships between the selected stocks.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def visualize_closing_price_over_time(df):
    # Create figure and axis objects with a single subplot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot closing price
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price ($)', color=color)
    ax1.plot(df['Date'], df['Close'], color=color, linewidth=1, label='Closing Price')
    ax1.tick_params(axis='y', labelcolor=color)

    # Create second y-axis that shares x-axis
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Returns', color=color)
    ax2.plot(df['Date'], df['Returns'], color=color, linewidth=1, alpha=0.7, label='Returns')
    ax2.tick_params(axis='y', labelcolor=color)

    # Add title and grid
    plt.title('Closing Price and Returns Over Time')
    ax1.grid(True, alpha=0.3)

    # Add legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()
    plt.show()
