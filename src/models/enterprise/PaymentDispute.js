'use strict';

/**
 * ============================================================================
 * EduPulse Enterprise Entity Model: PaymentDispute
 * Description: Financial invoice payment chargeback and disputes
 * ============================================================================
 */

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class PaymentDispute extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.id = data.id !== undefined ? data.id : null;
    this.payment_id = data.payment_id !== undefined ? data.payment_id : null;
    this.reason_code = data.reason_code !== undefined ? data.reason_code : null;
    this.dispute_amount = data.dispute_amount !== undefined ? data.dispute_amount : null;
    this.resolution_notes = data.resolution_notes !== undefined ? data.resolution_notes : null;
    this.status = data.status !== undefined ? data.status : null;
  }

  static get tableName() {
    return 'paymentdispute_records';
  }

  validate() {
    const errors = [];
    if (this.id === null || this.id === undefined || this.id === '') {
      errors.push('Field \'id\' is required on PaymentDispute.');
    }
    if (this.payment_id === null || this.payment_id === undefined || this.payment_id === '') {
      errors.push('Field \'payment_id\' is required on PaymentDispute.');
    }
    if (this.reason_code === null || this.reason_code === undefined || this.reason_code === '') {
      errors.push('Field \'reason_code\' is required on PaymentDispute.');
    }
    return {
      isValid: errors.length === 0,
      errors
    };
  }

  toFormattedJSON() {
    return {
      ...this.toJSON(),
      _entityType: 'PaymentDispute',
      _description: 'Financial invoice payment chargeback and disputes',
      _formattedTimestamp: new Date(this.updated_at).toLocaleString()
    };
  }
}

module.exports = PaymentDispute;
