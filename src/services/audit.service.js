'use strict';

/**
 * System Security & Audit Logging Service
 */

const db = require('../../database/db');

class AuditService {
  /**
   * Record security or administrative mutation action
   */
  logAction(userId, action, entityType, entityId = null, details = {}, ip = '127.0.0.1') {
    const log = db.insert('audit_logs', {
      id: `aud_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
      user_id: userId || 'system',
      action,
      entity_type: entityType,
      entity_id: entityId,
      ip_address: ip,
      details: typeof details === 'string' ? details : JSON.stringify(details),
      created_at: new Date().toISOString()
    });
    return log;
  }

  /**
   * Get recent audit trails
   */
  getRecentLogs(limit = 50) {
    const logs = db.find('audit_logs');
    return logs.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, limit);
  }
}

module.exports = new AuditService();
