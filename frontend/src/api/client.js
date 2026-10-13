import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

// Create persistent local session key
let clientSessionId = localStorage.getItem('job_agent_session_id');
if (!clientSessionId) {
  clientSessionId = 'user-' + Math.random().toString(36).substring(2, 10);
  localStorage.setItem('job_agent_session_id', clientSessionId);
}

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
    'X-Client-Session': clientSessionId,
  },
  timeout: 20000,
});

export const api = {
  // Health
  checkHealth: () => apiClient.get('/health/'),

  // Dashboard & Digest
  getDashboardStats: () => apiClient.get('/dashboard-stats/'),
  getDailyDigest: () => apiClient.get('/daily-digest/'),
  getMetaOptions: () => apiClient.get('/jobs/meta_options/'),

  // Jobs
  getJobs: (params = {}) => apiClient.get('/jobs/', { params }),
  getJobDetail: (id) => apiClient.get(`/jobs/${id}/`),

  // Saved Jobs
  getSavedJobs: () => apiClient.get('/saved-jobs/'),
  saveJob: (jobId, notes = '') => apiClient.post('/saved-jobs/', { job: jobId, notes }),
  removeSavedJob: (id) => apiClient.delete(`/saved-jobs/${id}/`),

  // Application Tracker
  getApplications: () => apiClient.get('/tracker/'),
  createApplication: (data) => apiClient.post('/tracker/', data),
  updateApplication: (id, data) => apiClient.patch(`/tracker/${id}/`, data),
  deleteApplication: (id) => apiClient.delete(`/tracker/${id}/`),

  // Discovery Runs
  getDiscoveryRuns: () => apiClient.get('/runs/'),
  getLatestRunSummary: () => apiClient.get('/runs/latest-summary/'),
  triggerDiscovery: () => apiClient.post('/runs/trigger/'),

  // User Preferences
  getPreferences: () => apiClient.get('/user/preferences/'),
  updatePreferences: (data) => apiClient.put('/user/preferences/', data),

  // Job Sources
  getSources: () => apiClient.get('/sources/'),
};

export default apiClient;
