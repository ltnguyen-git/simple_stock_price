import streamlit as st 
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from stocknews import StockNews

ticker = st.sidebar.text_input("Ticker")
start_date =  st.sidebar.date_input("Start Date")
end_date =  st.sidebar.date_input("End Date")

st.title("Simple Stock Price App")
st.write(f'Show are the stock ***Adj Close price*** and ***volume*** of {ticker}')


# tickerSymbol ="GOOGL"

Data = yf.download(ticker,start=start_date, end=end_date )



fig =  px.line(Data, x= Data.index, y=Data['Adj Close'], title= ticker)
st.plotly_chart(fig)
st.header('Volume Price')
st.line_chart(Data.Volume)

pricing_data, news = st.tabs(["pricing_data","news"])

with pricing_data:
    st.header('price Movements')
    data2 = Data
    data2['% Change'] = Data['Adj Close']/ Data['Adj Close'].shift(1) - 1
    data2.dropna(inplace=True)
    st.write(data2)
    annual_return = data2['% Change'].mean()*252*100
    st.write('Annual Return is', annual_return,'%')
    stdev = np.std(data2['% Change'])*np.sqrt(252)
    st.write('Standard Deviation is',stdev*100,'%')
    st.write('Risk Adj. Return is', annual_return/(stdev*100))    



with news:
    st.header(f'News of {ticker}')
    sn = StockNews(ticker, save_news = False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        new_sentiment = df_news['sentiment_summary'][i]
        st.write(f'New Sentiment {new_sentiment}')
