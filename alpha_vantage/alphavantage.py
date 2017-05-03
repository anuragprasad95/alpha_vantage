try:
    # Python 3 import
    from urllib.request import urlopen
except ImportError:
    # Python 2.* import
    from urllib2 import urlopen

from simplejson import loads


class AlphaVantage:
    """
        This class is in charge of creating a python interface between the Alpha
        Vantage restful API and your python application
    """
    _ALPHA_VANTAGE_API_URL = "http://www.alphavantage.co/query?"
    _ALPHA_VANTAGE_MATH_MAP = ['SMA','EMA','WMA','DEMA','TEMA', 'TRIMA','T3',
    'KAMA','MAMA']
    def __init__(self, key=None):
        if key is None:
            raise ValueError('Get a free key from the alphavantage website')
        self.key = key

    def _handle_api_call(self, url, data_key, meta_data_key="Meta Data"):
        """ Handle the return call from the api and return a data and meta_data
        object. It raises a ValueError on problems

        Keyword arguments:
        url -- The url of the service
        data_key -- The key for getting the data from the jso object
        meta_data_key -- The key for getting the meta data information out of
        the json object
        """
        json_response = self._data_request(url)
        if 'Error Message' in json_response or not json_response:
            if json_response:
                raise ValueError('ERROR getting data form api',
                             json_response['Error Message'])
            else:
                raise ValueError('Error getting data from api, no return'\
                 ' message from the api url (possibly wrong symbol/param)')
        data = json_response[data_key]
        meta_data = json_response[meta_data_key]
        return data, meta_data

    def _data_request(self, url):
        """ Request data from the given url and return it as a json
        object. It raises URLError

        Keyword arguments:
        url -- The url of the service
        """
        response = urlopen(url)
        url_response = response.read()
        json_response = loads(url_response)
        return json_response

    def get_intraday(self, symbol, interval='15min', outputsize='compact'):
        """ Return intraday time series in two json objects as data and
        meta_data. It raises ValueError when problems arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min'
        (default '15min')
        outputsize -- The size of the call, supported values are
        'compact' and 'full; the first returns the last 100 points in the
        data series, and 'full' returns the full-length intraday times
        series, commonly above 1MB (default 'compact')
        """
        _FUNCTION_KEY = "TIME_SERIES_INTRADAY"
        url = "{}function={}&symbol={}&interval={}&outputsize={}&apikey={}\
        ".format(AlphaVantage._ALPHA_VANTAGE_API_URL, _FUNCTION_KEY,  symbol,
                 interval, outputsize, self.key)
        return self._handle_api_call(url, 'Time Series ({})'.format(interval),
        'Meta Data')

    def get_daily(self, symbol, outputsize='compact'):
        """ Return daily time series in two json objects as data and
        meta_data. It raises ValueError when problems arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        outputsize -- The size of the call, supported values are
        'compact' and 'full; the first returns the last 100 points in the
        data series, and 'full' returns the full-length intraday times
        series, commonly above 1MB (default 'compact')
        """
        _FUNCTION_KEY = "TIME_SERIES_DAILY"
        url = "{}function={}&symbol={}&outputsize={}&apikey={}".format(
        AlphaVantage._ALPHA_VANTAGE_API_URL, _FUNCTION_KEY,  symbol, outputsize,
        self.key)
        return self._handle_api_call(url, 'Time Series (Daily)', 'Meta Data')


    def get_weekly(self, symbol):
        """ Return weekly time series in two json objects as data and
        meta_data. It raises ValueError when problems arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data

        """
        _FUNCTION_KEY = "TIME_SERIES_WEEKLY"
        url = "{}function={}&symbol={}&apikey={}".format(
        AlphaVantage._ALPHA_VANTAGE_API_URL, _FUNCTION_KEY, symbol, self.key)
        return self._handle_api_call(url, 'Weekly Time Series', 'Meta Data')

    def get_monthly(self, symbol):
        """ Return monthly time series in two json objects as data and
        meta_data. It raises ValueError when problems arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data

        """
        _FUNCTION_KEY = "TIME_SERIES_MONTHLY"
        url = "{}function={}&symbol={}&apikey={}".format(
        AlphaVantage._ALPHA_VANTAGE_API_URL, _FUNCTION_KEY, symbol, self.key)
        return self._handle_api_call(url, 'Monthly Time Series', 'Meta Data')

    def get_sma(self, symbol, interval='60min', time_period=20, series_type='close'):
        """ Return simple moving average time series in two json objects as data and
        meta_data. It raises ValueError when problems arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
        'weekly', 'monthly' (default '60min')
        time_period -- How many data points to average (default 20)
        series_type -- The desired price type in the time series. Four types
        are supported: 'close', 'open', 'high', 'low' (default 'close')
        """
        _FUNCTION_KEY = "SMA"
        url = "{}function={}&symbol={}&interval={}&time_period={}"\
        "&series_type={}&apikey={}".format(AlphaVantage._ALPHA_VANTAGE_API_URL,
        _FUNCTION_KEY, symbol, interval, time_period, series_type, self.key)
        return self._handle_api_call(url,'Technical Analysis: SMA','Meta Data')

    def get_ema(self, symbol, interval='60min', time_period=20, series_type='close'):
        """ Return exponential moving average time series in two json objects
        as data and meta_data. It raises ValueError when problems arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
        'weekly', 'monthly' (default '60min')
        time_period -- How many data points to average (default 20)
        series_type -- The desired price type in the time series. Four types
        are supported: 'close', 'open', 'high', 'low' (default 'close')
        """
        _FUNCTION_KEY = "EMA"
        url = "{}function={}&symbol={}&interval={}&time_period={}"\
        "&series_type={}&apikey={}".format(AlphaVantage._ALPHA_VANTAGE_API_URL,
        _FUNCTION_KEY, symbol, interval, time_period, series_type, self.key)
        return self._handle_api_call(url,'Technical Analysis: EMA','Meta Data')

    def get_wma(self, symbol, interval='60min', time_period=20, series_type='close'):
        """ Return weighted moving average time series in two json objects
        as data and meta_data. It raises ValueError when problems arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
        'weekly', 'monthly' (default '60min')
        time_period -- How many data points to average (default 20)
        series_type -- The desired price type in the time series. Four types
        are supported: 'close', 'open', 'high', 'low' (default 'close')
        """
        _FUNCTION_KEY = "WMA"
        url = "{}function={}&symbol={}&interval={}&time_period={}"\
        "&series_type={}&apikey={}".format(AlphaVantage._ALPHA_VANTAGE_API_URL,
        _FUNCTION_KEY, symbol, interval, time_period, series_type, self.key)
        return self._handle_api_call(url,'Technical Analysis: WMA','Meta Data')

    def get_dema(self, symbol, interval='60min', time_period=20, series_type='close'):
        """ Return double exponential moving average time series in two json
        objects as data and meta_data. It raises ValueError when problems arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
        'weekly', 'monthly' (default '60min')
        time_period -- How many data points to average (default 20)
        series_type -- The desired price type in the time series. Four types
        are supported: 'close', 'open', 'high', 'low' (default 'close')
        """
        _FUNCTION_KEY = "DEMA"
        url = "{}function={}&symbol={}&interval={}&time_period={}"\
        "&series_type={}&apikey={}".format(AlphaVantage._ALPHA_VANTAGE_API_URL,
        _FUNCTION_KEY, symbol, interval, time_period, series_type, self.key)
        return self._handle_api_call(url,'Technical Analysis: DEMA','Meta Data')

    def get_tema(self, symbol, interval='60min', time_period=20, series_type='close'):
        """ Return triple exponential moving average time series in two json
        objects as data and meta_data. It raises ValueError when problems arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
        'weekly', 'monthly' (default '60min')
        time_period -- How many data points to average (default 20)
        series_type -- The desired price type in the time series. Four types
        are supported: 'close', 'open', 'high', 'low' (default 'close')
        """
        _FUNCTION_KEY = "TEMA"
        url = "{}function={}&symbol={}&interval={}&time_period={}"\
        "&series_type={}&apikey={}".format(AlphaVantage._ALPHA_VANTAGE_API_URL,
        _FUNCTION_KEY, symbol, interval, time_period, series_type, self.key)
        return self._handle_api_call(url,'Technical Analysis: TEMA','Meta Data')

    def get_trima(self, symbol, interval='60min', time_period=20, series_type='close'):
        """ Return triangular moving average time series in two json
        objects as data and meta_data. It raises ValueError when problems arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
        'weekly', 'monthly' (default '60min')
        time_period -- How many data points to average (default 20)
        series_type -- The desired price type in the time series. Four types
        are supported: 'close', 'open', 'high', 'low' (default 'close')
        """
        _FUNCTION_KEY = "TRIMA"
        url = "{}function={}&symbol={}&interval={}&time_period={}"\
        "&series_type={}&apikey={}".format(AlphaVantage._ALPHA_VANTAGE_API_URL,
        _FUNCTION_KEY, symbol, interval, time_period, series_type, self.key)
        return self._handle_api_call(url,'Technical Analysis: TRIMA','Meta Data')

    def get_kama(self, symbol, interval='60min', time_period=20, series_type='close'):
        """ Return Kaufman adaptative moving average time series in two json
        objects as data and meta_data. It raises ValueError when problems arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
        'weekly', 'monthly' (default '60min')
        time_period -- How many data points to average (default 20)
        series_type -- The desired price type in the time series. Four types
        are supported: 'close', 'open', 'high', 'low' (default 'close')
        """
        _FUNCTION_KEY = "KAMA"
        url = "{}function={}&symbol={}&interval={}&time_period={}"\
        "&series_type={}&apikey={}".format(AlphaVantage._ALPHA_VANTAGE_API_URL,
        _FUNCTION_KEY, symbol, interval, time_period, series_type, self.key)
        return self._handle_api_call(url,'Technical Analysis: KAMA','Meta Data')

    def get_mama(self, symbol, interval='60min', time_period=20, series_type='close',
    fastlimit=None, slowlimit=None):
        """ Return MESA adaptative moving average time series in two json
        objects as data and meta_data. It raises ValueError when problems arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
        'weekly', 'monthly' (default '60min')
        time_period -- How many data points to average (default 20)
        series_type -- The desired price type in the time series. Four types
        are supported: 'close', 'open', 'high', 'low' (default 'close')
        fastlimit -- Positive floats for the fast limit are accepted
        (default=None)
        slowlimit -- Positive floats for the slow limit are accepted
        (default=None)
        """
        _FUNCTION_KEY = "MAMA"
        url = "{}function={}&symbol={}&interval={}&time_period={}"\
        "&series_type={}".format(AlphaVantage._ALPHA_VANTAGE_API_URL,
        _FUNCTION_KEY, symbol, interval, time_period, series_type)
        if fastlimit:
            url="{}&fastlimit={}".format(url,fastlimit)
        if slowlimit:
            url="{}&slowlimit={}".format(url, slowlimit)
        url = "{}&apikey={}".format(url, self.key)
        return self._handle_api_call(url,'Technical Analysis: MAMA','Meta Data')

    def get_t3(self, symbol, interval='60min', time_period=20, series_type='close'):
        """ Return triple exponential moving average time series in two json
        objects as data and meta_data. It raises ValueError when problems arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
        'weekly', 'monthly' (default '60min')
        time_period -- How many data points to average (default 20)
        series_type -- The desired price type in the time series. Four types
        are supported: 'close', 'open', 'high', 'low' (default 'close')
        """
        _FUNCTION_KEY = "T3"
        url = "{}function={}&symbol={}&interval={}&time_period={}"\
        "&series_type={}&apikey={}".format(AlphaVantage._ALPHA_VANTAGE_API_URL,
        _FUNCTION_KEY, symbol, interval, time_period, series_type, self.key)
        return self._handle_api_call(url,'Technical Analysis: T3','Meta Data')

    def get_macd(self, symbol, interval='60min', series_type='close',
    fastperiod=None, slowperiod=None, signalperiod=None):
        """ Return the moving average convergence/divergence time series in two
        json objects as data and meta_data. It raises ValueError when problems
        arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
        'weekly', 'monthly' (default '60min'
        series_type -- The desired price type in the time series. Four types
        are supported: 'close', 'open', 'high', 'low' (default 'close')
        fastperiod -- Positive integers are accepted (default=None)
        slowperiod -- Positive integers are accepted (default=None)
        signalperiod -- Positive integers are accepted (default=None)
        """
        _FUNCTION_KEY = "MACD"
        url = "{}function={}&symbol={}&interval={}&series_type={}".format(
        AlphaVantage._ALPHA_VANTAGE_API_URL,_FUNCTION_KEY, symbol, interval,
        series_type)
        if fastperiod:
            url="{}&fastperiod={}".format(url,fastperiod)
        if slowperiod:
            url="{}&slowperiod={}".format(url, slowperiod)
        if signalperiod:
            url="{}&signalperiod={}".format(url, signalperiod)
        url = "{}&apikey={}".format(url, self.key)
        return self._handle_api_call(url,'Technical Analysis: MACD','Meta Data')

    def get_macdext(self, symbol, interval='60min', series_type='close',
    fastperiod=None, slowperiod=None, signalperiod=None, fastmatype=None,
    slowmatype=None, signalmatype=None):
        """ Return the moving average convergence/divergence time series in two
        json objects as data and meta_data. It raises ValueError when problems
        arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
        'weekly', 'monthly' (default '60min')
        series_type -- The desired price type in the time series. Four types
        are supported: 'close', 'open', 'high', 'low' (default 'close')
        fastperiod -- Positive integers are accepted (default=None)
        slowperiod -- Positive integers are accepted (default=None)
        signalperiod -- Positive integers are accepted (default=None)
        fastmatype -- Moving average type for the faster moving average.
        By default, fastmatype=0. Integers 0 - 8 are accepted
        (check  down the mappings) or the string containing the math type can
        also be used.
        slowmatype -- Moving average type for the slower moving average.
        By default, slowmatype=0. Integers 0 - 8 are accepted
        (check down the mappings) or the string containing the math type can
        also be used.
        signalmatype -- Moving average type for the signal moving average.
        By default, signalmatype=0. Integers 0 - 8 are accepted
        (check down the mappings) or the string containing the math type can
        also be used.

        0 = Simple Moving Average (SMA),
        1 = Exponential Moving Average (EMA),
        2 = Weighted Moving Average (WMA),
        3 = Double Exponential Moving Average (DEMA),
        4 = Triple Exponential Moving Average (TEMA),
        5 = Triangular Moving Average (TRIMA),
        6 = T3 Moving Average,
        7 = Kaufman Adaptive Moving Average (KAMA),
        8 = MESA Adaptive Moving Average (MAMA)
        """
        _FUNCTION_KEY = "MACDEXT"
        url = "{}function={}&symbol={}&interval={}&series_type={}".format(
        AlphaVantage._ALPHA_VANTAGE_API_URL,_FUNCTION_KEY, symbol, interval,
        series_type)
        if fastperiod:
            url="{}&fastperiod={}".format(url,fastperiod)
        if slowperiod:
            url="{}&slowperiod={}".format(url, slowperiod)
        if signalperiod:
            url="{}&signalperiod={}".format(url, signalperiod)
        if fastmatype:
            # Check if it is an integer or a string
            try:
                value = int(fastmatype)
            except ValueError:
                value = AlphaVantage._ALPHA_VANTAGE_MATH_MAP.index(fastmatype)
            url="{}&fastmatype={}".format(url, value)
        if slowmatype:
            # Check if it is an integer or a string
            try:
                value = int(slowmatype)
            except ValueError:
                value = AlphaVantage._ALPHA_VANTAGE_MATH_MAP.index(slowmatype)
            url="{}&slowmatype={}".format(url, value)
        if signalmatype:
            # Check if it is an integer or a string
            try:
                value = int(signalmatype)
            except ValueError:
                value = AlphaVantage._ALPHA_VANTAGE_MATH_MAP.index(signalmatype)
            url="{}&signalmatype={}".format(url, value)
        url = "{}&apikey={}".format(url, self.key)
        return self._handle_api_call(url,'Technical Analysis: MACDEXT',
        'Meta Data')


if __name__ == '__main__':
    av = AlphaVantage(key='486U')
    data, meta_data = av.get_sma('GOOGL')
    print(data)