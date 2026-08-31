'use strict';

const db = require('../../database/db');
const Lead = require('../models/Lead');
const leadScoringService = require('../services/lead-scoring.service');
const auditService = require('../services/audit.service');

class LeadsController {
  async getAll(req, res) {
    try {
      const { stage, counselor_id, search } = req.query;
      let leads = Lead.find();

      if (stage && stage !== 'all') {
        leads = leads.filter(l => l.stage === stage);
      }
      if (counselor_id && counselor_id !== 'all') {
        leads = leads.filter(l => l.assigned_counselor_id === counselor_id);
      }
      if (search) {
        const q = search.toLowerCase();
        leads = leads.filter(l => 
          l.first_name.toLowerCase().includes(q) || 
          l.last_name.toLowerCase().includes(q) || 
          l.email.toLowerCase().includes(q) ||
          l.phone.includes(q)
        );
      }

      const detailed = leads.map(l => l.toDetailedJSON());
      return res.status(200).json({ success: true, count: detailed.length, data: detailed });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async getById(req, res) {
    try {
      const lead = Lead.findById(req.params.id);
      if (!lead) return res.status(404).json({ success: false, message: 'Lead not found.' });
      return res.status(200).json({ success: true, data: lead.toDetailedJSON() });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async create(req, res) {
    try {
      const { first_name, last_name, email, phone, source, interested_course_id, budget_range, preferred_intake, notes } = req.body;
      if (!first_name || !last_name || !email || !phone) {
        return res.status(400).json({ success: false, message: 'First Name, Last Name, Email, and Phone are required.' });
      }

      // Auto-assign counselor if available
      const counselors = db.find('users', { role: 'counselor', is_active: 1 });
      const assignedCounselorId = counselors.length > 0 ? counselors[Math.floor(Math.random() * counselors.length)].id : null;

      const newLead = Lead.create({
        first_name,
        last_name,
        email,
        phone,
        alternate_phone: req.body.alternate_phone || '',
        source: source || 'Website Inbound',
        stage: 'new',
        interested_course_id: interested_course_id || null,
        assigned_counselor_id: req.body.assigned_counselor_id || assignedCounselorId,
        budget_range: budget_range || '',
        preferred_intake: preferred_intake || 'Fall 2026',
        country: req.body.country || 'India',
        city: req.body.city || '',
        notes: notes || '',
        qualification_status: 'New Inquiry'
      });

      // Compute score
      newLead.lead_score = leadScoringService.calculateScore(newLead, []);
      newLead.save();

      auditService.logAction(req.user?.id, 'CREATE_LEAD', 'leads', newLead.id, { email: newLead.email }, req.ip);

      return res.status(201).json({ success: true, message: 'Lead captured successfully.', data: newLead.toDetailedJSON() });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }

  async update(req, res) {
    try {
      const lead = Lead.findById(req.params.id);
      if (!lead) return res.status(404).json({ success: false, message: 'Lead not found.' });

      Object.assign(lead, req.body);
      const interactions = db.find('lead_interactions', { lead_id: lead.id });
      lead.lead_score = leadScoringService.calculateScore(lead, interactions);
      lead.save();

      auditService.logAction(req.user?.id, 'UPDATE_LEAD', 'leads', lead.id, req.body, req.ip);

      return res.status(200).json({ success: true, message: 'Lead updated successfully.', data: lead.toDetailedJSON() });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }

  async addInteraction(req, res) {
    try {
      const lead = Lead.findById(req.params.id);
      if (!lead) return res.status(404).json({ success: false, message: 'Lead not found.' });

      const { interaction_type, summary, outcome, duration_minutes, scheduled_follow_up } = req.body;
      const intr = db.insert('lead_interactions', {
        id: `intr_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
        lead_id: lead.id,
        user_id: req.user?.id || 'usr_counselor_01',
        interaction_type: interaction_type || 'phone_call',
        summary: summary || '',
        outcome: outcome || '',
        duration_minutes: Number(duration_minutes) || 0,
        scheduled_follow_up: scheduled_follow_up || null
      });

      lead.last_contacted_at = new Date().toISOString();
      if (scheduled_follow_up) lead.next_follow_up_date = scheduled_follow_up;
      
      const interactions = db.find('lead_interactions', { lead_id: lead.id });
      lead.lead_score = leadScoringService.calculateScore(lead, interactions);
      lead.save();

      return res.status(201).json({ success: true, message: 'Interaction logged.', data: intr });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }

  async delete(req, res) {
    try {
      const lead = Lead.findById(req.params.id);
      if (!lead) return res.status(404).json({ success: false, message: 'Lead not found.' });

      lead.delete();
      db.deleteWhere('lead_interactions', { lead_id: req.params.id });
      auditService.logAction(req.user?.id, 'DELETE_LEAD', 'leads', req.params.id, {}, req.ip);

      return res.status(200).json({ success: true, message: 'Lead deleted.' });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }
}

module.exports = new LeadsController();
