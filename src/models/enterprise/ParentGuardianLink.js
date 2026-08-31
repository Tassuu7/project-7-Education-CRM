'use strict';

/**
 * ============================================================================
 * EduPulse Enterprise Entity Model: ParentGuardianLink
 * Description: Student to parent relationship links
 * ============================================================================
 */

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class ParentGuardianLink extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id !== undefined ? data.id : null;
    this.student_id = data.student_id !== undefined ? data.student_id : null;
    this.parent_user_id = data.parent_user_id !== undefined ? data.parent_user_id : null;
    this.relationship_type = data.relationship_type !== undefined ? data.relationship_type : null;
    this.is_primary_contact = data.is_primary_contact !== undefined ? data.is_primary_contact : null;
    this.emergency_phone = data.emergency_phone !== undefined ? data.emergency_phone : null;
  }

  static get tableName() {
    return 'parentguardianlink_records';
  }

  validate() {
    const errors = [];
    if (this.id === null || this.id === undefined || this.id === '') {
      errors.push('Field \'id\' is required on ParentGuardianLink.');
    }
    if (this.student_id === null || this.student_id === undefined || this.student_id === '') {
      errors.push('Field \'student_id\' is required on ParentGuardianLink.');
    }
    if (this.parent_user_id === null || this.parent_user_id === undefined || this.parent_user_id === '') {
      errors.push('Field \'parent_user_id\' is required on ParentGuardianLink.');
    }
    return {
      isValid: errors.length === 0,
      errors
    };
  }

  toFormattedJSON() {
    return {
      ...this.toJSON(),
      _entityType: 'ParentGuardianLink',
      _description: 'Student to parent relationship links',
      _formattedTimestamp: new Date(this.updated_at).toLocaleString()
    };
  }
}

module.exports = ParentGuardianLink;
