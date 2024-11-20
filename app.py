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

aapl_df = extract_and_clean_data(df, 'AAPL') # extract and clean data for Apple
googl_df = extract_and_clean_data(df, 'GOOGL') # extract and clean data for Alphabet
wmt_df = extract_and_clean_data(df, 'WMT') # extract and clean data for Walmart

print(correlation_matrix([aapl_df, googl_df, wmt_df]))

visualize_closing_and_returns(aapl_df)
