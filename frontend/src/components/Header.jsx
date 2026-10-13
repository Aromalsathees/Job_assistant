import React, { useState, useEffect } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import {
  Compass,
  Search,
  Bookmark,
  BriefcaseBusiness,
  Activity,
  Settings as SettingsIcon,
  Play,
  CheckCircle2,
  AlertTriangle,
  Menu,
  X
} from 'lucide-react';
import { api } from '../api/client';

export default function Header({ onTriggerDiscovery }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [healthStatus, setHealthStatus] = useState('checking');

  useEffect(() => {
    api.checkHealth()
      .then(() => setHealthStatus('healthy'))
      .catch(() => setHealthStatus('offline'));
  }, []);

  const navLinks = [
    { to: '/', label: 'Dashboard', icon: Compass },
    { to: '/jobs', label: 'Job Search', icon: Search },
    { to: '/saved', label: 'Saved Jobs', icon: Bookmark },
    { to: '/tracker', label: 'Application Tracker', icon: BriefcaseBusiness },
    { to: '/runs', label: 'Discovery Runs', icon: Activity },
    { to: '/settings', label: 'Settings', icon: SettingsIcon },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <div className="flex items-center gap-3">
            <Link to="/" className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-brand-600 flex items-center justify-center text-white font-black text-lg shadow-sm">
                ⚡
              </div>
              <div>
                <span className="font-extrabold text-sm sm:text-base tracking-tight text-slate-900 block leading-tight">
                  South India Fresher
                </span>
                <span className="text-[11px] font-semibold text-brand-600 uppercase tracking-wider block">
                  Job Intelligence Agent
                </span>
              </div>
            </Link>

            {/* Health status badge */}
            <div className="hidden lg:flex items-center gap-1.5 ml-4 pl-4 border-l border-slate-200 text-xs">
              <span
                className={`w-2 h-2 rounded-full ${
                  healthStatus === 'healthy' ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'
                }`}
              />
              <span className="text-slate-500 font-medium">
                {healthStatus === 'healthy' ? 'Agent Live' : 'Connecting'}
              </span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                    isActive
                      ? 'bg-brand-50 text-brand-700'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                  }`
                }
              >
                <Icon className="w-3.5 h-3.5" />
                {label}
              </NavLink>
            ))}
          </nav>

          {/* Action: Run Discovery Now */}
          <div className="flex items-center gap-2">
            <button
              onClick={onTriggerDiscovery}
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold bg-brand-600 hover:bg-brand-700 text-white shadow-sm transition-colors"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span className="hidden sm:inline">Run Discovery</span>
            </button>

            {/* Mobile menu trigger */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-1.5 rounded-lg text-slate-600 hover:bg-slate-100"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile navigation drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-white px-4 pt-2 pb-4 space-y-1">
          {navLinks.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={() => setMobileMenuOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium ${
                  isActive ? 'bg-brand-50 text-brand-700 font-bold' : 'text-slate-700 hover:bg-slate-50'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              {label}
            </NavLink>
          ))}
        </div>
      )}
    </header>
  );
}
