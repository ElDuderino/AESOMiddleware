import os
import time
import pandas as pd
from datetime import datetime
from aeso_api.aeso_api_config import AESOAPIConfig
from aeso_api.aeso_api_query import AESOAPIQuery
from aeso_api.aeso_response_entities import PoolPriceReportItem


class AESODatabaseBuilder:

    def __init__(self):

        # Initialize configuration and query objects
        config = AESOAPIConfig('config.cfg')
        self.api_query = AESOAPIQuery(config)

    def build_database(self, start_year=2010):
        """
        Fetches data from AESO API from start_year to today's date and saves it as a CSV.
        """
        today = datetime.today()
        end_year = today.year
        all_data = []

        for year in range(start_year, end_year + 1):
            start_date = f"{year}-01-01"
            end_date = f"{year}-12-31" if year < end_year else today.strftime("%Y-%m-%d")

            print(f"Fetching data for {start_date} to {end_date}")

            results = self.api_query.get_pool_price_report(start_date, end_date)
            all_data.extend(results)

            print(f"Fetched data for year {year}. Waiting 5 seconds before the next request...")
            time.sleep(5)

        # Convert list of PoolPriceReportItems to pandas DataFrame
        data = {
            "begin_datetime_utc": [item.get_begin_datetime_utc() for item in all_data],
            "begin_datetime_mpt": [item.get_begin_datetime_mpt() for item in all_data],
            "pool_price": [item.get_pool_price() for item in all_data],
            "forecast_pool_price": [item.get_forecast_pool_price() for item in all_data],
            "rolling_30day_avg": [item.get_rolling_30day_avg() for item in all_data]
        }

        df = pd.DataFrame(data)
        df['begin_datetime_utc'] = pd.to_datetime(df['begin_datetime_utc'])
        df['begin_datetime_mpt'] = pd.to_datetime(df['begin_datetime_mpt'])
        df['pool_price'] = df['pool_price'].astype(float)
        df['forecast_pool_price'] = df['forecast_pool_price'].astype(float)
        df['rolling_30day_avg'] = df['rolling_30day_avg'].astype(float)

        # Save to CSV
        df.to_csv("pool_price_report_data.csv", index=False)
        print("Database built and saved to pool_price_report_data.csv")
        return df

    def load_database(self):
        """
        Loads the pool price report CSV, checks the most recent date in it,
        and backfills any missing data up to today's date. If the file doesn't exist, calls build_database.
        """
        file_path = "pool_price_report_data.csv"
        today = datetime.today().strftime("%Y-%m-%d")

        if not os.path.exists(file_path):
            print("CSV file not found, building database...")
            return self.build_database()

        # Load existing data
        df = pd.read_csv(file_path, parse_dates=['begin_datetime_utc', 'begin_datetime_mpt'])

        # Find the most recent date in the existing data
        most_recent_date = df['begin_datetime_utc'].max().strftime("%Y-%m-%d")

        if most_recent_date >= today:
            print("Database is up-to-date.")
            return df

        # Backfill from the day after the most recent date to today
        start_date = (pd.to_datetime(most_recent_date) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        results = self.api_query.get_pool_price_report(start_date, today)

        # Convert results to DataFrame and append to the existing data
        new_data = {
            "begin_datetime_utc": [item.get_begin_datetime_utc() for item in results],
            "begin_datetime_mpt": [item.get_begin_datetime_mpt() for item in results],
            "pool_price": [item.get_pool_price() for item in results],
            "forecast_pool_price": [item.get_forecast_pool_price() for item in results],
            "rolling_30day_avg": [item.get_rolling_30day_avg() for item in results]
        }
        new_df = pd.DataFrame(new_data)
        new_df['begin_datetime_utc'] = pd.to_datetime(new_df['begin_datetime_utc'])
        new_df['begin_datetime_mpt'] = pd.to_datetime(new_df['begin_datetime_mpt'])
        new_df['pool_price'] = new_df['pool_price'].astype(float)
        new_df['forecast_pool_price'] = new_df['forecast_pool_price'].astype(float)
        new_df['rolling_30day_avg'] = new_df['rolling_30day_avg'].astype(float)

        # Append new data and save
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(file_path, index=False)
        print("Database updated with missing data.")
        return df
