'use strict';

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
