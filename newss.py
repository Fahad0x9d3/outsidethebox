import requests
import pandas as pd

# Define API endpoint and parameters
url = 'https://api.binance.com/api/v3/klines'
params = {
    'symbol': 'XRPUSDT',
    'interval': '1h',
    'limit': 10000
}

# Retrieve data from Binance API
response = requests.get(url, params=params)
data = response.json()

# Convert data to pandas dataframe
df = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])

# Convert timestamp to datetime format
df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')

# Define trading strategies
def strategy_1(df):
    # Convert Close column to numeric data type
    df['Close'] = pd.to_numeric(df['Close'])

    # Buy signal: price crosses above 50-day moving average
    if df['Close'].iloc[-1] > df['Close'].rolling(window=50).mean().iloc[-1]:
        return 'Buy'
    # Sell signal: price crosses below 50-day moving average
    elif df['Close'].iloc[-1] < df['Close'].rolling(window=50).mean().iloc[-1]:
        return 'Sell'
    else:
        return 'Hold'

def strategy_2(df):
    # Convert Close column to numeric data type
    df.loc[:, 'Close'] = pd.to_numeric(df['Close'])

    # Buy signal: price crosses above 200-day moving average
    if df['Close'].iloc[-1] > df['Close'].rolling(window=200).mean().iloc[-1]:
        return 'Buy'
    # Sell signal: price crosses below 200-day moving average
    elif df['Close'].iloc[-1] < df['Close'].rolling(window=200).mean().iloc[-1]:
        return 'Sell'
    else:
        return 'Hold'

def strategy_3(df):
    # Convert Close column to numeric data type
    df.loc[:, 'Close'] = pd.to_numeric(df['Close'])

    # Buy signal: MACD line crosses above signal line
    if df['Close'].iloc[-1] > df['Close'].ewm(span=12).mean().iloc[-1] - df['Close'].ewm(span=26).mean().iloc[-1]:
        return 'Buy'
    # Sell signal: MACD line crosses below signal line
    elif df['Close'].iloc[-1] < df['Close'].ewm(span=12).mean().iloc[-1] - df['Close'].ewm(span=26).mean().iloc[-1]:
        return 'Sell'
    else:
        return 'Hold'

def strategy_4(df):
    # Convert Close column to numeric data type
    df.loc[:, 'Close'] = pd.to_numeric(df['Close'])

    # Calculate RSI
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Buy signal: RSI crosses above 30
    if rsi.iloc[-1] > 30:
        return 'Buy'
    # Sell signal: RSI crosses below 70
    elif rsi.iloc[-1] < 70:
        return 'Sell'
    else:
        return 'Hold'

def strategy_5(df):
    # Convert Close column to numeric data type
    df.loc[:, 'Close'] = pd.to_numeric(df['Close'])

    # Buy signal: price crosses above upper Bollinger Band
    if df['Close'].iloc[-1] > df['Close'].rolling(window=20).mean().iloc[-1] + 2 * df['Close'].rolling(window=20).std().iloc[-1]:
        return 'Buy'
    # Sell signal: price crosses below lower Bollinger Band
    elif df['Close'].iloc[-1] < df['Close'].rolling(window=20).mean().iloc[-1] - 2 * df['Close'].rolling(window=20).std().iloc[-1]:
        return 'Sell'
    else:
        return 'Hold'

# Apply trading strategies to data
signals = []
for i in range(len(df)):
    signals.append([
        df['Open time'].iloc[i],
        strategy_1(df.iloc[:i+1]),
        strategy_2(df.iloc[:i+1]),
        strategy_3(df.iloc[:i+1]),
        strategy_4(df.iloc[:i+1]),
        strategy_5(df.iloc[:i+1])
    ])

# Convert signals to pandas dataframe
signals_df = pd.DataFrame(signals, columns=['Date', 'Strategy 1', 'Strategy 2', 'Strategy 3', 'Strategy 4', 'Strategy 5'])
signals_df.set_index('Date', inplace=True)

# Print buy/sell recommendations for most recent date
print('Most recent signals:')
print(signals_df.iloc[-1])
