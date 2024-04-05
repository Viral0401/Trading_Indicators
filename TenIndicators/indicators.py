import MetaTrader5 as mt5
import pandas as pd


def get_past_rates(symbol:str,timeframe:int,count:int):
    rates = mt5.copy_rates_from_pos(symbol, timeframe,0,count)
    rates_frame = pd.DataFrame(rates)
    #if not in_unix:
    rates_frame["converted_time"] = pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame = rates_frame[['converted_time','time', 'open', 'high', 'low', 'close']]
    return rates_frame



def get_simple_moving_average(rates, period):
    rates["sma"] = rates['close'].rolling(period).mean()
    print(rates.tail(1))
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
    rates['histogram'] = rates['macd'] - rates['signal']
    return rates


def reltive_strength_index(rates, period=14):
    delta = rates['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    rates['rsi'] = 100 - (100 / (1 + rs))
    return rates

def rsi_signal(df, period=14):
    # setting the RSI Period
    rsi_period = period

    # to calculate RSI, we first need to calculate the exponential weighted aveage gain and loss during the period
    df['gain'] = (df['close'] - df['open']).apply(lambda x: x if x > 0 else 0)
    df['loss'] = (df['close'] - df['open']).apply(lambda x: -x if x < 0 else 0)

    # here we use the same formula to calculate Exponential Moving Average
    df['ema_gain'] = df['gain'].ewm(span=rsi_period, min_periods=rsi_period).mean()
    df['ema_loss'] = df['loss'].ewm(span=rsi_period, min_periods=rsi_period).mean()

    # the Relative Strength is the ratio between the exponential avg gain divided by the exponential avg loss
    df['rs'] = df['ema_gain'] / df['ema_loss']

    # the RSI is calculated based on the Relative Strength using the following formula
    df['rsi'] = 100 - (100 / (df['rs'] + 1))
    return df


