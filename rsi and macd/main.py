import pandas as pd
from TenIndicators.indicators import *

df = pd.read_csv('pastdata.csv')
print(df.head())

ate_macd = moving_average_convergence_divergence(df, 26, 12, 9)
rates_macd = exponential_moving_average(df, 20)
rate_macd = get_simple_moving_average(df, 20)
rsi = reltive_strength_index(df, 14)  # Calculating RSI with a 14-period window

final_rates = pd.concat([rate_macd.reset_index(drop=True), rsi.reset_index(drop=True)], axis=1)

# Drop duplicate columns
final_rates = final_rates.loc[:,~final_rates.columns.duplicated()]

# Print data types of macd and signal columns
print(final_rates[['macd', 'signal']].dtypes)

# Further investigation of final_rates DataFrame
print(final_rates.head())

trades = pd.DataFrame(columns=['state', 'order_type', 'open_time',
                               'open_price', 'close_time', 'close_price',
                               'exit_type', 'macd_value_at_sell', 'signal_value_at_sell', 'histogram', 'volume', "buy_sma_greater_ema"
                               ])


def is_bearish_crossover_over_zero(df, index):
    row = df.iloc[index]
    prev_row = df.iloc[index - 1]
    hist_trend_bearish = row['histogram'] < prev_row['histogram']
    macd_crossover = row['macd'] < row['signal']
    bearish_trend = row['signal'] > 0 and row['macd'] > 0 and macd_crossover and hist_trend_bearish
    return bearish_trend

rows, columns = final_rates.shape
sold = False
sell_price = 0
tp = .0060
sl = .0009
last_sold_index = 0
trading_units = 100000
last_sold_timestamp = None
exit_from_hrs = 3

for index, row in final_rates.iterrows():
    if index > 30 and ((index + 1) < rows):
        bearish_trend = is_bearish_crossover_over_zero(final_rates, index)
        rsi_overbought = row['rsi'] > 70  # RSI greater than 70 indicates overbought condition

        current_index_last_sold_delta = index - last_sold_index
        if not sold:
            if bearish_trend and rsi_overbought:
                print("Bearish trend and RSI overbought", row['converted_time'])
                sell_price = final_rates.iloc[index + 1]['open']
                last_sold_index = index
                stop_loss_price = sell_price + sl
                take_profit_price = sell_price - tp
                sma_greater_ema = row['sma'] < row['ema']
                trades.loc[len(trades)] = ['open', 'sell', final_rates.iloc[index + 1]['converted_time'], sell_price, None, None, None, row['macd'], row['signal'], row['histogram'], row['tick_volume'], None]
                last_sold_timestamp = final_rates.iloc[index + 1]['time']
                exit_time_stamp = last_sold_timestamp + (exit_from_hrs * 60 * 60)
                sold = True

        elif sold and (current_index_last_sold_delta > 3):
            if row['high'] > stop_loss_price:
                exit_type = "stop_loss"
                sold = False
                sma_greater_ema = row['sma'] < row['ema']
                trades.loc[trades['state'] == 'open', ['state', 'close_time', 'close_price', 'exit_type', "buy_sma_greater_ema"]] = ['closed', row['converted_time'], stop_loss_price, exit_type, sma_greater_ema]

            elif row['low'] < take_profit_price:
                sold = False
                exit_type = "take_profit"
                sma_greater_ema = row['sma'] < row['ema']
                trades.loc[trades['state'] == 'open', ['state', 'close_time', 'close_price', 'exit_type', 'buy_sma_greater_ema']] = ['closed', final_rates.iloc[index]['converted_time'], take_profit_price, exit_type, sma_greater_ema]

            elif rsi_overbought and bearish_trend:
                continue
            else:
                sold = False
                close_price = final_rates.iloc[index + 1]['open']
                if sell_price > close_price:
                    exit_type = "profit_on_bullish_trend"
                else:
                    exit_type = "loss_on_bullish_trend"
                sma_greater_ema = row['sma'] < row['ema']
                trades.loc[trades['state'] == 'open', ['state', 'close_time', 'close_price', 'exit_type', 'buy_sma_greater_ema']] = ['closed', final_rates.iloc[index + 1]['converted_time'], final_rates.iloc[index + 1]['open'], exit_type, sma_greater_ema]

def calc_profit(x):
    if x['order_type'] == 'sell':
        try:
            return (x['open_price'] - x['close_price']) * trading_units
        except:
            return 0

def cal_exit_type(row):
    try:
        if row['close_price'] < row['open_price']:
            return "profit"
        else:
            return "loss"
    except:
        return "none"

trades['profit'] = trades.apply(calc_profit, axis=1)
trades['pnl'] = trades['profit'].cumsum()
trades['trade_type'] = trades.apply(cal_exit_type, axis=1)
trade_type_counts = trades['trade_type'].value_counts()
print(trade_type_counts)

exit_types = trades['exit_type'].value_counts()
print("Exit types", exit_types)

trades.to_csv('is_bearish_crossover.csv', index=True)