#!/usr/bin/env python3
"""
EduPulse CRM - Controllers Generator
Generates REST API Controllers for handling incoming HTTP requests, input validation, permissions, and formatted responses.
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

    # src/controllers/auth.controller.js
    write("src/controllers/auth.controller.js", """'use strict';

const authService = require('../services/auth.service');
const auditService = require('../services/audit.service');

class AuthController {
  async login(req, res) {
    try {
      const { username, password } = req.body || {};
      const result = await authService.login(username, password);
      
      auditService.logAction(result.user.id, 'USER_LOGIN', 'users', result.user.id, { ip: req.ip }, req.ip);
      
      return res.status(200).json({
        success: true,
        message: 'Login successful.',
        data: result
      });
    } catch (err) {
      return res.status(401).json({
        success: false,
        message: err.message || 'Authentication failed.'
      });
    }
  }

  async register(req, res) {
    try {
      const result = await authService.register(req.body);
      auditService.logAction(result.user.id, 'USER_REGISTER', 'users', result.user.id, { role: result.user.role }, req.ip);

      return res.status(201).json({
        success: true,
        message: 'Registration successful.',
        data: result
      });
    } catch (err) {
      return res.status(400).json({
        success: false,
        message: err.message || 'Registration failed.'
      });
    }
  }

  async me(req, res) {
    if (!req.user) {
      return res.status(401).json({ success: false, message: 'Unauthenticated.' });
    }
    return res.status(200).json({
      success: true,
      data: req.user
    });
  }

  async logout(req, res) {
    if (req.user) {
      auditService.logAction(req.user.id, 'USER_LOGOUT', 'users', req.user.id, {}, req.ip);
    }
    return res.status(200).json({
      success: true,
      message: 'Logged out successfully.'
    });
  }
}

module.exports = new AuthController();
""")

    # src/controllers/leads.controller.js
    write("src/controllers/leads.controller.js", """'use strict';

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
""")

    # src/controllers/admissions.controller.js
    write("src/controllers/admissions.controller.js", """'use strict';

const db = require('../../database/db');
const admissionsService = require('../services/admissions.service');
const auditService = require('../services/audit.service');

class AdmissionsController {
  async getAllApplications(req, res) {
    try {
      const { status } = req.query;
      let apps = db.find('student_applications');
      if (status && status !== 'all') {
        apps = apps.filter(a => a.status === status);
      }

      const enhanced = apps.map(app => {
        const course = db.findById('courses', app.course_id);
        const reviewer = app.reviewer_id ? db.findById('users', app.reviewer_id) : null;
        return {
          ...app,
          course: course ? { id: course.id, code: course.code, title: course.title } : null,
          reviewer: reviewer ? { id: reviewer.id, name: `${reviewer.first_name} ${reviewer.last_name}` } : null
        };
      });

      return res.status(200).json({ success: true, count: enhanced.length, data: enhanced });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async createApplication(req, res) {
    try {
      const { course_id, first_name, last_name, email, phone, dob, high_school_percentage, entrance_exam_score } = req.body;
      if (!course_id || !first_name || !last_name || !email || !phone) {
        return res.status(400).json({ success: false, message: 'Required application fields missing.' });
      }

      const app = db.insert('student_applications', {
        id: `app_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
        lead_id: req.body.lead_id || null,
        course_id,
        first_name,
        last_name,
        email,
        phone,
        dob: dob || '2005-01-01',
        gender: req.body.gender || 'Not Specified',
        high_school_percentage: Number(high_school_percentage) || 85.0,
        entrance_exam_score: Number(entrance_exam_score) || 80.0,
        status: 'submitted',
        applied_at: new Date().toISOString()
      });

      auditService.logAction(req.user?.id, 'SUBMIT_APPLICATION', 'student_applications', app.id, { email: app.email }, req.ip);

      return res.status(201).json({ success: true, message: 'Application submitted successfully.', data: app });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }

  async enrollApplication(req, res) {
    try {
      const result = await admissionsService.approveAndEnroll(
        req.params.id,
        req.user?.id || 'usr_admin_01',
        req.body
      );

      auditService.logAction(req.user?.id, 'ENROLL_STUDENT', 'students', result.student.id, { applicationId: req.params.id }, req.ip);

      return res.status(200).json({
        success: true,
        message: 'Applicant successfully enrolled and registered as student.',
        data: result
      });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }
}

module.exports = new AdmissionsController();
""")

    # src/controllers/students.controller.js
    write("src/controllers/students.controller.js", """'use strict';

const db = require('../../database/db');
const Student = require('../models/Student');
const auditService = require('../services/audit.service');

class StudentsController {
  async getAll(req, res) {
    try {
      const { course_id, batch_id, status, search } = req.query;
      let students = Student.find();

      if (course_id && course_id !== 'all') {
        students = students.filter(s => s.primary_course_id === course_id);
      }
      if (batch_id && batch_id !== 'all') {
        students = students.filter(s => s.current_batch_id === batch_id);
      }
      if (status && status !== 'all') {
        students = students.filter(s => s.enrollment_status === status);
      }
      if (search) {
        const q = search.toLowerCase();
        students = students.filter(s => 
          s.first_name.toLowerCase().includes(q) || 
          s.last_name.toLowerCase().includes(q) || 
          s.student_id_number.toLowerCase().includes(q) ||
          s.email.toLowerCase().includes(q)
        );
      }

      const detailed = students.map(s => s.toDetailedJSON());
      return res.status(200).json({ success: true, count: detailed.length, data: detailed });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async getById(req, res) {
    try {
      const student = Student.findById(req.params.id);
      if (!student) return res.status(404).json({ success: false, message: 'Student record not found.' });
      return res.status(200).json({ success: true, data: student.toDetailedJSON() });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async update(req, res) {
    try {
      const student = Student.findById(req.params.id);
      if (!student) return res.status(404).json({ success: false, message: 'Student record not found.' });

      Object.assign(student, req.body);
      student.save();

      auditService.logAction(req.user?.id, 'UPDATE_STUDENT', 'students', student.id, req.body, req.ip);

      return res.status(200).json({ success: true, message: 'Student profile updated.', data: student.toDetailedJSON() });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }
}

module.exports = new StudentsController();
""")

    # src/controllers/courses.controller.js
    write("src/controllers/courses.controller.js", """'use strict';

const Course = require('../models/Course');
const db = require('../../database/db');
const auditService = require('../services/audit.service');

class CoursesController {
  async getAll(req, res) {
    try {
      const courses = Course.find();
      const detailed = courses.map(c => c.toDetailedJSON());
      return res.status(200).json({ success: true, count: detailed.length, data: detailed });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async getById(req, res) {
    try {
      const course = Course.findById(req.params.id);
      if (!course) return res.status(404).json({ success: false, message: 'Course program not found.' });
      return res.status(200).json({ success: true, data: course.toDetailedJSON() });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async create(req, res) {
    try {
      const { code, title, department, degree_level, duration_months, total_credits, base_tuition_fee, description } = req.body;
      if (!code || !title || !department || !base_tuition_fee) {
        return res.status(400).json({ success: false, message: 'Required course attributes missing.' });
      }

      const newCourse = Course.create({
        code: code.trim().toUpperCase(),
        title: title.trim(),
        department,
        degree_level: degree_level || 'Bachelor',
        duration_months: Number(duration_months) || 36,
        total_credits: Number(total_credits) || 120,
        base_tuition_fee: Number(base_tuition_fee),
        description: description || '',
        syllabus_outline: req.body.syllabus_outline || '',
        is_active: 1
      });

      auditService.logAction(req.user?.id, 'CREATE_COURSE', 'courses', newCourse.id, { code: newCourse.code }, req.ip);

      return res.status(201).json({ success: true, message: 'Course program created.', data: newCourse.toDetailedJSON() });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }
}

module.exports = new CoursesController();
""")

    # src/controllers/finance.controller.js
    write("src/controllers/finance.controller.js", """'use strict';

const db = require('../../database/db');
const Invoice = require('../models/Invoice');
const billingService = require('../services/billing.service');
const auditService = require('../services/audit.service');

class FinanceController {
  async getInvoices(req, res) {
    try {
      const { status, student_id } = req.query;
      let invoices = Invoice.find();

      if (status && status !== 'all') {
        invoices = invoices.filter(i => i.status === status);
      }
      if (student_id) {
        invoices = invoices.filter(i => i.student_id === student_id);
      }

      const detailed = invoices.map(i => i.toDetailedJSON());
      return res.status(200).json({ success: true, count: detailed.length, data: detailed });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async createInvoice(req, res) {
    try {
      const result = await billingService.createInvoice(req.body);
      auditService.logAction(req.user?.id, 'CREATE_INVOICE', 'invoices', result.id, { amount: result.total_amount }, req.ip);
      return res.status(201).json({ success: true, message: 'Invoice generated successfully.', data: result });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }

  async recordPayment(req, res) {
    try {
      const result = await billingService.recordPayment(
        req.params.id,
        req.body,
        req.user?.id || 'usr_finance_01'
      );
      auditService.logAction(req.user?.id, 'RECORD_PAYMENT', 'payments', result.payment.id, { invoiceId: req.params.id, amount: req.body.amount }, req.ip);

      return res.status(200).json({ success: true, message: 'Payment recorded successfully.', data: result });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }

  async getOverview(req, res) {
    try {
      const overview = await billingService.getFinancialOverview();
      return res.status(200).json({ success: true, data: overview });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }
}

module.exports = new FinanceController();
""")

    # src/controllers/academic.controller.js
    write("src/controllers/academic.controller.js", """'use strict';

const db = require('../../database/db');
const academicService = require('../services/academic.service');
const auditService = require('../services/audit.service');

class AcademicController {
  async getAttendanceSessions(req, res) {
    try {
      const { batch_id } = req.query;
      let sessions = db.find('attendance_sessions');
      if (batch_id && batch_id !== 'all') {
        sessions = sessions.filter(s => s.batch_id === batch_id);
      }

      const enhanced = sessions.map(sess => {
        const batch = db.findById('batches', sess.batch_id);
        const course = db.findById('courses', sess.course_id);
        const instructor = db.findById('users', sess.instructor_id);
        const records = db.find('attendance_records', { session_id: sess.id });
        return {
          ...sess,
          batchName: batch ? batch.batch_name : 'Unknown',
          courseTitle: course ? course.title : 'Unknown',
          instructorName: instructor ? `${instructor.first_name} ${instructor.last_name}` : 'Unknown',
          totalMarked: records.length,
          presentCount: records.filter(r => r.status === 'present').length
        };
      });

      return res.status(200).json({ success: true, count: enhanced.length, data: enhanced });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async submitAttendance(req, res) {
    try {
      const { session, records } = req.body;
      const result = await academicService.recordAttendanceSession(
        session,
        records,
        req.user?.id || 'usr_instructor_01'
      );
      auditService.logAction(req.user?.id, 'RECORD_ATTENDANCE', 'attendance_sessions', result.session.id, { recordsCount: result.recordsCount }, req.ip);

      return res.status(201).json({ success: true, message: 'Attendance recorded successfully.', data: result });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }

  async getGradebook(req, res) {
    try {
      const { batch_id, student_id } = req.query;
      let gradeItems = db.find('grade_items');
      if (batch_id && batch_id !== 'all') {
        gradeItems = gradeItems.filter(g => g.batch_id === batch_id);
      }

      let studentGrades = db.find('student_grades');
      if (student_id) {
        studentGrades = studentGrades.filter(g => g.student_id === student_id);
      }

      return res.status(200).json({
        success: true,
        data: {
          items: gradeItems,
          grades: studentGrades
        }
      });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async submitGrade(req, res) {
    try {
      const { grade_item_id, student_id, score_obtained, feedback } = req.body;
      const result = await academicService.gradeStudent(
        grade_item_id,
        student_id,
        score_obtained,
        req.user?.id || 'usr_instructor_01',
        feedback
      );
      auditService.logAction(req.user?.id, 'ENTER_GRADE', 'student_grades', result.id, { studentId: student_id, score: score_obtained }, req.ip);

      return res.status(200).json({ success: true, message: 'Grade recorded successfully.', data: result });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }
}

module.exports = new AcademicController();
""")

    # src/controllers/tickets.controller.js
    write("src/controllers/tickets.controller.js", """'use strict';

const SupportTicket = require('../models/SupportTicket');
const db = require('../../database/db');
const auditService = require('../services/audit.service');

class TicketsController {
  async getAll(req, res) {
    try {
      const { status, category, priority } = req.query;
      let tickets = SupportTicket.find();

      if (status && status !== 'all') {
        tickets = tickets.filter(t => t.status === status);
      }
      if (category && category !== 'all') {
        tickets = tickets.filter(t => t.category === category);
      }
      if (priority && priority !== 'all') {
        tickets = tickets.filter(t => t.priority === priority);
      }

      const detailed = tickets.map(t => t.toDetailedJSON());
      return res.status(200).json({ success: true, count: detailed.length, data: detailed });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async getById(req, res) {
    try {
      const ticket = SupportTicket.findById(req.params.id);
      if (!ticket) return res.status(404).json({ success: false, message: 'Support ticket not found.' });
      return res.status(200).json({ success: true, data: ticket.toDetailedJSON() });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async create(req, res) {
    try {
      const { category, priority, subject, description } = req.body;
      if (!category || !subject || !description) {
        return res.status(400).json({ success: false, message: 'Category, subject, and description are required.' });
      }

      const ticketNumber = `TKT-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
      const newTicket = SupportTicket.create({
        ticket_number: ticketNumber,
        user_id: req.user?.id || 'usr_student_01',
        category,
        priority: priority || 'medium',
        status: 'open',
        subject,
        description
      });

      auditService.logAction(req.user?.id, 'CREATE_TICKET', 'support_tickets', newTicket.id, { ticketNumber }, req.ip);

      return res.status(201).json({ success: true, message: 'Support ticket submitted.', data: newTicket.toDetailedJSON() });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }

  async addReply(req, res) {
    try {
      const ticket = SupportTicket.findById(req.params.id);
      if (!ticket) return res.status(404).json({ success: false, message: 'Support ticket not found.' });

      const { message, is_staff_reply } = req.body;
      if (!message) return res.status(400).json({ success: false, message: 'Message content is required.' });

      const reply = ticket.addReply(req.user?.id || 'usr_admin_01', message, is_staff_reply ? 1 : 0);
      return res.status(201).json({ success: true, message: 'Reply sent.', data: reply });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }

  async updateStatus(req, res) {
    try {
      const ticket = SupportTicket.findById(req.params.id);
      if (!ticket) return res.status(404).json({ success: false, message: 'Support ticket not found.' });

      const { status, resolution_notes } = req.body;
      ticket.status = status || ticket.status;
      if (resolution_notes) ticket.resolution_notes = resolution_notes;
      if (status === 'resolved' || status === 'closed') ticket.resolved_at = new Date().toISOString();
      ticket.save();

      auditService.logAction(req.user?.id, 'UPDATE_TICKET_STATUS', 'support_tickets', ticket.id, { status }, req.ip);

      return res.status(200).json({ success: true, message: 'Ticket status updated.', data: ticket.toDetailedJSON() });
    } catch (err) {
      return res.status(400).json({ success: false, message: err.message });
    }
  }
}

module.exports = new TicketsController();
""")

    # src/controllers/analytics.controller.js
    write("src/controllers/analytics.controller.js", """'use strict';

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
""")

    # src/controllers/export.controller.js
    write("src/controllers/export.controller.js", """'use strict';

const exportService = require('../services/export.service');

class ExportController {
  async exportCSV(req, res) {
    try {
      const tableName = req.params.table;
      const csv = exportService.exportTableToCSV(tableName);
      
      res.setHeader('Content-Type', 'text/csv');
      res.setHeader('Content-Disposition', `attachment; filename="edupulse_${tableName}_${Date.now()}.csv"`);
      return res.status(200).send(csv);
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async exportJSON(req, res) {
    try {
      const tableName = req.params.table;
      const data = exportService.exportTableToJSON(tableName);
      return res.status(200).json({ success: true, table: tableName, data });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }
}

module.exports = new ExportController();
""")

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent.parent)
