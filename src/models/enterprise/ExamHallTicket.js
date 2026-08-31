'use strict';

/**
 * ============================================================================
 * EduPulse Enterprise Entity Model: ExamHallTicket
 * Description: Examination hall tickets and seated desk numbers
 * ============================================================================
 */

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class ExamHallTicket extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id !== undefined ? data.id : null;
    this.student_id = data.student_id !== undefined ? data.student_id : null;
    this.exam_id = data.exam_id !== undefined ? data.exam_id : null;
    this.hall_number = data.hall_number !== undefined ? data.hall_number : null;
    this.seat_code = data.seat_code !== undefined ? data.seat_code : null;
    this.verification_qr = data.verification_qr !== undefined ? data.verification_qr : null;
    this.status = data.status !== undefined ? data.status : null;
  }

  static get tableName() {
    return 'examhallticket_records';
  }

  validate() {
    const errors = [];
    if (this.id === null || this.id === undefined || this.id === '') {
      errors.push('Field \'id\' is required on ExamHallTicket.');
    }
    if (this.student_id === null || this.student_id === undefined || this.student_id === '') {
      errors.push('Field \'student_id\' is required on ExamHallTicket.');
    }
    if (this.exam_id === null || this.exam_id === undefined || this.exam_id === '') {
      errors.push('Field \'exam_id\' is required on ExamHallTicket.');
    }
    return {
      isValid: errors.length === 0,
      errors
    };
  }

  toFormattedJSON() {
    return {
      ...this.toJSON(),
      _entityType: 'ExamHallTicket',
      _description: 'Examination hall tickets and seated desk numbers',
      _formattedTimestamp: new Date(this.updated_at).toLocaleString()
    };
  }
}

module.exports = ExamHallTicket;
