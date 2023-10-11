class PoolPriceReportItem:
    """
    Contract for the pool price report items
    """
    def __init__(self,
                 begin_datetime_utc=None,
                 begin_datetime_mpt=None,
                 pool_price: float = None,
                 forecast_pool_price: float = None,
                 rolling_30day_avg: float = None):
        self._begin_datetime_utc = begin_datetime_utc
        self._begin_datetime_mpt = begin_datetime_mpt
        self._pool_price = pool_price
        self._forecast_pool_price = forecast_pool_price
        self._rolling_30day_avg = rolling_30day_avg

    def get_begin_datetime_utc(self):
        return self._begin_datetime_utc

    def set_begin_datetime_utc(self, begin_datetime_utc):
        self._begin_datetime_utc = begin_datetime_utc

    def get_begin_datetime_mpt(self):
        return self._begin_datetime_mpt

    def set_begin_datetime_mpt(self, begin_datetime_mpt):
        self._begin_datetime_mpt = begin_datetime_mpt

    def get_pool_price(self) -> float:
        return self._pool_price

    def set_pool_price(self, pool_price: float):
        self._pool_price = pool_price

    def get_forecast_pool_price(self) -> float:
        return self._forecast_pool_price

    def set_forecast_pool_price(self, forecast_pool_price: float):
        self._forecast_pool_price = forecast_pool_price

    def get_rolling_30day_avg(self) -> float:
        return self._rolling_30day_avg

    def set_rolling_30day_avg(self, rolling_30day_avg: float):
        self._rolling_30day_avg = rolling_30day_avg

    def __repr__(self):
        return "{{begin_datetime_utc: {}, begin_datetime_mpt: {}, pool_price: {}, forecast_pool_price: {}, rolling_30day_avg: {} }}".format(
            self._begin_datetime_utc,
            self._begin_datetime_mpt,
            self._pool_price,
            self._forecast_pool_price,
            self._rolling_30day_avg
        )
