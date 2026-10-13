import React, { useState } from 'react';
import { X, Play, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { api } from '../api/client';

export default function RunDiscoveryModal({ isOpen, onClose, onComplete }) {
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  if (!isOpen) return null;

  const handleRun = async () => {
    setRunning(true);
    setResult(null);
    setError(null);
    try {
      const res = await api.triggerDiscovery();
      setResult(res.data.run);
      if (onComplete) onComplete(res.data.run);
    } catch (err) {
      const errMsg = err.response?.data?.message || err.response?.data?.error || err.message;
      setError(errMsg);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xl max-w-lg w-full p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 p-1 rounded-lg"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3 mb-4">
          <div className="p-2.5 rounded-xl bg-brand-50 text-brand-600">
            <Play className="w-5 h-5 fill-current" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900">Run Job Discovery Agent</h3>
            <p className="text-xs text-slate-500">Autonomous multi-source fresher IT intelligence sweep</p>
          </div>
        </div>

        <div className="text-xs text-slate-600 space-y-2 mb-6 bg-slate-50 p-4 rounded-xl border border-slate-200">
          <p className="font-semibold text-slate-700">Workflow execution order:</p>
          <ol className="list-decimal list-inside space-y-1 text-slate-500">
            <li>Poll active sources (Technopark, Infopark, Direct Feeds, Remotive, Arbeitnow)</li>
            <li>Normalize schemas and extract technical skills</li>
            <li>Enforce strict 0–1 year experience filter (excludes &gt;1 year &amp; separates unclear)</li>
            <li>Verify employer domains and campus official registries</li>
            <li>Rank by Kerala/Kochi priority and freshness</li>
            <li>Idempotently persist with audit logs</li>
          </ol>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-50 border border-red-200 text-xs text-red-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {result && (
          <div className="mb-4 p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 space-y-2">
            <div className="flex items-center gap-2 font-bold">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Discovery Completed Successfully!</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-slate-700 pt-2 border-t border-emerald-200/60 font-medium">
              <div>Jobs Discovered: <span className="font-bold text-emerald-700">{result.jobs_discovered}</span></div>
              <div>Jobs Updated: <span className="font-bold">{result.jobs_updated}</span></div>
              <div>Ineligible Excluded: <span className="font-bold text-rose-600">{result.ineligible_excluded}</span></div>
              <div>Official Verified: <span className="font-bold text-emerald-700">{result.official_verified_count}</span></div>
              <div>Duration: <span className="font-bold">{result.duration_seconds}s</span></div>
            </div>
          </div>
        )}

        <div className="flex items-center justify-end gap-3 pt-2">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-800 rounded-lg"
          >
            Close
          </button>
          <button
            onClick={handleRun}
            disabled={running}
            className="px-5 py-2 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-lg shadow-sm disabled:opacity-50 flex items-center gap-2 transition-colors"
          >
            {running ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Running Discovery...</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>Start Sweep Now</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
