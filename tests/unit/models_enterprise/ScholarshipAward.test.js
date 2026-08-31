'use strict';

/**
 * ============================================================================
 * Unit Test Suite for Model: ScholarshipAward
 * ============================================================================
 */

const assert = require('assert');
const ScholarshipAward = require('../../../src/models/enterprise/ScholarshipAward');

describe('Enterprise Model: ScholarshipAward', () => {
  it('should instantiate ScholarshipAward with default properties', () => {
    const instance = new ScholarshipAward();
    assert.strictEqual(instance.constructor.tableName, 'scholarshipaward_records');
  });

  it('should fail validation when required fields are missing', () => {
    const instance = new ScholarshipAward();
    const val = instance.validate();
    assert.strictEqual(val.isValid, false);
    assert(val.errors.length > 0);
  });

  it('should pass validation when required fields are supplied', () => {
    const payload = {
      id: 'TEST_VAL_001',
      student_id: 'TEST_VAL_002',
      scholarship_name: 'TEST_VAL_003'
    };
    const instance = new ScholarshipAward(payload);
    const val = instance.validate();
    assert.strictEqual(val.isValid, true);
  });

  it('should serialize to formatted JSON properly', () => {
    const instance = new ScholarshipAward({ id: 'REC_001' });
    const json = instance.toFormattedJSON();
    assert.strictEqual(json._entityType, 'ScholarshipAward');
  });
});
