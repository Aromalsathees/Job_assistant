import React, { useState, useEffect } from 'react';
import { Search, SlidersHorizontal, AlertCircle, Sparkles, HelpCircle } from 'lucide-react';
import JobCard from '../components/JobCard';
import FilterSidebar from '../components/FilterSidebar';
import Pagination from '../components/Pagination';
import { api } from '../api/client';

export default function JobSearch() {
  const [jobs, setJobs] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [cities, setCities] = useState([]);

  // Search & Filter state
  const [filters, setFilters] = useState({
    search: '',
    city: '',
    work_mode: '',
    eligibility: 'ELIGIBLE_FRESHER', // STRICT DEFAULT: only 0-1 year
    eligibility_category: '',
    verification_status: '',
    salary_disclosed: '',
    ordering: '-ranking_score',
    page: 1,
  });

  const [searchInput, setSearchInput] = useState('');

  useEffect(() => {
    // Load meta options for dropdowns
    api.getMetaOptions().then((res) => {
      setCities(res.data.cities || []);
    }).catch((e) => console.error(e));
  }, []);

  useEffect(() => {
    fetchJobsList();
  }, [filters]);

  const fetchJobsList = async () => {
    setLoading(true);
    try {
      const params = { ...filters };
      // Clean empty keys
      Object.keys(params).forEach((k) => {
        if (params[k] === '' || params[k] === null) delete params[k];
      });

      const res = await api.getJobs(params);
      const data = res.data;
      if (data.results) {
        setJobs(data.results);
        setTotalCount(data.count || 0);
      } else if (Array.isArray(data)) {
        setJobs(data);
        setTotalCount(data.length);
      }
    } catch (err) {
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setFilters({ ...filters, search: searchInput, page: 1 });
  };

  const handleResetFilters = () => {
    setSearchInput('');
    setFilters({
      search: '',
      city: '',
      work_mode: '',
      eligibility: 'ELIGIBLE_FRESHER',
      eligibility_category: '',
      verification_status: '',
      salary_disclosed: '',
      ordering: '-ranking_score',
      page: 1,
    });
  };

  return (
    <div className="space-y-6">
      {/* Header & Search Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <div className="max-w-3xl">
          <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
            Fresher Job Discovery & Search
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Browse genuine openings filtered strictly for 0–1 year of professional experience.
          </p>
        </div>

        {/* Search input form */}
        <form onSubmit={handleSearchSubmit} className="mt-5 flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              placeholder="Search by job title, company name, or technology skills (e.g. Python, Django, FastAPI, AI Agent)..."
              className="w-full pl-10 pr-4 py-2.5 text-xs sm:text-sm rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-brand-500 focus:outline-none transition-all"
            />
          </div>
          <button
            type="submit"
            className="px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-brand-600 hover:bg-brand-700 text-white shadow-sm transition-colors"
          >
            Search
          </button>
        </form>

        {/* Eligibility Mode Notification Banner */}
        <div className="mt-4 pt-4 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2">
            {filters.eligibility === 'ELIGIBLE_FRESHER' ? (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 font-semibold border border-emerald-200">
                <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
                Strict 0–1 Year Filter Active
              </span>
            ) : filters.eligibility === 'ELIGIBILITY_UNCLEAR' ? (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-amber-50 text-amber-800 font-semibold border border-amber-200">
                <HelpCircle className="w-3.5 h-3.5 text-amber-600" />
                Viewing Experience Unclear Listings
              </span>
            ) : (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-100 text-slate-800 font-semibold border border-slate-200">
                Viewing All Categories (Including Experienced)
              </span>
            )}

            <span className="text-slate-500 hidden sm:inline">
              {filters.eligibility === 'ELIGIBLE_FRESHER' && 'Senior & 2+ yrs roles excluded.'}
            </span>
          </div>

          {/* Quick tab switcher */}
          <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-lg">
            <button
              onClick={() => setFilters({ ...filters, eligibility: 'ELIGIBLE_FRESHER', page: 1 })}
              className={`px-2.5 py-1 rounded-md text-[11px] font-bold transition-colors ${
                filters.eligibility === 'ELIGIBLE_FRESHER'
                  ? 'bg-white text-brand-700 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Freshers (0-1y)
            </button>
            <button
              onClick={() => setFilters({ ...filters, eligibility: 'ELIGIBILITY_UNCLEAR', page: 1 })}
              className={`px-2.5 py-1 rounded-md text-[11px] font-bold transition-colors ${
                filters.eligibility === 'ELIGIBILITY_UNCLEAR'
                  ? 'bg-white text-amber-800 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Unclear Exp
            </button>
            <button
              onClick={() => setFilters({ ...filters, eligibility: 'ALL', page: 1 })}
              className={`px-2.5 py-1 rounded-md text-[11px] font-bold transition-colors ${
                filters.eligibility === 'ALL'
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              All Listings
            </button>
          </div>
        </div>
      </div>

      {/* Main Content Layout: Filters + Results Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        {/* Sidebar Filters */}
        <div className="lg:col-span-1">
          <FilterSidebar
            filters={filters}
            onChange={setFilters}
            onReset={handleResetFilters}
            cities={cities}
          />
        </div>

        {/* Results Column */}
        <div className="lg:col-span-3 space-y-4">
          {/* Controls Bar: Sort & Count */}
          <div className="flex items-center justify-between text-xs text-slate-500 bg-white p-3.5 rounded-xl border border-slate-200">
            <span className="font-semibold text-slate-700">
              {totalCount} {totalCount === 1 ? 'Job' : 'Jobs'} Found
            </span>

            <div className="flex items-center gap-2">
              <span className="font-medium">Sort by:</span>
              <select
                value={filters.ordering}
                onChange={(e) => setFilters({ ...filters, ordering: e.target.value, page: 1 })}
                className="rounded-lg border-slate-200 text-xs font-semibold text-slate-700 bg-slate-50 py-1 px-2 focus:border-brand-500 focus:ring-0"
              >
                <option value="-ranking_score">Kerala Priority &amp; Relevance</option>
                <option value="-first_discovered_at">Newest First</option>
                <option value="-salary_min">Highest Published Salary</option>
              </select>
            </div>
          </div>

          {/* Cards Grid */}
          {loading ? (
            <div className="flex items-center justify-center py-20 bg-white rounded-xl border border-slate-200">
              <div className="flex flex-col items-center gap-3">
                <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
                <p className="text-xs text-slate-500 font-medium">Filtering jobs...</p>
              </div>
            </div>
          ) : jobs.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {jobs.map((job) => (
                <JobCard key={job.id} job={job} />
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-slate-100 text-slate-400 mx-auto flex items-center justify-center">
                <AlertCircle className="w-6 h-6" />
              </div>
              <h3 className="text-sm font-bold text-slate-900">No matching fresher jobs found</h3>
              <p className="text-xs text-slate-500 max-w-md mx-auto">
                No jobs match the current filter combination. Remember that jobs requiring &gt;1 year experience are strictly excluded from default matching.
              </p>
              <button
                onClick={handleResetFilters}
                className="mt-2 inline-flex items-center px-4 py-2 rounded-lg text-xs font-bold text-brand-600 bg-brand-50 hover:bg-brand-100 transition-colors"
              >
                Reset All Filters
              </button>
            </div>
          )}

          {/* Pagination */}
          <Pagination
            count={totalCount}
            pageSize={15}
            currentPage={filters.page || 1}
            onPageChange={(p) => setFilters({ ...filters, page: p })}
          />
        </div>
      </div>
    </div>
  );
}
