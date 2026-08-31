#!/usr/bin/env python3
"""
EduPulse CRM - Business Logic Services Generator
Generates enterprise-grade services with comprehensive business algorithms, validation, and domain logic.
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

    # src/services/auth.service.js
    write("src/services/auth.service.js", """'use strict';

/**
 * Authentication and Session Management Service
 */

const crypto = require('crypto');
const db = require('../../database/db');
const User = require('../models/User');
const config = require('../../config/app.config');

class AuthService {
  /**
   * Authenticate user with credentials
   */
  async login(usernameOrEmail, password) {
    if (!usernameOrEmail || !password) {
      throw new Error('Username/Email and Password are required.');
    }

    const cleanInput = usernameOrEmail.trim().toLowerCase();
    const userRow = db.findOne('users', (val, item) => 
      item.email.toLowerCase() === cleanInput || item.username.toLowerCase() === cleanInput
    );

    if (!userRow) {
      throw new Error('Invalid credentials or account does not exist.');
    }

    const user = new User(userRow);
    if (!user.verifyPassword(password)) {
      throw new Error('Invalid credentials.');
    }

    if (!user.is_active) {
      throw new Error('Account is inactive. Please contact your system administrator.');
    }

    // Update last login timestamp
    user.last_login_at = new Date().toISOString();
    user.save();

    // Generate token payload
    const token = this.generateToken(user);

    return {
      token,
      user: user.toSafeJSON()
    };
  }

  /**
   * Register a new user account
   */
  async register(userData) {
    const { username, email, password, first_name, last_name, role = 'student', phone } = userData;

    if (!username || !email || !password || !first_name || !last_name) {
      throw new Error('All required registration fields must be provided.');
    }

    // Check uniqueness
    const existingEmail = db.findOne('users', { email: email.trim().toLowerCase() });
    if (existingEmail) {
      throw new Error('Email address is already in use.');
    }

    const existingUser = db.findOne('users', { username: username.trim().toLowerCase() });
    if (existingUser) {
      throw new Error('Username is already taken.');
    }

    const passwordHash = User.hashPassword(password);
    const newUser = User.create({
      id: `usr_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
      username: username.trim().toLowerCase(),
      email: email.trim().toLowerCase(),
      password_hash: passwordHash,
      first_name: first_name.trim(),
      last_name: last_name.trim(),
      role,
      phone: phone ? phone.trim() : '',
      is_active: 1,
      last_login_at: new Date().toISOString()
    });

    const token = this.generateToken(newUser);
    return {
      token,
      user: newUser.toSafeJSON()
    };
  }

  /**
   * Generate simple signed token
   */
  generateToken(user) {
    const payload = {
      userId: user.id,
      email: user.email,
      role: user.role,
      issuedAt: Date.now(),
      expiresAt: Date.now() + (config.security.tokenExpirySeconds * 1000)
    };

    const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url');
    const body = Buffer.from(JSON.stringify(payload)).toString('base64url');
    const signature = crypto.createHmac('sha256', config.security.jwtSecret)
      .update(`${header}.${body}`)
      .digest('base64url');

    return `${header}.${body}.${signature}`;
  }

  /**
   * Verify token integrity and expiration
   */
  verifyToken(token) {
    if (!token) return null;
    const parts = token.split('.');
    if (parts.length !== 3) return null;

    const [header, body, signature] = parts;
    const expectedSignature = crypto.createHmac('sha256', config.security.jwtSecret)
      .update(`${header}.${body}`)
      .digest('base64url');

    if (signature !== expectedSignature) {
      return null;
    }

    try {
      const payload = JSON.parse(Buffer.from(body, 'base64url').toString('utf8'));
      if (payload.expiresAt && Date.now() > payload.expiresAt) {
        return null; // Expired
      }
      return payload;
    } catch {
      return null;
    }
  }

  /**
   * Fetch current authenticated user by ID
   */
  async getCurrentUser(userId) {
    const user = User.findById(userId);
    if (!user) return null;
    return user.toSafeJSON();
  }
}

module.exports = new AuthService();
""")

    # src/services/lead-scoring.service.js
    write("src/services/lead-scoring.service.js", """'use strict';

/**
 * Intelligent Multi-Factor Lead Scoring Service
 * Computes propensity score (0-100) based on source, budget, timeline, and interaction frequency.
 */

class LeadScoringService {
  /**
   * Calculate lead score based on domain attributes
   */
  calculateScore(lead, interactions = []) {
    let score = 20; // Base score

    // 1. Source Weighting
    const sourceWeights = {
      'Alumni Referral': 30,
      'Direct Campus Walk-in': 25,
      'Education Fair 2026': 20,
      'Website Inbound': 15,
      'Google Search Ads': 12,
      'Partner Agent': 15,
      'Social Media Campaign': 8,
      'Campus Seminar': 18
    };
    score += (sourceWeights[lead.source] || 10);

    // 2. Budget Qualification
    if (lead.budget_range) {
      if (lead.budget_range.includes('15,000') || lead.budget_range.includes('18,000') || lead.budget_range.includes('+')) {
        score += 15;
      } else if (lead.budget_range.includes('10,000')) {
        score += 10;
      } else {
        score += 5;
      }
    }

    // 3. Stage Progression Bonus
    const stageScores = {
      'new': 0,
      'contacted': 5,
      'qualified': 15,
      'counseling_scheduled': 25,
      'application_submitted': 35,
      'enrolled': 45,
      'unqualified': -20,
      'lost': -30
    };
    score += (stageScores[lead.stage] || 0);

    // 4. Interaction Intensity
    if (interactions && interactions.length > 0) {
      score += Math.min(20, interactions.length * 5);
      
      const hasCampusVisit = interactions.some(i => i.interaction_type === 'campus_visit' || i.interaction_type === 'in_person_meeting');
      if (hasCampusVisit) score += 10;
    }

    // 5. Contact Completeness
    if (lead.email && lead.phone && lead.city) score += 5;
    if (lead.alternate_phone) score += 3;

    // Clamp between 0 and 100
    return Math.max(0, Math.min(100, Math.round(score)));
  }

  /**
   * Determine temperature rating
   */
  getTemperature(score) {
    if (score >= 75) return 'Hot';
    if (score >= 45) return 'Warm';
    return 'Cold';
  }
}

module.exports = new LeadScoringService();
""")

    # src/services/admissions.service.js
    write("src/services/admissions.service.js", """'use strict';

/**
 * Admissions & Student Enrollment Pipeline Service
 */

const db = require('../../database/db');
const Student = require('../models/Student');
const Lead = require('../models/Lead');
const Invoice = require('../models/Invoice');
const User = require('../models/User');

class AdmissionsService {
  /**
   * Process and approve an application, converting to enrolled student
   */
  async approveAndEnroll(applicationId, reviewerId, options = {}) {
    const app = db.findById('student_applications', applicationId);
    if (!app) throw new Error('Application not found.');

    if (app.status === 'enrolled') {
      throw new Error('Candidate is already enrolled.');
    }

    const course = db.findById('courses', app.course_id);
    if (!course) throw new Error('Applied course not found.');

    // 1. Update Application status
    db.updateById('student_applications', applicationId, {
      status: 'enrolled',
      reviewer_id: reviewerId,
      decision_at: new Date().toISOString(),
      review_notes: options.review_notes || 'Approved for enrollment.'
    });

    // 2. Create User Account if not exists
    let studentUser = db.findOne('users', { email: app.email });
    if (!studentUser) {
      const generatedUsername = `stu_${app.first_name.toLowerCase()}_${Math.floor(100 + Math.random() * 900)}`;
      studentUser = User.create({
        username: generatedUsername,
        email: app.email,
        password_hash: User.hashPassword('student123'),
        first_name: app.first_name,
        last_name: app.last_name,
        role: 'student',
        phone: app.phone,
        is_active: 1
      });
    }

    // 3. Create Enrolled Student Record
    const studentCount = db.count('students');
    const studentIdNumber = `STU-${new Date().getFullYear()}-${String(studentCount + 1).padStart(3, '0')}`;
    
    // Find active batch for course
    const batch = db.findOne('batches', { course_id: app.course_id, status: 'active' }) ||
                  db.findOne('batches', { course_id: app.course_id });

    const newStudent = Student.create({
      user_id: studentUser.id,
      student_id_number: studentIdNumber,
      application_id: app.id,
      first_name: app.first_name,
      last_name: app.last_name,
      email: app.email,
      phone: app.phone,
      dob: app.dob,
      primary_course_id: app.course_id,
      current_batch_id: batch ? batch.id : null,
      current_semester: 1,
      enrollment_status: 'active',
      cumulative_gpa: 0.0,
      total_credits_earned: 0,
      enrolled_date: new Date().toISOString().split('T')[0]
    });

    // 4. Generate Initial Semester Tuition Invoice
    const invoiceNum = `INV-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
    const semTuition = course.base_tuition_fee / (course.duration_months / 6);
    const invoice = Invoice.create({
      invoice_number: invoiceNum,
      student_id: newStudent.id,
      course_id: course.id,
      title: `Semester 1 Tuition & Registration Fee - ${course.code}`,
      amount: semTuition,
      discount_amount: options.scholarshipDiscount || 0.0,
      tax_amount: Number((semTuition * 0.05).toFixed(2)),
      due_date: new Date(Date.now() + 14 * 86400000).toISOString().split('T')[0],
      status: 'pending',
      notes: 'Initial admission invoice generated upon enrollment.'
    });

    // 5. Update Lead stage if originated from lead
    if (app.lead_id) {
      db.updateById('leads', app.lead_id, {
        stage: 'enrolled',
        qualification_status: 'Enrolled'
      });
    }

    return {
      application: db.findById('student_applications', applicationId),
      student: newStudent,
      invoice
    };
  }
}

module.exports = new AdmissionsService();
""")

    # src/services/billing.service.js
    write("src/services/billing.service.js", """'use strict';

/**
 * Finance, Invoicing, and Payment Gateway Simulation Service
 */

const db = require('../../database/db');
const Invoice = require('../models/Invoice');

class BillingService {
  /**
   * Create a new invoice
   */
  async createInvoice(invoiceData) {
    const { student_id, course_id, title, amount, discount_amount = 0, tax_amount = 0, due_date, notes } = invoiceData;

    if (!student_id || !course_id || !title || !amount || !due_date) {
      throw new Error('Missing required invoice parameters.');
    }

    const student = db.findById('students', student_id);
    if (!student) throw new Error('Student not found.');

    const invoiceNum = `INV-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
    const total = Number(amount) - Number(discount_amount) + Number(tax_amount);

    const invoice = Invoice.create({
      invoice_number: invoiceNum,
      student_id,
      course_id,
      title,
      amount: Number(amount),
      discount_amount: Number(discount_amount),
      tax_amount: Number(tax_amount),
      total_amount: total,
      amount_paid: 0.0,
      balance_due: total,
      due_date,
      status: 'pending',
      notes: notes || ''
    });

    return invoice.toDetailedJSON();
  }

  /**
   * Process payment for an invoice
   */
  async recordPayment(invoiceId, paymentData, userId) {
    const invoice = Invoice.findById(invoiceId);
    if (!invoice) throw new Error('Invoice not found.');

    const amount = Number(paymentData.amount);
    if (isNaN(amount) || amount <= 0) {
      throw new Error('Payment amount must be greater than zero.');
    }

    if (amount > invoice.balance_due) {
      throw new Error(`Payment amount ($${amount}) exceeds balance due ($${invoice.balance_due}).`);
    }

    const payment = invoice.recordPayment(
      amount,
      paymentData.payment_method || 'bank_transfer',
      paymentData.transaction_reference || `TXN-${Date.now()}`,
      userId,
      paymentData.notes || ''
    );

    return {
      invoice: invoice.toDetailedJSON(),
      payment
    };
  }

  /**
   * Get financial summary statistics
   */
  async getFinancialOverview() {
    const invoices = db.find('invoices');
    const payments = db.find('payments');

    let totalBilled = 0;
    let totalCollected = 0;
    let totalOutstanding = 0;
    let overdueCount = 0;

    const today = new Date().toISOString().split('T')[0];

    invoices.forEach(inv => {
      totalBilled += Number(inv.total_amount || 0);
      totalCollected += Number(inv.amount_paid || 0);
      totalOutstanding += Number(inv.balance_due || 0);

      if (inv.status !== 'paid' && inv.due_date < today) {
        overdueCount++;
      }
    });

    return {
      totalBilled: Number(totalBilled.toFixed(2)),
      totalCollected: Number(totalCollected.toFixed(2)),
      totalOutstanding: Number(totalOutstanding.toFixed(2)),
      collectionRate: totalBilled > 0 ? Number(((totalCollected / totalBilled) * 100).toFixed(1)) : 0,
      totalInvoicesCount: invoices.length,
      totalPaymentsCount: payments.length,
      overdueCount
    };
  }
}

module.exports = new BillingService();
""")

    # src/services/academic.service.js
    write("src/services/academic.service.js", """'use strict';

/**
 * Academic Management, Attendance, and Grading Service
 */

const db = require('../../database/db');

class AcademicService {
  /**
   * Log attendance session and batch records
   */
  async recordAttendanceSession(sessionData, records = [], instructorId) {
    const { batch_id, course_id, module_id, session_date, topic_covered, start_time, end_time } = sessionData;

    if (!batch_id || !course_id || !session_date) {
      throw new Error('Batch, Course, and Session Date are required.');
    }

    const sessionId = `att_sess_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    const session = db.insert('attendance_sessions', {
      id: sessionId,
      batch_id,
      course_id,
      module_id: module_id || null,
      instructor_id: instructorId,
      session_date,
      start_time: start_time || '09:00',
      end_time: end_time || '11:00',
      topic_covered: topic_covered || 'Lecture'
    });

    const insertedRecords = [];
    for (const rec of records) {
      const record = db.insert('attendance_records', {
        id: `att_rec_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
        session_id: sessionId,
        student_id: rec.student_id,
        status: rec.status || 'present',
        remarks: rec.remarks || ''
      });
      insertedRecords.push(record);
    }

    return {
      session,
      recordsCount: insertedRecords.length
    };
  }

  /**
   * Grade a student for an assessment
   */
  async gradeStudent(gradeItemId, studentId, scoreObtained, gradedByUserId, feedback = '') {
    const item = db.findById('grade_items', gradeItemId);
    if (!item) throw new Error('Assessment item not found.');

    const score = Number(scoreObtained);
    if (isNaN(score) || score < 0 || score > item.max_score) {
      throw new Error(`Score must be between 0 and ${item.max_score}.`);
    }

    const percentage = (score / item.max_score) * 100;
    let letterGrade = 'F';
    let gpaPoints = 0.0;

    if (percentage >= 95) { letterGrade = 'A+'; gpaPoints = 4.0; }
    else if (percentage >= 90) { letterGrade = 'A'; gpaPoints = 3.8; }
    else if (percentage >= 85) { letterGrade = 'B+'; gpaPoints = 3.4; }
    else if (percentage >= 80) { letterGrade = 'B'; gpaPoints = 3.0; }
    else if (percentage >= 75) { letterGrade = 'C+'; gpaPoints = 2.5; }
    else if (percentage >= 70) { letterGrade = 'C'; gpaPoints = 2.0; }
    else if (percentage >= 60) { letterGrade = 'D'; gpaPoints = 1.0; }

    const existingGrade = db.findOne('student_grades', { grade_item_id: gradeItemId, student_id: studentId });
    let savedGrade;

    if (existingGrade) {
      savedGrade = db.updateById('student_grades', existingGrade.id, {
        score_obtained: score,
        letter_grade: letterGrade,
        gpa_points: gpaPoints,
        feedback,
        graded_by_user_id: gradedByUserId
      });
    } else {
      savedGrade = db.insert('student_grades', {
        id: `grd_rec_${Date.now()}`,
        grade_item_id: gradeItemId,
        student_id: studentId,
        score_obtained: score,
        letter_grade: letterGrade,
        gpa_points: gpaPoints,
        feedback,
        graded_by_user_id: gradedByUserId
      });
    }

    // Recalculate student cumulative GPA
    this.recalculateStudentGPA(studentId);

    return savedGrade;
  }

  /**
   * Recalculate student cumulative GPA based on all graded items
   */
  recalculateStudentGPA(studentId) {
    const grades = db.find('student_grades', { student_id: studentId });
    if (grades.length === 0) return;

    let totalPoints = 0;
    for (const g of grades) {
      totalPoints += Number(g.gpa_points || 0);
    }
    const newGpa = Number((totalPoints / grades.length).toFixed(2));
    db.updateById('students', studentId, { cumulative_gpa: newGpa });
  }
}

module.exports = new AcademicService();
""")

    # src/services/analytics.service.js
    write("src/services/analytics.service.js", """'use strict';

/**
 * Analytics and Business Intelligence Dashboard Engine
 */

const db = require('../../database/db');

class AnalyticsService {
  /**
   * Generate holistic executive summary dashboard metrics
   */
  async getDashboardSummary() {
    const totalLeads = db.count('leads');
    const newLeads = db.count('leads', { stage: 'new' });
    const enrolledLeads = db.count('leads', { stage: 'enrolled' });
    const totalStudents = db.count('students', { enrollment_status: 'active' });
    const totalCourses = db.count('courses', { is_active: 1 });
    const openTickets = db.count('support_tickets', (val, t) => t.status === 'open' || t.status === 'in_progress');

    // Lead stage funnel breakdown
    const leadsByStage = {
      new: db.count('leads', { stage: 'new' }),
      contacted: db.count('leads', { stage: 'contacted' }),
      qualified: db.count('leads', { stage: 'qualified' }),
      counseling_scheduled: db.count('leads', { stage: 'counseling_scheduled' }),
      application_submitted: db.count('leads', { stage: 'application_submitted' }),
      enrolled: db.count('leads', { stage: 'enrolled' })
    };

    // Revenue metrics
    const invoices = db.find('invoices');
    let totalRevenueCollected = 0;
    let totalRevenuePending = 0;
    invoices.forEach(inv => {
      totalRevenueCollected += Number(inv.amount_paid || 0);
      totalRevenuePending += Number(inv.balance_due || 0);
    });

    // Conversion rate
    const conversionRate = totalLeads > 0 ? Number(((enrolledLeads / totalLeads) * 100).toFixed(1)) : 0;

    return {
      kpis: {
        totalLeads,
        newLeads,
        enrolledLeads,
        totalStudents,
        totalCourses,
        openTickets,
        conversionRate,
        totalRevenueCollected: Number(totalRevenueCollected.toFixed(2)),
        totalRevenuePending: Number(totalRevenuePending.toFixed(2))
      },
      funnel: leadsByStage,
      recentActivity: db.find('lead_interactions').slice(-5).reverse(),
      announcements: db.find('announcements').slice(-3)
    };
  }
}

module.exports = new AnalyticsService();
""")

    # src/services/export.service.js
    write("src/services/export.service.js", """'use strict';

/**
 * Data Export & Reporting Service (CSV / JSON / PDF simulation)
 */

const db = require('../../database/db');

class ExportService {
  /**
   * Export table data as CSV string
   */
  exportTableToCSV(tableName) {
    const rows = db.find(tableName);
    if (!rows || rows.length === 0) {
      return 'No data available for export.';
    }

    const headers = Object.keys(rows[0]);
    const csvLines = [headers.join(',')];

    for (const row of rows) {
      const line = headers.map(header => {
        let val = row[header];
        if (val === null || val === undefined) val = '';
        val = String(val).replace(/"/g, '""');
        if (val.includes(',') || val.includes('\\n') || val.includes('"')) {
          val = `"${val}"`;
        }
        return val;
      });
      csvLines.push(line.join(','));
    }

    return csvLines.join('\\n');
  }

  /**
   * Export table as structured JSON
   */
  exportTableToJSON(tableName) {
    return db.find(tableName);
  }
}

module.exports = new ExportService();
""")

    # src/services/audit.service.js
    write("src/services/audit.service.js", """'use strict';

/**
 * System Security & Audit Logging Service
 */

const db = require('../../database/db');

class AuditService {
  /**
   * Record security or administrative mutation action
   */
  logAction(userId, action, entityType, entityId = null, details = {}, ip = '127.0.0.1') {
    const log = db.insert('audit_logs', {
      id: `aud_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
      user_id: userId || 'system',
      action,
      entity_type: entityType,
      entity_id: entityId,
      ip_address: ip,
      details: typeof details === 'string' ? details : JSON.stringify(details),
      created_at: new Date().toISOString()
    });
    return log;
  }

  /**
   * Get recent audit trails
   */
  getRecentLogs(limit = 50) {
    const logs = db.find('audit_logs');
    return logs.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, limit);
  }
}

module.exports = new AuditService();
""")

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent.parent)
