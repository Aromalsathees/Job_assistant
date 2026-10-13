import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  Building2,
  MapPin,
  ExternalLink,
  Bookmark,
  Check,
  Calendar,
  Banknote,
  ArrowLeft,
  ShieldCheck,
  AlertTriangle,
  Sparkles,
  Info,
  Clock,
  Briefcase
} from 'lucide-react';
import VerificationBadge from '../components/VerificationBadge';
import EligibilityBadge from '../components/EligibilityBadge';
import { api } from '../api/client';

export default function JobDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saved, setSaved] = useState(false);
  const [trackerStatus, setTrackerStatus] = useState('');
  const [trackingLoading, setTrackingLoading] = useState(false);

  useEffect(() => {
    loadJob();
  }, [id]);

  const loadJob = async () => {
    setLoading(true);
    try {
      const res = await api.getJobDetail(id);
      setJob(res.data);
    } catch (err) {
      console.error('Error loading job detail:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      await api.saveJob(job.id);
      setSaved(true);
    } catch (err) {
      console.error(err);
    }
  };

  const handleTrackApplication = async (status) => {
    setTrackingLoading(true);
    try {
      await api.createApplication({
        job: job.id,
        status: status,
        notes: `Added from Job Details page at ${new Date().toLocaleDateString()}`,
      });
      setTrackerStatus(status);
    } catch (err) {
      console.error(err);
    } finally {
      setTrackingLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-xs text-slate-500 font-medium">Loading job details...</p>
        </div>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-4">
        <h2 className="text-base font-bold text-slate-900">Job Not Found</h2>
        <p className="text-xs text-slate-500">The requested job listing could not be found or has expired.</p>
        <Link
          to="/jobs"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold bg-brand-600 text-white"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Job Search
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Back button */}
      <div>
        <button
          onClick={() => navigate(-1)}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Listings
        </button>
      </div>

      {/* Main Job Header Card */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-3 pb-6 border-b border-slate-100">
          <div className="space-y-2">
            <div className="flex flex-wrap items-center gap-2">
              <EligibilityBadge category={job.eligibility_category} classification={job.eligibility_classification} />
              <VerificationBadge status={job.verification_status} />
              <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-700 capitalize">
                {job.work_mode?.toLowerCase()}
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-700 capitalize">
                {job.employment_type?.replace('_', ' ').toLowerCase()}
              </span>
            </div>

            <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
              {job.title}
            </h1>

            <div className="flex flex-wrap items-center gap-4 text-xs font-medium text-slate-600">
              <span className="flex items-center gap-1.5 text-slate-800 font-bold">
                <Building2 className="w-4 h-4 text-slate-400" />
                {job.company_name}
              </span>
              <span className="flex items-center gap-1.5">
                <MapPin className="w-4 h-4 text-slate-400" />
                {job.city || job.location} ({job.state})
              </span>
              <span className="flex items-center gap-1.5 text-slate-500">
                <Calendar className="w-4 h-4 text-slate-400" />
                Discovered: {new Date(job.first_discovered_at).toLocaleDateString()}
              </span>
            </div>
          </div>

          {/* Action CTAs */}
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={handleSave}
              className={`p-2 rounded-xl border transition-colors flex items-center gap-1.5 text-xs font-semibold ${
                saved
                  ? 'bg-amber-50 text-amber-700 border-amber-300'
                  : 'text-slate-600 hover:bg-slate-50 border-slate-200'
              }`}
            >
              {saved ? <Check className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
              <span>{saved ? 'Saved' : 'Save Job'}</span>
            </button>

            <a
              href={job.official_apply_url || job.original_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-brand-600 hover:bg-brand-700 text-white shadow-sm transition-colors"
            >
              <span>Apply on Official Link</span>
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        </div>

        {/* Key Metrics Row */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 p-4 rounded-xl bg-slate-50/80 border border-slate-100 text-xs">
          <div>
            <span className="text-slate-400 font-medium block">Experience Criteria</span>
            <span className="font-bold text-slate-800 text-sm mt-0.5 block">
              {job.experience_raw_text || '0–1 Year (Fresher Eligible)'}
            </span>
            <span className="text-[11px] text-emerald-700 font-medium">Strict Fresher Filter Verified</span>
          </div>

          <div>
            <span className="text-slate-400 font-medium block">Compensation</span>
            <span className="font-bold text-slate-800 text-sm mt-0.5 block">
              {job.salary_disclosed && job.salary_raw_text ? job.salary_raw_text : 'Undisclosed in listing'}
            </span>
            <span className="text-[11px] text-slate-500 font-medium">
              {job.salary_disclosed ? 'Disclosed by employer' : 'Not published'}
            </span>
          </div>

          <div>
            <span className="text-slate-400 font-medium block">Source Provenance</span>
            <span className="font-bold text-slate-800 text-sm mt-0.5 block truncate">
              {job.source_name || 'Verified Career Feed'}
            </span>
            <a
              href={job.original_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-[11px] text-brand-600 font-medium hover:underline flex items-center gap-1 mt-0.5"
            >
              <span>View Original Listing URL</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>

        {/* Required Technical Skills */}
        {job.required_skills && job.required_skills.length > 0 && (
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2.5">
              Technical Stack &amp; Skills Required
            </h3>
            <div className="flex flex-wrap gap-2">
              {job.required_skills.map((skill, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 rounded-lg text-xs font-semibold bg-brand-50 text-brand-800 border border-brand-200"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* AI-Generated Summary Disclaimer Banner */}
        {job.ai_summary && (
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-2">
            <div className="flex items-center gap-2 font-bold text-slate-800">
              <Sparkles className="w-4 h-4 text-brand-600" />
              <span>AI Executive Summary &amp; Overview</span>
              <span className="text-[10px] uppercase font-bold px-2 py-0.2 rounded bg-amber-100 text-amber-800">
                AI Generated Summary
              </span>
            </div>
            <p className="text-slate-600 leading-relaxed italic">{job.ai_summary}</p>
            <p className="text-[11px] text-slate-400">
              * Note: The AI summary is provided for quick evaluation. Always review the verbatim Original Description below for binding job requirements.
            </p>
          </div>
        )}

        {/* Original Verbatim Description */}
        <div>
          <div className="flex items-center justify-between mb-3 pb-2 border-b border-slate-100">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Original Job Description (Verbatim as Published)
            </h3>
            <span className="text-[11px] text-slate-400 font-medium">Unmodified Original Content</span>
          </div>

          <div
            className="prose prose-sm max-w-none text-xs sm:text-sm text-slate-700 leading-relaxed bg-slate-50/50 p-5 rounded-xl border border-slate-100 whitespace-pre-line"
            dangerouslySetInnerHTML={{ __html: job.original_description }}
          />
        </div>

        {/* Verification Audit Records */}
        {job.verification_records && job.verification_records.length > 0 && (
          <div className="border-t border-slate-100 pt-6 space-y-3">
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-700">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>Authenticity Verification Evidence Trail</span>
            </div>

            <div className="space-y-2">
              {job.verification_records.map((rec) => (
                <div
                  key={rec.id}
                  className="p-3 rounded-lg border border-slate-200 bg-slate-50 text-xs text-slate-600 flex flex-col sm:flex-row sm:items-center justify-between gap-2"
                >
                  <div>
                    <span className="font-bold text-slate-800 mr-2">{rec.evidence_type}:</span>
                    <span>{rec.evidence_details}</span>
                  </div>
                  <span className="text-[11px] text-slate-400 flex-shrink-0">
                    Checked {new Date(rec.checked_at).toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Application Tracker Quick Add */}
        <div className="border-t border-slate-100 pt-6 flex flex-wrap items-center justify-between gap-3 text-xs bg-brand-50/50 p-4 rounded-xl border border-brand-100">
          <div>
            <h4 className="font-bold text-brand-900">Track This Job in Your Applications</h4>
            <p className="text-slate-500">Record your progress from Interest to Applied, Interview, or Offer.</p>
          </div>

          <div className="flex items-center gap-2">
            {['INTERESTED', 'TO_APPLY', 'APPLIED'].map((st) => (
              <button
                key={st}
                onClick={() => handleTrackApplication(st)}
                disabled={trackingLoading || trackerStatus === st}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-colors ${
                  trackerStatus === st
                    ? 'bg-emerald-600 text-white border-emerald-600'
                    : 'bg-white text-slate-700 hover:bg-slate-50 border-slate-200'
                }`}
              >
                {trackerStatus === st ? `Tracked as ${st}` : `+ ${st.replace('_', ' ')}`}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
