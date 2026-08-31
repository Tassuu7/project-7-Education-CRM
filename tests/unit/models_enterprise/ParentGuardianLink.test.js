'use strict';

/**
 * ============================================================================
 * Unit Test Suite for Model: ParentGuardianLink
 * ============================================================================
 */

const assert = require('assert');
const ParentGuardianLink = require('../../../src/models/enterprise/ParentGuardianLink');

describe('Enterprise Model: ParentGuardianLink', () => {
  it('should instantiate ParentGuardianLink with default properties', () => {
    const instance = new ParentGuardianLink();
    assert.strictEqual(instance.constructor.tableName, 'parentguardianlink_records');
  });

  it('should fail validation when required fields are missing', () => {
    const instance = new ParentGuardianLink();
    const val = instance.validate();
    assert.strictEqual(val.isValid, false);
    assert(val.errors.length > 0);
  });

  it('should pass validation when required fields are supplied', () => {
    const payload = {
      id: 'TEST_VAL_001',
      student_id: 'TEST_VAL_002',
      parent_user_id: 'TEST_VAL_003'
    };
    const instance = new ParentGuardianLink(payload);
    const val = instance.validate();
    assert.strictEqual(val.isValid, true);
  });

  it('should serialize to formatted JSON properly', () => {
    const instance = new ParentGuardianLink({ id: 'REC_001' });
    const json = instance.toFormattedJSON();
    assert.strictEqual(json._entityType, 'ParentGuardianLink');
  });
});
