'use strict';

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
