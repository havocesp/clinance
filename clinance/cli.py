#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time as tm
from collections import OrderedDict

import begin
import pandas as pd
import pantulipy as ta
import term as trm
from panance import Panance, _LIMITS
from tabulate import tabulate

if not len(sys.argv[1:]):
    sys.argv.append('-h')

OHLCV_FIELDS = ['real', 'open', 'high', 'low', 'close', 'volume']

echo = print if sys.platform in 'win32' else trm.writeLine

VOLUME_HEADERS = ['Symbol', 'Last Vol.', 'Prev. Vol.', 'Close']
DEPTH_HEADERS = ['Ask', 'Amount', 'Bid', 'Amount']
TABLE_CONFIG = dict(stralign='right', numalign='right', floatfmt='9.8f')

help_fmt = begin.formatters.compose(begin.formatters.RawDescription, begin.formatters.ArgumentDefaults)


@begin.subcommand
@begin.convert(amount=float, price=float)
def sell(symbol, amount, price):
    """
    Place a limit sell order.

    :param str symbol: trade pair (example: BTC/USDT)
    :param amount: amount to sell in base currency ("max" or percentage as "<n>%" are also accepted)
    :type amount: str or float
    :param price:  order sell price ("bid" or "ask" also accepted)
    :type price: str or float
    """

    echo(api.limit_sell(symbol, amount, price))


@begin.subcommand
@begin.convert(amount=float, price=float)
def buy(symbol, amount, price):
    """
    Place a limit buy order.

    :param str symbol: trade pair (example: BTC/USDT)
    :param amount: amount to buy in quote currency ("max" or percentage as "<n>%" are also accepted)
    :type amount: str or float
    :param price:  order buy price ("bid" or "ask" also accepted)
    :type price: str or float
    """
    echo(api.limit_buy(symbol, amount, price))


@begin.subcommand
@begin.convert(order_id=int)
def cancel(symbol, order_id):
    """
    Cancel an order by id.

    :param str symbol:
    :param int order_id: the order id
    """
    echo(api.cancel_order(order_id, symbol))


@begin.subcommand
def cost(symbol):
    """
    Get weighted average cost for a symbol.

    :param str symbol: trade pair (example: BTC/USDT)
    """
    costs = api.get_weighted_average_cost(symbol=symbol)
    echo('[{}] Cost: {:12.8f}'.format(symbol, costs))


@begin.subcommand
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
    echo(tabulate(result, headers='keys'))


@begin.subcommand
def balance(coin=None, detailed='n'):
    """
    Get all open orders for a symbol.

    :param str coin: if set it will work as balance a filter (example: BTC) (default None)
    :param str detailed: set to "y" to get a detailed view of your wallet (default "n")
    """

    coin = str(coin).upper() if not str(coin).isupper() else str(coin)
    detailed = str(detailed).lower()
    params = dict()
    if 'y' in detailed:
        params = dict(detailed=True)
    if coin not in 'NONE':
        params.update(coin=coin)
    balance = api.get_balances(**params)  # type: pd.DataFrame
    balance.index = pd.Index(data=balance.index.map(lambda s: '[' + s.title() + ']'), name='Status')

    echo(tabulate(balance.sort_index().to_records(index=True), headers='keys'))


@begin.subcommand
@begin.convert(factor=float)
def stoploss(symbol, factor=1.5, period=14, current=False):
    """
    Get ATR based stop loss price for a symbol.

    :param str symbol: trade pair (example: BTC/USDT)
    :param float factor: ATR factor (default 1.5)
    :param bool current: if True stop loss will be calculated from current value instead last buy price
    """
    ohlc = api.get_ohlc(symbol, '15m')
    atr = ta.atr(ohlc, period)
    last_buy_price = 0.0

    if not current:
        for l in _LIMITS:
            last_buy = api.get_user_trades(symbol, l, 'buy')

            if not last_buy.empty:
                last_buy_price = last_buy.price.values[-1]
    else:

        lasts = api.get_trades(symbol, 5)
        last_buy_price = lasts.price[-1]

    atr_value = atr[-1]
    atr_variation = factor * atr_value

    echo('[{: <9}] Cost: {:12.8f}, StopLoss: {:12.8f}'.format(symbol, last_buy_price, last_buy_price - atr_variation))


@begin.subcommand
@begin.convert(coin=str)
def profit(coin):
    """
    Get current profit for a currency.

    :param str coin: a currency or list of comma separated currencies (example: BTC,ETH)
    """

    coin = str(coin).upper()

    if 'NONE' not in coin:
        if ',' in coin:
            coin = [s for s in map(lambda s: s.upper().replace(' ', ''), coin.split(','))]
        else:
            coin = [coin.replace(' ', '')]
        for c in coin:
            echo('[{}] Profit: {:+10.8f}, Cost:  {:10.8f}'.format(c.upper(), *api.get_profit(c)))
            tm.sleep(1)
    else:
        echo('ERROR: invalid coin {}'.format(coin), trm.red)


@begin.subcommand
@begin.convert(symbol=str, limit=int)
def depth(symbol, limit=10):
    """
    Get order book data for a symbol.

    :param str symbol: trade pair (example: BTC/USDT).
    :param int limit: max rows to retrieve.
    """

    ob = api.get_depth(symbol, limit=limit)
    base, quote = symbol.split('/')

    num_format = '9.8f'
    if 'USD' in quote:
        num_format = '9.3f'
    TABLE_CONFIG.update(floatfmt=num_format)
    echo(tabulate(ob.values, headers=DEPTH_HEADERS, disable_numparse=[1, 3], **TABLE_CONFIG))


@begin.subcommand
@begin.convert(minvol=float, limit=int, exchange=str)
def volume(min_vol=1000.0, limit=20, exchange='BTC'):
    """
    Show an desc volume sorted symbol list for 1 minute time-frame (useful to detect rising markets)

    :param float min_vol: volume filter cutoff value (default 1000.0 BTC)
    :param int limit: limit markets list
    :param str exchange: exchange used (default BTC)
    """

    tickers = api.get_tickers(market=exchange).query('quoteVolume > {}'.format(min_vol))
    tickers = tickers.sort_values('quoteVolume', ascending=False).T
    if len(tickers) > limit:
        tickers = tickers[:limit]
    table_data = list()

    tf = '1m'

    for num, ts in enumerate(tickers.keys()):
        if num == 0: trm.clear()

        trm.pos(1, 1), trm.clearLine()
        echo('({:d}/{:d}) Loading {} ...\n'.format(num + 1, len(tickers.columns), ts))
        ohlc = api.get_ohlc(ts, timeframe=tf)  # type: pd.DataFrame

        ohlc['qvolume'] = ohlc['close'] * ohlc['volume']

        if (ohlc['qvolume'] > min_vol)[-3:].all():
            continue
        tickers[ts]['ohlc'] = ohlc
        last = '{:9.8f}'.format(tickers[ts]['last'])

        table_data.append([ts, tickers[ts]['ohlc']['qvolume'][-1], tickers[ts]['ohlc']['qvolume'][-2], last])

    print(tabulate(table_data, headers=VOLUME_HEADERS, numalign='right', floatfmt='.3f'))  # disable_numparse=[3]))


@begin.subcommand
@begin.convert(symbols=str)
def ticker(symbols):
    """
    Get ticker data for a symbol.

    :param str symbols: trade pair (example: BTC/USDT).
    """

    if ',' in symbols.replace(' ', ''):
        symbols = [s for s in map(lambda s: str(s).upper(), symbols.split(','))]
    else:
        symbols = [str(symbols).upper()]
    tickers = api.get_tickers(symbols=symbols).T  # type: pd.DataFrame
    data = list()
    for symbol in symbols:
        ticker = tickers[symbol].T  # type: pd.Series

        if ticker is not None:
            ticker['Symbol'] = symbol
            ticker.drop(['change', 'baseVolume', 'previousClose', 'bidVolume', 'askVolume'], inplace=True)
            ticker.T.index = ticker.T.index.map(lambda s: s.title() if isinstance(s, str) else s)
            ticker['Volume'] = ticker.pop('Quotevolume')
            ticker['VWAP'] = ticker.pop('Vwap')
            ticker['Percent'] = round(ticker.pop('Percentage'), 2)
            ticker['Volume'] = '{:9.2f}'.format(ticker.pop('Volume'))

            ticker_dict = ticker.to_dict(into=OrderedDict)  # type: OrderedDict

            ticker_dict.move_to_end('Symbol', last=False)
            ticker_dict.move_to_end('Volume')
            ticker_dict.move_to_end('Percent')

            data.extend([ticker_dict])

    fields_count = len(data[0].keys())
    tbl = tabulate(data, headers='keys', numalign='right', floatfmt='9.8f',
                   disable_numparse=[fields_count - 2, fields_count - 1])
    echo(tbl)


@begin.start(auto_convert=True, formatter_class=help_fmt)
@begin.logging
def main(csv=False, json=False, version=False):
    """
    Binance cryptocurrency exchange client from CLI
    """
    global api
    if version: pass
    if csv: pass
    if json: pass
    key = os.getenv('BINANCE_KEY')
    secret = os.getenv('BINANCE_SECRET')
    globals().update(api=Panance(key, secret) if key and secret else Panance())
