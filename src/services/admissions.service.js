'use strict';

/**
 * Admissions & Student Enrollment Pipeline Service
 */

const db = require('../../database/db');
const Student = require('../models/Student');
const Lead = require('../models/Lead');
const Invoice = require('../models/Invoice');
const User = require('../models/User');

class AdmissionsService {
  /**
   * Process and approve an application, converting to enrolled student
   */
  async approveAndEnroll(applicationId, reviewerId, options = {}) {
    const app = db.findById('student_applications', applicationId);
    if (!app) throw new Error('Application not found.');

    if (app.status === 'enrolled') {
      throw new Error('Candidate is already enrolled.');
    }

    const course = db.findById('courses', app.course_id);
    if (!course) throw new Error('Applied course not found.');

    // 1. Update Application status
    db.updateById('student_applications', applicationId, {
      status: 'enrolled',
      reviewer_id: reviewerId,
      decision_at: new Date().toISOString(),
      review_notes: options.review_notes || 'Approved for enrollment.'
    });

    // 2. Create User Account if not exists
    let studentUser = db.findOne('users', { email: app.email });
    if (!studentUser) {
      const generatedUsername = `stu_${app.first_name.toLowerCase()}_${Math.floor(100 + Math.random() * 900)}`;
      studentUser = User.create({
        username: generatedUsername,
        email: app.email,
        password_hash: User.hashPassword('student123'),
        first_name: app.first_name,
        last_name: app.last_name,
        role: 'student',
        phone: app.phone,
        is_active: 1
      });
    }

    // 3. Create Enrolled Student Record
    const studentCount = db.count('students');
    const studentIdNumber = `STU-${new Date().getFullYear()}-${String(studentCount + 1).padStart(3, '0')}`;
    
    // Find active batch for course
    const batch = db.findOne('batches', { course_id: app.course_id, status: 'active' }) ||
                  db.findOne('batches', { course_id: app.course_id });

    const newStudent = Student.create({
      user_id: studentUser.id,
      student_id_number: studentIdNumber,
      application_id: app.id,
      first_name: app.first_name,
      last_name: app.last_name,
      email: app.email,
      phone: app.phone,
      dob: app.dob,
      primary_course_id: app.course_id,
      current_batch_id: batch ? batch.id : null,
      current_semester: 1,
      enrollment_status: 'active',
      cumulative_gpa: 0.0,
      total_credits_earned: 0,
      enrolled_date: new Date().toISOString().split('T')[0]
    });

    // 4. Generate Initial Semester Tuition Invoice
    const invoiceNum = `INV-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`;
    const semTuition = course.base_tuition_fee / (course.duration_months / 6);
    const invoice = Invoice.create({
      invoice_number: invoiceNum,
      student_id: newStudent.id,
      course_id: course.id,
      title: `Semester 1 Tuition & Registration Fee - ${course.code}`,
      amount: semTuition,
      discount_amount: options.scholarshipDiscount || 0.0,
      tax_amount: Number((semTuition * 0.05).toFixed(2)),
      due_date: new Date(Date.now() + 14 * 86400000).toISOString().split('T')[0],
      status: 'pending',
      notes: 'Initial admission invoice generated upon enrollment.'
    });

    // 5. Update Lead stage if originated from lead
    if (app.lead_id) {
      db.updateById('leads', app.lead_id, {
        stage: 'enrolled',
        qualification_status: 'Enrolled'
      });
    }

    return {
      application: db.findById('student_applications', applicationId),
      student: newStudent,
      invoice
    };
  }
}

module.exports = new AdmissionsService();
