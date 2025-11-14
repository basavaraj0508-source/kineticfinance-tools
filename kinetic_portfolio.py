import streamlit as st
import pandas as pd
import yfinance as yf

st.title("KineticFinance Portfolio Tracker")

# User input
stocks = st.text_area("Enter stock symbols separated by commas (e.g., AAPL,MSFT,GOOGL)")
investment = st.text_area("Enter corresponding investments separated by commas (e.g., 1000,2000,1500)")

if st.button("Calculate Portfolio"):
    try:
        symbols = [s.strip() for s in stocks.split(",")]
        amounts = [float(a.strip()) for a in investment.split(",")]

        data = {}
        for i, sym in enumerate(symbols):
            price = yf.Ticker(sym).history(period="1d")['Close'][0]
            value = amounts[i] * price / price  # simple demo
            data[sym] = {"Investment": amounts[i], "Current Price": price, "Value": value}

        df = pd.DataFrame(data).T
        st.write(df)
        st.write("Total Portfolio Value: $", df["Value"].sum())

    except Exception as e:
        st.error(f"Error: {e}")

