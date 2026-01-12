class ConfidenceEngine:
    @staticmethod
    def calculate_score(market_state: dict, bias_result: dict):
        """
        Calculate Confidence Score (0-100).
        
        Factors:
        - Weekly Bias Aligned: +20
        - Daily Bias Aligned: +20
        - 1H Trend (Setup) Aligned: +20
        - 15M Entry Ready: +20
        - Risk Safe (Low Volatility): +20
        
        Returns:
            int: Score
        """
        score = 0
        
        # Factor 1 & 2: Macro Alignment
        # If Daily Bias is BUY/SELL, it implied Weekly was supportive or we are in a strong Daily move.
        # Let's strictly follow the input dicts.
        
        target_dir = bias_result.get('bias') # BUY or SELL or WAIT
        
        if target_dir == "WAIT":
            return 0 # If Bias says WAIT, confidence is irrelevant (or 0)
            
        # Check Weekly
        if market_state.get('weekly_bias') == "BULLISH" and target_dir == "BUY":
            score += 20
        elif market_state.get('weekly_bias') == "BEARISH" and target_dir == "SELL":
             score += 20
             
        # Check Daily
        if market_state.get('daily_bias') == target_dir:
            score += 20
            
        # Check 1H Setup
        if bias_result.get('setup_phase') == "CONTINUATION": # or PULLBACK
             score += 20
             
        # Check 15M Entry
        if bias_result.get('entry_zone') == "READY":
             score += 20
             
        # Check Risk
        if market_state.get('risk') == "SAFE":
             score += 20
             
        return score
