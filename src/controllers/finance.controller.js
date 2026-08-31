'use strict';

const db = require('../../database/db');
const Invoice = require('../models/Invoice');
const billingService = require('../services/billing.service');
const auditService = require('../services/audit.service');

class FinanceController {
  async getInvoices(req, res) {
    try {
      const { status, student_id } = req.query;
      let invoices = Invoice.find();

      if (status && status !== 'all') {
        invoices = invoices.filter(i => i.status === status);
      }
      if (student_id) {
        invoices = invoices.filter(i => i.student_id === student_id);
      }

      const detailed = invoices.map(i => i.toDetailedJSON());
      return res.status(200).json({ success: true, count: detailed.length, data: detailed });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async createInvoice(req, res) {
    try {
      const result = await billingService.createInvoice(req.body);
      auditService.logAction(req.user?.id, 'CREATE_INVOICE', 'invoices', result.id, { amount: result.total_amount }, req.ip);
      return res.status(201).json({ success: true, message: 'Invoice generated successfully.', data: result });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }

  async recordPayment(req, res) {
    try {
      const result = await billingService.recordPayment(
        req.params.id,
        req.body,
        req.user?.id || 'usr_finance_01'
      );
      auditService.logAction(req.user?.id, 'RECORD_PAYMENT', 'payments', result.payment.id, { invoiceId: req.params.id, amount: req.body.amount }, req.ip);

      return res.status(200).json({ success: true, message: 'Payment recorded successfully.', data: result });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }

  async getOverview(req, res) {
    try {
      const overview = await billingService.getFinancialOverview();
      return res.status(200).json({ success: true, data: overview });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }
}

module.exports = new FinanceController();
