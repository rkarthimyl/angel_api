import pandas as pd
import numpy as np
# import mplfinance as mpf
# import matplotlib.pyplot as plt

# Generate Example OHLC Data
data = {
    'Date': pd.date_range(start="2024-03-01", periods=10, freq='D'),
    'Open': [100, 102, 104, 106, 110, 108, 107, 103, 101, 99],
    'High': [105, 108, 107, 109, 112, 110, 108, 105, 103, 100],
    'Low': [99, 101, 103, 105, 109, 106, 105, 101, 99, 98],
    'Close': [104, 100, 106, 102, 111, 107, 106, 102, 100, 99],
    'Volume': [1000, 1500, 1200, 1800, 1300, 1600, 1400, 1700, 1550, 1650]
}


# Function to classify candlestick types
def identify_candlestick(row):
    open_price = row['Open']
    high = row['High']
    low = row['Low']
    close = row['Close']
    
    body = abs(close - open_price)
    upper_wick = high - max(open_price, close)
    lower_wick = min(open_price, close) - low
    total_range = high - low

    # Define thresholds
    body_size_ratio = body / total_range if total_range != 0 else 0
    wick_ratio = 0.3  # Wick proportion

    if close > open_price:
        if body_size_ratio > 0.7:
            return "Bullish Marubozu"
        elif lower_wick > body * 2:
            return "Hammer (Bullish Reversal)"
        elif lower_wick > upper_wick:
            return "Bullish Pin Bar"
    elif close < open_price:
        if body_size_ratio > 0.7:
            return "Bearish Marubozu"
        elif upper_wick > body * 2:
            return "Shooting Star (Bearish Reversal)"
        elif upper_wick > lower_wick:
            return "Bearish Pin Bar"
    if body_size_ratio < 0.3:
        if upper_wick > total_range * wick_ratio and lower_wick > total_range * wick_ratio:
            return "Doji"
        elif lower_wick > total_range * wick_ratio:
            return "Dragonfly Doji"
        elif upper_wick > total_range * wick_ratio:
            return "Gravestone Doji"
    
    return "Unknown"


# Function to Update Annotation
def update_annot(ind):
    index = ind["ind"][0]  # Get the first index from hover
    date = df.index[index].strftime('%Y-%m-%d')
    candle_type = df.iloc[index]['Candle_Type']
    annot.xy = (index, df.iloc[index]['Close'])
    annot.set_text(f"{date}\n{candle_type}")
    annot.set_visible(True)

# Mouse Hover Event
def on_hover(event):
    if event.inaxes == ax:
        for i, date in enumerate(df.index):
            if event.xdata and abs(event.xdata - i) < 0.5:  # Check proximity
                update_annot({'ind': [i]})
                fig.canvas.draw_idle()
                return
    annot.set_visible(False)
    fig.canvas.draw_idle()

# def show_Chart(df):
#     # df = pd.DataFrame(data)
#     # df.set_index('Date', inplace=True)
    
#     # Apply classification
#     df['Candle_Type'] = df.apply(identify_candlestick, axis=1)

#     # Plot with mplfinance
#     fig, ax = plt.subplots(figsize=(10, 6))
#     mpf.plot(df, type='candle', ax=ax, style='charles', volume=False)

#     # Create Annotation for Hover
#     annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
#                         bbox=dict(boxstyle="round", fc="w"),
#                         arrowprops=dict(arrowstyle="->"))
#     annot.set_visible(False)


#     fig.canvas.mpl_connect("motion_notify_event", on_hover)
#     plt.show()
