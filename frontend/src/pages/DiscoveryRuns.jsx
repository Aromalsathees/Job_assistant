import React, { useEffect, useState } from 'react';
import {
  Activity,
  Play,
  CheckCircle2,
  AlertOctagon,
  Clock,
  Layers,
  ShieldCheck,
  RefreshCw,
  Server
} from 'lucide-react';
import { api } from '../api/client';

export default function DiscoveryRuns({ onTriggerDiscovery }) {
  const [runs, setRuns] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRuns();
  }, []);

  const loadRuns = async () => {
    setLoading(true);
    try {
      const [runsRes, sumRes] = await Promise.all([
        api.getDiscoveryRuns(),
        api.getLatestRunSummary(),
      ]);
      setRuns(runsRes.data.results || runsRes.data || []);
      setSummary(sumRes.data);
    } catch (err) {
      console.error('Error fetching discovery runs:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const lastRun = summary?.last_successful_run;

  return (
    <div className="space-y-6">
      {/* Top Banner & Trigger */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <div>
          <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
            Discovery Run Audits &amp; History
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Track background automated sweeps, source statuses, and deduplication audit logs.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={loadRuns}
            className="p-2 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 transition-colors"
            title="Refresh logs"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
          <button
            onClick={onTriggerDiscovery}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold bg-brand-600 hover:bg-brand-700 text-white shadow-sm transition-colors"
          >
            <Play className="w-4 h-4 fill-current" />
            <span>Run Discovery Now</span>
          </button>
        </div>
      </div>

      {/* Last Successful Run Snapshot Card */}
      {lastRun && (
        <div className="bg-emerald-50/60 rounded-xl border border-emerald-200 p-5 text-xs text-slate-700 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 font-bold text-emerald-900">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Last Successful Discovery Execution</span>
            </div>
            <span className="font-semibold text-emerald-700 text-[11px]">
              Executed on {new Date(lastRun.started_at).toLocaleString()}
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-white p-3 rounded-lg border border-emerald-100">
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-bold">New Jobs</span>
              <span className="text-sm font-extrabold text-emerald-700">{lastRun.jobs_discovered}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-bold">Updated</span>
              <span className="text-sm font-extrabold text-slate-800">{lastRun.jobs_updated}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-bold">Ineligible Excluded</span>
              <span className="text-sm font-extrabold text-rose-600">{lastRun.ineligible_excluded}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-bold">Official Verified</span>
              <span className="text-sm font-extrabold text-brand-700">{lastRun.official_verified_count}</span>
            </div>
          </div>
        </div>
      )}

      {/* Discovery Runs Table */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-900">Historical Execution Log</h2>
          <span className="text-xs text-slate-500 font-medium">{runs.length} Runs Logged</span>
        </div>

        {runs.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-600">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 uppercase font-bold text-[10px]">
                <tr>
                  <th className="px-5 py-3">Status</th>
                  <th className="px-5 py-3">Started At</th>
                  <th className="px-5 py-3">Duration</th>
                  <th className="px-5 py-3">Discovered</th>
                  <th className="px-5 py-3">Updated</th>
                  <th className="px-5 py-3">Excluded (&gt;1y)</th>
                  <th className="px-5 py-3">Verified</th>
                  <th className="px-5 py-3">Sources</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {runs.map((r) => (
                  <tr key={r.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="px-5 py-3.5">
                      <span
                        className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full font-bold text-[11px] ${
                          r.status === 'SUCCESS'
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                            : r.status === 'RUNNING'
                            ? 'bg-blue-50 text-blue-700 border border-blue-200 animate-pulse'
                            : 'bg-amber-50 text-amber-700 border border-amber-200'
                        }`}
                      >
                        {r.status}
                      </span>
                    </td>
                    <td className="px-5 py-3.5 font-medium text-slate-800">
                      {new Date(r.started_at).toLocaleString()}
                    </td>
                    <td className="px-5 py-3.5 font-medium">{r.duration_seconds}s</td>
                    <td className="px-5 py-3.5 font-bold text-emerald-700">{r.jobs_discovered}</td>
                    <td className="px-5 py-3.5">{r.jobs_updated}</td>
                    <td className="px-5 py-3.5 font-semibold text-rose-600">{r.ineligible_excluded}</td>
                    <td className="px-5 py-3.5 font-semibold text-brand-700">{r.official_verified_count}</td>
                    <td className="px-5 py-3.5">
                      <div className="flex flex-wrap gap-1 max-w-xs">
                        {(r.sources_checked || []).map((s, idx) => (
                          <span
                            key={idx}
                            className="px-1.5 py-0.2 rounded text-[10px] bg-slate-100 text-slate-600 truncate"
                          >
                            {s}
                          </span>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-8 text-center text-xs text-slate-500">
            No discovery sweeps recorded yet. Click "Run Discovery Now" to launch the agent.
          </div>
        )}
      </div>
    </div>
  );
}
