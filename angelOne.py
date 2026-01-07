import pandas as pd
import numpy as np
import mplfinance as mpf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.dates as mdates
from sklearn.preprocessing import MinMaxScaler

# import test2 as t2

def place_Order(smartApi):
    try:
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": "SBIN-EQ",
            "symboltoken": "3045",
            "transactiontype": "BUY",
            "exchange": "NSE",
            "ordertype": "LIMIT",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": "19600",
            "squareoff": "0",
            "stoploss": "0",
            "quantity": "1"
            }
        
        # Method 1: Place an order and return the order ID
        orderid = smartApi.placeOrder(orderparams)
        return (f"PlaceOrder : {orderid}")
        # Method 2: Place an order and return the full response
        #response = smartApi.placeOrderFullResponse(orderparams)
        #print(f"PlaceOrder : {response}")
    except Exception as e:
        return f"Order placement failed: {e}"

def cancel_order(smartApi, variety, orderid):
    try:

        # Method 1: Place an order and return the order ID
        response = smartApi.cancelOrder(orderid, variety)
        return (f"CancelOrder : {response}")
        # Method 2: Place an order and return the full response
        #response = smartApi.placeOrderFullResponse(orderparams)
        #print(f"PlaceOrder : {response}")
    except Exception as e:
        return f"Order placement failed: {e}"

def stoploss_Order(smartApi,stoploss_price,quantity,symboltoken,tradingsymbol,exchange,transactiontype,producttype,ordertype,duration,price,triggerprice):
    try:
        orderparams =  {
            "variety": "STOPLOSS",
            "tradingsymbol": tradingsymbol,
            "symboltoken": symboltoken,
            "transactiontype": transactiontype,
            "exchange": exchange,
            "ordertype": ordertype,
            "producttype": producttype,
            "duration": duration,
            "price": price,               # Limit price (e.g., sell at ₹11.50 or better)
            "triggerprice": triggerprice,        # Trigger when price <= ₹12.00
            "quantity": quantity
        }

        # orderparams =  {
        #     "variety": "STOPLOSS",
        #     "tradingsymbol": tradingsymbol,
        #     "symboltoken": symboltoken,
        #     "transactiontype": "SELL",
        #     "exchange": "BFO",
        #     "ordertype": "STOPLOSS_LIMIT",
        #     "producttype": "CARRYFORWARD",
        #     "duration": "DAY",
        #     "price": "10.50",               # Limit price (e.g., sell at ₹11.50 or better)
        #     "triggerprice": "11.00",        # Trigger when price <= ₹12.00
        #     "quantity": "20"
        # }


        # Method 1: Place an order and return the order ID
        orderid = smartApi.placeOrder(orderparams)
        return (f"PlaceOrder : {orderid}")
        # Method 2: Place an order and return the full response
        #response = smartApi.placeOrderFullResponse(orderparams)
        #print(f"PlaceOrder : {response}")
    except Exception as e:
        return f"Order placement failed: {e}"


def get_CandleStick(smartApi):
    try:
        historicParam={
        "exchange": "NSE",
        "symboltoken": "3045",
        "interval": "FIVE_MINUTE",
        "fromdate": "2025-02-01 09:00", 
        "todate": "2025-03-05 12:15"
        }
        response=smartApi.getCandleData(historicParam)
        data=response['data']
        print(f"GetCandleData : {data}")
        get_Chart(data)
    except Exception as e:
        print(f"Historic Api failed: {e}")

def get_Chart(data):
    # Load CSV
    

    df = pd.DataFrame(data)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
   
    df['Volume']=0
    # Convert Date to datetime and set as index
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date').sort_index()
    


    # Predict next 10 time steps
    future_steps = 10
    df['Prediction'] = df['Close'].shift(-future_steps)
    df.dropna(inplace=True)


    # Define X (features) and y (target)
    X = np.array(df[['Close']])
    y = np.array(df['Prediction'])

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Linear Regression Model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict Future Prices
    last_closing_price = df['Close'].iloc[-future_steps:].values.reshape(-1, 1)
    future_prices = model.predict(last_closing_price)

    # Create Future Dates
    future_dates = pd.date_range(start=df.index[-1], periods=future_steps+1, freq='5T')[1:]
    # future_df = pd.DataFrame({'Date': future_dates, 'Predicted_Close': future_prices})
    # future_df.set_index('Date', inplace=True)

    predicted_close = np.linspace(df['Close'].iloc[-1], df['Close'].iloc[-1] * 1.02, future_steps)
    predicted_open = np.roll(predicted_close, 1)
    predicted_open[0] = df['Close'].iloc[-1]
    predicted_high = predicted_close * 1.02
    predicted_low = predicted_close * 0.98

    # Create Future DataFrame
    future_df = pd.DataFrame({
        'Date': future_dates,
        'Open': predicted_open,
        'High': predicted_high,
        'Low': predicted_low,
        'Close': predicted_close,
        'Volume': np.zeros(future_steps)  # Volume = 0 for predicted data
    })
    future_df.set_index('Date', inplace=True)

    df_combined = pd.concat([df.tail(30), future_df])
    # t2.chartCheck(df)
    exit()
    mc.show_Chart(df_combined)
    #mpf.plot(df_combined, type='candle', style='charles', volume=True, title="Actual Prices", datetime_format='%H:%M',ylabel="Price")

    fig, ax = mpf.plot(df_combined, 
                    type='candle', 
                    style='charles', 
                    volume=True, 
                    title="5-Minute Interval Candlestick Chart", 
                    ylabel="Price", 
                    datetime_format='%H:%M', 
                    returnfig=True)  # Return figure for further customization

    ax[0].xaxis.set_major_locator(mdates.MinuteLocator(interval=600))  # Set x-axis labels every 5 minutes
    #ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))   # Format x-axis labels as HH:MM
    ax[0].tick_params(axis='x', rotation=90)  # Rotate labels for better visibility

    mpf.show()