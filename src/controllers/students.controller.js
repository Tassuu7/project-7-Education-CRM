'use strict';

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
