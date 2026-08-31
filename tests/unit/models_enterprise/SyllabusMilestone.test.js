'use strict';

/**
 * ============================================================================
 * Unit Test Suite for Model: SyllabusMilestone
 * ============================================================================
 */

const assert = require('assert');
const SyllabusMilestone = require('../../../src/models/enterprise/SyllabusMilestone');

describe('Enterprise Model: SyllabusMilestone', () => {
  it('should instantiate SyllabusMilestone with default properties', () => {
    const instance = new SyllabusMilestone();
    assert.strictEqual(instance.constructor.tableName, 'syllabusmilestone_records');
  });

  it('should fail validation when required fields are missing', () => {
    const instance = new SyllabusMilestone();
    const val = instance.validate();
    assert.strictEqual(val.isValid, false);
    assert(val.errors.length > 0);
  });

  it('should pass validation when required fields are supplied', () => {
    const payload = {
      id: 'TEST_VAL_001',
      course_id: 'TEST_VAL_002',
      module_id: 'TEST_VAL_003'
    };
    const instance = new SyllabusMilestone(payload);
    const val = instance.validate();
    assert.strictEqual(val.isValid, true);
  });

  it('should serialize to formatted JSON properly', () => {
    const instance = new SyllabusMilestone({ id: 'REC_001' });
    const json = instance.toFormattedJSON();
    assert.strictEqual(json._entityType, 'SyllabusMilestone');
  });
});
