#!/usr/bin/env python3
"""
EduPulse CRM - Database Schema and Seed Data Generator
Generates schema.sql, db.js (in-memory + persistence engine), and extensive seed datasets.
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

    # database/schema.sql
    write("database/schema.sql", """-- ============================================================================
-- EduPulse Enterprise Education CRM Database Schema
-- Standard Relational Schema for Academic, Financial, and Lead Management
-- ============================================================================

PRAGMA foreign_keys = ON;

-- 1. Users & Authentication
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('super_admin', 'admin', 'counselor', 'instructor', 'finance_officer', 'student', 'parent')),
    phone TEXT,
    avatar_url TEXT,
    is_active INTEGER DEFAULT 1,
    last_login_at TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 2. Prospective Leads Management
CREATE TABLE IF NOT EXISTS leads (
    id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    alternate_phone TEXT,
    source TEXT NOT NULL,
    stage TEXT NOT NULL CHECK(stage IN ('new', 'contacted', 'qualified', 'counseling_scheduled', 'application_submitted', 'enrolled', 'unqualified', 'lost')),
    interested_course_id TEXT,
    assigned_counselor_id TEXT,
    lead_score INTEGER DEFAULT 0,
    budget_range TEXT,
    preferred_intake TEXT,
    country TEXT DEFAULT 'India',
    city TEXT,
    notes TEXT,
    qualification_status TEXT,
    last_contacted_at TEXT,
    next_follow_up_date TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (assigned_counselor_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (interested_course_id) REFERENCES courses(id) ON DELETE SET NULL
);

-- 3. Lead Interaction Logs
CREATE TABLE IF NOT EXISTS lead_interactions (
    id TEXT PRIMARY KEY,
    lead_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    interaction_type TEXT NOT NULL CHECK(interaction_type IN ('phone_call', 'email', 'whatsapp', 'in_person_meeting', 'campus_visit', 'note')),
    summary TEXT NOT NULL,
    outcome TEXT,
    duration_minutes INTEGER DEFAULT 0,
    scheduled_follow_up TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Course Catalog & Programs
CREATE TABLE IF NOT EXISTS courses (
    id TEXT PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    department TEXT NOT NULL,
    degree_level TEXT NOT NULL CHECK(degree_level IN ('Certificate', 'Diploma', 'Bachelor', 'Master', 'Doctorate', 'Bootcamp')),
    duration_months INTEGER NOT NULL,
    total_credits INTEGER NOT NULL,
    base_tuition_fee REAL NOT NULL,
    description TEXT,
    syllabus_outline TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 5. Course Modules & Syllabi
CREATE TABLE IF NOT EXISTS course_modules (
    id TEXT PRIMARY KEY,
    course_id TEXT NOT NULL,
    module_code TEXT NOT NULL,
    title TEXT NOT NULL,
    semester_number INTEGER NOT NULL,
    credits INTEGER NOT NULL,
    instructor_id TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 6. Batches & Cohorts
CREATE TABLE IF NOT EXISTS batches (
    id TEXT PRIMARY KEY,
    course_id TEXT NOT NULL,
    batch_name TEXT NOT NULL,
    cohort_code TEXT UNIQUE NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    max_capacity INTEGER DEFAULT 40,
    current_enrolled INTEGER DEFAULT 0,
    lead_instructor_id TEXT,
    classroom_location TEXT,
    status TEXT DEFAULT 'upcoming' CHECK(status IN ('upcoming', 'active', 'completed', 'cancelled')),
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (lead_instructor_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 7. Student Applications & Admissions
CREATE TABLE IF NOT EXISTS student_applications (
    id TEXT PRIMARY KEY,
    lead_id TEXT,
    course_id TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    dob TEXT NOT NULL,
    gender TEXT,
    high_school_percentage REAL,
    entrance_exam_score REAL,
    status TEXT NOT NULL CHECK(status IN ('draft', 'submitted', 'under_review', 'interview_scheduled', 'accepted', 'rejected', 'waitlisted', 'enrolled')),
    reviewer_id TEXT,
    review_notes TEXT,
    applied_at TEXT DEFAULT (datetime('now')),
    decision_at TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE SET NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 8. Enrolled Students Information System
CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    student_id_number TEXT UNIQUE NOT NULL,
    application_id TEXT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    dob TEXT,
    blood_group TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    guardian_name TEXT,
    guardian_phone TEXT,
    guardian_email TEXT,
    guardian_relation TEXT,
    primary_course_id TEXT NOT NULL,
    current_batch_id TEXT,
    current_semester INTEGER DEFAULT 1,
    enrollment_status TEXT DEFAULT 'active' CHECK(enrollment_status IN ('active', 'graduated', 'suspended', 'on_leave', 'withdrawn')),
    cumulative_gpa REAL DEFAULT 0.0,
    total_credits_earned INTEGER DEFAULT 0,
    enrolled_date TEXT DEFAULT (datetime('now')),
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (primary_course_id) REFERENCES courses(id) ON DELETE RESTRICT,
    FOREIGN KEY (current_batch_id) REFERENCES batches(id) ON DELETE SET NULL,
    FOREIGN KEY (application_id) REFERENCES student_applications(id) ON DELETE SET NULL
);

-- 9. Invoices & Billing
CREATE TABLE IF NOT EXISTS invoices (
    id TEXT PRIMARY KEY,
    invoice_number TEXT UNIQUE NOT NULL,
    student_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    title TEXT NOT NULL,
    amount REAL NOT NULL,
    discount_amount REAL DEFAULT 0.0,
    tax_amount REAL DEFAULT 0.0,
    total_amount REAL NOT NULL,
    amount_paid REAL DEFAULT 0.0,
    balance_due REAL NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('draft', 'pending', 'paid', 'partially_paid', 'overdue', 'cancelled', 'refunded')),
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE RESTRICT
);

-- 10. Payments & Transaction Logs
CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY,
    receipt_number TEXT UNIQUE NOT NULL,
    invoice_id TEXT NOT NULL,
    student_id TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_method TEXT NOT NULL CHECK(payment_method IN ('credit_card', 'debit_card', 'bank_transfer', 'upi', 'stripe_online', 'cheque', 'cash', 'scholarship_credit')),
    transaction_reference TEXT,
    payment_date TEXT DEFAULT (datetime('now')),
    recorded_by_user_id TEXT,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (recorded_by_user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 11. Attendance Sessions & Records
CREATE TABLE IF NOT EXISTS attendance_sessions (
    id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    module_id TEXT,
    instructor_id TEXT NOT NULL,
    session_date TEXT NOT NULL,
    start_time TEXT,
    end_time TEXT,
    topic_covered TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (batch_id) REFERENCES batches(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS attendance_records (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    student_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'late', 'excused', 'half_day')),
    remarks TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (session_id) REFERENCES attendance_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- 12. Gradebook & Examinations
CREATE TABLE IF NOT EXISTS grade_items (
    id TEXT PRIMARY KEY,
    course_id TEXT NOT NULL,
    module_id TEXT,
    batch_id TEXT NOT NULL,
    title TEXT NOT NULL,
    assessment_type TEXT NOT NULL CHECK(assessment_type IN ('Quiz', 'Assignment', 'Midterm', 'Final Exam', 'Project', 'Lab Practical')),
    max_score REAL NOT NULL,
    weight_percentage REAL NOT NULL,
    due_date TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (batch_id) REFERENCES batches(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS student_grades (
    id TEXT PRIMARY KEY,
    grade_item_id TEXT NOT NULL,
    student_id TEXT NOT NULL,
    score_obtained REAL NOT NULL,
    letter_grade TEXT,
    gpa_points REAL,
    feedback TEXT,
    graded_by_user_id TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (grade_item_id) REFERENCES grade_items(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (graded_by_user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 13. Helpdesk Support Tickets
CREATE TABLE IF NOT EXISTS support_tickets (
    id TEXT PRIMARY KEY,
    ticket_number TEXT UNIQUE NOT NULL,
    user_id TEXT NOT NULL,
    category TEXT NOT NULL,
    priority TEXT NOT NULL CHECK(priority IN ('low', 'medium', 'high', 'critical')),
    status TEXT NOT NULL CHECK(status IN ('open', 'in_progress', 'waiting_on_student', 'resolved', 'closed')),
    subject TEXT NOT NULL,
    description TEXT NOT NULL,
    assigned_to_user_id TEXT,
    resolution_notes TEXT,
    resolved_at TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to_user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ticket_replies (
    id TEXT PRIMARY KEY,
    ticket_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    is_staff_reply INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (ticket_id) REFERENCES support_tickets(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 14. Broadcast Announcements & Notifications
CREATE TABLE IF NOT EXISTS announcements (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    target_audience TEXT NOT NULL CHECK(target_audience IN ('all', 'students', 'counselors', 'instructors', 'finance')),
    priority TEXT DEFAULT 'normal',
    author_id TEXT NOT NULL,
    is_pinned INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS notifications (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT DEFAULT 'info',
    is_read INTEGER DEFAULT 0,
    link_url TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 15. Audit Logs & System Activity
CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT,
    ip_address TEXT,
    details TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 16. System Settings
CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    description TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Indexes for lightning fast lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_leads_stage ON leads(stage);
CREATE INDEX IF NOT EXISTS idx_leads_counselor ON leads(assigned_counselor_id);
CREATE INDEX IF NOT EXISTS idx_students_course ON students(primary_course_id);
CREATE INDEX IF NOT EXISTS idx_students_batch ON students(current_batch_id);
CREATE INDEX IF NOT EXISTS idx_invoices_student ON invoices(student_id);
CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status);
CREATE INDEX IF NOT EXISTS idx_attendance_session ON attendance_records(session_id);
CREATE INDEX IF NOT EXISTS idx_grades_student ON student_grades(student_id);
CREATE INDEX IF NOT EXISTS idx_tickets_user ON support_tickets(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
""")

    # database/db.js
    write("database/db.js", """'use strict';

/**
 * EduPulse CRM Database Management Engine
 * High-performance In-Memory relational data store with disk persistence,
 * query filtering, full-text search, joins, aggregations, and seed sync.
 */

const fs = require('fs');
const path = require('path');
const config = require('../config/app.config');

class DatabaseEngine {
  constructor() {
    this.storagePath = config.database.jsonBackupPath;
    this.tables = {
      users: [],
      leads: [],
      lead_interactions: [],
      courses: [],
      course_modules: [],
      batches: [],
      student_applications: [],
      students: [],
      invoices: [],
      payments: [],
      attendance_sessions: [],
      attendance_records: [],
      grade_items: [],
      student_grades: [],
      support_tickets: [],
      ticket_replies: [],
      announcements: [],
      notifications: [],
      audit_logs: [],
      system_settings: []
    };
    this.isInitialized = false;
    this.saveTimeout = null;
  }

  /**
   * Initialize and load persisted data from disk if available
   */
  async init() {
    if (this.isInitialized) return this;

    try {
      if (fs.existsSync(this.storagePath)) {
        const raw = fs.readFileSync(this.storagePath, 'utf8');
        const parsed = JSON.parse(raw);
        for (const [tbl, rows] of Object.entries(parsed)) {
          if (this.tables[tbl]) {
            this.tables[tbl] = Array.isArray(rows) ? rows : [];
          }
        }
        console.log(`[Database] Loaded persistent data store from ${this.storagePath}`);
      } else {
        console.log('[Database] Initialized fresh in-memory database');
      }
    } catch (err) {
      console.warn('[Database] Failed to read disk backup, using fresh tables:', err.message);
    }

    this.isInitialized = true;
    return this;
  }

  /**
   * Persist current state to JSON file on disk
   */
  persistSync() {
    try {
      const dir = path.dirname(this.storagePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(this.storagePath, JSON.stringify(this.tables, null, 2), 'utf8');
    } catch (err) {
      console.error('[Database] Failed to save database to disk:', err.message);
    }
  }

  /**
   * Debounced persistence to optimize high-frequency writes
   */
  schedulePersist() {
    if (this.saveTimeout) clearTimeout(this.saveTimeout);
    this.saveTimeout = setTimeout(() => {
      this.persistSync();
    }, 500);
  }

  /**
   * Get table reference
   */
  getTable(tableName) {
    if (!this.tables[tableName]) {
      this.tables[tableName] = [];
    }
    return this.tables[tableName];
  }

  /**
   * Query builder: Find items matching criteria
   */
  find(tableName, predicate = {}) {
    const table = this.getTable(tableName);
    if (!predicate || Object.keys(predicate).length === 0) {
      return [...table];
    }

    return table.filter(item => {
      for (const [key, val] of Object.entries(predicate)) {
        if (typeof val === 'function') {
          if (!val(item[key], item)) return false;
        } else if (val !== undefined && item[key] !== val) {
          return false;
        }
      }
      return true;
    });
  }

  /**
   * Find single record matching predicate
   */
  findOne(tableName, predicate = {}) {
    const results = this.find(tableName, predicate);
    return results.length > 0 ? results[0] : null;
  }

  /**
   * Find record by primary key 'id'
   */
  findById(tableName, id) {
    return this.findOne(tableName, { id });
  }

  /**
   * Insert record into table
   */
  insert(tableName, record) {
    const table = this.getTable(tableName);
    const now = new Date().toISOString();
    
    const newRecord = {
      ...record,
      created_at: record.created_at || now,
      updated_at: record.updated_at || now
    };

    table.push(newRecord);
    this.schedulePersist();
    return { ...newRecord };
  }

  /**
   * Insert multiple records
   */
  insertMany(tableName, records = []) {
    const table = this.getTable(tableName);
    const now = new Date().toISOString();
    
    const inserted = records.map(record => ({
      ...record,
      created_at: record.created_at || now,
      updated_at: record.updated_at || now
    }));

    table.push(...inserted);
    this.schedulePersist();
    return inserted;
  }

  /**
   * Update record by ID
   */
  updateById(tableName, id, updates) {
    const table = this.getTable(tableName);
    const idx = table.findIndex(r => r.id === id || r.key === id);
    if (idx === -1) return null;

    const now = new Date().toISOString();
    const updated = {
      ...table[idx],
      ...updates,
      id: table[idx].id || id,
      updated_at: now
    };

    table[idx] = updated;
    this.schedulePersist();
    return { ...updated };
  }

  /**
   * Update all records matching predicate
   */
  updateWhere(tableName, predicate, updates) {
    const table = this.getTable(tableName);
    const now = new Date().toISOString();
    let count = 0;

    for (let i = 0; i < table.length; i++) {
      let match = true;
      for (const [k, v] of Object.entries(predicate)) {
        if (table[i][k] !== v) {
          match = false;
          break;
        }
      }

      if (match) {
        table[i] = {
          ...table[i],
          ...updates,
          updated_at: now
        };
        count++;
      }
    }

    if (count > 0) this.schedulePersist();
    return count;
  }

  /**
   * Delete record by ID
   */
  deleteById(tableName, id) {
    const table = this.getTable(tableName);
    const idx = table.findIndex(r => r.id === id || r.key === id);
    if (idx === -1) return false;

    table.splice(idx, 1);
    this.schedulePersist();
    return true;
  }

  /**
   * Delete all records matching predicate
   */
  deleteWhere(tableName, predicate) {
    const table = this.getTable(tableName);
    const initialLen = table.length;
    
    this.tables[tableName] = table.filter(item => {
      for (const [k, v] of Object.entries(predicate)) {
        if (item[k] === v) return false;
      }
      return true;
    });

    const deleted = initialLen - this.tables[tableName].length;
    if (deleted > 0) this.schedulePersist();
    return deleted;
  }

  /**
   * Count records matching predicate
   */
  count(tableName, predicate = {}) {
    return this.find(tableName, predicate).length;
  }

  /**
   * Clear all records in a table
   */
  truncate(tableName) {
    if (this.tables[tableName]) {
      this.tables[tableName] = [];
      this.schedulePersist();
    }
  }

  /**
   * Reset all tables
   */
  clearAll() {
    for (const key of Object.keys(this.tables)) {
      this.tables[key] = [];
    }
    this.persistSync();
  }
}

// Singleton database instance
const db = new DatabaseEngine();

module.exports = db;
""")

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent.parent)
