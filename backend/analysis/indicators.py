import pandas as pd
import pandas_ta as ta

class Indicators:
    @staticmethod
    def add_all_indicators(df: pd.DataFrame):
        """
        Adds EMA (9, 21, 50, 200), ATR (14), and MACD to the DataFrame.
        Operates in-place (modifies the df).
        """
        if df is None or df.empty:
            return df

        # EMAs
        df['ema_9'] = ta.ema(df['close'], length=9)
        df['ema_21'] = ta.ema(df['close'], length=21)
        df['ema_50'] = ta.ema(df['close'], length=50)
        df['ema_200'] = ta.ema(df['close'], length=200)

        # ATR (Volatility)
        df['atr_14'] = ta.atr(df['high'], df['low'], df['close'], length=14)

        # MACD (Momentum) usually 12, 26, 9
        macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
        # pandas_ta returns columns like MACD_12_26_9, MACDh_12_26_9, MACDs_12_26_9
        # strict naming for cleanliness
        if macd is not None:
             df = pd.concat([df, macd], axis=1)
             # Rename for simpler access if needed, or just rely on 'MACD_12_26_9' etc.
             # Standardizing:
             df.rename(columns={
                 'MACD_12_26_9': 'macd',
                 'MACDh_12_26_9': 'macd_hist',
                 'MACDs_12_26_9': 'macd_signal'
             }, inplace=True)

        return df
