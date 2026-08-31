'use strict';

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
