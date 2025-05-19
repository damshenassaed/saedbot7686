
import yfinance as yf
import pandas as pd
import time

def get_xau_data():
    df = yf.download("XAUUSD=X", interval="1m", period="1d")
    return df

def calculate_indicators(df):
    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def check_signals(df):
    latest = df.iloc[-1]
    if latest['RSI'] < 30 and latest['MACD'] > latest['Signal']:
        return "سیگنال لانگ (خرید)"
    elif latest['RSI'] > 70 and latest['MACD'] < latest['Signal']:
        return "سیگنال شورت (فروش)"
    else:
        return "سیگنال مشخصی نیست"

def main_loop():
    while True:
        try:
            df = get_xau_data()
            df = calculate_indicators(df)
            signal = check_signals(df)
            print(f"\n[{time.strftime('%H:%M:%S')}] {signal}")
            time.sleep(60)
        except Exception as e:
            print("خطا:", e)
            time.sleep(60)

if __name__ == "__main__":
    main_loop()
