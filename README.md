# EduPulse Enterprise Education CRM & Student Lifecycle Management Platform

EduPulse is an enterprise-grade, full-lifecycle Education Customer Relationship Management (CRM) and Student Information System (SIS). Designed for colleges, universities, academies, and vocational institutes, it unifies prospective lead capture, counselor outreach pipelines, admissions reviews, course catalogs, tuition fee billing, attendance marking, gradebook GPA calculations, support helpdesk ticketing, and business intelligence reporting into a single platform.

---

## 🌟 Key Functional Modules

### 1. Inbound Leads CRM & Intelligent Scoring
- Multi-channel lead capture (Web, Education Fairs, Social Media, Partner Agents, Referrals).
- Multi-factor lead scoring algorithm (0-100) evaluating engagement, budget, stage progression, and counselor touchpoints.
- Interactive Kanban drag-and-drop pipeline across 6 qualification stages.
- Counseling interaction call logs, meeting notes, and scheduled follow-ups.

### 2. Admissions & Applicant Screening
- Comprehensive applicant review queue with high school percentage and entrance examination scores.
- One-click applicant enrollment converting prospects to active students with automated Student ID assignment (`STU-YYYY-XXX`).
- Automated initial semester invoice generation upon enrollment.

### 3. Student Information System (SIS)
- 360-degree student profile containing enrollment records, guardian contact details, blood groups, and address records.
- Real-time GPA tracking, credit accumulation, and attendance percentage monitoring.

### 4. Course Catalog & Cohort Management
- Multi-degree level program management (Bachelor, Master, Diploma, Certificate).
- Detailed curriculum modules, credit hours, and syllabus outlines.
- Cohort and batch scheduling with classroom location and instructor assignments.

### 5. Tuition Billing, Invoicing & Receipts
- Semester tuition fee structures, scholarship discounts, and tax computations.
- Split installment schedules, overdue status tracking, and balance due calculations.
- Payment processing simulation across UPI, Bank Transfer, Credit Card, and Cash with printable receipts.

### 6. Classroom Attendance & Academic Gradebook
- Daily/lecture session attendance marking with threshold warning indicators (<75%).
- Configurable academic grading scales mapping scores to letter grades (A+, A, B, etc.) and 4.0 GPA rubric.

### 7. Support Helpdesk & Ticketing
- Multi-category support desk (Admissions, Billing, Academic, Technical, General).
- SLA tracking with priority escalation and threaded student-staff discussion.

### 8. Analytics, BI & Export Center
- Real-time admissions conversion funnels and financial collection rate analytics.
- One-click CSV and JSON data export engine for external audits and reporting.

---

## 🚀 Quick Start Guide

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- Git

### Installation & Execution

```bash
# 1. Clone repository
git clone https://github.com/Tassuu7/project-7-Education-CRM.git
cd project-7-Education-CRM

# 2. Run automated test suite
npm test

# 3. Launch application server
npm start
```

Open your browser and navigate to:
👉 **`http://localhost:4050`**

---

## 🔑 Pre-Configured Demo Accounts

| Role | Username | Password | Purpose |
|---|---|---|---|
| **Super Admin** | `superadmin` | `admin123` | Full access across all CRM modules and settings |
| **Admissions Counselor** | `counselor_rachel` | `counselor123` | Lead pipeline, interaction logging & calls |
| **Faculty / Instructor** | `prof_alan` | `faculty123` | Attendance sessions & gradebook grading |
| **Finance Officer** | `finance_elena` | `finance123` | Invoice ledger & payment collection |
| **Enrolled Student** | `student_rohit` | `student123` | Student portal, grades, attendance & fees |

---

## 📊 Codebase Metrics & Verification

To verify the Lines of Code (LOC) and system health:

```bash
# Run code metrics scanner
python measure.py

# Package complete standalone zip distribution
python scripts/package-project.py
```

---

## 🛡️ Architecture & Security Standards
- **Zero Third-Party Vendor Locks**: Custom high-performance in-memory persistence engine with JSON snapshot backups.
- **Role-Based Access Control (RBAC)**: Strict permission boundaries enforced at controller and route levels.
- **Sensitive Data Shield**: `.env` and sensitive files are excluded from source control.
- **Enterprise-Grade UI**: Pure modern CSS3 with custom variables, dark/light theme switching, and responsive design.

---

*EduPulse CRM — Built for modern educational institutions.*
