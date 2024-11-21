# imports
import pandas as pd
import plotly.graph_objects as go

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
