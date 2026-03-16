"use client";

type Props = {
  loading: boolean;
  error: string | null;
  lastPrediction:
    | {
        recommended_box: string;
        confidence_score: number;
        efficiency_score: number;
      }
    | null;
};

export function PredictionPanel({ loading, error, lastPrediction }: Props) {
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
      <h2 className="mb-3 text-sm font-semibold">Latest prediction</h2>
      {loading && (
        <p className="text-xs text-slate-400">Running packaging prediction…</p>
      )}
      {error && <p className="text-xs text-red-400">{error}</p>}
      {!loading && !error && !lastPrediction && (
        <p className="text-xs text-slate-400">
          Select or upload an order to see prediction results.
        </p>
      )}
      {lastPrediction && (
        <div className="space-y-1 text-sm">
          <p>
            <span className="text-slate-400">Recommended box: </span>
            <span className="font-medium">{lastPrediction.recommended_box}</span>
          </p>
          <p>
            <span className="text-slate-400">Confidence: </span>
            <span className="font-medium">
              {(lastPrediction.confidence_score * 100).toFixed(1)}%
            </span>
          </p>
          <p>
            <span className="text-slate-400">Efficiency: </span>
            <span className="font-medium">
              {(lastPrediction.efficiency_score * 100).toFixed(1)}%
            </span>
          </p>
        </div>
      )}
    </div>
  );
}

