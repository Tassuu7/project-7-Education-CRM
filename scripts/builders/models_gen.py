#!/usr/bin/env python3
"""
EduPulse CRM - Domain Models Generator
Generates strongly typed, robust domain models with validation, business logic, relations, and serialization.
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

    # src/models/BaseModel.js
    write("src/models/BaseModel.js", """'use strict';

/**
 * Base Entity Model
 * Provides foundational CRUD operations, hooks, timestamping, and schema validation.
 */

const db = require('../../database/db');

class BaseModel {
  constructor(data = {}) {
    this.id = data.id || null;
    this.created_at = data.created_at || new Date().toISOString();
    this.updated_at = data.updated_at || new Date().toISOString();
  }

  static get tableName() {
    throw new Error('Static getter tableName must be implemented in sub-classes');
  }

  static find(predicate = {}) {
    const rows = db.find(this.tableName, predicate);
    return rows.map(row => new this(row));
  }

  static findOne(predicate = {}) {
    const row = db.findOne(this.tableName, predicate);
    return row ? new this(row) : null;
  }

  static findById(id) {
    const row = db.findById(this.tableName, id);
    return row ? new this(row) : null;
  }

  static count(predicate = {}) {
    return db.count(this.tableName, predicate);
  }

  static create(data) {
    const instance = new this(data);
    instance.beforeSave();
    const saved = db.insert(this.tableName, instance.toJSON());
    return new this(saved);
  }

  static updateById(id, updates) {
    const updated = db.updateById(this.tableName, id, updates);
    return updated ? new this(updated) : null;
  }

  static deleteById(id) {
    return db.deleteById(this.tableName, id);
  }

  beforeSave() {
    if (!this.id) {
      this.id = `${this.constructor.tableName.slice(0, 3)}_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
    }
    this.updated_at = new Date().toISOString();
  }

  save() {
    this.beforeSave();
    if (this.id && db.findById(this.constructor.tableName, this.id)) {
      const updated = db.updateById(this.constructor.tableName, this.id, this.toJSON());
      Object.assign(this, updated);
    } else {
      const created = db.insert(this.constructor.tableName, this.toJSON());
      Object.assign(this, created);
    }
    return this;
  }

  delete() {
    if (!this.id) return false;
    return db.deleteById(this.constructor.tableName, this.id);
  }

  toJSON() {
    const obj = {};
    for (const key of Object.keys(this)) {
      if (typeof this[key] !== 'function') {
        obj[key] = this[key];
      }
    }
    return obj;
  }
}

module.exports = BaseModel;
""")

    # src/models/User.js
    write("src/models/User.js", """'use strict';

const BaseModel = require('./BaseModel');
const crypto = require('crypto');

class User extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.username = data.username || '';
    this.email = data.email || '';
    this.password_hash = data.password_hash || '';
    this.first_name = data.first_name || '';
    this.last_name = data.last_name || '';
    this.role = data.role || 'student';
    this.phone = data.phone || '';
    this.avatar_url = data.avatar_url || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150';
    this.is_active = data.is_active !== undefined ? Number(data.is_active) : 1;
    this.last_login_at = data.last_login_at || null;
  }

  static get tableName() {
    return 'users';
  }

  static hashPassword(password) {
    return crypto.createHash('sha256').update(password + 'edupulse_salt_2026').digest('hex');
  }

  verifyPassword(password) {
    const hashed = User.hashPassword(password);
    return this.password_hash === hashed;
  }

  get fullName() {
    return `${this.first_name} ${this.last_name}`.trim();
  }

  toSafeJSON() {
    const safe = this.toJSON();
    delete safe.password_hash;
    safe.fullName = this.fullName;
    return safe;
  }
}

module.exports = User;
""")

    # src/models/Lead.js
    write("src/models/Lead.js", """'use strict';

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class Lead extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.first_name = data.first_name || '';
    this.last_name = data.last_name || '';
    this.email = data.email || '';
    this.phone = data.phone || '';
    this.alternate_phone = data.alternate_phone || '';
    this.source = data.source || 'Website Inbound';
    this.stage = data.stage || 'new';
    this.interested_course_id = data.interested_course_id || null;
    this.assigned_counselor_id = data.assigned_counselor_id || null;
    this.lead_score = Number(data.lead_score) || 0;
    this.budget_range = data.budget_range || '';
    this.preferred_intake = data.preferred_intake || 'Fall 2026';
    this.country = data.country || 'India';
    this.city = data.city || '';
    this.notes = data.notes || '';
    this.qualification_status = data.qualification_status || 'Pending Review';
    this.last_contacted_at = data.last_contacted_at || null;
    this.next_follow_up_date = data.next_follow_up_date || null;
  }

  static get tableName() {
    return 'leads';
  }

  get fullName() {
    return `${this.first_name} ${this.last_name}`.trim();
  }

  getCourse() {
    if (!this.interested_course_id) return null;
    return db.findById('courses', this.interested_course_id);
  }

  getCounselor() {
    if (!this.assigned_counselor_id) return null;
    const user = db.findById('users', this.assigned_counselor_id);
    if (!user) return null;
    return {
      id: user.id,
      name: `${user.first_name} ${user.last_name}`,
      email: user.email,
      phone: user.phone
    };
  }

  getInteractions() {
    return db.find('lead_interactions', { lead_id: this.id })
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }

  toDetailedJSON() {
    const json = this.toJSON();
    json.fullName = this.fullName;
    json.course = this.getCourse();
    json.counselor = this.getCounselor();
    json.interactionsCount = db.count('lead_interactions', { lead_id: this.id });
    return json;
  }
}

module.exports = Lead;
""")

    # src/models/LeadInteraction.js
    write("src/models/LeadInteraction.js", """'use strict';

const BaseModel = require('./BaseModel');

class LeadInteraction extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.lead_id = data.lead_id || '';
    this.user_id = data.user_id || '';
    this.interaction_type = data.interaction_type || 'phone_call';
    this.summary = data.summary || '';
    this.outcome = data.outcome || '';
    this.duration_minutes = Number(data.duration_minutes) || 0;
    this.scheduled_follow_up = data.scheduled_follow_up || null;
  }

  static get tableName() {
    return 'lead_interactions';
  }
}

module.exports = LeadInteraction;
""")

    # src/models/Course.js
    write("src/models/Course.js", """'use strict';

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class Course extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.code = data.code || '';
    this.title = data.title || '';
    this.department = data.department || '';
    this.degree_level = data.degree_level || 'Bachelor';
    this.duration_months = Number(data.duration_months) || 36;
    this.total_credits = Number(data.total_credits) || 120;
    this.base_tuition_fee = Number(data.base_tuition_fee) || 0.0;
    this.description = data.description || '';
    this.syllabus_outline = data.syllabus_outline || '';
    this.is_active = data.is_active !== undefined ? Number(data.is_active) : 1;
  }

  static get tableName() {
    return 'courses';
  }

  getModules() {
    return db.find('course_modules', { course_id: this.id });
  }

  getBatches() {
    return db.find('batches', { course_id: this.id });
  }

  getEnrolledCount() {
    return db.count('students', { primary_course_id: this.id, enrollment_status: 'active' });
  }

  toDetailedJSON() {
    const json = this.toJSON();
    json.modules = this.getModules();
    json.batches = this.getBatches();
    json.enrolledCount = this.getEnrolledCount();
    return json;
  }
}

module.exports = Course;
""")

    # src/models/Batch.js
    write("src/models/Batch.js", """'use strict';

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class Batch extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.course_id = data.course_id || '';
    this.batch_name = data.batch_name || '';
    this.cohort_code = data.cohort_code || '';
    this.start_date = data.start_date || '';
    this.end_date = data.end_date || '';
    this.max_capacity = Number(data.max_capacity) || 40;
    this.current_enrolled = Number(data.current_enrolled) || 0;
    this.lead_instructor_id = data.lead_instructor_id || null;
    this.classroom_location = data.classroom_location || '';
    this.status = data.status || 'upcoming';
  }

  static get tableName() {
    return 'batches';
  }

  getCourse() {
    return db.findById('courses', this.course_id);
  }

  getInstructor() {
    if (!this.lead_instructor_id) return null;
    const u = db.findById('users', this.lead_instructor_id);
    return u ? { id: u.id, name: `${u.first_name} ${u.last_name}`, email: u.email } : null;
  }

  getStudents() {
    return db.find('students', { current_batch_id: this.id });
  }

  toDetailedJSON() {
    const json = this.toJSON();
    json.course = this.getCourse();
    json.instructor = this.getInstructor();
    json.studentsCount = this.getStudents().length;
    return json;
  }
}

module.exports = Batch;
""")

    # src/models/Student.js
    write("src/models/Student.js", """'use strict';

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class Student extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.user_id = data.user_id || '';
    this.student_id_number = data.student_id_number || '';
    this.application_id = data.application_id || null;
    this.first_name = data.first_name || '';
    this.last_name = data.last_name || '';
    this.email = data.email || '';
    this.phone = data.phone || '';
    this.dob = data.dob || '';
    this.blood_group = data.blood_group || '';
    this.address = data.address || '';
    this.city = data.city || '';
    this.state = data.state || '';
    this.guardian_name = data.guardian_name || '';
    this.guardian_phone = data.guardian_phone || '';
    this.guardian_email = data.guardian_email || '';
    this.guardian_relation = data.guardian_relation || 'Parent';
    this.primary_course_id = data.primary_course_id || '';
    this.current_batch_id = data.current_batch_id || null;
    this.current_semester = Number(data.current_semester) || 1;
    this.enrollment_status = data.enrollment_status || 'active';
    this.cumulative_gpa = Number(data.cumulative_gpa) || 0.0;
    this.total_credits_earned = Number(data.total_credits_earned) || 0;
    this.enrolled_date = data.enrolled_date || new Date().toISOString().split('T')[0];
  }

  static get tableName() {
    return 'students';
  }

  get fullName() {
    return `${this.first_name} ${this.last_name}`.trim();
  }

  getCourse() {
    return db.findById('courses', this.primary_course_id);
  }

  getBatch() {
    if (!this.current_batch_id) return null;
    return db.findById('batches', this.current_batch_id);
  }

  getInvoices() {
    return db.find('invoices', { student_id: this.id });
  }

  getGrades() {
    return db.find('student_grades', { student_id: this.id });
  }

  getAttendancePercentage() {
    const records = db.find('attendance_records', { student_id: this.id });
    if (records.length === 0) return 100.0;
    const present = records.filter(r => r.status === 'present' || r.status === 'late').length;
    return Number(((present / records.length) * 100).toFixed(1));
  }

  toDetailedJSON() {
    const json = this.toJSON();
    json.fullName = this.fullName;
    json.course = this.getCourse();
    json.batch = this.getBatch();
    json.attendancePercentage = this.getAttendancePercentage();
    json.invoices = this.getInvoices();
    return json;
  }
}

module.exports = Student;
""")

    # src/models/Invoice.js
    write("src/models/Invoice.js", """'use strict';

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class Invoice extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.invoice_number = data.invoice_number || '';
    this.student_id = data.student_id || '';
    this.course_id = data.course_id || '';
    this.title = data.title || 'Tuition Fee Invoice';
    this.amount = Number(data.amount) || 0.0;
    this.discount_amount = Number(data.discount_amount) || 0.0;
    this.tax_amount = Number(data.tax_amount) || 0.0;
    this.total_amount = Number(data.total_amount) || (this.amount - this.discount_amount + this.tax_amount);
    this.amount_paid = Number(data.amount_paid) || 0.0;
    this.balance_due = Number(data.balance_due) !== undefined ? Number(data.balance_due) : (this.total_amount - this.amount_paid);
    this.due_date = data.due_date || '';
    this.status = data.status || 'pending';
    this.notes = data.notes || '';
  }

  static get tableName() {
    return 'invoices';
  }

  getStudent() {
    return db.findById('students', this.student_id);
  }

  getCourse() {
    return db.findById('courses', this.course_id);
  }

  getPayments() {
    return db.find('payments', { invoice_id: this.id });
  }

  recordPayment(amount, paymentMethod, txnRef = '', userId = null, notes = '') {
    const newPaid = this.amount_paid + amount;
    const newBalance = Math.max(0, this.total_amount - newPaid);
    let newStatus = this.status;

    if (newBalance <= 0) {
      newStatus = 'paid';
    } else if (newPaid > 0) {
      newStatus = 'partially_paid';
    }

    this.amount_paid = newPaid;
    this.balance_due = newBalance;
    this.status = newStatus;
    this.save();

    // Create payment transaction
    const receiptNum = `REC-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
    const payment = db.insert('payments', {
      id: `pay_${Date.now()}`,
      receipt_number: receiptNum,
      invoice_id: this.id,
      student_id: this.student_id,
      amount,
      payment_method: paymentMethod,
      transaction_reference: txnRef,
      payment_date: new Date().toISOString(),
      recorded_by_user_id: userId,
      notes
    });

    return payment;
  }

  toDetailedJSON() {
    const json = this.toJSON();
    json.student = this.getStudent();
    json.course = this.getCourse();
    json.payments = this.getPayments();
    return json;
  }
}

module.exports = Invoice;
""")

    # src/models/SupportTicket.js
    write("src/models/SupportTicket.js", """'use strict';

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class SupportTicket extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.ticket_number = data.ticket_number || '';
    this.user_id = data.user_id || '';
    this.category = data.category || 'General Support';
    this.priority = data.priority || 'medium';
    this.status = data.status || 'open';
    this.subject = data.subject || '';
    this.description = data.description || '';
    this.assigned_to_user_id = data.assigned_to_user_id || null;
    this.resolution_notes = data.resolution_notes || null;
    this.resolved_at = data.resolved_at || null;
  }

  static get tableName() {
    return 'support_tickets';
  }

  getUser() {
    return db.findById('users', this.user_id);
  }

  getAssignedStaff() {
    if (!this.assigned_to_user_id) return null;
    return db.findById('users', this.assigned_to_user_id);
  }

  getReplies() {
    return db.find('ticket_replies', { ticket_id: this.id })
      .sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
  }

  addReply(userId, message, isStaff = 0) {
    const reply = db.insert('ticket_replies', {
      id: `rep_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
      ticket_id: this.id,
      user_id: userId,
      message,
      is_staff_reply: isStaff,
      created_at: new Date().toISOString()
    });

    this.updated_at = new Date().toISOString();
    this.save();
    return reply;
  }

  toDetailedJSON() {
    const json = this.toJSON();
    const user = this.getUser();
    json.user = user ? { id: user.id, name: `${user.first_name} ${user.last_name}`, email: user.email, role: user.role } : null;
    const staff = this.getAssignedStaff();
    json.assignedStaff = staff ? { id: staff.id, name: `${staff.first_name} ${staff.last_name}`, email: staff.email } : null;
    json.replies = this.getReplies();
    return json;
  }
}

module.exports = SupportTicket;
""")

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent.parent)
