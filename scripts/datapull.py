#imports
import yfinance as yf
import pandas as pd
from datetime import datetime as dt


# Download and organize data for each ticker
def download_and_organize_data(tickers, start_date, end_date, interval):
    # Initialize dataframe
    df_final = pd.DataFrame()

    # For each stock, add the data to the dataframe
    for ticker in tickers:
        print(f"Downloading data for {ticker}")
        # Get the data
        stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False, interval=interval)

        # Convert to DataFrame and format
        df = stock_data.reset_index()
        df['Ticker'] = ticker
        df = df[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df.columns = ['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['Open'] = df['Open'].round(2)
        df['High'] = df['High'].round(2)
        df['Low'] = df['Low'].round(2)
        df['Close'] = df['Close'].round(2)
        df['Volume'] = df['Volume'].fillna(0).astype(int)
        df_final = pd.concat([df_final, df])

    df_final = df_final.sort_values(['Ticker', "Date"]).reset_index(drop=True)
    return df_final


# Display basic statistics about the dataframe
def summarize_data(df):
    # Display basic statistics
    print("Dataset Summary:")
    print(f"Total number of rows: {len(df)}")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Number of companies: {df['Ticker'].nunique()}")

    # This displays a Series containing the data type of each column
    print("\nColumn Data Types:")
    print(df.dtypes)
    print("First few rows: \n", df.head(), "\n")


# Tests
# assert store["Date"] == "datetime64[ns, UTC]", "dates are not the right type"