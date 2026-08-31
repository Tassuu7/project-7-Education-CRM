'use strict';

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class Lead extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.first_name = data.first_name || '';
    this.last_name = data.last_name || '';
    this.email = data.email || '';
    this.phone = data.phone || '';
    this.alternate_phone = data.alternate_phone || '';
    this.source = data.source || 'Website Inbound';
    this.stage = data.stage || 'new';
    this.interested_course_id = data.interested_course_id || null;
    this.assigned_counselor_id = data.assigned_counselor_id || null;
    this.lead_score = Number(data.lead_score) || 0;
    this.budget_range = data.budget_range || '';
    this.preferred_intake = data.preferred_intake || 'Fall 2026';
    this.country = data.country || 'India';
    this.city = data.city || '';
    this.notes = data.notes || '';
    this.qualification_status = data.qualification_status || 'Pending Review';
    this.last_contacted_at = data.last_contacted_at || null;
    this.next_follow_up_date = data.next_follow_up_date || null;
  }

  static get tableName() {
    return 'leads';
  }

  get fullName() {
    return `${this.first_name} ${this.last_name}`.trim();
  }

  getCourse() {
    if (!this.interested_course_id) return null;
    return db.findById('courses', this.interested_course_id);
  }

  getCounselor() {
    if (!this.assigned_counselor_id) return null;
    const user = db.findById('users', this.assigned_counselor_id);
    if (!user) return null;
    return {
      id: user.id,
      name: `${user.first_name} ${user.last_name}`,
      email: user.email,
      phone: user.phone
    };
  }

  getInteractions() {
    return db.find('lead_interactions', { lead_id: this.id })
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }

  toDetailedJSON() {
    const json = this.toJSON();
    json.fullName = this.fullName;
    json.course = this.getCourse();
    json.counselor = this.getCounselor();
    json.interactionsCount = db.count('lead_interactions', { lead_id: this.id });
    return json;
  }
}

module.exports = Lead;
