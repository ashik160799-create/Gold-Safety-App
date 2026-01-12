from backend.data.loader import DataLoader
from backend.analysis.indicators import Indicators
from backend.analysis.market_state import MarketState
from backend.analysis.bias import BiasEngine
from backend.analysis.confidence import ConfidenceEngine

class AnalysisEngine:
    def __init__(self, csv_path: str = None):
        self.loader = DataLoader(csv_path)

    def run_analysis(self):
        # 1. Load Data
        data = self.loader.get_combined_data()
        if not data:
            return {"error": "Failed to load data. Please check CSV path or internet connection."}

        # 2. Add Indicators
        # Iterate over all frames and add indicators
        for tf, df in data.items():
            Indicators.add_all_indicators(df)
            
        # 3. Layer 1: Macro State
        macro_res = MarketState.analyze_macro_state(data.get('1W'), data.get('1D'))
        
        # 4. Layer 2 & 3: Intraday Bias
        bias_res = BiasEngine.calculate_intraday_bias(macro_res, data.get('1H'), data.get('15M'))
        
        # 5. Confidence
        score = ConfidenceEngine.calculate_score(macro_res, bias_res)
        
        # 6. Final Guidance Construction
        guidance = self._generate_guidance(macro_res, bias_res, score)
        
        return {
            "market_state": macro_res['market_state'], # TRENDING, RANGING, DANGEROUS
            "bias": bias_res['bias'], # BUY, SELL, WAIT
            "confidence": score,
            "risk": macro_res['risk'], # SAFE, HIGH
            "details": {
                "weekly": macro_res['weekly_bias'],
                "daily": macro_res['daily_bias'],
                "setup_1h": bias_res['setup_phase'],
                "entry_15m": bias_res['entry_zone']
            },
            "guidance": guidance
        }

    def _generate_guidance(self, macro, bias, score):
        if macro['market_state'] == "DANGEROUS":
            return "MARKET IS DANGEROUS (High Volatility). DO NOT TRADE. Protect capital."
        
        if score < 60:
            return "Confidence is Low (<60%). WAIT. Do not force a trade."
            
        direction = bias['bias']
        if direction == "WAIT":
            return "Conflicting signals. WAIT for better alignment."
            
        return f"Bias is {direction}. Confidence {score}%. Look for {direction} confirmation on 5M. No chasing."
