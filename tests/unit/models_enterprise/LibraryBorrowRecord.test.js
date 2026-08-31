'use strict';

/**
 * ============================================================================
 * Unit Test Suite for Model: LibraryBorrowRecord
 * ============================================================================
 */

const assert = require('assert');
const LibraryBorrowRecord = require('../../../src/models/enterprise/LibraryBorrowRecord');

describe('Enterprise Model: LibraryBorrowRecord', () => {
  it('should instantiate LibraryBorrowRecord with default properties', () => {
    const instance = new LibraryBorrowRecord();
    assert.strictEqual(instance.constructor.tableName, 'libraryborrowrecord_records');
  });

  it('should fail validation when required fields are missing', () => {
    const instance = new LibraryBorrowRecord();
    const val = instance.validate();
    assert.strictEqual(val.isValid, false);
    assert(val.errors.length > 0);
  });

  it('should pass validation when required fields are supplied', () => {
    const payload = {
      id: 'TEST_VAL_001',
      student_id: 'TEST_VAL_002',
      isbn: 'TEST_VAL_003'
    };
    const instance = new LibraryBorrowRecord(payload);
    const val = instance.validate();
    assert.strictEqual(val.isValid, true);
  });

  it('should serialize to formatted JSON properly', () => {
    const instance = new LibraryBorrowRecord({ id: 'REC_001' });
    const json = instance.toFormattedJSON();
    assert.strictEqual(json._entityType, 'LibraryBorrowRecord');
  });
});
