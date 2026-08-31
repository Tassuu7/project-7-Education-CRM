'use strict';

/**
 * ============================================================================
 * EduPulse Enterprise Entity Model: SyllabusMilestone
 * Description: Curriculum week milestone progress
 * ============================================================================
 */

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class SyllabusMilestone extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id !== undefined ? data.id : null;
    this.course_id = data.course_id !== undefined ? data.course_id : null;
    this.module_id = data.module_id !== undefined ? data.module_id : null;
    this.milestone_title = data.milestone_title !== undefined ? data.milestone_title : null;
    this.week_number = data.week_number !== undefined ? data.week_number : null;
    this.target_completion_date = data.target_completion_date !== undefined ? data.target_completion_date : null;
    this.status = data.status !== undefined ? data.status : null;
  }

  static get tableName() {
    return 'syllabusmilestone_records';
  }

  validate() {
    const errors = [];
    if (this.id === null || this.id === undefined || this.id === '') {
      errors.push('Field \'id\' is required on SyllabusMilestone.');
    }
    if (this.course_id === null || this.course_id === undefined || this.course_id === '') {
      errors.push('Field \'course_id\' is required on SyllabusMilestone.');
    }
    if (this.module_id === null || this.module_id === undefined || this.module_id === '') {
      errors.push('Field \'module_id\' is required on SyllabusMilestone.');
    }
    return {
      isValid: errors.length === 0,
      errors
    };
  }

  toFormattedJSON() {
    return {
      ...this.toJSON(),
      _entityType: 'SyllabusMilestone',
      _description: 'Curriculum week milestone progress',
      _formattedTimestamp: new Date(this.updated_at).toLocaleString()
    };
  }
}

module.exports = SyllabusMilestone;
