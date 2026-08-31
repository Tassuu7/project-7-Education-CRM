#!/usr/bin/env python3
"""
EduPulse CRM - Middlewares, Utilities, Templates, and Route Handlers Generator
"""

import os
from pathlib import Path

def generate(base_dir):
    def write(rel, content):
        p = Path(base_dir) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {rel}")

    # src/middlewares/auth.middleware.js
    write("src/middlewares/auth.middleware.js", """'use strict';

const authService = require('../services/auth.service');
const User = require('../models/User');

function authenticate(req, res, next) {
  const authHeader = req.headers.authorization || '';
  let token = null;

  if (authHeader.startsWith('Bearer ')) {
    token = authHeader.substring(7);
  } else if (req.headers['x-access-token']) {
    token = req.headers['x-access-token'];
  } else if (req.cookies && req.cookies.edupulse_session) {
    token = req.cookies.edupulse_session;
  }

  if (!token) {
    // Check if development guest bypass or default
    return next();
  }

  const payload = authService.verifyToken(token);
  if (payload && payload.userId) {
    const user = User.findById(payload.userId);
    if (user && user.is_active) {
      req.user = user.toSafeJSON();
    }
  }

  next();
}

function requireAuth(req, res, next) {
  if (!req.user) {
    return res.status(401).json({
      success: false,
      message: 'Unauthorized. Authentication token is missing or expired.'
    });
  }
  next();
}

module.exports = { authenticate, requireAuth };
""")

    # src/middlewares/rbac.middleware.js
    write("src/middlewares/rbac.middleware.js", """'use strict';

const { hasPermission, hasAnyPermission, ROLES } = require('../../config/permissions');

function requirePermission(permission) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ success: false, message: 'Unauthenticated.' });
    }

    if (req.user.role === ROLES.SUPER_ADMIN || req.user.role === ROLES.ADMIN) {
      return next();
    }

    if (!hasPermission(req.user.role, permission)) {
      return res.status(403).json({
        success: false,
        message: `Forbidden. Role '${req.user.role}' lacks permission '${permission}'.`
      });
    }

    next();
  };
}

function requireRoles(...roles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ success: false, message: 'Unauthenticated.' });
    }

    if (roles.includes(req.user.role) || req.user.role === ROLES.SUPER_ADMIN) {
      return next();
    }

    return res.status(403).json({
      success: false,
      message: `Forbidden. Role '${req.user.role}' is not authorized for this resource.`
    });
  };
}

module.exports = { requirePermission, requireRoles };
""")

    # src/middlewares/error.middleware.js
    write("src/middlewares/error.middleware.js", """'use strict';

function errorHandler(err, req, res, next) {
  console.error('[Error Middleware]', err.stack || err.message);

  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';

  res.status(status).json({
    success: false,
    error: {
      message,
      statusCode: status,
      timestamp: new Date().toISOString()
    }
  });
}

function notFoundHandler(req, res) {
  res.status(404).json({
    success: false,
    message: `Resource not found at ${req.originalUrl}`
  });
}

module.exports = { errorHandler, notFoundHandler };
""")

    # src/middlewares/rate-limiter.middleware.js
    write("src/middlewares/rate-limiter.middleware.js", """'use strict';

const requestCounts = new Map();

function rateLimiter(options = { windowMs: 60000, max: 200 }) {
  return (req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress || 'unknown';
    const now = Date.now();

    if (!requestCounts.has(ip)) {
      requestCounts.set(ip, { count: 1, resetTime: now + options.windowMs });
      return next();
    }

    const tracker = requestCounts.get(ip);
    if (now > tracker.resetTime) {
      tracker.count = 1;
      tracker.resetTime = now + options.windowMs;
      return next();
    }

    tracker.count++;
    if (tracker.count > options.max) {
      return res.status(429).json({
        success: false,
        message: 'Too many requests. Please slow down and try again shortly.'
      });
    }

    next();
  };
}

module.exports = rateLimiter;
""")

    # src/middlewares/logger.middleware.js
    write("src/middlewares/logger.middleware.js", """'use strict';

function requestLogger(req, res, next) {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`[HTTP] ${req.method} ${req.originalUrl} | Status: ${res.statusCode} | Duration: ${duration}ms | User: ${req.user ? req.user.username : 'Anonymous'}`);
  });
  next();
}

module.exports = requestLogger;
""")

    # src/utils/validator.util.js
    write("src/utils/validator.util.js", """'use strict';

class Validator {
  static isEmail(email) {
    if (!email || typeof email !== 'string') return false;
    const re = /^(([^<>()\\[\\]\\\\.,;:\\s@"]+(\\.[^<>()\\[\\]\\\\.,;:\\s@"]+)*)|(".+"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$/;
    return re.test(email.toLowerCase());
  }

  static isPhone(phone) {
    if (!phone || typeof phone !== 'string') return false;
    return /^[+0-9\\s-()]{7,20}$/.test(phone);
  }

  static isPositiveNumber(num) {
    return typeof num === 'number' && !isNaN(num) && num >= 0;
  }

  static sanitizeString(str) {
    if (typeof str !== 'string') return '';
    return str.trim().replace(/[<>]/g, '');
  }
}

module.exports = Validator;
""")

    # src/utils/formatter.util.js
    write("src/utils/formatter.util.js", """'use strict';

class Formatter {
  static formatCurrency(amount, currency = 'USD', symbol = '$') {
    const num = Number(amount) || 0;
    return `${symbol}${num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  }

  static formatDate(dateInput) {
    if (!dateInput) return 'N/A';
    const d = new Date(dateInput);
    if (isNaN(d.getTime())) return 'Invalid Date';
    return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
  }

  static formatDateTime(dateInput) {
    if (!dateInput) return 'N/A';
    const d = new Date(dateInput);
    if (isNaN(d.getTime())) return 'Invalid Date';
    return d.toLocaleString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  }
}

module.exports = Formatter;
""")

    # src/templates/email-templates.js
    write("src/templates/email-templates.js", """'use strict';

function getAdmissionOfferEmail(applicantName, courseName, term, depositAmount) {
  return `
  <!DOCTYPE html>
  <html>
  <head>
    <style>
      body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f7fc; margin: 0; padding: 20px; }
      .card { max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 32px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
      .header { border-bottom: 2px solid #4f46e5; padding-bottom: 16px; margin-bottom: 24px; }
      .header h1 { color: #1e1b4b; margin: 0; font-size: 24px; }
      .content { color: #334155; line-height: 1.6; font-size: 15px; }
      .highlight-box { background: #eef2ff; border-left: 4px solid #4f46e5; padding: 16px; border-radius: 6px; margin: 20px 0; }
      .btn { display: inline-block; background: #4f46e5; color: #ffffff; padding: 12px 28px; border-radius: 8px; text-decoration: none; font-weight: 600; }
      .footer { margin-top: 32px; font-size: 12px; color: #94a3b8; text-align: center; }
    </style>
  </head>
  <body>
    <div class="card">
      <div class="header">
        <h1>EduPulse Institute - Offer of Admission</h1>
      </div>
      <div class="content">
        <p>Dear <strong>${applicantName}</strong>,</p>
        <p>Congratulations! On behalf of the Academic Admissions Committee, we are delighted to offer you provisional admission to:</p>
        <div class="highlight-box">
          <p><strong>Program:</strong> ${courseName}</p>
          <p><strong>Intake Term:</strong> ${term}</p>
          <p><strong>Initial Deposit Due:</strong> $${depositAmount}</p>
        </div>
        <p>Please log in to your student portal to accept your offer and complete registration formalities.</p>
        <p style="text-align: center; margin-top: 24px;">
          <a href="http://localhost:4050" class="btn">Access Student Portal</a>
        </p>
      </div>
      <div class="footer">
        <p>EduPulse Institute of Advanced Technology & Management | Office of Admissions</p>
      </div>
    </div>
  </body>
  </html>
  `;
}

module.exports = { getAdmissionOfferEmail };
""")

    # src/routes/api.router.js
    write("src/routes/api.router.js", """'use strict';

/**
 * Master REST API Gateway Router
 */

const express = require('express');
const router = express.Router();

const authController = require('../controllers/auth.controller');
const leadsController = require('../controllers/leads.controller');
const admissionsController = require('../controllers/admissions.controller');
const studentsController = require('../controllers/students.controller');
const coursesController = require('../controllers/courses.controller');
const financeController = require('../controllers/finance.controller');
const academicController = require('../controllers/academic.controller');
const ticketsController = require('../controllers/tickets.controller');
const analyticsController = require('../controllers/analytics.controller');
const exportController = require('../controllers/export.controller');

const { requireAuth } = require('../middlewares/auth.middleware');
const { requireRoles } = require('../middlewares/rbac.middleware');
const db = require('../../database/db');

// Health Check
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    uptime: process.uptime()
  });
});

// Authentication Routes
router.post('/auth/login', (req, res) => authController.login(req, res));
router.post('/auth/register', (req, res) => authController.register(req, res));
router.get('/auth/me', (req, res) => authController.me(req, res));
router.post('/auth/logout', (req, res) => authController.logout(req, res));

// Analytics Summary
router.get('/analytics/summary', (req, res) => analyticsController.getSummary(req, res));

// Leads CRM Routes
router.get('/leads', (req, res) => leadsController.getAll(req, res));
router.get('/leads/:id', (req, res) => leadsController.getById(req, res));
router.post('/leads', (req, res) => leadsController.create(req, res));
router.put('/leads/:id', (req, res) => leadsController.update(req, res));
router.post('/leads/:id/interactions', (req, res) => leadsController.addInteraction(req, res));
router.delete('/leads/:id', (req, res) => leadsController.delete(req, res));

// Admissions & Applications
router.get('/admissions/applications', (req, res) => admissionsController.getAllApplications(req, res));
router.post('/admissions/applications', (req, res) => admissionsController.createApplication(req, res));
router.post('/admissions/applications/:id/enroll', (req, res) => admissionsController.enrollApplication(req, res));

// Student Information System
router.get('/students', (req, res) => studentsController.getAll(req, res));
router.get('/students/:id', (req, res) => studentsController.getById(req, res));
router.put('/students/:id', (req, res) => studentsController.update(req, res));

// Courses & Batches
router.get('/courses', (req, res) => coursesController.getAll(req, res));
router.get('/courses/:id', (req, res) => coursesController.getById(req, res));
router.post('/courses', (req, res) => coursesController.create(req, res));
router.get('/batches', (req, res) => {
  const batches = db.find('batches').map(b => {
    const crs = db.findById('courses', b.course_id);
    return { ...b, courseTitle: crs ? crs.title : 'Course' };
  });
  res.json({ success: true, data: batches });
});

// Finance & Invoicing
router.get('/finance/overview', (req, res) => financeController.getOverview(req, res));
router.get('/finance/invoices', (req, res) => financeController.getInvoices(req, res));
router.post('/finance/invoices', (req, res) => financeController.createInvoice(req, res));
router.post('/finance/invoices/:id/pay', (req, res) => financeController.recordPayment(req, res));

// Academic, Attendance & Gradebook
router.get('/academic/attendance-sessions', (req, res) => academicController.getAttendanceSessions(req, res));
router.post('/academic/attendance', (req, res) => academicController.submitAttendance(req, res));
router.get('/academic/gradebook', (req, res) => academicController.getGradebook(req, res));
router.post('/academic/grades', (req, res) => academicController.submitGrade(req, res));

// Support Tickets Helpdesk
router.get('/tickets', (req, res) => ticketsController.getAll(req, res));
router.get('/tickets/:id', (req, res) => ticketsController.getById(req, res));
router.post('/tickets', (req, res) => ticketsController.create(req, res));
router.post('/tickets/:id/reply', (req, res) => ticketsController.addReply(req, res));
router.put('/tickets/:id/status', (req, res) => ticketsController.updateStatus(req, res));

// Announcements & Notifications
router.get('/announcements', (req, res) => {
  const items = db.find('announcements').sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  res.json({ success: true, data: items });
});
router.get('/notifications', (req, res) => {
  const items = db.find('notifications');
  res.json({ success: true, data: items });
});

// Export Routes
router.get('/export/:table/csv', (req, res) => exportController.exportCSV(req, res));
router.get('/export/:table/json', (req, res) => exportController.exportJSON(req, res));

// Users List for dropdowns/assignment
router.get('/system/users', (req, res) => {
  const users = db.find('users').map(u => ({
    id: u.id,
    name: `${u.first_name} ${u.last_name}`,
    email: u.email,
    role: u.role,
    avatar: u.avatar_url
  }));
  res.json({ success: true, data: users });
});

module.exports = router;
""")

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent.parent)
