import pandas as pd
import yfinance as yf

#df = pd.read_csv('data/cleaned_data.csv')

"""
Headers:
- Date	datetime64[ns, UTC]
- Ticker	object
- Open	float64
- High	float64
- Low	float64
- Close	float64
- Volume	int64
"""

# Check if the headers match the expected headers
def check_header_consistency(df, expected_headers=['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']):
    missing_headers = [header for header in expected_headers if header not in df.columns]
    if missing_headers:
        raise ValueError(f"Missing required headers: {missing_headers}. \nFound headers: {list(df.columns)}")
    return True

# Check if all rows have the same ticker value
def check_ticker_consistency(df, ticker):
    if not (df['Ticker'] == ticker).all():
        raise ValueError(f"Inconsistent ticker values found. Expected all values to be {ticker}. \nFound values: {df['Ticker'].unique()}")
    return True

# Truncate datetime values to day level
def day_truncate(df):
    df['Date'] = df['Date'].dt.normalize()  # Truncates time to midnight (00:00:00)

# Extract data for a specific stock
def extract_stock_data(df, ticker):
    return df[df['Ticker'] == ticker]

# Forward fill missing values
def forward_fill_missing_values(df):
    # Create an explicit copy
    df = df.copy()
    df.loc[:, ['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].ffill()
    return df

# Backfill missing values
def backfill_missing_values(df):
    # Modify columns in place, preserve all columns
    df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].bfill()
    return df

# Add closing returns to the dataframe
def add_closing_returns(df):
    # Create an explicit copy
    df = df.copy()
    df.loc[:, 'Returns'] = df['Close'].pct_change()
    return df

# Add money flow to the dataframe
def add_money_flow(df):
    # Create an explicit copy
    df = df.copy()
    df.loc[:, 'Money_Flow'] = df['Volume'] * ((df['Close'] + df['Open']) / 2)
    return df

# Extract and clean data for a specific stock
def extract_and_clean_data(df, ticker):
    stock_df = extract_stock_data(df, ticker=ticker) # extract data for a single stock

    # check to make sure all rows in the dataframe have the same ticker value
    check_header_consistency(stock_df)
    check_ticker_consistency(stock_df, ticker=ticker)

    stock_df = forward_fill_missing_values(stock_df) # forward fill missing values

    stock_df = add_closing_returns(stock_df) # add closing returns
    stock_df["Returns"].iloc[0] = 0 # forward fill missing values

    stock_df = add_money_flow(stock_df) # add money flow (trading volume in dollars estimated with closing price and share volume)
    return stock_df

def download_and_clean_stock_data(ticker, start_date=None, end_date=None, interval='1d',headers=['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']):
    # Get stock price data
    stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False, interval=interval)
    stock_df = stock_data.reset_index()
    stock_df['Ticker'] = ticker
    stock_df = add_closing_returns(stock_df) # add closing returns
    stock_df["Returns"].iloc[0] = 0 # forward fill missing values
    stock_df = add_money_flow(stock_df)

    # Get fundamental data
    ticker_info = yf.Ticker(ticker).info
    stock_df['Dividend_Rate'] = ticker_info.get('dividendRate', None)
    stock_df['PB_Ratio'] = ticker_info.get('priceToBook', None)
    stock_df['PE_Ratio'] = ticker_info.get('trailingPE', None)
    stock_df['Dividend_Yield'] = ticker_info.get('dividendYield', None)
    stock_df['Beta'] = ticker_info.get('beta', None)
    stock_df['Fifty_Two_Week_High'] = ticker_info.get('fiftyTwoWeekHigh', None)
    stock_df['Total_Revenue'] = ticker_info.get('totalRevenue', None)
    stock_df['Profit_Margins'] = ticker_info.get('profitMargins', None)
    stock_df['Debt_to_Equity'] = ticker_info.get('debtToEquity', None)

    # check to make sure all rows in the dataframe have the same ticker value
    check_header_consistency(stock_df)
    check_ticker_consistency(stock_df, ticker=ticker)

    stock_df = forward_fill_missing_values(stock_df) # forward fill missing values
    stock_df = add_closing_returns(stock_df) # add closing returns
    stock_df = add_money_flow(stock_df) # add money flow (trading volume in dollars estimated with closing price and share volume)
    return stock_df
