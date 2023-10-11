from aeso_api_config import AESOAPIConfig
import requests
from requests.models import PreparedRequest
import json
from aeso_response_entities import *
import logging


class AESOAPIQuery:
    """
    Use this class for querying the AESO API
    """

    def __init__(self, api_config: AESOAPIConfig):
        self.api_config = api_config
        self.logger = logging.getLogger(__name__)

    def get_pool_price_report(self, start_date, end_date=None) -> list[PoolPriceReportItem]:
        """
        Fetch pool price report for the date range: startDate (yyyy-mm-dd) to endDate (yyyy-mm-dd).
        The endDate is optional. If endDate is omitted, fetched data will include the pool price values for all the
        completed settlement hours of the day specified by startDate.

        To fetch the latest pool price, include the date of that hour in your query.

        The API will return data for a maximum of 1 year at a time.

        """
        url = self.api_config.get_api_url() + "/v1.1/price/poolPrice"

        params = {
            'startDate': start_date
        }

        if end_date is not None:
            params['endDate'] = end_date

        req = PreparedRequest()
        req.prepare_url(url, params)
        print(req.url)

        headers = {"X-API-Key": self.api_config.get_api_access_token()}

        response = requests.get(req.url, headers=headers)

        if response.status_code == 200:

            pool_price_items: list[PoolPriceReportItem] = []

            json_response = json.loads(response.content.decode())

            for report_raw in json_response['return']['Pool Price Report']:
                try:
                    pool_price_item = PoolPriceReportItem(
                        report_raw['begin_datetime_utc'],
                        report_raw['begin_datetime_mpt'],
                        float(report_raw['pool_price']),
                        float(report_raw['forecast_pool_price']),
                        float(report_raw['rolling_30day_avg'])
                    )
                    pool_price_items.append(pool_price_item)
                except ValueError as ve:
                    self.logger.error("Could not parse report:{}".format(report_raw))

            return pool_price_items

        else:
            self.logger.error("Invalid response code:{}".format(response.status_code))
            return None
