'use strict';

/**
 * ============================================================================
 * EduPulse Multi-Currency Tuition Billing & Gateway Settlement Engine
 * Feature Branch: feature/finance-billing
 * ============================================================================
 */

const db = require('../../database/db');
const Formatter = require('../utils/formatter.util');

class TuitionPaymentGatewayService {
  constructor() {
    this.supportedGateways = ['stripe', 'razorpay', 'paypal', 'bank_wire', 'upi_instant'];
    this.exchangeRates = {
      USD: 1.0,
      EUR: 0.92,
      GBP: 0.79,
      INR: 83.25,
      AED: 3.67
    };
  }

  processGatewayTransaction(invoiceId, paymentPayload) {
    const invoice = db.findById('invoices', invoiceId);
    if (!invoice) throw new Error('Invoice not found for gateway capture.');

    const amount = Number(paymentPayload.amount);
    const currency = paymentPayload.currency || 'USD';
    const rate = this.exchangeRates[currency] || 1.0;
    const baseAmountUSD = amount / rate;

    const receiptNumber = `REC-${new Date().getFullYear()}-${Math.floor(10000 + Math.random() * 90000)}`;
    const transactionId = `GATEWAY_${paymentPayload.gateway || 'STRIPE'}_${Date.now()}`;

    const paymentRecord = db.insert('payments', {
      id: `pay_gw_${Date.now()}`,
      receipt_number: receiptNumber,
      invoice_id: invoiceId,
      student_id: invoice.student_id,
      amount: Number(baseAmountUSD.toFixed(2)),
      payment_method: paymentPayload.gateway || 'stripe_online',
      transaction_reference: transactionId,
      payment_date: new Date().toISOString(),
      notes: `Captured via ${paymentPayload.gateway} in ${currency} (FX Rate: ${rate})`
    });

    const newAmountPaid = Number(invoice.amount_paid || 0) + Number(baseAmountUSD.toFixed(2));
    const newBalanceDue = Math.max(0, Number(invoice.total_amount) - newAmountPaid);
    const newStatus = newBalanceDue <= 0 ? 'paid' : 'partially_paid';

    db.updateById('invoices', invoiceId, {
      amount_paid: newAmountPaid,
      balance_due: newBalanceDue,
      status: newStatus
    });

    return {
      success: true,
      transactionId,
      receiptNumber,
      amountCaptured: baseAmountUSD,
      invoiceStatus: newStatus,
      timestamp: new Date().toISOString()
    };
  }
}

module.exports = new TuitionPaymentGatewayService();
