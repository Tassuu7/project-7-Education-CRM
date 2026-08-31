'use strict';

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
  console.log('================================================================\n');

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

  console.log('\n2. Role-Based Access Control (RBAC) Tests:');
  assert(hasPermission(ROLES.SUPER_ADMIN, PERMISSIONS.LEADS_CREATE), 'Super Admin has LEADS_CREATE permission');
  assert(hasPermission(ROLES.COUNSELOR, PERMISSIONS.LEADS_EDIT), 'Counselor has LEADS_EDIT permission');
  assert(!hasPermission(ROLES.STUDENT, PERMISSIONS.FINANCE_INVOICE_CREATE), 'Student forbidden from creating invoices');

  console.log('\n3. Lead Scoring & Pipeline Tests:');
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

  console.log('\n4. Admissions & Student Enrollment Flow:');
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

  console.log('\n5. Finance & Payment Processing Tests:');
  const financeOverview = await billingService.getFinancialOverview();
  assert(financeOverview.totalBilled > 0, 'Billing service computes total billed tuition');
  assert(financeOverview.totalCollected > 0, 'Billing service computes collected revenue');

  const paymentRes = await billingService.recordPayment('inv_2026_002', {
    amount: 500,
    payment_method: 'bank_transfer'
  }, 'usr_finance_01');
  assert(paymentRes.payment && paymentRes.payment.amount === 500, 'Payment recorded and credited to invoice balance');

  console.log('\n6. Academic Attendance & GPA Recalculation:');
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

  console.log('\n7. Utilities & Data Export Tests:');
  assert(Validator.isEmail('student@edupulse.edu'), 'Validator accurately validates valid emails');
  assert(!Validator.isEmail('invalid-email'), 'Validator rejects malformed emails');
  assert(Formatter.formatCurrency(12500) === '$12,500.00', 'Formatter outputs formatted currency string');

  const csv = exportService.exportTableToCSV('leads');
  assert(typeof csv === 'string' && csv.includes('first_name'), 'Export service produces standard CSV string');

  console.log('\n================================================================');
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
