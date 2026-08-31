'use strict';

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
