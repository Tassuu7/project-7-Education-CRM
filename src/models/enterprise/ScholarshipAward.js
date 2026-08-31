'use strict';

/**
 * ============================================================================
 * EduPulse Enterprise Entity Model: ScholarshipAward
 * Description: Scholarships, bursaries and grant awards
 * ============================================================================
 */

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class ScholarshipAward extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id !== undefined ? data.id : null;
    this.student_id = data.student_id !== undefined ? data.student_id : null;
    this.scholarship_name = data.scholarship_name !== undefined ? data.scholarship_name : null;
    this.award_amount = data.award_amount !== undefined ? data.award_amount : null;
    this.disbursement_term = data.disbursement_term !== undefined ? data.disbursement_term : null;
    this.criteria_verified = data.criteria_verified !== undefined ? data.criteria_verified : null;
    this.status = data.status !== undefined ? data.status : null;
  }

  static get tableName() {
    return 'scholarshipaward_records';
  }

  validate() {
    const errors = [];
    if (this.id === null || this.id === undefined || this.id === '') {
      errors.push('Field \'id\' is required on ScholarshipAward.');
    }
    if (this.student_id === null || this.student_id === undefined || this.student_id === '') {
      errors.push('Field \'student_id\' is required on ScholarshipAward.');
    }
    if (this.scholarship_name === null || this.scholarship_name === undefined || this.scholarship_name === '') {
      errors.push('Field \'scholarship_name\' is required on ScholarshipAward.');
    }
    return {
      isValid: errors.length === 0,
      errors
    };
  }

  toFormattedJSON() {
    return {
      ...this.toJSON(),
      _entityType: 'ScholarshipAward',
      _description: 'Scholarships, bursaries and grant awards',
      _formattedTimestamp: new Date(this.updated_at).toLocaleString()
    };
  }
}

module.exports = ScholarshipAward;
