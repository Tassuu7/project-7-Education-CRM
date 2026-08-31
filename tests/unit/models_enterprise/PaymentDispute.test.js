'use strict';

/**
 * ============================================================================
 * Unit Test Suite for Model: PaymentDispute
 * ============================================================================
 */

const assert = require('assert');
const PaymentDispute = require('../../../src/models/enterprise/PaymentDispute');

describe('Enterprise Model: PaymentDispute', () => {
  it('should instantiate PaymentDispute with default properties', () => {
    const instance = new PaymentDispute();
    assert.strictEqual(instance.constructor.tableName, 'paymentdispute_records');
  });

  it('should fail validation when required fields are missing', () => {
    const instance = new PaymentDispute();
    const val = instance.validate();
    assert.strictEqual(val.isValid, false);
    assert(val.errors.length > 0);
  });

  it('should pass validation when required fields are supplied', () => {
    const payload = {
      id: 'TEST_VAL_001',
      payment_id: 'TEST_VAL_002',
      reason_code: 'TEST_VAL_003'
    };
    const instance = new PaymentDispute(payload);
    const val = instance.validate();
    assert.strictEqual(val.isValid, true);
  });

  it('should serialize to formatted JSON properly', () => {
    const instance = new PaymentDispute({ id: 'REC_001' });
    const json = instance.toFormattedJSON();
    assert.strictEqual(json._entityType, 'PaymentDispute');
  });
});
