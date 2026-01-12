import yfinance as yf
import pandas as pd
import os

class DataLoader:
    def __init__(self, csv_path: str = None):
        """
        Initialize DataLoader.
        :param csv_path: Path to the MT5 export CSV file for intraday data.
        """
        self.csv_path = csv_path

    def fetch_macro_data(self):
        """
        Fetch 1W and 1D data from Yahoo Finance (GC=F) for Macro Bias.
        """
        try:
            # We fetch enough data to calculate EMA 200 (need at least 200 periods)
            gold_weekly = yf.download("GC=F", interval="1wk", period="5y", progress=False)
            gold_daily = yf.download("GC=F", interval="1d", period="2y", progress=False)
            
            # Simple check if empty
            if gold_weekly.empty or gold_daily.empty:
                raise ValueError("Yahoo Finance returned empty data.")

            return {
                "1W": gold_weekly,
                "1D": gold_daily
            }
        except Exception as e:
            print(f"Error fetching Yahoo Finance data: {e}")
            return None

    def load_intraday_data(self):
        """
        Load intraday data from the provided CSV file.
        Expected columns: Date, Time, Open, High, Low, Close, Tick Volume (standard MT5 export).
        """
        if not self.csv_path or not os.path.exists(self.csv_path):
            print("CSV path not provided or file does not exist.")
            return None

        try:
            # Assuming MT5 CSV format: <DATE>\t<TIME>\t<OPEN>\t<HIGH>\t<LOW>\t<CLOSE>\t<TICKVOL>\t<VOL>\t<SPREAD>
            # OR standard CSV: Date,Time,Open,High,Low,Close...
            # We'll try to handle standard CSV headers. 
            
            # Read CSV - Adjust params based on actual MT5 export format if needed.
            # Usually MT5 exports are tab-delimited or comma-delimited.
            # Let's assume standard comma first, or try to detect.
            df = pd.read_csv(self.csv_path)
            
            # Clean headers
            df.columns = [c.strip().lower() for c in df.columns]
            
            # Create datetime column
            # Check for 'date' and 'time' columns
            if 'date' in df.columns and 'time' in df.columns:
                df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
            elif 'datetime' in df.columns:
                df['datetime'] = pd.to_datetime(df['datetime'])
            else:
                # If MT5 export is headerless or different, this might need adjustment.
                # For now, assuming headers exist.
                 pass

            df.set_index('datetime', inplace=True)
            df.sort_index(inplace=True)
            
            # Resample to needed timeframes if the CSV is 1M or 5M
            # Logic: If CSV is 1M, we can build 5M, 15M, 1H.
            # For simplicity, let's assume the CSV is the base timeframe (e.g. 5M).
            # We will generate dict of DataFrames.
            
            return df

        except Exception as e:
            print(f"Error loading CSV data: {e}")
            return None

    def get_combined_data(self):
        """
        Returns a dictionary containing all necessary DataFrames.
        keys: '1W', '1D', '1H', '15M', '5M' (derived from CSV)
        """
        macro_data = self.fetch_macro_data()
        if not macro_data:
            return None
            
        intraday_df = self.load_intraday_data()
        
        data = {
            '1W': macro_data['1W'],
            '1D': macro_data['1D']
        }
        
        if intraday_df is not None:
             # Resample logic
             # Ensuring we have numeric columns for resampling
             ohlc_dict = {
                 'open': 'first',
                 'high': 'max',
                 'low': 'min',
                 'close': 'last',
                 'tickvol': 'sum' if 'tickvol' in intraday_df.columns else 'first'
             }
             
             # Check if columns exist
             available_cols = {}
             for k, v in ohlc_dict.items():
                 if k in intraday_df.columns:
                     available_cols[k] = v
            
             if not available_cols:
                 # Fallback if names are different or index issues
                 return data

             # Resample
             data['1H'] = intraday_df.resample('1h').agg(available_cols).dropna()
             data['15M'] = intraday_df.resample('15min').agg(available_cols).dropna()
             data['5M'] = intraday_df.resample('5min').agg(available_cols).dropna()
             
             # Also keep raw if needed, or just 5M as base
        
        return data
