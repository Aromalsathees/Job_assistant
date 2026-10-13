import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Sparkles,
  ShieldCheck,
  CheckCircle2,
  Calendar,
  Building,
  ArrowRight,
  TrendingUp,
  MapPin,
  Clock,
  Search,
  Activity
} from 'lucide-react';
import StatCard from '../components/StatCard';
import JobCard from '../components/JobCard';
import { api } from '../api/client';

export default function Dashboard({ onTriggerDiscovery }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [digest, setDigest] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [statsRes, digestRes] = await Promise.all([
        api.getDashboardStats(),
        api.getDailyDigest(),
      ]);
      setStats(statsRes.data);
      setDigest(digestRes.data);
    } catch (err) {
      console.error('Error loading dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-xs text-slate-500 font-medium">Loading fresher job intelligence...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Hero Welcome Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-brand-900 via-brand-800 to-slate-900 text-white p-6 sm:p-8 shadow-sm">
        <div className="relative z-10 max-w-3xl space-y-3">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-brand-500/20 text-brand-300 border border-brand-500/30">
            <Sparkles className="w-3.5 h-3.5 text-brand-400" />
            Strict 0–1 Year Experience Verification Active
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            South India Fresher Job Intelligence Agent
          </h1>
          <p className="text-sm text-slate-300 leading-relaxed">
            Real-time automated discovery for entry-level IT careers. Highest default ranking for{' '}
            <strong className="text-white">Kerala (Infopark Kochi, Technopark Trivandrum)</strong>,{' '}
            <strong className="text-white">Tamil Nadu (Chennai, Coimbatore)</strong>, and{' '}
            <strong className="text-white">Bengaluru</strong>. Jobs requiring &gt;1 year mandatory experience are strictly excluded from matching.
          </p>

          <div className="flex flex-wrap items-center gap-3 pt-2">
            <Link
              to="/jobs"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-900 hover:bg-slate-100 transition-colors shadow-sm"
            >
              <Search className="w-4 h-4 text-brand-600" />
              Explore All Matching Jobs
            </Link>
            <button
              onClick={onTriggerDiscovery}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold bg-brand-600 hover:bg-brand-500 text-white transition-colors"
            >
              <Activity className="w-4 h-4" />
              Trigger Discovery Sweep
            </button>
          </div>
        </div>

        {/* Decorative background shape */}
        <div className="absolute -right-12 -bottom-12 w-64 h-64 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Eligible Fresher Jobs"
          value={stats?.total_eligible_jobs ?? 0}
          subtitle="Strictly 0–1 year experience only"
          icon={Sparkles}
          color="emerald"
        />
        <StatCard
          title="Official Verified"
          value={stats?.official_verified_jobs ?? 0}
          subtitle="Direct campus & official portal verified"
          icon={ShieldCheck}
          color="blue"
        />
        <StatCard
          title="Discovered (7 Days)"
          value={stats?.new_discovered_7d ?? 0}
          subtitle="Fresh openings indexed recently"
          icon={TrendingUp}
          color="purple"
        />
        <StatCard
          title="Ineligible Excluded"
          value={stats?.ineligible_experienced_jobs ?? 0}
          subtitle="Filtered out (>1 yr mandatory exp)"
          icon={CheckCircle2}
          color="amber"
        />
      </div>

      {/* City Breakdown & Daily Digest Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* City Distribution */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm lg:col-span-2">
          <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-4">
            <div>
              <h2 className="text-sm font-bold text-slate-900">Job Distribution by IT City</h2>
              <p className="text-xs text-slate-500">Live verified openings across major South India tech corridors</p>
            </div>
            <span className="text-[11px] font-semibold text-brand-600 bg-brand-50 px-2.5 py-1 rounded-full border border-brand-100">
              Kerala Priority #1
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {(stats?.jobs_by_city || []).map((item) => (
              <div
                key={item.city}
                className="p-3.5 rounded-xl border border-slate-100 bg-slate-50/70 hover:bg-white hover:border-brand-200 transition-all"
              >
                <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-700">
                  <MapPin className="w-3.5 h-3.5 text-brand-600" />
                  <span className="truncate">{item.city}</span>
                </div>
                <div className="mt-2 text-xl font-extrabold text-slate-900">{item.count}</div>
                <span className="text-[10px] text-slate-400 font-medium">Eligible freshers</span>
              </div>
            ))}
          </div>

          {/* Experience Breakdown Pills */}
          <div className="mt-6 pt-5 border-t border-slate-100">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">
              Eligibility Tier Breakdown
            </h3>
            <div className="flex flex-wrap gap-2">
              {(stats?.experience_breakdown || []).map((cat) => (
                <div
                  key={cat.eligibility_category}
                  className="px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 text-slate-700 border border-slate-200 flex items-center gap-2"
                >
                  <span className="capitalize">{cat.eligibility_category.replace(/_/g, ' ').toLowerCase()}</span>
                  <span className="px-1.5 py-0.2 bg-white rounded text-slate-900 font-bold text-[11px]">
                    {cat.count}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Daily Intelligence Digest Card */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-brand-600" />
                <h2 className="text-sm font-bold text-slate-900">Today's Fresher Briefing</h2>
              </div>
              <span className="text-[10px] text-slate-400 font-medium">
                {digest ? new Date(digest.report_date).toLocaleDateString() : 'Today'}
              </span>
            </div>

            <div className="space-y-3 text-xs text-slate-600">
              <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-100 text-emerald-900 font-medium space-y-1">
                <p className="font-bold text-emerald-800">24h Summary:</p>
                <p>• {digest?.total_new_eligible || 0} new fresher openings discovered</p>
                <p>• {digest?.official_verified_count || 0} direct campus/employer verified</p>
                <p>• {digest?.kerala_count || 0} positions in Kerala IT Parks</p>
              </div>

              {digest?.top_openings && digest.top_openings.length > 0 && (
                <div className="space-y-2 mt-3">
                  <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
                    Featured Openings:
                  </p>
                  {digest.top_openings.slice(0, 3).map((top, idx) => (
                    <div key={idx} className="p-2.5 rounded-lg border border-slate-100 bg-slate-50">
                      <p className="font-bold text-slate-800 text-xs truncate">{top.title}</p>
                      <p className="text-[11px] text-slate-500">{top.company} • {top.city}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="pt-4 border-t border-slate-100 mt-4">
            <Link
              to="/jobs"
              className="w-full inline-flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg text-xs font-bold text-brand-700 bg-brand-50 hover:bg-brand-100 transition-colors"
            >
              <span>View Full Daily Report</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>

      {/* Latest Matching Jobs */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Recently Discovered Fresher Jobs</h2>
            <p className="text-xs text-slate-500">Directly fetched, normalized, and eligibility-verified</p>
          </div>
          <Link
            to="/jobs"
            className="text-xs font-semibold text-brand-600 hover:text-brand-700 flex items-center gap-1"
          >
            <span>View All</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {stats?.recent_jobs && stats.recent_jobs.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {stats.recent_jobs.map((job) => (
              <JobCard key={job.id} job={job} />
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-xl border border-slate-200 p-8 text-center text-slate-500 text-xs">
            No matching jobs discovered yet. Click "Run Discovery" to trigger the intelligence agent.
          </div>
        )}
      </div>
    </div>
  );
}
