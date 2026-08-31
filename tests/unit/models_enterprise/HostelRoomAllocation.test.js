'use strict';

/**
 * ============================================================================
 * Unit Test Suite for Model: HostelRoomAllocation
 * ============================================================================
 */

const assert = require('assert');
const HostelRoomAllocation = require('../../../src/models/enterprise/HostelRoomAllocation');

describe('Enterprise Model: HostelRoomAllocation', () => {
  it('should instantiate HostelRoomAllocation with default properties', () => {
    const instance = new HostelRoomAllocation();
    assert.strictEqual(instance.constructor.tableName, 'hostelroomallocation_records');
  });

  it('should fail validation when required fields are missing', () => {
    const instance = new HostelRoomAllocation();
    const val = instance.validate();
    assert.strictEqual(val.isValid, false);
    assert(val.errors.length > 0);
  });

  it('should pass validation when required fields are supplied', () => {
    const payload = {
      id: 'TEST_VAL_001',
      student_id: 'TEST_VAL_002',
      building_code: 'TEST_VAL_003'
    };
    const instance = new HostelRoomAllocation(payload);
    const val = instance.validate();
    assert.strictEqual(val.isValid, true);
  });

  it('should serialize to formatted JSON properly', () => {
    const instance = new HostelRoomAllocation({ id: 'REC_001' });
    const json = instance.toFormattedJSON();
    assert.strictEqual(json._entityType, 'HostelRoomAllocation');
  });
});
