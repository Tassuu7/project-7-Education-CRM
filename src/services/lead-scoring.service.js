'use strict';

/**
 * Intelligent Multi-Factor Lead Scoring Service
 * Computes propensity score (0-100) based on source, budget, timeline, and interaction frequency.
 */

class LeadScoringService {
  /**
   * Calculate lead score based on domain attributes
   */
  calculateScore(lead, interactions = []) {
    let score = 20; // Base score

    // 1. Source Weighting
    const sourceWeights = {
      'Alumni Referral': 30,
      'Direct Campus Walk-in': 25,
      'Education Fair 2026': 20,
      'Website Inbound': 15,
      'Google Search Ads': 12,
      'Partner Agent': 15,
      'Social Media Campaign': 8,
      'Campus Seminar': 18
    };
    score += (sourceWeights[lead.source] || 10);

    // 2. Budget Qualification
    if (lead.budget_range) {
      if (lead.budget_range.includes('15,000') || lead.budget_range.includes('18,000') || lead.budget_range.includes('+')) {
        score += 15;
      } else if (lead.budget_range.includes('10,000')) {
        score += 10;
      } else {
        score += 5;
      }
    }

    // 3. Stage Progression Bonus
    const stageScores = {
      'new': 0,
      'contacted': 5,
      'qualified': 15,
      'counseling_scheduled': 25,
      'application_submitted': 35,
      'enrolled': 45,
      'unqualified': -20,
      'lost': -30
    };
    score += (stageScores[lead.stage] || 0);

    // 4. Interaction Intensity
    if (interactions && interactions.length > 0) {
      score += Math.min(20, interactions.length * 5);
      
      const hasCampusVisit = interactions.some(i => i.interaction_type === 'campus_visit' || i.interaction_type === 'in_person_meeting');
      if (hasCampusVisit) score += 10;
    }

    // 5. Contact Completeness
    if (lead.email && lead.phone && lead.city) score += 5;
    if (lead.alternate_phone) score += 3;

    // Clamp between 0 and 100
    return Math.max(0, Math.min(100, Math.round(score)));
  }

  /**
   * Determine temperature rating
   */
  getTemperature(score) {
    if (score >= 75) return 'Hot';
    if (score >= 45) return 'Warm';
    return 'Cold';
  }
}

module.exports = new LeadScoringService();
