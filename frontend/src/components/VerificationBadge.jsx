import React from 'react';
import { ShieldCheck, CheckCircle2, AlertCircle, AlertOctagon, Clock } from 'lucide-react';

export default function VerificationBadge({ status }) {
  switch (status) {
    case 'OFFICIAL_VERIFIED':
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          Official Source Verified
        </span>
      );
    case 'TRUSTED_BOARD':
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
          <CheckCircle2 className="w-3.5 h-3.5 text-blue-600" />
          Trusted Job-Board
        </span>
      );
    case 'SUSPICIOUS':
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-300">
          <AlertOctagon className="w-3.5 h-3.5 text-rose-600" />
          Flagged Suspicious
        </span>
      );
    case 'EXPIRED':
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-600 border border-slate-300">
          <Clock className="w-3.5 h-3.5" />
          Expired / Inactive
        </span>
      );
    case 'NEEDS_VERIFICATION':
    default:
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
          <AlertCircle className="w-3.5 h-3.5 text-amber-600" />
          Needs Verification
        </span>
      );
  }
}
