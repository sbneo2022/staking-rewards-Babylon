import streamlit as st
import pandas as pd
from price import get_assets_data
from staking import display_staking_data

# This is a Streamlit app that compares cryptocurrency price and staking metrics.
st.set_page_config(layout="wide")
st.title("Cryptocurrency Asset Metrics")

# Load the CSV file with staking data
file_path_staking = 'offline_data/staking_data.csv'
df_staking = pd.read_csv(file_path_staking)

# Convert staking data to more readable formats
df_staking['staking_marketcap'] = df_staking['staking_marketcap'].apply(lambda x: f"${x/1e9:.1f}B")
df_staking['net_issuance'] = df_staking['net_issuance'].apply(lambda x: f"${x/1e9:.1f}B")

# Load the CSV file with price data
file_path_prices = "offline_data/price_data.csv"
df_price = pd.read_csv(file_path_prices)

# Get the list of assets for price data
assets = df_price['assets'].unique()

# Create a switch to toggle between staking data and price data
view_option = st.selectbox("Select Data View", ("Staking Metrics", "Price Metrics"))

if view_option == "Staking Metrics":
    display_staking_data(df_staking)
elif view_option == "Price Metrics":
    get_assets_data(df_price)


