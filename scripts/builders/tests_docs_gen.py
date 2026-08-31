#!/usr/bin/env python3
"""
EduPulse CRM - Automated Tests, Documentation, and Utilities Generator
"""

import os
from pathlib import Path

def generate(base_dir):
    def write(rel, content):
        p = Path(base_dir) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {rel}")

    # tests/run-tests.js
    write("tests/run-tests.js", """'use strict';

/**
 * EduPulse CRM - Master Automated Test Runner
 */

const db = require('../database/db');
const { runSeed } = require('../database/seeders/seed-all');
const authService = require('../src/services/auth.service');
const leadScoringService = require('../src/services/lead-scoring.service');
const admissionsService = require('../src/services/admissions.service');
const billingService = require('../src/services/billing.service');
const academicService = require('../src/services/academic.service');
const exportService = require('../src/services/export.service');
const { hasPermission, ROLES, PERMISSIONS } = require('../config/permissions');
const Validator = require('../src/utils/validator.util');
const Formatter = require('../src/utils/formatter.util');

let totalTests = 0;
let passedTests = 0;
let failedTests = 0;

function assert(condition, testName) {
  totalTests++;
  if (condition) {
    passedTests++;
    console.log(`  [PASS] ${testName}`);
  } else {
    failedTests++;
    console.error(`  [FAIL] ${testName}`);
  }
}

async function runAllTests() {
  console.log('================================================================');
  console.log('           EDUPULSE CRM - AUTOMATED TEST SUITE EXECUTION        ');
  console.log('================================================================\\n');

  // Seed database
  await runSeed();

  console.log('1. Authentication & Token Security Tests:');
  const loginRes = await authService.login('superadmin', 'admin123');
  assert(loginRes && loginRes.token, 'Super admin login returns session token');
  assert(loginRes.user.role === 'super_admin', 'Authenticated user has correct role');

  const tokenPayload = authService.verifyToken(loginRes.token);
  assert(tokenPayload && tokenPayload.userId === 'usr_superadmin_01', 'Token verification extracts valid payload');

  let failedLogin = false;
  try {
    await authService.login('superadmin', 'wrong_pass');
  } catch {
    failedLogin = true;
  }
  assert(failedLogin, 'Invalid credentials properly rejected with error');

  console.log('\\n2. Role-Based Access Control (RBAC) Tests:');
  assert(hasPermission(ROLES.SUPER_ADMIN, PERMISSIONS.LEADS_CREATE), 'Super Admin has LEADS_CREATE permission');
  assert(hasPermission(ROLES.COUNSELOR, PERMISSIONS.LEADS_EDIT), 'Counselor has LEADS_EDIT permission');
  assert(!hasPermission(ROLES.STUDENT, PERMISSIONS.FINANCE_INVOICE_CREATE), 'Student forbidden from creating invoices');

  console.log('\\n3. Lead Scoring & Pipeline Tests:');
  const testLead = {
    source: 'Alumni Referral',
    budget_range: '$15,000+',
    stage: 'qualified',
    email: 'test@example.com',
    phone: '+1234567890',
    city: 'San Francisco'
  };
  const interactions = [
    { interaction_type: 'campus_visit' },
    { interaction_type: 'phone_call' }
  ];
  const score = leadScoringService.calculateScore(testLead, interactions);
  assert(score >= 75, `High-intent lead calculates score >= 75 (Calculated: ${score})`);
  assert(leadScoringService.getTemperature(score) === 'Hot', 'High score evaluates to Hot temperature');

  console.log('\\n4. Admissions & Student Enrollment Flow:');
  const testApp = db.insert('student_applications', {
    id: `app_test_${Date.now()}`,
    course_id: 'crs_cs_01',
    first_name: 'Test',
    last_name: 'Applicant',
    email: `test.app.${Date.now()}@example.com`,
    phone: '+1-555-9988',
    dob: '2005-01-01',
    status: 'submitted'
  });
  const enrollRes = await admissionsService.approveAndEnroll(testApp.id, 'usr_admin_01');
  assert(enrollRes.student && enrollRes.student.student_id_number, 'Applicant enrolled and student ID assigned');
  assert(enrollRes.invoice && enrollRes.invoice.total_amount > 0, 'Tuition invoice automatically generated on enrollment');

  console.log('\\n5. Finance & Payment Processing Tests:');
  const financeOverview = await billingService.getFinancialOverview();
  assert(financeOverview.totalBilled > 0, 'Billing service computes total billed tuition');
  assert(financeOverview.totalCollected > 0, 'Billing service computes collected revenue');

  const paymentRes = await billingService.recordPayment('inv_2026_002', {
    amount: 500,
    payment_method: 'bank_transfer'
  }, 'usr_finance_01');
  assert(paymentRes.payment && paymentRes.payment.amount === 500, 'Payment recorded and credited to invoice balance');

  console.log('\\n6. Academic Attendance & GPA Recalculation:');
  const attRes = await academicService.recordAttendanceSession({
    batch_id: 'batch_cs_2026_a',
    course_id: 'crs_cs_01',
    session_date: '2026-08-31'
  }, [
    { student_id: 'stu_001', status: 'present' }
  ], 'usr_instructor_01');
  assert(attRes.session && attRes.recordsCount === 1, 'Attendance session logged with student records');

  const gradeRes = await academicService.gradeStudent('grd_item_001', 'stu_001', 95, 'usr_instructor_01');
  assert(gradeRes.letter_grade === 'A+' && gradeRes.gpa_points === 4.0, 'Grading scale maps 95% to A+ and 4.0 GPA');

  console.log('\\n7. Utilities & Data Export Tests:');
  assert(Validator.isEmail('student@edupulse.edu'), 'Validator accurately validates valid emails');
  assert(!Validator.isEmail('invalid-email'), 'Validator rejects malformed emails');
  assert(Formatter.formatCurrency(12500) === '$12,500.00', 'Formatter outputs formatted currency string');

  const csv = exportService.exportTableToCSV('leads');
  assert(typeof csv === 'string' && csv.includes('first_name'), 'Export service produces standard CSV string');

  console.log('\\n================================================================');
  console.log(`TEST SUMMARY: ${passedTests} / ${totalTests} Passed (${failedTests} Failed)`);
  console.log('================================================================');

  if (failedTests > 0) {
    process.exit(1);
  }
}

runAllTests().catch(err => {
  console.error('[Test Error]', err);
  process.exit(1);
});
""")

    # scripts/package-project.py
    write("scripts/package-project.py", """#!/usr/bin/env python3
# EduPulse CRM - Project Packaging & Zip Archive Utility
# Creates a standalone, clean zip distribution of the codebase.

import os
import sys
import shutil
import zipfile
from pathlib import Path

def create_zip():
    base_dir = Path(__file__).resolve().parent.parent
    zip_filename = base_dir / "EduPulse-Education-CRM.zip"

    exclude_dirs = {'.git', 'node_modules', '__pycache__', '.pytest_cache', 'dist', 'build'}
    exclude_files = {'EduPulse-Education-CRM.zip', '.DS_Store', 'Thumbs.db'}

    print(f"Creating project zip archive: {zip_filename.name} ...")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
            for file in files:
                if file in exclude_files or file.endswith('.pyc'):
                    continue
                file_path = Path(root) / file
                arcname = file_path.relative_to(base_dir)
                zipf.write(file_path, arcname)

    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"[SUCCESS] Zip package created successfully: {zip_filename} ({size_mb:.2f} MB)")

if __name__ == '__main__':
    create_zip()
""")

    # scripts/verify-health.js
    write("scripts/verify-health.js", """'use strict';

const http = require('http');

const req = http.get('http://localhost:4050/api/v1/health', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log('[Health Check] Status Code:', res.statusCode);
    console.log('[Health Check] Response:', data);
    process.exit(res.statusCode === 200 ? 0 : 1);
  });
});

req.on('error', (err) => {
  console.error('[Health Check Error] Server is not reachable:', err.message);
  process.exit(1);
});
""")

    # README.md
    write("README.md", """# EduPulse Enterprise Education CRM & Student Lifecycle Management Platform

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
""")

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent.parent)
