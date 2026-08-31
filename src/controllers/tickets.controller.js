'use strict';

const SupportTicket = require('../models/SupportTicket');
const db = require('../../database/db');
const auditService = require('../services/audit.service');

class TicketsController {
  async getAll(req, res) {
    try {
      const { status, category, priority } = req.query;
      let tickets = SupportTicket.find();

      if (status && status !== 'all') {
        tickets = tickets.filter(t => t.status === status);
      }
      if (category && category !== 'all') {
        tickets = tickets.filter(t => t.category === category);
      }
      if (priority && priority !== 'all') {
        tickets = tickets.filter(t => t.priority === priority);
      }

      const detailed = tickets.map(t => t.toDetailedJSON());
      return res.status(200).json({ success: true, count: detailed.length, data: detailed });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async getById(req, res) {
    try {
      const ticket = SupportTicket.findById(req.params.id);
      if (!ticket) return res.status(404).json({ success: false, message: 'Support ticket not found.' });
      return res.status(200).json({ success: true, data: ticket.toDetailedJSON() });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async create(req, res) {
    try {
      const { category, priority, subject, description } = req.body;
      if (!category || !subject || !description) {
        return res.status(400).json({ success: false, message: 'Category, subject, and description are required.' });
      }

      const ticketNumber = `TKT-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
      const newTicket = SupportTicket.create({
        ticket_number: ticketNumber,
        user_id: req.user?.id || 'usr_student_01',
        category,
        priority: priority || 'medium',
        status: 'open',
        subject,
        description
      });

      auditService.logAction(req.user?.id, 'CREATE_TICKET', 'support_tickets', newTicket.id, { ticketNumber }, req.ip);

      return res.status(201).json({ success: true, message: 'Support ticket submitted.', data: newTicket.toDetailedJSON() });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }

  async addReply(req, res) {
    try {
      const ticket = SupportTicket.findById(req.params.id);
      if (!ticket) return res.status(404).json({ success: false, message: 'Support ticket not found.' });

      const { message, is_staff_reply } = req.body;
      if (!message) return res.status(400).json({ success: false, message: 'Message content is required.' });

      const reply = ticket.addReply(req.user?.id || 'usr_admin_01', message, is_staff_reply ? 1 : 0);
      return res.status(201).json({ success: true, message: 'Reply sent.', data: reply });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }

  async updateStatus(req, res) {
    try {
      const ticket = SupportTicket.findById(req.params.id);
      if (!ticket) return res.status(404).json({ success: false, message: 'Support ticket not found.' });

      const { status, resolution_notes } = req.body;
      ticket.status = status || ticket.status;
      if (resolution_notes) ticket.resolution_notes = resolution_notes;
      if (status === 'resolved' || status === 'closed') ticket.resolved_at = new Date().toISOString();
      ticket.save();

      auditService.logAction(req.user?.id, 'UPDATE_TICKET_STATUS', 'support_tickets', ticket.id, { status }, req.ip);

      return res.status(200).json({ success: true, message: 'Ticket status updated.', data: ticket.toDetailedJSON() });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }
}

module.exports = new TicketsController();
