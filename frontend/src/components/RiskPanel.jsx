import React from 'react';

const RiskPanel = ({ guidance, details }) => {
    return (
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Guidance */}
            <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
                <h3 className="text-blue-400 text-xs font-bold uppercase mb-2">🤖 Strategy Guidance</h3>
                <p className="text-gray-200 text-lg leading-relaxed font-medium">
                    "{guidance}"
                </p>
            </div>

            {/* Details Grid */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
                <h3 className="text-gray-500 text-xs font-bold uppercase mb-3">Logic Breakdown</h3>
                <div className="grid grid-cols-2 gap-y-4 gap-x-2 text-sm">
                    <div>
                        <span className="block text-gray-600 text-xs">Weekly Bias</span>
                        <span className={`font-mono ${details.weekly === 'BULLISH' ? 'text-green-400' : details.weekly === 'BEARISH' ? 'text-red-400' : 'text-yellow-400'}`}>
                            {details.weekly || '-'}
                        </span>
                    </div>
                    <div>
                        <span className="block text-gray-600 text-xs">Daily Bias</span>
                        <span className={`font-mono ${details.daily === 'BUY' ? 'text-green-400' : details.daily === 'SELL' ? 'text-red-400' : 'text-yellow-400'}`}>
                            {details.daily || '-'}
                        </span>
                    </div>
                    <div>
                        <span className="block text-gray-600 text-xs">1H Setup</span>
                        <span className="font-mono text-gray-300">
                            {details.setup_1h || '-'}
                        </span>
                    </div>
                    <div>
                        <span className="block text-gray-600 text-xs">15M Entry</span>
                        <span className="font-mono text-gray-300">
                            {details.entry_15m || '-'}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RiskPanel;
