'use strict';

/**
 * ============================================================================
 * Unit Test Suite for Model: AlumniCareerPlacement
 * ============================================================================
 */

const assert = require('assert');
const AlumniCareerPlacement = require('../../../src/models/enterprise/AlumniCareerPlacement');

describe('Enterprise Model: AlumniCareerPlacement', () => {
  it('should instantiate AlumniCareerPlacement with default properties', () => {
    const instance = new AlumniCareerPlacement();
    assert.strictEqual(instance.constructor.tableName, 'alumnicareerplacement_records');
  });

  it('should fail validation when required fields are missing', () => {
    const instance = new AlumniCareerPlacement();
    const val = instance.validate();
    assert.strictEqual(val.isValid, false);
    assert(val.errors.length > 0);
  });

  it('should pass validation when required fields are supplied', () => {
    const payload = {
      id: 'TEST_VAL_001',
      student_id: 'TEST_VAL_002',
      company_name: 'TEST_VAL_003'
    };
    const instance = new AlumniCareerPlacement(payload);
    const val = instance.validate();
    assert.strictEqual(val.isValid, true);
  });

  it('should serialize to formatted JSON properly', () => {
    const instance = new AlumniCareerPlacement({ id: 'REC_001' });
    const json = instance.toFormattedJSON();
    assert.strictEqual(json._entityType, 'AlumniCareerPlacement');
  });
});
