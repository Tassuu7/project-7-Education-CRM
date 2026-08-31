'use strict';

/**
 * ============================================================================
 * EduPulse Enterprise Entity Model: LibraryBorrowRecord
 * Description: Campus library book loans and returns
 * ============================================================================
 */

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class LibraryBorrowRecord extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id !== undefined ? data.id : null;
    this.student_id = data.student_id !== undefined ? data.student_id : null;
    this.isbn = data.isbn !== undefined ? data.isbn : null;
    this.book_title = data.book_title !== undefined ? data.book_title : null;
    this.borrow_date = data.borrow_date !== undefined ? data.borrow_date : null;
    this.due_date = data.due_date !== undefined ? data.due_date : null;
    this.fine_amount = data.fine_amount !== undefined ? data.fine_amount : null;
    this.status = data.status !== undefined ? data.status : null;
  }

  static get tableName() {
    return 'libraryborrowrecord_records';
  }

  validate() {
    const errors = [];
    if (this.id === null || this.id === undefined || this.id === '') {
      errors.push('Field \'id\' is required on LibraryBorrowRecord.');
    }
    if (this.student_id === null || this.student_id === undefined || this.student_id === '') {
      errors.push('Field \'student_id\' is required on LibraryBorrowRecord.');
    }
    if (this.isbn === null || this.isbn === undefined || this.isbn === '') {
      errors.push('Field \'isbn\' is required on LibraryBorrowRecord.');
    }
    return {
      isValid: errors.length === 0,
      errors
    };
  }

  toFormattedJSON() {
    return {
      ...this.toJSON(),
      _entityType: 'LibraryBorrowRecord',
      _description: 'Campus library book loans and returns',
      _formattedTimestamp: new Date(this.updated_at).toLocaleString()
    };
  }
}

module.exports = LibraryBorrowRecord;
