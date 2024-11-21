import streamlit as st
from scripts.datapull import *
from scripts.dataclean import *
from scripts.EDA import *
from scripts.modeling import moving_average_analysis
import plotly.graph_objects as go
from datetime import datetime as dt
import yfinance as yf

# Title
st.title("Stock Analysis Dashboard")

# Sidebar for inputs
st.sidebar.header("Parameters")

# Add custom stock input 
custom_stock = st.sidebar.text_input("Enter Custom Stock Symbol:", "")

# Stock selection
tickers = ['AAPL', 'MSFT', 'TSLA', 'GOOGL', 'META', 'NVDA', 'AMZN', 'WMT', 'COST']
if custom_stock not in tickers:
    tickers.append(custom_stock)

selected_stocks = st.sidebar.multiselect("Select Stocks", tickers, 
                                       default=['AAPL', 'GOOGL', 'WMT'] if not custom_stock else [custom_stock])

# Date range
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start Date", dt(2023,11,7))
end_date = col2.date_input("End Date", dt(2024,11,7))

# Interval selection
interval = st.sidebar.selectbox("Select Interval", ['1d', '1wk', '1mo'], index=0)

if st.sidebar.button("Analyze"):
    with st.spinner("Analyzing data..."):
        try:
            # Validate custom stock if entered
            if custom_stock:
                try:
                    stock = yf.Ticker(custom_stock)
                    info = stock.info
                    st.sidebar.success(f"Found {custom_stock}: {info.get('longName', 'Company')}")
                except:
                    st.sidebar.error(f"Invalid stock symbol: {custom_stock}")
                    st.stop()

            # Get and process data
            df = download_and_organize_data(tickers, start_date, end_date, interval)
            day_truncate(df)
            
            # Create tabs for different analyses
            tab1, tab2, tab3 = st.tabs(["Stock Prices", "Moving Averages", "Correlation Analysis"])
            
            with tab1:
                st.subheader("Stock Price Analysis")
                for ticker in selected_stocks:
                    
                    stock_df = extract_and_clean_data(df, ticker)
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df['Close'], 
                                           mode='lines', name=f'{ticker} Close Price'))
                    fig.update_layout(title=f'{ticker} Stock Price',
                                    xaxis_title="Date",
                                    yaxis_title="Price")
                    st.plotly_chart(fig)
            
            with tab2:
                st.subheader("Moving Averages Analysis")
                for ticker in selected_stocks:
                    stock_df = extract_and_clean_data(df, ticker)
                    fig = moving_average_analysis(stock_df, ticker)
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                st.subheader("Correlation Analysis")
                stock_dfs = [extract_and_clean_data(df, ticker) for ticker in selected_stocks]
                correlation = correlation_matrix(stock_dfs)
                st.dataframe(correlation)

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Add some explanation text at the bottom
st.markdown("""
### How to use this dashboard:
1. Enter a custom stock symbol (optional)
2. Select stocks from the sidebar
3. Choose your date range
4. Select the data interval
5. Click 'Analyze' to see results
6. Switch between tabs to view different analyses
""")
