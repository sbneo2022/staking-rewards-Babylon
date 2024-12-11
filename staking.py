import pandas as pd
import plotly.express as px
import streamlit as st

def display_staking_data(df_staking: pd.DataFrame) -> None:
    """
    This function displays staking metrics data in a user-friendly format. It converts 'inflation_rate' and 'reward_rate' 
    columns to percentage format and displays the dataframe with these values. It also generates bar plots for each metric 
    comparison between assets.

    Parameters:
    df_staking (pd.DataFrame): A pandas DataFrame containing staking metrics data. The DataFrame should have at least two columns: 'assets' and other metric columns.

    Returns:
    None: The function does not return any value. It displays the staking metrics data and plots using Streamlit.
    """
    # Create a copy of the dataframe for display purposes
    df_display = df_staking.copy()

    # Convert 'inflation_rate' and 'reward_rate' to percentage format and add the '%' sign in the copied dataframe for display
    if 'inflation_rate' in df_display.columns:
        df_display['inflation_rate'] = df_display['inflation_rate'].apply(lambda x: f"{x * 100:.2f}%")
    if 'reward_rate' in df_display.columns:
        df_display['reward_rate'] = df_display['reward_rate'].apply(lambda x: f"{x * 100:.2f}%")

    # Show the dataframe with percentage formatted values
    st.write("### Staking Metrics Data (with percentages for inflation and reward rates)")
    st.dataframe(df_display)

    # Define a custom color palette for the assets
    color_discrete_map = {asset: px.colors.qualitative.Plotly[i % 10] for i, asset in enumerate(df_staking['assets'].unique())}

    # Metrics for comparison (excluding the 'assets' column)
    staking_metrics = df_staking.columns.tolist()[1:]  

    # Iterate through the metrics and handle percentage columns
    for metric in staking_metrics:
        # Plot the comparison for each metric (without modifying the original values)
        st.write(f"### {metric.capitalize().replace('_', ' ')} Comparison")
        fig = px.bar(df_staking, x='assets', y=metric, title=f'{metric.capitalize().replace("_", " ")} Comparison between Assets', 
                     color='assets', color_discrete_map=color_discrete_map)

        # Display the plot
        st.plotly_chart(fig)

