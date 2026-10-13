import React from 'react';
import { Sparkles, GraduationCap, Briefcase, HelpCircle, Clock } from 'lucide-react';

export default function EligibilityBadge({ category, classification }) {
  if (classification === 'ELIGIBILITY_UNCLEAR') {
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-medium bg-amber-100 text-amber-800">
        <HelpCircle className="w-3 h-3" />
        Eligibility Unclear
      </span>
    );
  }

  if (classification === 'INELIGIBLE_EXPERIENCED') {
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-medium bg-red-100 text-red-800">
        Experienced (>1 Yr)
      </span>
    );
  }

  switch (category) {
    case 'FRESHER_0':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-medium bg-teal-100 text-teal-800 border border-teal-200">
          <Sparkles className="w-3 h-3 text-teal-600" />
          Fresher / 0 Yrs
        </span>
      );
    case '0_6_MONTHS':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-medium bg-cyan-100 text-cyan-800 border border-cyan-200">
          <Clock className="w-3 h-3 text-cyan-600" />
          0–6 Months
        </span>
      );
    case '6_12_MONTHS':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-medium bg-sky-100 text-sky-800 border border-sky-200">
          <Clock className="w-3 h-3 text-sky-600" />
          6–12 Months
        </span>
      );
    case 'GRADUATE_TRAINEE':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-medium bg-indigo-100 text-indigo-800 border border-indigo-200">
          <GraduationCap className="w-3 h-3 text-indigo-600" />
          Graduate Trainee
        </span>
      );
    case 'INTERNSHIP_FRESHER':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-medium bg-purple-100 text-purple-800 border border-purple-200">
          <Briefcase className="w-3 h-3 text-purple-600" />
          Fresher Internship
        </span>
      );
    case '0_1_YEAR':
    default:
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-medium bg-emerald-100 text-emerald-800 border border-emerald-200">
          <Sparkles className="w-3 h-3 text-emerald-600" />
          0–1 Year
        </span>
      );
  }
}
