'use strict';

/**
 * ============================================================================
 * EduPulse Enterprise Entity Model: DisciplinaryCase
 * Description: Campus conduct and honor code reviews
 * ============================================================================
 */

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class DisciplinaryCase extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id !== undefined ? data.id : null;
    this.student_id = data.student_id !== undefined ? data.student_id : null;
    this.incident_date = data.incident_date !== undefined ? data.incident_date : null;
    this.description = data.description !== undefined ? data.description : null;
    this.action_taken = data.action_taken !== undefined ? data.action_taken : null;
    this.hearing_date = data.hearing_date !== undefined ? data.hearing_date : null;
    this.status = data.status !== undefined ? data.status : null;
  }

  static get tableName() {
    return 'disciplinarycase_records';
  }

  validate() {
    const errors = [];
    if (this.id === null || this.id === undefined || this.id === '') {
      errors.push('Field \'id\' is required on DisciplinaryCase.');
    }
    if (this.student_id === null || this.student_id === undefined || this.student_id === '') {
      errors.push('Field \'student_id\' is required on DisciplinaryCase.');
    }
    if (this.incident_date === null || this.incident_date === undefined || this.incident_date === '') {
      errors.push('Field \'incident_date\' is required on DisciplinaryCase.');
    }
    return {
      isValid: errors.length === 0,
      errors
    };
  }

  toFormattedJSON() {
    return {
      ...this.toJSON(),
      _entityType: 'DisciplinaryCase',
      _description: 'Campus conduct and honor code reviews',
      _formattedTimestamp: new Date(this.updated_at).toLocaleString()
    };
  }
}

module.exports = DisciplinaryCase;
