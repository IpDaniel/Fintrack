# this document will focus on the creation of the functions neccesary in order to do a gacha analysis
from datapull import *
from dataclean import *
from EDA import *
import numpy as np
import pandas as pd
from arch import arch_model
# sample data
tickers = ['AAPL'] # starter set of stocks
start_date = dt(2023,11,7) # start date
end_date = dt(2024,11,7) # end date
interval = '1d' # interval


# Example usage with APPL
df = download_and_organize_data(tickers, start_date, end_date, interval) # download and organize data
day_truncate(df) # truncate datetime values to day level
summarize_data(df) # summarize data in terminal for debugging purposes

aapl_df = extract_and_clean_data(df, 'AAPL') # extract and clean data for Apple

def collect_coefficients(df):
    # utilizing arch because parameter estimation is a pain the ass
    # arch_model is a method to calculate all this shit for us, but we're just gonna use 
    # it for the coefficients because they'd be a pain in the ass to calculate by ourselves
    # p is the number of lagged parts and q is the order of arch
    # because we;re using a garch(1,1) model we only are using one at a time
    model = arch_model(df['log_returns'], vol='Garch', p=1, q=1)
    model_fit = model.fit()
    params = model_fit.params
    return params["omega"], params["alpha[1]"], params["beta[1]"]




# one thing we need to do is calculate the beta alpha and omega
def create_log_returns(value):
    log_ret = np.log(1 + value)
    return log_ret
def create_squared_returns(log_ret):
    sqaured = log_ret ** 2
    return sqaured

# example log return
aapl_df["log_returns"] =  aapl_df["Returns"].apply(lambda x: create_log_returns(x))
aapl_df["squared_return"] =  aapl_df["log_returns"].apply(lambda x: create_squared_returns(x))
omega, alpha, beta = collect_coefficients(aapl_df)
print(aapl_df.head())
def calculate_cond_variance(df, beta=beta, alpha=alpha, omega=omega):
    conditional = [df["log_returns"].var()]
    r_squared = df["squared_return"].to_numpy()

    for i in range(1, len(r_squared)):
        conditional.append(omega + alpha * r_squared[i-1] + conditional[i-1])
    df["Conditional"] = conditional
    return df 

def calculate_future_variance(df, beta, days):
    df["log_returns"] =  aapl_df["Returns"].apply(lambda x: create_log_returns(x))
    df["squared_return"] =  aapl_df["log_returns"].apply(lambda x: create_squared_returns(x))
    omega, alpha, beta = collect_coefficients(df)
    df = calculate_cond_variance(df)
    return df
        
    
    
    

df = calculate_cond_variance(aapl_df)

# notes about the coefficients
# omege represents the baseline level of volatility or the long term average variance
# alpha reflects the senitivity of the volatility to recent squared returns
# beta reflects the persistence of past volatility (how much old influences new)

# yay log returns and squared retaurns work

# next step is to

