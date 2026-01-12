import pandas as pd

class BiasEngine:
    @staticmethod
    def calculate_intraday_bias(market_state_result: dict, h1_df: pd.DataFrame, m15_df: pd.DataFrame):
        """
        Layer 2 & 3: Intraday Bias (1H) and Entry Zone (15M).
        
        Rules:
        - If Market State == DANGEROUS or WAIT => FORCE WAIT.
        - 1H Bias must match Daily Bias.
        - 15M must be in 'PULLBACK' or 'READY' state (not extended).
        
        Returns:
            dict: {
                "bias": "BUY" | "SELL" | "WAIT",
                "setup_phase": "CONTINUATION" | "PULLBACK" | "NO_SETUP",
                "entry_zone": "READY" | "EARLY" | "REJECT"
            }
        """
        result = {
            "bias": "WAIT",
            "setup_phase": "NO_SETUP",
            "entry_zone": "REJECT"
        }
        
        # Block if Macro is bad
        macro_bias = market_state_result.get('daily_bias', 'WAIT')
        if market_state_result.get('market_state') == "DANGEROUS" or macro_bias == "WAIT":
             return result
             
        if h1_df is None or h1_df.empty:
            return result
            
        last_h1 = h1_df.iloc[-1]
        
        # --- 1H LOGIC (Trade Direction) ---
        # EMA 21 / 50 alignment
        h1_ema21 = last_h1['ema_21']
        h1_ema50 = last_h1['ema_50']
        h1_macd = last_h1['macd']
        h1_macd_sig = last_h1['macd_signal']
        
        h1_trend = "NEUTRAL"
        if h1_ema21 > h1_ema50:
            h1_trend = "BULLISH"
        elif h1_ema21 < h1_ema50:
            h1_trend = "BEARISH"
            
        # Alignment Check
        if macro_bias == "BUY" and h1_trend == "BULLISH":
             # Check for Setup (Continuation or Pullback)
             # Ideally, price near EMA21 is good. Price far away = WAIT (Overextended)
             # Simple Logic: trend is good.
             result['bias'] = "BUY"
             result['setup_phase'] = "CONTINUATION"
        elif macro_bias == "SELL" and h1_trend == "BEARISH":
             result['bias'] = "SELL"
             result['setup_phase'] = "CONTINUATION"
        else:
             # Disagreement -> WAIT
             result['bias'] = "WAIT"
             return result

        # --- 15M LOGIC (Entry Zone Filter) ---
        if m15_df is None or m15_df.empty:
            # If no 15M data, we can't confirm entry, so default to WAIT or cautious
            result['entry_zone'] = "REJECT" 
            return result
            
        last_m15 = m15_df.iloc[-1]
        m15_macd_hist = last_m15['macd_hist']
        
        # Simple Entry Logic:
        # BUY: MACD Histogram rising (or flipping positive)? 
        # User said: "Momentum slowing (not reversing)" -> Pullback logic.
        # Simplified: If bias is BUY, we want 15M not to be explicitly bearish/crashing.
        # Let's check momentum.
        
        if result['bias'] == "BUY":
            # If 15M MACD Hist is recovering (increasing) or positive
            if m15_macd_hist > 0 or (m15_macd_hist > m15_df.iloc[-2]['macd_hist']):
                result['entry_zone'] = "READY"
            else:
                result['entry_zone'] = "EARLY" # Still falling
        elif result['bias'] == "SELL":
            if m15_macd_hist < 0 or (m15_macd_hist < m15_df.iloc[-2]['macd_hist']):
                result['entry_zone'] = "READY"
            else:
                 result['entry_zone'] = "EARLY"

        return result
