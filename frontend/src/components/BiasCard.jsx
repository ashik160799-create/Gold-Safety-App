import React from 'react';

const BiasCard = ({ bias, confidence, setupPhase }) => {
    // bias: "BUY", "SELL", "WAIT"
    // confidence: 0-100
    // setupPhase: "CONTINUATION", "PULLBACK", "NO_SETUP"

    const isBuy = bias === 'BUY';
    const isSell = bias === 'SELL';
    const isWait = bias === 'WAIT';

    let borderColor = 'border-gray-700';
    let textColor = 'text-gray-400';

    if (isBuy) {
        borderColor = 'border-green-500';
        textColor = 'text-green-500';
    } else if (isSell) {
        borderColor = 'border-red-500';
        textColor = 'text-red-500';
    }

    return (
        <div className={`bg-gray-900 border-2 ${borderColor} rounded-xl p-6 relative overflow-hidden transition-all duration-300`}>
            <h2 className="text-gray-400 text-sm uppercase tracking-widest mb-2">Directional Bias</h2>

            <div className="flex items-center justify-between">
                <div className={`text-4xl font-black ${textColor}`}>
                    {bias}
                </div>

                <div className="text-right">
                    <div className="text-sm text-gray-500">Confidence</div>
                    <div className={`text-2xl font-bold ${confidence < 60 ? 'text-red-400' : 'text-white'}`}>
                        {confidence}%
                    </div>
                </div>
            </div>

            {!isWait && (
                <div className="mt-4 flex gap-2">
                    <span className="bg-gray-800 text-gray-300 px-3 py-1 text-xs rounded-md border border-gray-700">
                        Setup: {setupPhase}
                    </span>
                </div>
            )}

            {/* Visual Bar for Confidence */}
            <div className="w-full bg-gray-800 h-1.5 mt-6 rounded-full overflow-hidden">
                <div
                    className={`h-full ${confidence < 60 ? 'bg-red-500' : 'bg-blue-500'} transition-all duration-1000`}
                    style={{ width: `${confidence}%` }}
                ></div>
            </div>
        </div>
    );
};

export default BiasCard;
