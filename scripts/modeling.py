# imports
import pandas as pd
import plotly.graph_objects as go
from garch import *  
from arch import arch_model
import numpy as np

def calculate_moving_averages(df, short_window=20, long_window=50):
    # Short-term moving average (e.g., 20 days)
    df['Short_MA'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
    
    # Long-term moving average (e.g., 50 days)
    df['Long_MA'] = df['Close'].rolling(window=long_window, min_periods=1).mean()
    return df

def identify_crossovers(df):
    df['Crossover'] = ((df['Short_MA'] > df['Long_MA']) & 
                       (df['Short_MA'].shift(1) <= df['Long_MA'].shift(1)))
    return df

def plot_moving_averages(df, ticker):
    # Create the figure
    fig = go.Figure()
    
    # Add closing price
    fig.add_trace(
        go.Scatter(
            x=df.index,  # Changed from df['Date'] to df.index for Streamlit compatibility
            y=df['Close'],
            name=f'{ticker} Closing Price',
            line=dict(color='blue', width=1),
            opacity=0.7
        )
    )
    
    # Add short-term moving average
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['Short_MA'],
            name='Short-Term MA (20 days)',
            line=dict(color='green', width=1, dash='dash')
        )
    )
    
    # Add long-term moving average
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['Long_MA'],
            name='Long-Term MA (50 days)',
            line=dict(color='red', width=1, dash='dash')
        )
    )
    
    # Add crossover points
    crossover_points = df[df['Crossover']]
    fig.add_trace(
        go.Scatter(
            x=crossover_points.index,
            y=crossover_points['Close'],
            mode='markers',
            name='Crossover Points',
            marker=dict(
                color='red',
                size=8,
                symbol='circle'
            )
        )
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f'{ticker} Moving Averages',
            x=0.5,
            font=dict(size=20)
        ),
        xaxis_title='Date',
        yaxis_title='Price',
        hovermode='x unified',
        showlegend=True,
        template='plotly_white',
        height=600,
        xaxis=dict(rangeslider=dict(visible=True))
    )
    
    return fig

def moving_average_analysis(df, ticker, short_window=20, long_window=50):
    df = calculate_moving_averages(df, short_window, long_window)
    df = identify_crossovers(df)
    return plot_moving_averages(df, ticker)  # Return the figure instead of showing it

def monte_carlo_simulation(df, days, iterations):
    framework = np.zeros((iterations, days))  # matrix for storing price paths
    framework[:, 0] = df["Close"].iloc[-1]  # Start with the last known price
    
    df, omega, alpha, beta = calculate_future_variance(df)
    
    # Drift is the mean log return from historical data
    drift = np.mean(df["log_returns"])
    
    z_shocks = np.random.normal(0, 1, (iterations, days - 1))  # random normal shocks for each path
    conditional_volatility = df["Conditional"].iloc[-1]
    drift_matrix = np.full((iterations, df.shape[0]), drift)
    print(drift_matrix.shape)

    # Loop through each day to simulate the price path
    for i in range(1, days):
        # previous days shock
        simulated_log_return = np.log(framework[:, i-1] / framework[:, i-2]) if i > 2 else drift
        drift_matrix = np.append(drift_matrix, simulated_log_return.reshape(-1, 1)
, axis=1) if i > 2 else drift_matrix
        shock = simulated_log_return - (np.mean(drift_matrix))
  # The shock (log returns difference)
        shock_squared = shock**2  # Squared shock to update volatility
        
        # Update the conditional volatility using GARCH model
        conditional_volatility = omega + alpha * shock_squared + beta * conditional_volatility
        
    # Update price paths using GBM
        framework[:, i] = framework[:, i-1] * np.exp((drift - 0.5 * conditional_volatility) + np.sqrt(conditional_volatility) * z_shocks[:, i-1])

    x_days = np.arange(1, days + 1)  # Days 1 to 'days'

        # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(
            go.Scatter(
                x=x_days,  # Days as the x-axis
                y=np.mean(framework, axis=0),  # Prices for the current simulation
                mode="lines",
                name="Mean line",
                line=dict(width=5.0, color = "Black") # Customize line width
    
                )
            )

        # Add each simulation path as a trace
    for i in range(framework.shape[0]):  # Iterate over each simulation
        fig.add_trace(
            go.Scatter(
                x=x_days,  # Days as the x-axis
                y=framework[i, :],  # Prices for the current simulation
                mode="lines",
                name=f"Simulation {i + 1}",
                line=dict(width=1.5)  # Customize line width
                )
            )

        # Customize the layout
    fig.update_layout(
        title="Monte Carlo Simulated Asset Price Paths (Daily Breakdown)",
        xaxis_title="Days",
        yaxis_title="Asset Price",
        legend_title="Simulations",
        template="plotly_white",  # Choose a clean white background
        height=600,  # Optional: Figure height
        width=1000,  # Optional: Figure width
        )

        # Show the interactive figure
    fig.show()
    print(framework[1, :])
    return framework

aapl_df = extract_and_clean_data(df, 'AAPL')
monte = monte_carlo_simulation(aapl_df, 100, 100)
print(monte.shape)
    
    
    
