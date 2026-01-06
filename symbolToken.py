
def get_eq_token(df,symbol,exchange="NSE"):
    row = df[
        (df['name'] == symbol) &
        (df['exch_seg'] == exchange) 
        #& (df['instrumenttype'] == 'EQ')
    ]
    return row.iloc[0]['token']

def get_nifty_fut_token(df,symbol):
    nifty_fut = df[
        (df['name'] == 'NIFTY') &
        (df['exch_seg'] == 'NFO') &
        (df['instrumenttype'] == 'FUTIDX')
    ][['symbol','token','expiry']]
    return nifty_fut

def get_nifty_token(df,symbol):
    nifty_ce = df[
        (df['name'] == 'NIFTY') &
        (df['exch_seg'] == 'NFO') &
        (df['instrumenttype'] == 'OPTIDX') &
        (df['symbol'].str.endswith(symbol))
    ][['symbol','token','expiry']]
    nifty_ce = nifty_ce.sort_values(by='expiry', ascending=True)
    # Take the first row
    row = nifty_ce.iloc[0]

    # Return as symbol, token, expiry
    return row['symbol'], row['token'], row['expiry']

def get_sensex_token(df,symbol):
    nifty_ce = df[
        (df['name'] == 'SENSEX') &
        (df['exch_seg'] == 'BFO') &
        (df['instrumenttype'] == 'OPTIDX') &
        (df['symbol'].str.endswith(symbol))
    ][['symbol','token','expiry']]
    nifty_ce = nifty_ce.sort_values(by='expiry', ascending=True)
    # Take the first row
    row = nifty_ce.iloc[0]

    # Return as symbol, token, expiry
    return row['symbol'], row['token'], row['expiry']