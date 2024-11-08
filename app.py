from scripts.datapull import *
from scripts.dataclean import *
from scripts.EDA import *

# Constants
tickers = ['AAPL', 'MSFT', 'TSLA', 'GOOGL', 'META', 'NVDA', 'AMZN','WMT','COST'] # starter set of stocks
start_date = dt(2023,11,7) # start date
end_date = dt(2024,11,7) # end date
interval = '1d' # interval


# Example usage with APPL
df = download_and_organize_data(tickers, start_date, end_date, interval) # download and organize data
day_truncate(df) # truncate datetime values to day level
summarize_data(df) # summarize data in terminal for debugging purposes

aapl_df = extract_stock_data(df, 'AAPL') # extract data for a single stock
summarize_data(aapl_df)

# check to make sure all rows in the dataframe have the same ticker value
check_header_consistency(aapl_df)
check_ticker_consistency(aapl_df, 'AAPL')

aapl_df = forward_fill_missing_values(aapl_df) # forward fill missing values
aapl_df = add_closing_returns(aapl_df) # add closing returns
aapl_df = add_money_flow(aapl_df) # add money flow (trading volume in dollars estimated with closing price and share volume)

visualize_closing_price_over_time(aapl_df) # visualize closing price over time
