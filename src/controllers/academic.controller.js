'use strict';

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
