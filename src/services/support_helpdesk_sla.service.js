'use strict';

/**
 * ============================================================================
 * EduPulse Real-Time Helpdesk SLA & Priority Escalation Dispatcher
 * Feature Branch: feature/helpdesk-ticketing
 * ============================================================================
 */

const db = require('../../database/db');

class SupportHelpdeskSlaService {
  constructor() {
    this.slaThresholdHours = {
      critical: 4,
      high: 12,
      medium: 24,
      low: 48
    };
  }

  evaluateTicketSlaStatus(ticketId) {
    const ticket = db.findById('support_tickets', ticketId);
    if (!ticket) throw new Error('Ticket not found.');

    const createdTime = new Date(ticket.created_at).getTime();
    const now = Date.now();
    const elapsedHours = (now - createdTime) / (1000 * 60 * 60);
    const maxAllowedHours = this.slaThresholdHours[ticket.priority] || 24;

    const remainingHours = Math.max(0, maxAllowedHours - elapsedHours);
    const isBreached = elapsedHours > maxAllowedHours && ticket.status !== 'resolved' && ticket.status !== 'closed';

    let escalationLevel = 'NORMAL';
    if (isBreached) {
      escalationLevel = 'EXECUTIVE_ESCALATION';
    } else if (remainingHours < 2) {
      escalationLevel = 'URGENT_WARNING';
    }

    return {
      ticketId: ticket.id,
      ticketNumber: ticket.ticket_number,
      priority: ticket.priority,
      elapsedHours: Number(elapsedHours.toFixed(1)),
      maxAllowedHours,
      remainingHours: Number(remainingHours.toFixed(1)),
      isBreached,
      escalationLevel
    };
  }
}

module.exports = new SupportHelpdeskSlaService();
