'use strict';

/**
 * Analytics and Business Intelligence Dashboard Engine
 */

const db = require('../../database/db');

class AnalyticsService {
  /**
   * Generate holistic executive summary dashboard metrics
   */
  async getDashboardSummary() {
    const totalLeads = db.count('leads');
    const newLeads = db.count('leads', { stage: 'new' });
    const enrolledLeads = db.count('leads', { stage: 'enrolled' });
    const totalStudents = db.count('students', { enrollment_status: 'active' });
    const totalCourses = db.count('courses', { is_active: 1 });
    const openTickets = db.count('support_tickets', (val, t) => t.status === 'open' || t.status === 'in_progress');

    // Lead stage funnel breakdown
    const leadsByStage = {
      new: db.count('leads', { stage: 'new' }),
      contacted: db.count('leads', { stage: 'contacted' }),
      qualified: db.count('leads', { stage: 'qualified' }),
      counseling_scheduled: db.count('leads', { stage: 'counseling_scheduled' }),
      application_submitted: db.count('leads', { stage: 'application_submitted' }),
      enrolled: db.count('leads', { stage: 'enrolled' })
    };

    // Revenue metrics
    const invoices = db.find('invoices');
    let totalRevenueCollected = 0;
    let totalRevenuePending = 0;
    invoices.forEach(inv => {
      totalRevenueCollected += Number(inv.amount_paid || 0);
      totalRevenuePending += Number(inv.balance_due || 0);
    });

    // Conversion rate
    const conversionRate = totalLeads > 0 ? Number(((enrolledLeads / totalLeads) * 100).toFixed(1)) : 0;

    return {
      kpis: {
        totalLeads,
        newLeads,
        enrolledLeads,
        totalStudents,
        totalCourses,
        openTickets,
        conversionRate,
        totalRevenueCollected: Number(totalRevenueCollected.toFixed(2)),
        totalRevenuePending: Number(totalRevenuePending.toFixed(2))
      },
      funnel: leadsByStage,
      recentActivity: db.find('lead_interactions').slice(-5).reverse(),
      announcements: db.find('announcements').slice(-3)
    };
  }
}

module.exports = new AnalyticsService();
