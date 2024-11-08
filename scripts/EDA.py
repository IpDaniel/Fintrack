import pandas as pd
import matplotlib.pyplot as plt

# calculate and plot closing and returns over time with dual y-axis graph
def visualize_closing_and_returns(df):
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

# check if the date range exists in the dataframe
def date_range_in_df(df, from_date, to_date):
    # Check if the date range exists in the dataframe
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    return from_date >= min_date and to_date <= max_date and from_date <= to_date

# calculate mean, median, variance, and std dev for closing price over a given date range
def calculate_mean(df, from_date, to_date):
    return df[df['Date'] >= from_date][df['Date'] <= to_date]['Close'].mean()

# calculate median for closing price over a given date range
def calculate_median(df, from_date, to_date):
    return df[df['Date'] >= from_date][df['Date'] <= to_date]['Close'].median() 

# calculate variance for closing price over a given date range
def calculate_variance(df, from_date, to_date):
    return df[df['Date'] >= from_date][df['Date'] <= to_date]['Close'].var()

# calculate std dev for closing price over a given date range
def calculate_std_dev(df, from_date, to_date):
    return df[df['Date'] >= from_date][df['Date'] <= to_date]['Close'].std()

# calculate correlation between two stocks over a given date range
def correlation_between(stock_df_1, stock_df_2):
    # Merge the two dataframes on Date to ensure aligned data
    merged = pd.merge(stock_df_1[['Date', 'Close']], 
                     stock_df_2[['Date', 'Close']], 
                     on='Date', 
                     suffixes=('_1', '_2'))
    
    # Calculate correlation between closing prices
    return merged['Close_1'].corr(merged['Close_2'])

def correlation_matrix(stocks):
    # Get list of symbols for labels
    symbols = [stock['Ticker'].iloc[0] for stock in stocks]  # Get first value since Symbol is repeated
    
    # Create empty matrix using nested list comprehension
    matrix = [[correlation_between(stocks[i], stocks[j]) 
               for j in range(len(stocks))] 
               for i in range(len(stocks))]
    
    # Convert to DataFrame with labels
    corr_df = pd.DataFrame(matrix, index=symbols, columns=symbols)
    
    return corr_df