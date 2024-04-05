from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

def historgram_regression_trend_analysis(data, show_trend_line):
    # Extract the first 10 closing prices
    row, column = data.shape

    if row <2:
        row = row
    else:
        row = 2
    first_10_closes = data['histogram'][:row]
    
    # Prepare the data for linear regression
    # Reshape x data to (-1, 1) because it's a single feature
    x = np.arange(row).reshape(-1, 1)  # Indices as the independent variable
    y = first_10_closes.values.reshape(-1, 1)  # Closing prices as the dependent variable

    # Perform linear regression
    model = LinearRegression()
    model.fit(x, y)
  
    # Retrieve the slope (coefficient) of the line
    slope = model.coef_[0][0]
    # Determine the trend based on the slope
    if slope > 0:
        trend = "Uptrend"
    elif slope < 0:
        trend = "Downtrend"
    else:
        trend = "Sideways/No clear trend"
    if show_trend_line:
        y_pred = model.predict(x)
        plt.scatter(x, y, color='blue', label='Original Data')

        # Plot the regression line
        plt.plot(x, y_pred, color='red', label='Trend Line')
        plt.xlabel('Index')
        plt.ylabel('Histogram Value')
        plt.title('Histogram Regression Trend Analysis')
        plt.legend()

        # Show the plot
        plt.show()
    
    return trend



def close_price_regression_analysis(data, show_trend_line):
    # Extract the first 10 closing prices

    row,column = data.shape

    first_10_closes = data['close']
    
    # Prepare the data for linear regression
    # Reshape x data to (-1, 1) because it's a single feature
    x = np.arange(row).reshape(-1, 1)  # Indices as the independent variable
    y = first_10_closes.values.reshape(-1, 1)  # Closing prices as the dependent variable

    # Perform linear regression
    model = LinearRegression()
    model.fit(x, y)
  
    # Retrieve the slope (coefficient) of the line
    slope = model.coef_[0][0]

    slope_threshold = 0.0003
    # Determine the trend based on the slope
    if abs(slope) < slope_threshold:
        trend = "Sideways"
    elif slope > 0:
        trend = "Uptrend"
    else:
        trend = "Downtrend"

    #print(trend,slope)
    
    if show_trend_line:
        y_pred = model.predict(x)
        plt.scatter(x, y, color='blue', label='Original Data')

        # Plot the regression line
        plt.plot(x, y_pred, color='red', label='Trend Line')
        plt.xlabel('Index')
        plt.ylabel('Closing Price')
        plt.title('Closing Price Regression Trend Analysis')
        plt.legend()

        # Show the plot
        plt.show()
    
   
    
    return trend



