'use strict';

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
