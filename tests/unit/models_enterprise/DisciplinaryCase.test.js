'use strict';

/**
 * ============================================================================
 * Unit Test Suite for Model: DisciplinaryCase
 * ============================================================================
 */

const assert = require('assert');
const DisciplinaryCase = require('../../../src/models/enterprise/DisciplinaryCase');

describe('Enterprise Model: DisciplinaryCase', () => {
  it('should instantiate DisciplinaryCase with default properties', () => {
    const instance = new DisciplinaryCase();
    assert.strictEqual(instance.constructor.tableName, 'disciplinarycase_records');
  });

  it('should fail validation when required fields are missing', () => {
    const instance = new DisciplinaryCase();
    const val = instance.validate();
    assert.strictEqual(val.isValid, false);
    assert(val.errors.length > 0);
  });

  it('should pass validation when required fields are supplied', () => {
    const payload = {
      id: 'TEST_VAL_001',
      student_id: 'TEST_VAL_002',
      incident_date: 'TEST_VAL_003'
    };
    const instance = new DisciplinaryCase(payload);
    const val = instance.validate();
    assert.strictEqual(val.isValid, true);
  });

  it('should serialize to formatted JSON properly', () => {
    const instance = new DisciplinaryCase({ id: 'REC_001' });
    const json = instance.toFormattedJSON();
    assert.strictEqual(json._entityType, 'DisciplinaryCase');
  });
});
