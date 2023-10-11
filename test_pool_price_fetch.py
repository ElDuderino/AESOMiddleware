"""

"""
from aeso_api.aeso_api_config import AESOAPIConfig
from aeso_api.aeso_api_query import AESOAPIQuery
from aeso_api.aeso_response_entities import *
from datetime import datetime

config = AESOAPIConfig('config.cfg')

api_query = AESOAPIQuery(config)

start_date = "2023-10-10"

results: list[PoolPriceReportItem] = api_query.get_pool_price_report(start_date)

print(results)
