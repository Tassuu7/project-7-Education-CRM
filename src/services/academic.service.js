'use strict';

/**
 * Academic Management, Attendance, and Grading Service
 */

const db = require('../../database/db');

class AcademicService {
  /**
   * Log attendance session and batch records
   */
  async recordAttendanceSession(sessionData, records = [], instructorId) {
    const { batch_id, course_id, module_id, session_date, topic_covered, start_time, end_time } = sessionData;

    if (!batch_id || !course_id || !session_date) {
      throw new Error('Batch, Course, and Session Date are required.');
    }

    const sessionId = `att_sess_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    const session = db.insert('attendance_sessions', {
      id: sessionId,
      batch_id,
      course_id,
      module_id: module_id || null,
      instructor_id: instructorId,
      session_date,
      start_time: start_time || '09:00',
      end_time: end_time || '11:00',
      topic_covered: topic_covered || 'Lecture'
    });

    const insertedRecords = [];
    for (const rec of records) {
      const record = db.insert('attendance_records', {
        id: `att_rec_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
        session_id: sessionId,
        student_id: rec.student_id,
        status: rec.status || 'present',
        remarks: rec.remarks || ''
      });
      insertedRecords.push(record);
    }

    return {
      session,
      recordsCount: insertedRecords.length
    };
  }

  /**
   * Grade a student for an assessment
   */
  async gradeStudent(gradeItemId, studentId, scoreObtained, gradedByUserId, feedback = '') {
    const item = db.findById('grade_items', gradeItemId);
    if (!item) throw new Error('Assessment item not found.');

    const score = Number(scoreObtained);
    if (isNaN(score) || score < 0 || score > item.max_score) {
      throw new Error(`Score must be between 0 and ${item.max_score}.`);
    }

    const percentage = (score / item.max_score) * 100;
    let letterGrade = 'F';
    let gpaPoints = 0.0;

    if (percentage >= 95) { letterGrade = 'A+'; gpaPoints = 4.0; }
    else if (percentage >= 90) { letterGrade = 'A'; gpaPoints = 3.8; }
    else if (percentage >= 85) { letterGrade = 'B+'; gpaPoints = 3.4; }
    else if (percentage >= 80) { letterGrade = 'B'; gpaPoints = 3.0; }
    else if (percentage >= 75) { letterGrade = 'C+'; gpaPoints = 2.5; }
    else if (percentage >= 70) { letterGrade = 'C'; gpaPoints = 2.0; }
    else if (percentage >= 60) { letterGrade = 'D'; gpaPoints = 1.0; }

    const existingGrade = db.findOne('student_grades', { grade_item_id: gradeItemId, student_id: studentId });
    let savedGrade;

    if (existingGrade) {
      savedGrade = db.updateById('student_grades', existingGrade.id, {
        score_obtained: score,
        letter_grade: letterGrade,
        gpa_points: gpaPoints,
        feedback,
        graded_by_user_id: gradedByUserId
      });
    } else {
      savedGrade = db.insert('student_grades', {
        id: `grd_rec_${Date.now()}`,
        grade_item_id: gradeItemId,
        student_id: studentId,
        score_obtained: score,
        letter_grade: letterGrade,
        gpa_points: gpaPoints,
        feedback,
        graded_by_user_id: gradedByUserId
      });
    }

    // Recalculate student cumulative GPA
    this.recalculateStudentGPA(studentId);

    return savedGrade;
  }

  /**
   * Recalculate student cumulative GPA based on all graded items
   */
  recalculateStudentGPA(studentId) {
    const grades = db.find('student_grades', { student_id: studentId });
    if (grades.length === 0) return;

    let totalPoints = 0;
    for (const g of grades) {
      totalPoints += Number(g.gpa_points || 0);
    }
    const newGpa = Number((totalPoints / grades.length).toFixed(2));
    db.updateById('students', studentId, { cumulative_gpa: newGpa });
  }
}

module.exports = new AcademicService();
