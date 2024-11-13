import datetime
import pandas as pd
import torch
from chronos import ChronosPipeline
import numpy as np
from aeso_database_builder import AESODatabaseBuilder

adb = AESODatabaseBuilder()

# Load the database and get the last 6 months of data
df = adb.load_database()
df['begin_datetime_utc'] = pd.to_datetime(df['begin_datetime_utc'])
latest_data = df[df['begin_datetime_utc'] >= df['begin_datetime_utc'].max() - pd.Timedelta(days=180)]

# Set power quantity in MW (configurable)
power_quantity_mw = 1.0


# Prepare data for ChronosPipeline
def prepare_forecast_pipeline():
    pipeline = ChronosPipeline.from_pretrained(
        "amazon/chronos-t5-base",
        device_map="cpu",
        torch_dtype=torch.float32
    )
    return pipeline


def forecast_daily_prices(pipeline, day_data):
    """
    Forecasts daily pool prices using Chronos and identifies the optimal buy and sell times.
    """
    time_series_data = day_data['pool_price'].values
    context_length = len(time_series_data) - 1  # Exclude last hour if partial data
    context = torch.tensor(time_series_data[:context_length]).float().unsqueeze(0)

    forecast = pipeline.predict(context=context, prediction_length=24, num_samples=20)
    low, median, high = np.quantile(forecast[0].numpy(), [0.1, 0.5, 0.9], axis=0)

    buy_hour = median.argmin()
    sell_hour = median.argmax()

    return buy_hour, sell_hour, median[buy_hour], median[sell_hour]


# Initialize Chronos Pipeline
pipeline = prepare_forecast_pipeline()

# Backtest over the last 6 months
results = []
for day_start in pd.date_range(latest_data['begin_datetime_utc'].min(), latest_data['begin_datetime_utc'].max(),
                               freq='24H'):
    day_data = latest_data[(latest_data['begin_datetime_utc'] >= day_start) &
                           (latest_data['begin_datetime_utc'] < day_start + pd.Timedelta(days=1))]

    if len(day_data) < 24:
        continue  # Skip incomplete days

    # Forecast buy/sell prices for the day
    buy_hour, sell_hour, buy_price, sell_price = forecast_daily_prices(pipeline, day_data)

    # Get actual prices for true buy/sell comparison
    true_buy_hour = day_data['pool_price'].idxmin() % 24
    true_sell_hour = day_data['pool_price'].idxmax() % 24
    true_buy_price = day_data['pool_price'].min()
    true_sell_price = day_data['pool_price'].max()

    # Calculate profit
    predicted_profit = (sell_price - buy_price) * power_quantity_mw
    true_profit = (true_sell_price - true_buy_price) * power_quantity_mw

    results.append({
        "date": day_start,
        "predicted_buy_hour": buy_hour,
        "predicted_sell_hour": sell_hour,
        "true_buy_hour": true_buy_hour,
        "true_sell_hour": true_sell_hour,
        "predicted_profit": predicted_profit,
        "true_profit": true_profit
    })

# Convert results to DataFrame for summary
results_df = pd.DataFrame(results)
results_df.to_csv("backtest_results.csv", index=False)

# Summarize total profits
total_predicted_profit = results_df['predicted_profit'].sum()
total_true_profit = results_df['true_profit'].sum()

# Print summary
print("Backtest completed. Summary of profits:")
print(f"Total Predicted Profit: ${total_predicted_profit:,.2f}")
print(f"Total True Profit: ${total_true_profit:,.2f}")
