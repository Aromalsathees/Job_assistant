import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import JobSearch from './pages/JobSearch';
import JobDetail from './pages/JobDetail';
import SavedJobs from './pages/SavedJobs';
import ApplicationTracker from './pages/ApplicationTracker';
import DiscoveryRuns from './pages/DiscoveryRuns';
import Settings from './pages/Settings';
import RunDiscoveryModal from './components/RunDiscoveryModal';

export default function App() {
  const [discoveryModalOpen, setDiscoveryModalOpen] = useState(false);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
        <Header onTriggerDiscovery={() => setDiscoveryModalOpen(true)} />

        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route
              path="/"
              element={<Dashboard onTriggerDiscovery={() => setDiscoveryModalOpen(true)} />}
            />
            <Route path="/jobs" element={<JobSearch />} />
            <Route path="/jobs/:id" element={<JobDetail />} />
            <Route path="/saved" element={<SavedJobs />} />
            <Route path="/tracker" element={<ApplicationTracker />} />
            <Route
              path="/runs"
              element={<DiscoveryRuns onTriggerDiscovery={() => setDiscoveryModalOpen(true)} />}
            />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-slate-200 mt-auto py-6">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
            <div>
              <span className="font-bold text-slate-700">South India Fresher Job Intelligence Agent</span>
              <span className="ml-2">© 2026. Prioritizing Kerala (Kochi/Infopark, Trivandrum/Technopark) &amp; South India Freshers.</span>
            </div>
            <div className="flex items-center gap-4 text-slate-400">
              <span>Strict 0-1 Yr Experience Enforcement</span>
              <span>•</span>
              <span>Official Campus Verified Sources</span>
            </div>
          </div>
        </footer>

        {/* On-demand discovery modal */}
        <RunDiscoveryModal
          isOpen={discoveryModalOpen}
          onClose={() => setDiscoveryModalOpen(false)}
          onComplete={(run) => {
            console.log('Discovery sweep finished:', run);
          }}
        />
      </div>
    </BrowserRouter>
  );
}
