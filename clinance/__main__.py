#!/usr/bin/env python3
import pandas as pd
import defopt
import os
from tabulate import tabulate
from panance import Panance
from finta import TA
from clinance import __version__

volume_headers = ['Symbol', 'Vol. 0', 'Vol. 1', 'Vol. 2', 'Close']

key, secret = os.getenv('BINANCE_KEY'), os.getenv('BINANCE_SECRET')
api = Panance() if any((key is None, secret is None, not len(key), not len(secret))) else Panance(key, secret)


def sell(symbol, amount, price):
    """
    Place a limit sell order.

    :param str symbol: trade pair (example: BTC/USDT)
    :param amount: amount to sell in base currency ("max" or percentage as "<n>%" are also accepted)
    :type amount: str or float
    :param price:  order sell price ("bid" or "ask" also accepted)
    :type price: str or float
    """
    print(api.limit_sell(symbol, amount, price))


def buy(symbol, amount, price):
    """
    Place a limit buy order.

    :param str symbol: trade pair (example: BTC/USDT)
    :param amount: amount to buy in quote currency ("max" or percentage as "<n>%" are also accepted)
    :type amount: str or float
    :param price:  order buy price ("bid" or "ask" also accepted)
    :type price: str or float

    """
    print(api.limit_buy(symbol, amount, price))


def cancel(symbol, order_id):
    """
    Cancel an order by id.

    :param str symbol: trade pair (example: BTC/USDT)
    :param int order_id: the order id
    """
    print(api.cancel_order(order_id, symbol))


def cost(symbol):
    """
    Get weighted average cost for a symbol.

    :param str symbol: trade pair (example: BTC/USDT)
    """
    costs = api.get_weighted_average_cost(symbol=symbol)
    print('[{}] WAvg. Cost: {:12.8f}'.format(symbol, costs))


def open(symbol):
    """
    Get all open orders for a symbol.

    :param str symbol: trade pair (example: BTC/USDT)
    """
    open_orders = api.fetch_open_orders(symbol=symbol)
    result = list()
    if len(open_orders):
        for r in open_orders:
            del r['info'], r['lastTradeTimestamp'], r['fee'], r['symbol'], r['timestamp']
            r['date'] = r.pop('datetime').replace('T', ' ').split('.')[0]
            result.append(r)
    print(tabulate(result, headers='keys'))


def balance(coin=None):
    """
    Get all open orders for a symbol.

    :param str coin: if set it will work as balance a filter (example: BTC) (default None)
    """

    print(api.get_balances(coin=coin.upper()) if coin else api.get_balances())


def stoploss(symbol, factor=1.5, current: bool = False):
    """
    Get ATR based stop loss price for a symbol.

    :param str symbol: trade pair (example: BTC/USDT)
    :param float factor: ATR factor (default 1.5)
    :param current: if True stop loss will be calculated from current value instead last buy price
    """
    atr = TA.ATR(api.get_ohlc(symbol, '15m'))
    # print(atr.values[-1])
    last_buy_price = 0.0
    if not current:
        for l in api._LIMITS:
            last_buy = api.get_user_trades(symbol, l, 'buy')
            if not last_buy.empty:
                last_buy_price = last_buy.price.values[-1]
    else:
        lasts = api.get_trades(symbol, 5)
        last_buy_price = lasts.price.values[-1]
    atr_value = atr.values[-1]
    atr_variation = float(factor * atr_value)
    print('[{: <9}] Cost: {:12.8f}, StopLoss: {:12.8f}'.format(symbol, last_buy_price, last_buy_price - atr_variation))
    # print(api.get_balances(coin=coin.upper()) if coin else api.get_balances())


def profit(coin):
    """
    Get current profit for a currency.

    :param str coin: currency (example: BTC)
    """
    print('[{}] Profit: {:+10.8f}, Cost:  {:10.8f}'.format(coin.upper(), *api.get_profit(coin)))


def depth(symbol, limit=10):
    """
    Get order book data for a symbol.

    :param str symbol: trade pair (example: BTC/USDT)
    :param int limit: max rows to retrieve
    """
    ob = api.get_depth(symbol, limit=limit)
    base, quote = symbol.split('/')

    num_format = '9.8f'
    if 'USD' in quote:
        num_format = '9.3f'
    print(tabulate(ob.values, headers=['Ask', 'Amount', 'Bid', 'Amount'], stralign='right', numalign='right',
                   floatfmt=num_format, disable_numparse=[1, 3]))


def volume(limit=10, timeframe='1m', exchange='BTC'):
    """
    Show an desc volume sorted symbol list for 1 minute time-frame (useful to detect rising markets)

    :param int limit: limit list entries (default 10)
    :param str timeframe: time frame used. Accepted values: 1m, 3m, 5m, 15m, 1h, 2h, 4h, 1d (default 1m)
    :param str exchange: exchange used (default BTC)
    """
    tickers = api.get_tickers()  # type: pd.DataFrame

    filtered = tickers.T.select(lambda v: v.split('/')[1] in [exchange]).sort_values('baseVolume', ascending=False).T

    symbols = [*filtered.T.keys()][:limit]
    top_symbols = filtered.T[symbols].T
    table_data = list()
    if timeframe is not None and timeframe not in '1m':
        tf = timeframe

    for ts in top_symbols:

        ohlc = api.get_ohlc(ts, timeframe=tf)
        ohlc['qvolume'] = ohlc.close * ohlc.volume
        if not (ohlc.qvolume > 2.0)[-3:].all():
            continue
        vol0 = ohlc.qvolume[-1]
        vol1 = ohlc.qvolume[-2]
        vol2 = ohlc.qvolume[-3]
        close = ohlc.close.apply(lambda s: '{:9.8f}'.format(s))
        table_data.append([ts, vol0, vol1, vol2, close[-1]])
    print(tabulate(table_data, headers=volume_headers, numalign='right', floatfmt='.3f', disable_numparse=[4]))

    return filtered.T[symbols]


def main(args):
    global verbose, json, csv
    json, csv, verbose = False, False, False
    verbose = '--verbose' in args or '-v' in args
    version = '--version' in args or '-V' in args
    csv = '--csv' in args
    if not csv:
        json = '--json' in args

    if version:
        print(__version__)
        return 0
    else:
        defopt.run(cost, depth, volume, profit, stoploss, balance, buy, sell, cancel, open)
        return 0


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv[1:]))
