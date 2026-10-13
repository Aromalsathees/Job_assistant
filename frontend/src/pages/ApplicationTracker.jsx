import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Briefcase,
  Calendar,
  Building2,
  Clock,
  Plus,
  ExternalLink,
  Edit2,
  Trash2,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { api } from '../api/client';

const STAGES = [
  { id: 'INTERESTED', label: 'Interested', color: 'border-slate-300 bg-slate-50 text-slate-700' },
  { id: 'TO_APPLY', label: 'To Apply', color: 'border-blue-300 bg-blue-50 text-blue-700' },
  { id: 'APPLIED', label: 'Applied', color: 'border-amber-300 bg-amber-50 text-amber-700' },
  { id: 'ASSESSMENT', label: 'Assessment', color: 'border-purple-300 bg-purple-50 text-purple-700' },
  { id: 'INTERVIEW', label: 'Interview', color: 'border-indigo-300 bg-indigo-50 text-indigo-700' },
  { id: 'OFFER', label: 'Offer Received', color: 'border-emerald-300 bg-emerald-50 text-emerald-700' },
  { id: 'REJECTED', label: 'Rejected', color: 'border-rose-300 bg-rose-50 text-rose-700' },
  { id: 'WITHDRAWN', label: 'Withdrawn', color: 'border-gray-300 bg-gray-50 text-gray-700' },
];

export default function ApplicationTracker() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadApplications();
  }, []);

  const loadApplications = async () => {
    setLoading(true);
    try {
      const res = await api.getApplications();
      setApplications(res.data.results || res.data || []);
    } catch (err) {
      console.error('Error loading applications:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (appId, newStatus) => {
    try {
      await api.updateApplication(appId, { status: newStatus });
      setApplications(applications.map((a) => (a.id === appId ? { ...a, status: newStatus } : a)));
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (appId) => {
    try {
      await api.deleteApplication(appId);
      setApplications(applications.filter((a) => a.id !== appId));
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
          Application Progress Tracker
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Monitor all your entry-level IT applications across interview cycles.
        </p>

        {/* Disclaimer alert */}
        <div className="mt-3 p-3 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-800 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0 text-amber-600" />
          <span>
            <strong>Application Submission Policy:</strong> Applications are tracked locally in this dashboard. This system does not automatically submit job applications on your behalf; apply via the verified official employer link.
          </span>
        </div>
      </div>

      {applications.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {STAGES.map((stage) => {
            const stageApps = applications.filter((a) => a.status === stage.id);
            return (
              <div key={stage.id} className="bg-slate-100/70 rounded-xl p-3.5 space-y-3 flex flex-col">
                <div className="flex items-center justify-between">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-md border ${stage.color}`}>
                    {stage.label}
                  </span>
                  <span className="text-xs font-bold text-slate-400">{stageApps.length}</span>
                </div>

                <div className="space-y-2 flex-1">
                  {stageApps.map((app) => {
                    const job = app.job_details;
                    return (
                      <div
                        key={app.id}
                        className="bg-white rounded-lg border border-slate-200 p-3 shadow-xs space-y-2 text-xs"
                      >
                        <Link to={`/jobs/${job.id}`} className="font-bold text-slate-900 hover:text-brand-600 line-clamp-1 block">
                          {job.title}
                        </Link>
                        <p className="text-slate-600 flex items-center gap-1 text-[11px]">
                          <Building2 className="w-3 h-3 text-slate-400" />
                          {job.company_name}
                        </p>

                        {app.notes && (
                          <p className="text-[11px] text-slate-500 italic bg-slate-50 p-1.5 rounded border border-slate-100">
                            "{app.notes}"
                          </p>
                        )}

                        <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px]">
                          {/* Move to next stage select */}
                          <select
                            value={app.status}
                            onChange={(e) => handleStatusChange(app.id, e.target.value)}
                            className="text-[10px] py-0.5 px-1.5 rounded border border-slate-200 bg-slate-50 text-slate-700"
                          >
                            {STAGES.map((s) => (
                              <option key={s.id} value={s.id}>{s.label}</option>
                            ))}
                          </select>

                          <button
                            onClick={() => handleDelete(app.id)}
                            className="text-slate-400 hover:text-rose-600 p-1"
                            title="Remove from tracker"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </div>
                    );
                  })}
                  {stageApps.length === 0 && (
                    <div className="h-16 flex items-center justify-center border border-dashed border-slate-200 rounded-lg text-[11px] text-slate-400">
                      Empty stage
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3">
          <div className="w-12 h-12 rounded-full bg-slate-100 text-slate-400 mx-auto flex items-center justify-center">
            <Briefcase className="w-6 h-6" />
          </div>
          <h3 className="text-sm font-bold text-slate-900">No tracked applications yet</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Add jobs to this tracker from any Job Detail page to organize your interview pipeline.
          </p>
          <Link
            to="/jobs"
            className="mt-2 inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-bold text-brand-600 bg-brand-50 hover:bg-brand-100 transition-colors"
          >
            Find Fresh Openings to Apply
          </Link>
        </div>
      )}
    </div>
  );
}
