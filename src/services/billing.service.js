'use strict';

/**
 * Finance, Invoicing, and Payment Gateway Simulation Service
 */

const db = require('../../database/db');
const Invoice = require('../models/Invoice');

class BillingService {
  /**
   * Create a new invoice
   */
  async createInvoice(invoiceData) {
    const { student_id, course_id, title, amount, discount_amount = 0, tax_amount = 0, due_date, notes } = invoiceData;

    if (!student_id || !course_id || !title || !amount || !due_date) {
      throw new Error('Missing required invoice parameters.');
    }

    const student = db.findById('students', student_id);
    if (!student) throw new Error('Student not found.');

    const invoiceNum = `INV-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
    const total = Number(amount) - Number(discount_amount) + Number(tax_amount);

    const invoice = Invoice.create({
      invoice_number: invoiceNum,
      student_id,
      course_id,
      title,
      amount: Number(amount),
      discount_amount: Number(discount_amount),
      tax_amount: Number(tax_amount),
      total_amount: total,
      amount_paid: 0.0,
      balance_due: total,
      due_date,
      status: 'pending',
      notes: notes || ''
    });

    return invoice.toDetailedJSON();
  }

  /**
   * Process payment for an invoice
   */
  async recordPayment(invoiceId, paymentData, userId) {
    const invoice = Invoice.findById(invoiceId);
    if (!invoice) throw new Error('Invoice not found.');

    const amount = Number(paymentData.amount);
    if (isNaN(amount) || amount <= 0) {
      throw new Error('Payment amount must be greater than zero.');
    }

    if (amount > invoice.balance_due) {
      throw new Error(`Payment amount ($${amount}) exceeds balance due ($${invoice.balance_due}).`);
    }

    const payment = invoice.recordPayment(
      amount,
      paymentData.payment_method || 'bank_transfer',
      paymentData.transaction_reference || `TXN-${Date.now()}`,
      userId,
      paymentData.notes || ''
    );

    return {
      invoice: invoice.toDetailedJSON(),
      payment
    };
  }

  /**
   * Get financial summary statistics
   */
  async getFinancialOverview() {
    const invoices = db.find('invoices');
    const payments = db.find('payments');

    let totalBilled = 0;
    let totalCollected = 0;
    let totalOutstanding = 0;
    let overdueCount = 0;

    const today = new Date().toISOString().split('T')[0];

    invoices.forEach(inv => {
      totalBilled += Number(inv.total_amount || 0);
      totalCollected += Number(inv.amount_paid || 0);
      totalOutstanding += Number(inv.balance_due || 0);

      if (inv.status !== 'paid' && inv.due_date < today) {
        overdueCount++;
      }
    });

    return {
      totalBilled: Number(totalBilled.toFixed(2)),
      totalCollected: Number(totalCollected.toFixed(2)),
      totalOutstanding: Number(totalOutstanding.toFixed(2)),
      collectionRate: totalBilled > 0 ? Number(((totalCollected / totalBilled) * 100).toFixed(1)) : 0,
      totalInvoicesCount: invoices.length,
      totalPaymentsCount: payments.length,
      overdueCount
    };
  }
}

module.exports = new BillingService();
