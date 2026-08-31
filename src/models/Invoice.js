'use strict';

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class Invoice extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.invoice_number = data.invoice_number || '';
    this.student_id = data.student_id || '';
    this.course_id = data.course_id || '';
    this.title = data.title || 'Tuition Fee Invoice';
    this.amount = Number(data.amount) || 0.0;
    this.discount_amount = Number(data.discount_amount) || 0.0;
    this.tax_amount = Number(data.tax_amount) || 0.0;
    this.total_amount = Number(data.total_amount) || (this.amount - this.discount_amount + this.tax_amount);
    this.amount_paid = Number(data.amount_paid) || 0.0;
    this.balance_due = Number(data.balance_due) !== undefined ? Number(data.balance_due) : (this.total_amount - this.amount_paid);
    this.due_date = data.due_date || '';
    this.status = data.status || 'pending';
    this.notes = data.notes || '';
  }

  static get tableName() {
    return 'invoices';
  }

  getStudent() {
    return db.findById('students', this.student_id);
  }

  getCourse() {
    return db.findById('courses', this.course_id);
  }

  getPayments() {
    return db.find('payments', { invoice_id: this.id });
  }

  recordPayment(amount, paymentMethod, txnRef = '', userId = null, notes = '') {
    const newPaid = this.amount_paid + amount;
    const newBalance = Math.max(0, this.total_amount - newPaid);
    let newStatus = this.status;

    if (newBalance <= 0) {
      newStatus = 'paid';
    } else if (newPaid > 0) {
      newStatus = 'partially_paid';
    }

    this.amount_paid = newPaid;
    this.balance_due = newBalance;
    this.status = newStatus;
    this.save();

    // Create payment transaction
    const receiptNum = `REC-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
    const payment = db.insert('payments', {
      id: `pay_${Date.now()}`,
      receipt_number: receiptNum,
      invoice_id: this.id,
      student_id: this.student_id,
      amount,
      payment_method: paymentMethod,
      transaction_reference: txnRef,
      payment_date: new Date().toISOString(),
      recorded_by_user_id: userId,
      notes
    });

    return payment;
  }

  toDetailedJSON() {
    const json = this.toJSON();
    json.student = this.getStudent();
    json.course = this.getCourse();
    json.payments = this.getPayments();
    return json;
  }
}

module.exports = Invoice;
