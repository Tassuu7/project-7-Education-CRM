'use strict';

const BaseModel = require('./BaseModel');

class LeadInteraction extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.lead_id = data.lead_id || '';
    this.user_id = data.user_id || '';
    this.interaction_type = data.interaction_type || 'phone_call';
    this.summary = data.summary || '';
    this.outcome = data.outcome || '';
    this.duration_minutes = Number(data.duration_minutes) || 0;
    this.scheduled_follow_up = data.scheduled_follow_up || null;
  }

  static get tableName() {
    return 'lead_interactions';
  }
}

module.exports = LeadInteraction;
