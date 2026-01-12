import React from 'react';

const MarketState = ({ state, risk }) => {
  // state: "TRENDING", "RANGING", "DANGEROUS"
  // risk: "SAFE", "HIGH"

  const getColor = () => {
    if (state === 'DANGEROUS') return 'bg-red-600 shadow-[0_0_20px_rgba(220,38,38,0.6)]';
    if (state === 'RANGING') return 'bg-yellow-500 shadow-[0_0_15px_rgba(234,179,8,0.5)]';
    if (state === 'TRENDING') return 'bg-green-500 shadow-[0_0_15px_rgba(34,197,94,0.5)]';
    return 'bg-gray-700';
  };

  const getLabel = () => {
    if (state === 'DANGEROUS') return '🔴 DANGEROUS';
    if (state === 'RANGING') return '🟡 RANGING';
    if (state === 'TRENDING') return '🟢 TRENDING';
    return '⚪ LOADING';
  };

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 text-center flex flex-col items-center justify-center">
      <h2 className="text-gray-400 text-sm uppercase tracking-widest mb-4">Market State</h2>
      <div className={`text-2xl font-bold text-white px-8 py-3 rounded-full transition-all duration-300 ${getColor()}`}>
        {getLabel()}
      </div>
      {risk === 'HIGH' && (
        <p className="mt-3 text-red-400 font-mono text-xs animate-pulse">
          ⚠️ HIGH RISK / VOLATILITY
        </p>
      )}
    </div>
  );
};

export default MarketState;
