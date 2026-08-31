'use strict';

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
