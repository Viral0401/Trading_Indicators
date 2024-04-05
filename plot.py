import plotly.graph_objects as go
import pandas as pd

# Load the dataset
df = pd.read_csv('pastdata.csv')

# Create candlestick figure
fig = go.Figure(data=[go.Candlestick(x=df['converted_time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

# Customize layout
fig.update_layout(
    title='Candlestick Chart',
    xaxis_title='Time',
    yaxis_title='Price',
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="RebeccaPurple"
    )
)

# Show the plot
fig.show()
