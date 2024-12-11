import math
import pandas as pd
import plotly.express as px
import streamlit as st

def clean_numeric_columns(asset_data: pd.DataFrame):
    """
    Cleans numeric columns in a DataFrame by removing commas and converting them to float.

    Parameters:
    asset_data (pd.DataFrame): A DataFrame containing asset data, where the first column is assumed to be 'assets' (string),
                               and the remaining columns are numeric values possibly stored as strings with commas.

    Returns:
    pd.DataFrame: The modified DataFrame with numeric columns converted to float.
    """
    numeric_columns = asset_data.columns[1:]  # Assuming first column is 'assets' (string)
    for col in numeric_columns:
        if asset_data[col].dtype == object:
            # Replace commas with periods before conversion
            asset_data[col] = asset_data[col].apply(lambda x: float(str(x).replace(',', '.')) if isinstance(x, str) else x)

    return asset_data

def format_value(value, column):
    """
    Formats a given value based on the type of metric specified by the column name.

    Parameters:
    value (float): The numeric value to be formatted.
    column (str): The name of the column or metric type, which determines the formatting style.

    Returns:
    str: The formatted string representation of the value, which may include currency symbols, 
         percentage signs, or be scaled to millions, depending on the column type.
    """
    if column.lower() in ['scrip_dividend', 'price', 'earnings_per_share', 'price_to_earnings','scrip dividend']:
        return f"${value:,.3f}"  # Add dollar sign and format to 3 decimal places
    elif column.lower() in ['scrip_dividend_yield', 'reward_rate', 'cash dividend yield','scrip dividend yield', 'buyback yield', 
                            'preferential shares staker', 'ordinary shares staker', 'participant dilution' ]:
        return f"{value * 100:.2f}%"  # Convert to percentage, assuming 1 = 100%
    elif column.lower() in ['circulating_supply', 'buyback_nominal_amount', 'cash dividend', 
                            'buyback nominal amount', 'earnings', "ordinary shares"]:
        return f"{value / 1_000_000:,.2f}M"  # Format to millions
    else:
        return f"{value:,.2f}"  # Default format for other metrics (2 decimal places)

def calculations(price, circulating_supply, earnings, base_fees, preferential_shares, inflation_factor):
    """
    Performs financial calculations related to dividends, shares, and yields based on input parameters.

    Parameters:
    price (float): The current price of the asset.
    circulating_supply (float): The total circulating supply of the asset.
    earnings (float): The total earnings of the asset.
    base_fees (float): The base fees percentage used to calculate buyback and cash dividends.
    preferential_shares (float): The percentage of shares that are preferential.
    inflation_factor (float): The factor used to calculate the scrip dividend.

    Returns:
    dict: A dictionary containing calculated financial metrics including buyback nominal amount, cash dividend, 
          ordinary shares, cash dividend yield, scrip dividend, scrip dividend yield, buyback yield, 
          preferential shares staker, ordinary shares staker, and participant dilution.
    """
    # Earnings and dividends
    buyback_nominal_amount = float(earnings) * (base_fees / 100)
    cash_dividend = float(earnings) * (1 - (base_fees / 100))

    # Shares
    preferential_shares_amount = float(circulating_supply) * (preferential_shares / 100)
    ordinary_shares = float(circulating_supply) * (1 - (preferential_shares / 100))

    # Cash dividend yield
    cash_dividend_yield = (cash_dividend ) / (price * preferential_shares_amount) 

    # Scrip dividend and yield
    scrip_dividend = inflation_factor * math.sqrt(preferential_shares_amount)
    scrip_dividend_yield = scrip_dividend  / (preferential_shares_amount ) 

    # Buyback yield
    buyback_yield = (buyback_nominal_amount ) / (circulating_supply  * price) 

    # Staker rewards
    preferential_shares_staker = cash_dividend_yield + scrip_dividend_yield
    ordinary_shares_staker = (cash_dividend_yield - buyback_yield) / buyback_yield

    # Participant dilution
    participant_dilution = abs(preferential_shares_staker - ordinary_shares_staker)

    return {
        "Buyback Nominal Amount": buyback_nominal_amount,
        "Cash Dividend": cash_dividend,
        "Ordinary Shares": ordinary_shares,
        "Cash Dividend Yield": cash_dividend_yield,
        "Scrip Dividend": scrip_dividend,
        "Scrip Dividend Yield": scrip_dividend_yield,
        "Buyback Yield": buyback_yield,
        "Preferential Shares Staker": preferential_shares_staker,
        "Ordinary Shares Staker": ordinary_shares_staker,
        "Participant Dilution": participant_dilution
    }

def display_metrics_as_formated_list(asset_data: pd.DataFrame, base_fees, preferential_shares, inflation_factor):
    """
    Formats and returns a list of financial metrics for a given asset.

    Parameters:
    asset_data (pd.DataFrame): A DataFrame containing data for a specific asset, including price, circulating supply, and earnings.
    base_fees (float): The base fees percentage used in financial calculations.
    preferential_shares (float): The percentage of shares that are preferential.
    inflation_factor (float): The factor used to calculate the scrip dividend.

    Returns:
    dict: A dictionary containing the asset's name and formatted financial metrics, including cash dividend, cash dividend yield,
          preferential shares staker, scrip dividend, scrip dividend yield, ordinary shares staker, and participant dilution.
    """
    # Retrieve the relevant data for calculations
    price = asset_data['price'].values[0]
    circulating_supply = asset_data['circulating_supply'].values[0]
    earnings = asset_data['Earnings'].values[0]

    calculated_data = calculations(price, circulating_supply, earnings, base_fees, preferential_shares, inflation_factor)

    # Collect formatted metrics in a dictionary
    metrics = {
        "Asset": asset_data['assets'].values[0]
    }

    for column in asset_data.columns[1:]:
        if column == 'Market Cap':
            continue
        value = asset_data[column].values[0]
        formatted_value = format_value(value, column)
        metrics[column] = formatted_value

    # Add calculated metrics to the dictionary
    metrics.update({
        "Cash Dividend": format_value(calculated_data['Cash Dividend'], 'Cash Dividend'),
        "Cash Dividend Yield": format_value(calculated_data['Cash Dividend Yield'], 'Cash Dividend Yield'),
        "Preferential Shares Staker": format_value(calculated_data['Preferential Shares Staker'], 'Preferential Shares Staker'),
        "Scrip Dividend": format_value(calculated_data['Scrip Dividend'], 'Scrip Dividend'),
        "Scrip Dividend Yield": format_value(calculated_data['Scrip Dividend Yield'], 'Scrip Dividend Yield'),
        "Ordinary Shares Staker": format_value(calculated_data['Ordinary Shares Staker'], 'Ordinary Shares Staker'),
        "Participant Dilution": format_value(calculated_data['Participant Dilution'], 'Participant Dilution')
    })

    return metrics

def display_metrics_as_list(asset_data: pd.DataFrame, base_fees, preferential_shares, inflation_factor):
    # Retrieve the relevant data for calculations
    price = asset_data['price'].values[0]
    circulating_supply = asset_data['circulating_supply'].values[0]
    earnings = asset_data['Earnings'].values[0]

    calculated_data = calculations(price, circulating_supply, earnings, base_fees, preferential_shares, inflation_factor)

    # Collect formatted metrics in a dictionary
    metrics = {
        "Asset": asset_data['assets'].values[0]
    }

    for column in asset_data.columns[1:]:
        if column == 'Market Cap':
            continue
        value = asset_data[column].values[0]
        metrics[column] = value

    # Add calculated metrics to the dictionary
    metrics.update({
        "Cash Dividend": calculated_data['Cash Dividend'],
        "Cash Dividend Yield": calculated_data['Cash Dividend Yield'],
        "Preferential Shares Staker": calculated_data['Preferential Shares Staker'],
        "Scrip Dividend": calculated_data['Scrip Dividend'],
        "Scrip Dividend Yield": calculated_data['Scrip Dividend Yield'],
        "Ordinary Shares Staker": calculated_data['Ordinary Shares Staker'],
        "Participant Dilution": calculated_data['Participant Dilution']
    })

    return metrics




def get_assets_data(df_price: pd.DataFrame):
    all_assets_data = []
    all_assets_data_plots = []
    # Clean numeric columns to handle comma-separated values
    df_price = clean_numeric_columns(df_price)

    for asset in df_price['assets'].unique():
        asset_data = df_price[df_price['assets'] == asset]
        
        if asset_data.empty:
            st.write(f"Asset {asset} not found.")
            continue
        

        # Get metrics for the asset
        metrics = display_metrics_as_formated_list(asset_data, base_fees=90, preferential_shares=25, inflation_factor=166.3)
        all_assets_data.append(metrics)
        metrics_unformated = display_metrics_as_list(asset_data, base_fees=90, preferential_shares=25, inflation_factor=166.3)
        all_assets_data_plots.append(metrics_unformated)

    # Convert the list of dictionaries to a DataFrame
    df_metrics = pd.DataFrame(all_assets_data)
    df_metrics_plots = pd.DataFrame(all_assets_data_plots)

    df_metrics.drop(columns=['Ordinary Shares Staker'], inplace=True)
    df_metrics_plots.drop(columns=['Ordinary Shares Staker'], inplace=True)
    
    # Display the DataFrame in Streamlit
    
    # Split the DataFrame into two parts
    df_part1 = df_metrics[['Asset', 'price', 'circulating_supply', 'reward_rate', 'Earnings', 'earnings_per_share', 'price_to_earnings']]
    df_part2 = df_metrics[['Asset', 'Cash Dividend', 'Cash Dividend Yield', 'Preferential Shares Staker', 'Scrip Dividend', 'Scrip Dividend Yield', 'Participant Dilution']]

    # Display each part with a title
    st.write("### Price and Earnings Metrics")
    st.dataframe(df_part1, use_container_width=True)
    st.write("### Shareholder and Dilution Metrics")
    st.dataframe(df_part2, use_container_width=True)
    # Plot comparisons for each metric
    color_discrete_map = {asset: px.colors.qualitative.Plotly[i % 10] for i, asset in enumerate(df_price['assets'].unique())}
    
    metrics = df_metrics.columns.tolist()[1:]
    print(metrics)
    print(df_metrics)
    for metric in metrics:
        st.write(f"### {metric.capitalize().replace('_', ' ')} Comparison")
        fig = px.bar(
            df_metrics_plots, 
            x='Asset', 
            y=metric, 
            title=f'{metric.capitalize().replace("_", " ")} Comparison between Assets', 
            color='Asset', 
            color_discrete_map=color_discrete_map
        )
        fig.update_yaxes(type='log')  # Set y-axis to logarithmic scale
        st.plotly_chart(fig)

