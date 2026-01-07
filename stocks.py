import pandas as pd
from datetime import datetime
import myChart as mc
import mplfinance as mpf
import matplotlib.dates as mdates

def get_CandleStick(smartApi,exchange,symboltoken,interval):
    start_time = datetime.now().strftime("%Y-%m-%d 09:00")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"Start Time: {start_time}")
    print(f"Current Time: {current_time}")  
    try:
        historicParam={
        "exchange": exchange,
        "symboltoken": symboltoken,
        "interval": interval,
        "fromdate": start_time, 
        "todate": current_time
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
    df_combined=df.copy()

    mc.show_Chart(df_combined)
    #mpf.plot(df_combined, type='candle', style='charles', volume=True, title="Actual Prices", datetime_format='%H:%M',ylabel="Price")
    exit()
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

def get_SymbolToken(smartApi,exchange,symbol):
    try:
        response=smartApi.searchscrip({'exchange':exchange,'searchtext':symbol})
        data=response['data']
        print(f"Search Scrip : {data}")
    except Exception as e:
        print(f"Search Scrip Api failed: {e}")    
        
