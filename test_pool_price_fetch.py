"""

"""
from aeso_api.aeso_api_config import AESOAPIConfig
from aeso_api.aeso_api_query import AESOAPIQuery
from aeso_api.aeso_response_entities import *
from datetime import datetime

config = AESOAPIConfig('config.cfg')

api_query = AESOAPIQuery(config)

today_date = datetime.today()

start_date = f"{today_date.year-1}-{today_date.month}-{today_date.day}"
end_date = f"{today_date.year-1}-{today_date.month}-{today_date.day+2}"

print(f"Start date: {start_date} End date: {end_date}")

results: list[PoolPriceReportItem] = api_query.get_pool_price_report(start_date, end_date)

print(results)
print(len(results))
