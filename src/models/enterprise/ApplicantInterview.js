'use strict';

/**
 * ============================================================================
 * EduPulse Enterprise Entity Model: ApplicantInterview
 * Description: Interviews scheduled for applicant evaluations
 * ============================================================================
 */

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class ApplicantInterview extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id !== undefined ? data.id : null;
    this.application_id = data.application_id !== undefined ? data.application_id : null;
    this.interviewer_id = data.interviewer_id !== undefined ? data.interviewer_id : null;
    this.scheduled_time = data.scheduled_time !== undefined ? data.scheduled_time : null;
    this.feedback_score = data.feedback_score !== undefined ? data.feedback_score : null;
    this.recommendation = data.recommendation !== undefined ? data.recommendation : null;
    this.status = data.status !== undefined ? data.status : null;
  }

  static get tableName() {
    return 'applicantinterview_records';
  }

  validate() {
    const errors = [];
    if (this.id === null || this.id === undefined || this.id === '') {
      errors.push('Field \'id\' is required on ApplicantInterview.');
    }
    if (this.application_id === null || this.application_id === undefined || this.application_id === '') {
      errors.push('Field \'application_id\' is required on ApplicantInterview.');
    }
    if (this.interviewer_id === null || this.interviewer_id === undefined || this.interviewer_id === '') {
      errors.push('Field \'interviewer_id\' is required on ApplicantInterview.');
    }
    return {
      isValid: errors.length === 0,
      errors
    };
  }

  toFormattedJSON() {
    return {
      ...this.toJSON(),
      _entityType: 'ApplicantInterview',
      _description: 'Interviews scheduled for applicant evaluations',
      _formattedTimestamp: new Date(this.updated_at).toLocaleString()
    };
  }
}

module.exports = ApplicantInterview;
