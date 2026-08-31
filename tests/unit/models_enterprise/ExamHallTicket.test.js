'use strict';

/**
 * ============================================================================
 * Unit Test Suite for Model: ExamHallTicket
 * ============================================================================
 */

const assert = require('assert');
const ExamHallTicket = require('../../../src/models/enterprise/ExamHallTicket');

describe('Enterprise Model: ExamHallTicket', () => {
  it('should instantiate ExamHallTicket with default properties', () => {
    const instance = new ExamHallTicket();
    assert.strictEqual(instance.constructor.tableName, 'examhallticket_records');
  });

  it('should fail validation when required fields are missing', () => {
    const instance = new ExamHallTicket();
    const val = instance.validate();
    assert.strictEqual(val.isValid, false);
    assert(val.errors.length > 0);
  });

  it('should pass validation when required fields are supplied', () => {
    const payload = {
      id: 'TEST_VAL_001',
      student_id: 'TEST_VAL_002',
      exam_id: 'TEST_VAL_003'
    };
    const instance = new ExamHallTicket(payload);
    const val = instance.validate();
    assert.strictEqual(val.isValid, true);
  });

  it('should serialize to formatted JSON properly', () => {
    const instance = new ExamHallTicket({ id: 'REC_001' });
    const json = instance.toFormattedJSON();
    assert.strictEqual(json._entityType, 'ExamHallTicket');
  });
});
