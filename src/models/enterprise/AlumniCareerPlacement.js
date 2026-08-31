'use strict';

/**
 * ============================================================================
 * EduPulse Enterprise Entity Model: AlumniCareerPlacement
 * Description: Alumni employment and career records
 * ============================================================================
 */

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class AlumniCareerPlacement extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id !== undefined ? data.id : null;
    this.student_id = data.student_id !== undefined ? data.student_id : null;
    this.company_name = data.company_name !== undefined ? data.company_name : null;
    this.job_title = data.job_title !== undefined ? data.job_title : null;
    this.annual_package = data.annual_package !== undefined ? data.annual_package : null;
    this.placed_date = data.placed_date !== undefined ? data.placed_date : null;
    this.status = data.status !== undefined ? data.status : null;
  }

  static get tableName() {
    return 'alumnicareerplacement_records';
  }

  validate() {
    const errors = [];
    if (this.id === null || this.id === undefined || this.id === '') {
      errors.push('Field \'id\' is required on AlumniCareerPlacement.');
    }
    if (this.student_id === null || this.student_id === undefined || this.student_id === '') {
      errors.push('Field \'student_id\' is required on AlumniCareerPlacement.');
    }
    if (this.company_name === null || this.company_name === undefined || this.company_name === '') {
      errors.push('Field \'company_name\' is required on AlumniCareerPlacement.');
    }
    return {
      isValid: errors.length === 0,
      errors
    };
  }

  toFormattedJSON() {
    return {
      ...this.toJSON(),
      _entityType: 'AlumniCareerPlacement',
      _description: 'Alumni employment and career records',
      _formattedTimestamp: new Date(this.updated_at).toLocaleString()
    };
  }
}

module.exports = AlumniCareerPlacement;
