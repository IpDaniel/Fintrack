# imports
import pandas as pd
import matplotlib.pyplot as plt


# calculate moving averages
def calculate_moving_averages(df, short_window=20, long_window=50):

    # Short-term moving average (e.g., 20 days)
    df['Short_MA'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
    
    # Long-term moving average (e.g., 50 days)
    df['Long_MA'] = df['Close'].rolling(window=long_window, min_periods=1).mean()

    return df


# Function to identify crossover points
def identify_crossovers(df):
    df['Crossover'] = ((df['Short_MA'] > df['Long_MA']) & 
                       (df['Short_MA'].shift(1) <= df['Long_MA'].shift(1)))

    return df

# Function to plot stock prices and moving averages
def plot_moving_averages(df, ticker):
   
    plt.figure(figsize=(12, 6))
    
    # Plot the closing price
    plt.plot(df['Date'], df['Close'], label=f'{ticker} Closing Price', alpha=0.5, color='blue')
    
    # Plot the short-term moving average
    plt.plot(df['Date'], df['Short_MA'], label='Short-Term MA (20 days)', linestyle='--', color='green')
    
    # Plot the long-term moving average
    plt.plot(df['Date'], df['Long_MA'], label='Long-Term MA (50 days)', linestyle='--', color='red')
    
    # Highlight crossover points
    crossover_points = df[df['Crossover']]
    plt.scatter(crossover_points['Date'], crossover_points['Close'], 
                label='Crossover', color='red', zorder=5)

    # Title and labels
    plt.title(f'{ticker} Moving Averages', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    
    # Add legend
    plt.legend()
    
    # Add grid for readability
    plt.grid()
    
    # Display the plot
    plt.show()


# Main function to calculate, identify, and plot moving averages
def moving_average_analysis(df, ticker, short_window=20, long_window=50):

    # Calculate moving averages
    df = calculate_moving_averages(df, short_window, long_window)

    # Identify crossover points
    df = identify_crossovers(df)

    # Plot results
    plot_moving_averages(df, ticker)

    return df# Volume, return, opening, close.

def monte_carlo_model():
    print("model goes here")


