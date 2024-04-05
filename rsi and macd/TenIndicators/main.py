from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
import pytz
import mplfinance as mpf
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if not mt5.initialize():
    print("initialize() failed", mt5.last_error())
    mt5.shutdown()
    exit()

authorized = mt5.login(5615808, "4nIr!qCx", "FXView-Demo")

if not authorized:
    print("login() failed", mt5.last_error())
    mt5.shutdown()
    exit()

def get_past_rates(symbol:str,timeframe:int,count):
    rates = mt5.copy_rates_from_pos(symbol, timeframe,0,count)
    rates_frame = pd.DataFrame(rates)
    rates_frame["time"] = pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame = rates_frame[['time', 'open', 'high', 'low', 'close']]
    return rates_frame


def get_simple_moving_average(rates, period):
    rates["sma"] = rates['close'].rolling(period).mean()
    return rates

def exponential_moving_average(rates, period):
    rates["ema"] = rates['close'].ewm(span=period, min_periods=period).mean()
    return rates

def average_true_range(rates, period=14):
    rates['h-l'] = rates['high'] - rates['low']
    rates['h-yc'] = abs(rates['high'] - rates['close'].shift())
    rates['l-yc'] = abs(rates['low'] - rates['close'].shift())
    rates['tr'] = rates[['h-l', 'h-yc', 'l-yc']].max(axis=1, skipna=False)
    rates['atr'] = rates['tr'].rolling(period).mean()
    return rates


def bollinger_bands(rates, period=20, std=2):
    rates['sma'] = rates['close'].rolling(period).mean()
    rates['std'] = rates['close'].rolling(period).std()
    rates['upper_band'] = rates['sma'] + (rates['std'] * std)
    rates['lower_band'] = rates['sma'] - (rates['std'] * std)
    return rates

def moving_average_convergence_divergence(rates, period_long=26, period_short=12, period_signal=9):
    rates['ema_long'] = rates['close'].ewm(span=period_long, min_periods=period_long).mean()
    rates['ema_short'] = rates['close'].ewm(span=period_short, min_periods=period_short).mean()
    rates['macd'] = rates['ema_short'] - rates['ema_long']
    rates['signal'] = rates['macd'].ewm(span=period_signal, min_periods=period_signal).mean()
    return rates




