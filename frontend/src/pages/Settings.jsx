import React, { useEffect, useState } from 'react';
import { Settings as SettingsIcon, Save, CheckCircle2, Clock, MapPin, Briefcase, Mail } from 'lucide-react';
import { api } from '../api/client';

export default function Settings() {
  const [prefs, setPrefs] = useState({
    target_roles: [],
    target_locations: [],
    preferred_skills: [],
    preferred_work_modes: ['ONSITE', 'HYBRID', 'REMOTE'],
    min_salary: '',
    notification_email: '',
    daily_schedule_enabled: true,
    schedule_hour: 6,
    schedule_timezone: 'Asia/Kolkata',
  });
  const [loading, setLoading] = useState(true);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [roleInput, setRoleInput] = useState('');
  const [locationInput, setLocationInput] = useState('');
  const [skillInput, setSkillInput] = useState('');

  useEffect(() => {
    loadPreferences();
  }, []);

  const loadPreferences = async () => {
    setLoading(true);
    try {
      const res = await api.getPreferences();
      setPrefs({ ...res.data, min_salary: res.data.min_salary || '' });
    } catch (err) {
      console.error('Error fetching preferences:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSavedSuccess(false);
    try {
      const payload = {
        ...prefs,
        min_salary: prefs.min_salary ? parseFloat(prefs.min_salary) : null,
      };
      await api.updatePreferences(payload);
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 4000);
    } catch (err) {
      console.error('Error updating preferences:', err);
    }
  };

  const addTag = (type, val, setInput) => {
    if (!val.trim()) return;
    if (!prefs[type].includes(val.trim())) {
      setPrefs({ ...prefs, [type]: [...prefs[type], val.trim()] });
    }
    setInput('');
  };

  const removeTag = (type, item) => {
    setPrefs({ ...prefs, [type]: prefs[type].filter((x) => x !== item) });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
          Job Intelligence Preferences
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Customize target fresher roles, South India priority regions, and scheduled notification parameters.
        </p>
      </div>

      <form onSubmit={handleSave} className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-8">
        {savedSuccess && (
          <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-xs font-semibold text-emerald-800 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>Preferences successfully persisted to PostgreSQL backend.</span>
          </div>
        )}

        {/* Target Roles */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
            Target Job Roles &amp; Titles
          </label>
          <div className="flex gap-2 mb-2">
            <input
              type="text"
              value={roleInput}
              onChange={(e) => setRoleInput(e.target.value)}
              placeholder="Add role (e.g. Agentic AI Developer, Django REST Framework Developer)..."
              className="flex-1 text-xs rounded-xl border-slate-200 bg-slate-50 p-2.5 focus:bg-white focus:border-brand-500 focus:outline-none"
            />
            <button
              type="button"
              onClick={() => addTag('target_roles', roleInput, setRoleInput)}
              className="px-4 py-2 text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl"
            >
              Add
            </button>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {prefs.target_roles.map((r) => (
              <span
                key={r}
                className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-brand-50 text-brand-800 border border-brand-200 flex items-center gap-1.5"
              >
                {r}
                <button type="button" onClick={() => removeTag('target_roles', r)} className="text-slate-400 hover:text-slate-600">
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>

        {/* Target Locations */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
            Target Locations (Kerala &amp; South India Priority)
          </label>
          <div className="flex gap-2 mb-2">
            <input
              type="text"
              value={locationInput}
              onChange={(e) => setLocationInput(e.target.value)}
              placeholder="Add city/park (e.g. Kakkanad, Infopark, Coimbatore, Chennai)..."
              className="flex-1 text-xs rounded-xl border-slate-200 bg-slate-50 p-2.5 focus:bg-white focus:border-brand-500 focus:outline-none"
            />
            <button
              type="button"
              onClick={() => addTag('target_locations', locationInput, setLocationInput)}
              className="px-4 py-2 text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl"
            >
              Add
            </button>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {prefs.target_locations.map((loc) => (
              <span
                key={loc}
                className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200 flex items-center gap-1.5"
              >
                <MapPin className="w-3 h-3 text-slate-400" />
                {loc}
                <button type="button" onClick={() => removeTag('target_locations', loc)} className="text-slate-400 hover:text-slate-600">
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>

        {/* Preferred Skills */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
            Preferred Technical Skills
          </label>
          <div className="flex gap-2 mb-2">
            <input
              type="text"
              value={skillInput}
              onChange={(e) => setSkillInput(e.target.value)}
              placeholder="Add skill (e.g. LangChain, PostgreSQL, Tailwind, Docker)..."
              className="flex-1 text-xs rounded-xl border-slate-200 bg-slate-50 p-2.5 focus:bg-white focus:border-brand-500 focus:outline-none"
            />
            <button
              type="button"
              onClick={() => addTag('preferred_skills', skillInput, setSkillInput)}
              className="px-4 py-2 text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl"
            >
              Add
            </button>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {prefs.preferred_skills.map((s) => (
              <span
                key={s}
                className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200 flex items-center gap-1.5"
              >
                {s}
                <button type="button" onClick={() => removeTag('preferred_skills', s)} className="text-slate-400 hover:text-slate-600">
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>

        {/* Schedule & Notifications */}
        <div className="border-t border-slate-100 pt-6 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
            Daily Automated Discovery &amp; Schedule
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Schedule Time (IST)</label>
              <select
                value={prefs.schedule_hour}
                onChange={(e) => setPrefs({ ...prefs, schedule_hour: parseInt(e.target.value) })}
                className="w-full text-xs rounded-xl border-slate-200 bg-slate-50 p-2.5 focus:border-brand-500"
              >
                <option value={6}>06:00 AM IST (Recommended)</option>
                <option value={9}>09:00 AM IST</option>
                <option value={12}>12:00 PM IST</option>
                <option value={18}>06:00 PM IST</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Digest Recipient Email</label>
              <input
                type="email"
                value={prefs.notification_email || ''}
                onChange={(e) => setPrefs({ ...prefs, notification_email: e.target.value })}
                placeholder="fresher@example.com"
                className="w-full text-xs rounded-xl border-slate-200 bg-slate-50 p-2.5 focus:border-brand-500"
              />
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-4 flex justify-end">
          <button
            type="submit"
            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-brand-600 hover:bg-brand-700 text-white shadow-sm transition-colors"
          >
            <Save className="w-4 h-4" />
            <span>Save Preferences</span>
          </button>
        </div>
      </form>
    </div>
  );
}
