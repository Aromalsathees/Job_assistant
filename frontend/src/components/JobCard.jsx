import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { MapPin, Building2, ExternalLink, Bookmark, Check, Calendar, Banknote } from 'lucide-react';
import VerificationBadge from './VerificationBadge';
import EligibilityBadge from './EligibilityBadge';
import { api } from '../api/client';

export default function JobCard({ job, onSaveToggle, isSaved = false }) {
  const [saved, setSaved] = useState(isSaved);
  const [saving, setSaving] = useState(false);

  const handleSaveClick = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (!saved) {
        await api.saveJob(job.id);
        setSaved(true);
        if (onSaveToggle) onSaveToggle(job.id, true);
      } else {
        // If already saved, let parent handle or toggle
        if (onSaveToggle) onSaveToggle(job.id, false);
        setSaved(false);
      }
    } catch (err) {
      console.error('Error saving job:', err);
    } finally {
      setSaving(false);
    }
  };

  const isKerala = ['kochi', 'ernakulam', 'kakkanad', 'infopark', 'thiruvananthapuram', 'technopark', 'kozhikode', 'thrissur']
    .some((c) => (job.city || '').toLowerCase().includes(c) || (job.location || '').toLowerCase().includes(c));

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:shadow-md hover:border-brand-500/40 transition-all flex flex-col justify-between">
      <div>
        {/* Top bar: Verification & Eligibility badges */}
        <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
          <div className="flex flex-wrap items-center gap-1.5">
            <EligibilityBadge category={job.eligibility_category} classification={job.eligibility_classification} />
            <VerificationBadge status={job.verification_status} />
          </div>

          <button
            onClick={handleSaveClick}
            disabled={saving}
            className={`p-1.5 rounded-lg border transition-colors ${
              saved
                ? 'bg-amber-50 text-amber-600 border-amber-300'
                : 'text-slate-400 hover:text-slate-600 border-slate-200 hover:bg-slate-50'
            }`}
            title={saved ? 'Job Saved' : 'Save Job'}
          >
            {saved ? <Check className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
          </button>
        </div>

        {/* Job Title and Company */}
        <Link to={`/jobs/${job.id}`} className="group">
          <h3 className="text-base font-bold text-slate-900 group-hover:text-brand-600 transition-colors line-clamp-1">
            {job.title}
          </h3>
        </Link>

        <div className="flex items-center gap-1.5 text-sm font-medium text-slate-700 mt-1">
          <Building2 className="w-4 h-4 text-slate-400 flex-shrink-0" />
          <span className="truncate">{job.company_name}</span>
        </div>

        {/* Location & Mode */}
        <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 mt-2.5">
          <span className="flex items-center gap-1 font-medium">
            <MapPin className="w-3.5 h-3.5 text-slate-400" />
            {job.city || job.location}
            {isKerala && (
              <span className="ml-1 px-1.5 py-0.2 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800">
                Kerala IT
              </span>
            )}
          </span>

          <span className="px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium capitalize">
            {job.work_mode?.toLowerCase()}
          </span>

          <span className="px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium capitalize">
            {job.employment_type?.replace('_', ' ').toLowerCase()}
          </span>
        </div>

        {/* Salary */}
        {job.salary_disclosed && job.salary_raw_text && (
          <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-700 mt-2 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-100 w-fit">
            <Banknote className="w-3.5 h-3.5" />
            <span>{job.salary_raw_text}</span>
          </div>
        )}

        {/* Skills */}
        {job.required_skills && job.required_skills.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-3.5">
            {job.required_skills.slice(0, 4).map((skill, idx) => (
              <span
                key={idx}
                className="px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200"
              >
                {skill}
              </span>
            ))}
            {job.required_skills.length > 4 && (
              <span className="text-[10px] text-slate-400 font-medium self-center">
                +{job.required_skills.length - 4} more
              </span>
            )}
          </div>
        )}
      </div>

      {/* Footer CTA & Metadata */}
      <div className="border-t border-slate-100 pt-3.5 mt-4 flex items-center justify-between text-xs text-slate-500">
        <span className="flex items-center gap-1">
          <Calendar className="w-3.5 h-3.5 text-slate-400" />
          {job.first_discovered_at ? new Date(job.first_discovered_at).toLocaleDateString() : 'Recently added'}
        </span>

        <div className="flex items-center gap-2">
          <Link
            to={`/jobs/${job.id}`}
            className="font-semibold text-brand-600 hover:text-brand-700 px-2.5 py-1 rounded hover:bg-brand-50 transition-colors"
          >
            Details
          </Link>

          <a
            href={job.official_apply_url || job.original_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-semibold bg-brand-600 hover:bg-brand-700 text-white shadow-sm transition-colors"
          >
            Apply
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>
    </div>
  );
}
