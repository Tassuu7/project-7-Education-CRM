'use strict';

const analyticsService = require('../services/analytics.service');

class AnalyticsController {
  async getSummary(req, res) {
    try {
      const summary = await analyticsService.getDashboardSummary();
      return res.status(200).json({ success: true, data: summary });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }
}

module.exports = new AnalyticsController();
