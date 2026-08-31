'use strict';

/**
 * ============================================================================
 * Unit Test Suite for Model: ApplicantInterview
 * ============================================================================
 */

const assert = require('assert');
const ApplicantInterview = require('../../../src/models/enterprise/ApplicantInterview');

describe('Enterprise Model: ApplicantInterview', () => {
  it('should instantiate ApplicantInterview with default properties', () => {
    const instance = new ApplicantInterview();
    assert.strictEqual(instance.constructor.tableName, 'applicantinterview_records');
  });

  it('should fail validation when required fields are missing', () => {
    const instance = new ApplicantInterview();
    const val = instance.validate();
    assert.strictEqual(val.isValid, false);
    assert(val.errors.length > 0);
  });

  it('should pass validation when required fields are supplied', () => {
    const payload = {
      id: 'TEST_VAL_001',
      application_id: 'TEST_VAL_002',
      interviewer_id: 'TEST_VAL_003'
    };
    const instance = new ApplicantInterview(payload);
    const val = instance.validate();
    assert.strictEqual(val.isValid, true);
  });

  it('should serialize to formatted JSON properly', () => {
    const instance = new ApplicantInterview({ id: 'REC_001' });
    const json = instance.toFormattedJSON();
    assert.strictEqual(json._entityType, 'ApplicantInterview');
  });
});
