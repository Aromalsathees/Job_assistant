import React from 'react';
import { Filter, X, RotateCcw } from 'lucide-react';

export default function FilterSidebar({
  filters,
  onChange,
  onReset,
  cities = [],
}) {
  const update = (key, val) => {
    onChange({ ...filters, [key]: val, page: 1 });
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-6">
      <div className="flex items-center justify-between pb-3 border-b border-slate-100">
        <div className="flex items-center gap-2 font-bold text-slate-800 text-sm">
          <Filter className="w-4 h-4 text-brand-600" />
          <span>Filters & Eligibility</span>
        </div>
        <button
          onClick={onReset}
          className="text-xs text-slate-400 hover:text-brand-600 flex items-center gap-1 font-medium transition-colors"
          title="Reset all filters"
        >
          <RotateCcw className="w-3 h-3" />
          Reset
        </button>
      </div>

      {/* Strict 0-1 Year Eligibility Filter */}
      <div>
        <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
          Experience Eligibility
        </label>
        <select
          value={filters.eligibility || 'ELIGIBLE_FRESHER'}
          onChange={(e) => update('eligibility', e.target.value)}
          className="w-full text-xs rounded-lg border-slate-200 bg-slate-50 p-2 font-medium text-slate-800 focus:border-brand-500 focus:bg-white focus:ring-0"
        >
          <option value="ELIGIBLE_FRESHER">Strict Freshers Only (0–1 Year)</option>
          <option value="ELIGIBILITY_UNCLEAR">Eligibility Unclear (Separated)</option>
          <option value="ALL">All Categories (Includes Experienced)</option>
        </select>
        <p className="text-[11px] text-slate-400 mt-1">
          Default view excludes &gt;1 year experience &amp; unstated criteria.
        </p>
      </div>

      {/* Specific Experience Category */}
      <div>
        <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
          Category
        </label>
        <select
          value={filters.eligibility_category || ''}
          onChange={(e) => update('eligibility_category', e.target.value)}
          className="w-full text-xs rounded-lg border-slate-200 bg-slate-50 p-2 font-medium text-slate-800 focus:border-brand-500 focus:bg-white focus:ring-0"
        >
          <option value="">All Eligible Tiers</option>
          <option value="FRESHER_0">Fresher / 0 years</option>
          <option value="0_6_MONTHS">0–6 months</option>
          <option value="6_12_MONTHS">6–12 months</option>
          <option value="0_1_YEAR">0–1 year</option>
          <option value="GRADUATE_TRAINEE">Graduate Trainee</option>
          <option value="INTERNSHIP_FRESHER">Fresher Internship</option>
        </select>
      </div>

      {/* City / Location */}
      <div>
        <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
          Location / City
        </label>
        <select
          value={filters.city || ''}
          onChange={(e) => update('city', e.target.value)}
          className="w-full text-xs rounded-lg border-slate-200 bg-slate-50 p-2 font-medium text-slate-800 focus:border-brand-500 focus:bg-white focus:ring-0"
        >
          <option value="">All South India Locations</option>
          <optgroup label="Kerala IT Hubs (Priority)">
            <option value="Kochi">Kochi / Ernakulam / Infopark</option>
            <option value="Thiruvananthapuram">Thiruvananthapuram / Technopark</option>
            <option value="Kozhikode">Kozhikode / Cyberpark</option>
            <option value="Thrissur">Thrissur</option>
          </optgroup>
          <optgroup label="Tamil Nadu">
            <option value="Chennai">Chennai</option>
            <option value="Coimbatore">Coimbatore</option>
            <option value="Madurai">Madurai</option>
          </optgroup>
          <optgroup label="Other Tech Hubs">
            <option value="Bengaluru">Bengaluru</option>
            <option value="Hyderabad">Hyderabad</option>
            <option value="Remote">Remote (India)</option>
          </optgroup>
          {cities.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      {/* Work Mode */}
      <div>
        <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
          Work Mode
        </label>
        <div className="space-y-1.5">
          {['ONSITE', 'HYBRID', 'REMOTE'].map((mode) => (
            <label key={mode} className="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
              <input
                type="radio"
                name="work_mode"
                checked={filters.work_mode === mode}
                onChange={() => update('work_mode', filters.work_mode === mode ? '' : mode)}
                className="text-brand-600 focus:ring-brand-500 rounded border-slate-300"
              />
              <span className="capitalize">{mode.toLowerCase()}</span>
            </label>
          ))}
          {filters.work_mode && (
            <button
              onClick={() => update('work_mode', '')}
              className="text-[11px] text-brand-600 font-medium hover:underline pt-1 block"
            >
              Clear work mode
            </button>
          )}
        </div>
      </div>

      {/* Verification Status */}
      <div>
        <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
          Verification Status
        </label>
        <select
          value={filters.verification_status || ''}
          onChange={(e) => update('verification_status', e.target.value)}
          className="w-full text-xs rounded-lg border-slate-200 bg-slate-50 p-2 font-medium text-slate-800 focus:border-brand-500 focus:bg-white focus:ring-0"
        >
          <option value="">All Verification Levels</option>
          <option value="OFFICIAL_VERIFIED">Official Source Verified Only</option>
          <option value="TRUSTED_BOARD">Trusted Job-Board</option>
          <option value="NEEDS_VERIFICATION">Needs Verification</option>
        </select>
      </div>

      {/* Salary Disclosed Only */}
      <div className="pt-2 border-t border-slate-100">
        <label className="flex items-center gap-2 text-xs font-medium text-slate-700 cursor-pointer">
          <input
            type="checkbox"
            checked={Boolean(filters.salary_disclosed)}
            onChange={(e) => update('salary_disclosed', e.target.checked ? true : '')}
            className="rounded text-brand-600 focus:ring-brand-500 border-slate-300"
          />
          <span>Published Salary Only</span>
        </label>
      </div>
    </div>
  );
}
