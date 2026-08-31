'use strict';

/**
 * ============================================================================
 * EduPulse Enterprise Entity Model: HostelRoomAllocation
 * Description: Campus residential accommodation tracking
 * ============================================================================
 */

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class HostelRoomAllocation extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id !== undefined ? data.id : null;
    this.student_id = data.student_id !== undefined ? data.student_id : null;
    this.building_code = data.building_code !== undefined ? data.building_code : null;
    this.room_number = data.room_number !== undefined ? data.room_number : null;
    this.bed_identifier = data.bed_identifier !== undefined ? data.bed_identifier : null;
    this.check_in_date = data.check_in_date !== undefined ? data.check_in_date : null;
    this.status = data.status !== undefined ? data.status : null;
  }

  static get tableName() {
    return 'hostelroomallocation_records';
  }

  validate() {
    const errors = [];
    if (this.id === null || this.id === undefined || this.id === '') {
      errors.push('Field \'id\' is required on HostelRoomAllocation.');
    }
    if (this.student_id === null || this.student_id === undefined || this.student_id === '') {
      errors.push('Field \'student_id\' is required on HostelRoomAllocation.');
    }
    if (this.building_code === null || this.building_code === undefined || this.building_code === '') {
      errors.push('Field \'building_code\' is required on HostelRoomAllocation.');
    }
    return {
      isValid: errors.length === 0,
      errors
    };
  }

  toFormattedJSON() {
    return {
      ...this.toJSON(),
      _entityType: 'HostelRoomAllocation',
      _description: 'Campus residential accommodation tracking',
      _formattedTimestamp: new Date(this.updated_at).toLocaleString()
    };
  }
}

module.exports = HostelRoomAllocation;
