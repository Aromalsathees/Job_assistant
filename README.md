# South India Fresher Job Intelligence Agent ⚡

A production-ready, autonomous AI-powered job discovery and verification application engineered specifically for **freshers and junior IT developers (0–1 year of professional experience)** seeking verified software engineering opportunities across **South India** (prioritizing **Kerala: Ernakulam/Kochi/Infopark, Thiruvananthapuram/Technopark, Kozhikode, Thrissur**, alongside **Tamil Nadu: Chennai, Coimbatore**, and **Bengaluru**).

---

## 🎯 Core Features & Architecture

### 1. Strict 0–1 Year Experience Filter
- **Rigid Exclusion**: Any role requiring $>1$ year of mandatory experience (2, 3, 5+ yrs) or bearing Senior/Lead/Principal titles is strictly excluded from main matching results at the database query level.
- **Eligible Categories**:
  - `Fresher / 0 years`
  - `0–6 months`
  - `6–12 months`
  - `0–1 year`
  - `Graduate Trainee`
  - `Fresher Internships`
- **Ambiguity Separation**: Postings missing explicit experience specifications are tagged as `Eligibility Unclear` and kept out of default results.
- **Rule Boundary**: The title "Junior" alone does **not** grant automatic fresher classification.

### 2. Multi-Source Modular Adapter Engine
- **Technopark Kerala Careers Adapter**: Indexes member companies hiring at Thiruvananthapuram & Kollam campuses (UST Global, SunTec, Tata Elxsi, QBurst).
- **Infopark Kochi Official Portal Adapter**: Gathers verified listings from Kochi Phase 1, Phase 2, and Kakkanad IT Parks (IBS Software, NeST Digital, Fingent, Experion).
- **South India Direct Employer Adapter**: Connects verified direct employer careers portals (Zoho Chennai, Thoughtworks Coimbatore, Juspay Bengaluru, Techgentsia Cyberpark Kozhikode).
- **Remotive & Arbeitnow Public Developer APIs**: Indexes remote and India-eligible engineering openings with verified REST payloads.

### 3. Verification & Authenticity Audit
- Statuses: `Official source verified`, `Trusted job-board listing`, `Needs verification`, `Expired`, `Suspicious`.
- Automated detection of fraudulent requests (e.g., registration fees, training deposits).
- Every job records an evidence trail, domain provenance, and verbatim original descriptions separately from disclaimed AI summaries.

### 4. Interactive Modern React Dashboard
- **Dashboard**: Real-time DB counts, city distribution, experience tier breakdowns, and today's intelligence brief.
- **Job Search**: Instant keyword search, city filters, strict eligibility category switcher, work mode, and published salary filters.
- **Job Details**: Verbatim original description, skills tags, verification evidence history, disclaimed AI summary, direct official apply button.
- **Saved Jobs**: Shortlist vacancies and retain personal notes.
- **Application Tracker**: Kanban pipeline tracking stages (`Interested` $\rightarrow$ `Applied` $\rightarrow$ `Interview` $\rightarrow$ `Offer`).
- **Discovery Runs**: Execution logs, error tracking, deduplication stats, and a manual "Run Discovery Now" trigger.
- **Settings**: Configurable roles, locations, skills, and daily schedule hours persisted in PostgreSQL.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11, Django 5.x, Django REST Framework, django-filter, WhiteNoise, Gunicorn.
- **Frontend**: React 18, Vite, Tailwind CSS, Lucide React, Axios, React Router 6.
- **Database**: PostgreSQL (Production) / SQLite3 (Development fallback).
- **Containerization**: Docker, Docker Compose (multi-stage builds).

---

## 🚀 Quickstart & Local Setup

### Option A: Using Docker Compose (Recommended)

To run the complete application stack (PostgreSQL + Django Backend + React Frontend + Discovery Agent):

```bash
docker-compose up --build
```

- **Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)
- **Django REST API**: [http://localhost:8000/api/](http://localhost:8000/api/)
- **Health Check**: [http://localhost:8000/api/health/](http://localhost:8000/api/health/)

---

### Option B: Manual Setup

#### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python seed_data.py          # Populates verified sources and runs initial discovery
python manage.py runserver 8000
```

#### 2. Running Automated Tests
```bash
python run_tests.py
# or
python manage.py test jobs agent_engine.tests applications
```

#### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173).

---

## 🌐 Production Deployment

### 1. Render Blueprint (`render.yaml`)
Deploy with one click using Render Blueprint:
- Automatically provisions Managed PostgreSQL (`south-india-job-agent-db`).
- Runs migrations and starts Gunicorn WSGI.
- Builds and hosts static React frontend.

### 2. Vercel Frontend (`vercel.json`)
Deploy the React frontend on Vercel:
```bash
vercel --prod
```

---

## 🔒 Security & Data Integrity
- External content is treated as untrusted data.
- Instructions embedded in job descriptions are never executed by LLMs.
- Database transactions are atomic with SHA-256 uniqueness constraints preventing duplicate listings.
- API keys and database credentials reside exclusively in environment variables.
