'use strict';

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class SupportTicket extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.ticket_number = data.ticket_number || '';
    this.user_id = data.user_id || '';
    this.category = data.category || 'General Support';
    this.priority = data.priority || 'medium';
    this.status = data.status || 'open';
    this.subject = data.subject || '';
    this.description = data.description || '';
    this.assigned_to_user_id = data.assigned_to_user_id || null;
    this.resolution_notes = data.resolution_notes || null;
    this.resolved_at = data.resolved_at || null;
  }

  static get tableName() {
    return 'support_tickets';
  }

  getUser() {
    return db.findById('users', this.user_id);
  }

  getAssignedStaff() {
    if (!this.assigned_to_user_id) return null;
    return db.findById('users', this.assigned_to_user_id);
  }

  getReplies() {
    return db.find('ticket_replies', { ticket_id: this.id })
      .sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
  }

  addReply(userId, message, isStaff = 0) {
    const reply = db.insert('ticket_replies', {
      id: `rep_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
      ticket_id: this.id,
      user_id: userId,
      message,
      is_staff_reply: isStaff,
      created_at: new Date().toISOString()
    });

    this.updated_at = new Date().toISOString();
    this.save();
    return reply;
  }

  toDetailedJSON() {
    const json = this.toJSON();
    const user = this.getUser();
    json.user = user ? { id: user.id, name: `${user.first_name} ${user.last_name}`, email: user.email, role: user.role } : null;
    const staff = this.getAssignedStaff();
    json.assignedStaff = staff ? { id: staff.id, name: `${staff.first_name} ${staff.last_name}`, email: staff.email } : null;
    json.replies = this.getReplies();
    return json;
  }
}

module.exports = SupportTicket;
