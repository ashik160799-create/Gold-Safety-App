import React, { useState } from 'react';
import MarketState from './components/MarketState';
import BiasCard from './components/BiasCard';
import RiskPanel from './components/RiskPanel';

function App() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setAnalysis(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // In dev, assuming proxy or direct localhost:8000
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Analysis failed');
      }

      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setAnalysis(null);
    setError(null);
  };

  // Safety Check Calculation
  const isDangerous = analysis?.market_state === 'DANGEROUS';
  const isLowConfidence = analysis && analysis.confidence < 60;
  const isNoTrade = isDangerous || isLowConfidence;

  return (
    <div className="min-h-screen bg-black text-gray-200 font-sans selection:bg-yellow-500 selection:text-black">
      <div className="max-w-4xl mx-auto p-6">
        {/* Header */}
        <header className="flex justify-between items-center mb-10 border-b border-gray-800 pb-4">
          <div>
            <h1 className="text-2xl font-black tracking-tighter text-white">
              <span className="text-yellow-500">GOLD</span> SAFETY ENGINE
            </h1>
            <p className="text-xs text-gray-500 uppercase tracking-widest">
              XAU/USD Decision Support System
            </p>
          </div>
          <div className="text-right">
            <div className="text-xs font-mono text-gray-600">v1.0.0</div>
          </div>
        </header>

        {/* --- MAIN CONTENT AREA --- */}
        <main className="relative">

          {/* 1. Upload Section (Visible when no analysis) */}
          {!analysis && !loading && (
            <div className="flex flex-col items-center justify-center py-20 border-2 border-dashed border-gray-800 rounded-2xl hover:border-gray-700 transition-colors">
              <div className="bg-gray-900 p-4 rounded-full mb-4">
                <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
              </div>
              <h2 className="text-xl font-bold text-white mb-2">Upload MT5 Export</h2>
              <p className="text-gray-500 mb-6 text-sm">Select your XAUUSD .csv file to begin analysis</p>

              <label className="cursor-pointer bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-8 rounded-lg transition-all transform hover:scale-105 shadow-lg shadow-blue-900/50">
                <span>Select Start File</span>
                <input type="file" className="hidden" accept=".csv" onChange={handleFileUpload} />
              </label>

              {error && (
                <div className="mt-6 bg-red-900/30 border border-red-800 text-red-400 px-4 py-2 rounded-md text-sm">
                  ERROR: {error}
                </div>
              )}
            </div>
          )}

          {/* 2. Loading State */}
          {loading && (
            <div className="flex flex-col items-center justify-center py-32 animate-pulse">
              <div className="text-yellow-500 text-4xl mb-4 font-black">ANALYZING...</div>
              <p className="text-gray-500 text-xs uppercase tracking-widest">Checking Market Structure • Calculating Volatility • Verifying Bias</p>
            </div>
          )}

          {/* 3. Analysis Dashboard */}
          {analysis && (
            <div className={`transition-all duration-500 ${isNoTrade ? 'grayscale opacity-80' : ''}`}>

              {/* Top Controls */}
              <div className="flex justify-between items-center mb-6">
                <span className="text-xs text-gray-500 font-mono">DATA SOURCE: HYBRID (Yahoo + Upload)</span>
                <button
                  onClick={resetAnalysis}
                  className="text-xs text-gray-400 hover:text-white underline"
                >
                  Start New Analysis
                </button>
              </div>

              {/* GRID */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <MarketState state={analysis.market_state} risk={analysis.risk} />
                <BiasCard
                  bias={analysis.bias}
                  confidence={analysis.confidence}
                  setupPhase={analysis.details?.setup_1h}
                />
              </div>

              {/* RISK & GUIDANCE */}
              <RiskPanel guidance={analysis.guidance} details={analysis.details} />

            </div>
          )}

          {/* 4. OVERLAY - THE SAFETY NET */}
          {analysis && isNoTrade && (
            <div className="fixed inset-0 z-50 pointer-events-none flex items-center justify-center">
              <div className="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>
              <div className="relative bg-red-950/90 border-2 border-red-600 p-10 rounded-2xl max-w-lg text-center shadow-[0_0_50px_rgba(220,38,38,0.5)] transform scale-100 animate-bounce-slight">
                <h1 className="text-5xl font-black text-white mb-2">NO TRADE</h1>
                <h2 className="text-2xl font-bold text-red-200 mb-6">
                  {isDangerous ? 'MARKET IS DANGEROUS' : 'CONFIDENCE TOO LOW'}
                </h2>
                <div className="text-left bg-black/40 p-4 rounded-lg text-sm text-red-100 font-mono border border-red-800/50">
                  <p>❌ Strategy Violation Detected</p>
                  <ul className="list-disc list-inside mt-2 space-y-1 opacity-80">
                    {isDangerous && <li>Volatility exceeds safety limits</li>}
                    {isLowConfidence && <li>Score {analysis.confidence}% is below 60% threshold</li>}
                  </ul>
                </div>
                <p className="mt-6 text-gray-400 text-xs uppercase tracking-widest">
                  Protect your capital. Close the chart.
                </p>
              </div>
            </div>
          )}

        </main>
      </div>
    </div>
  );
}

export default App;
