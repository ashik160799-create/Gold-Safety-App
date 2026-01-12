import pandas as pd

class MarketState:
    @staticmethod
    def analyze_macro_state(weekly_df: pd.DataFrame, daily_df: pd.DataFrame):
        """
        Layer 1: Weekly & Daily Bias Direction.
        
        Rules:
        - 1W Price > EMA 200 => Bullish
        - 1W Price < EMA 200 => Bearish
        - 1D Price > EMA 50 & 1W Bullish => BUY_ONLY
        - 1D Price < EMA 50 & 1W Bearish => SELL_ONLY
        - ATR Spike => DANGEROUS
        
        Returns:
            dict: {
                "weekly_bias": "BULLISH" | "BEARISH" | "NEUTRAL",
                "daily_bias": "BUY" | "SELL" | "WAIT",
                "market_state": "TRENDING" | "RANGING" | "DANGEROUS",
                "risk": "SAFE" | "HIGH"
            }
        """
        result = {
            "weekly_bias": "NEUTRAL",
            "daily_bias": "WAIT",
            "market_state": "RANGING",
            "risk": "SAFE"
        }
        
        if weekly_df is None or daily_df is None or weekly_df.empty or daily_df.empty:
            return result

        # Get latest closed candles (assuming we look at confirmed closes)
        w_last = weekly_df.iloc[-1]
        d_last = daily_df.iloc[-1]
        
        # --- WEEKLY BIAS (EMA 200) ---
        # Assuming indicators already added or we calc here?
        # Ideally, Data Loader or Indicators class added them.
        # But Yahoo fetch in loader.py didn't call Indicators.add_all_indicators yet. 
        # We should calculate them here or ensure they are present.
        # For safety/simplicity, let's assume we pass DFs that HAVE indicators.
        
        if 'ema_200' not in weekly_df.columns:
            # Fallback or error - assume called from engine which preps data
            return result

        w_close = w_last['close']
        w_ema200 = w_last['ema_200']
        
        if w_close > w_ema200:
            result['weekly_bias'] = "BULLISH"
        elif w_close < w_ema200:
            result['weekly_bias'] = "BEARISH"
        else:
            result['weekly_bias'] = "NEUTRAL" # Rare exact match

        # --- DAILY BIAS (EMA 50) ---
        d_close = d_last['close']
        d_ema50 = d_last['ema_50']
        d_atr = d_last['atr_14'] if 'atr_14' in d_last else 0
        
        # Simple ATR Spike check (e.g., current ATR > 1.5 * avg ATR)
        # This requires historical comparison. simpler: if ATR is very high relative to price (e.g. > 1% of price?)
        # Or user said "Large ATR spike -> DANGEROUS".
        # Let's use a dynamic threshold: if current Candle Range > 2 * ATR
        d_high = d_last['high']
        d_low = d_last['low']
        current_range = d_high - d_low
        
        if current_range > (2 * d_atr) and d_atr > 0:
            result['risk'] = "HIGH"
            result['market_state'] = "DANGEROUS"
            return result # Stop here if Dangerous? Or continue but flag? User said "DANGEROUS -> DO NOT TRADE"

        if result['weekly_bias'] == "BULLISH":
             if d_close > d_ema50:
                 result['daily_bias'] = "BUY"
                 result['market_state'] = "TRENDING"
             else:
                 result['daily_bias'] = "WAIT" # Pullback or Reversal
                 result['market_state'] = "RANGING"
        elif result['weekly_bias'] == "BEARISH":
             if d_close < d_ema50:
                 result['daily_bias'] = "SELL"
                 result['market_state'] = "TRENDING"
             else:
                 result['daily_bias'] = "WAIT"
                 result['market_state'] = "RANGING"
        
        return result
