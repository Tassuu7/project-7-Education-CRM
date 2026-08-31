'use strict';

/**
 * Master Database Seeder Script
 * Synchronizes and populates all database tables with comprehensive sample data.
 */

const db = require('../db');
const { usersSeed } = require('./users.seed');
const { coursesSeed, courseModulesSeed, batchesSeed } = require('./courses.seed');
const { leadsSeed, leadInteractionsSeed } = require('./leads.seed');
const { applicationsSeed, studentsSeed } = require('./students.seed');
const { invoicesSeed, paymentsSeed } = require('./finance.seed');
const { attendanceSessionsSeed, attendanceRecordsSeed } = require('./attendance.seed');
const { gradeItemsSeed, studentGradesSeed } = require('./grades.seed');
const { ticketsSeed, ticketRepliesSeed } = require('./tickets.seed');
const { announcementsSeed, notificationsSeed, systemSettingsSeed } = require('./announcements.seed');

async function runSeed() {
  console.log('[Seeder] Starting EduPulse CRM complete database seeding...');
  await db.init();

  // Populate users
  db.truncate('users');
  db.insertMany('users', usersSeed);
  console.log(`[Seeder] Seeded ${usersSeed.length} users`);

  // Populate courses, modules, batches
  db.truncate('courses');
  db.insertMany('courses', coursesSeed);
  db.truncate('course_modules');
  db.insertMany('course_modules', courseModulesSeed);
  db.truncate('batches');
  db.insertMany('batches', batchesSeed);
  console.log(`[Seeder] Seeded ${coursesSeed.length} courses, ${courseModulesSeed.length} modules, ${batchesSeed.length} batches`);

  // Populate leads & interactions
  db.truncate('leads');
  db.insertMany('leads', leadsSeed);
  db.truncate('lead_interactions');
  db.insertMany('lead_interactions', leadInteractionsSeed);
  console.log(`[Seeder] Seeded ${leadsSeed.length} leads, ${leadInteractionsSeed.length} interactions`);

  // Populate applications & students
  db.truncate('student_applications');
  db.insertMany('student_applications', applicationsSeed);
  db.truncate('students');
  db.insertMany('students', studentsSeed);
  console.log(`[Seeder] Seeded ${applicationsSeed.length} applications, ${studentsSeed.length} students`);

  // Populate finance (invoices & payments)
  db.truncate('invoices');
  db.insertMany('invoices', invoicesSeed);
  db.truncate('payments');
  db.insertMany('payments', paymentsSeed);
  console.log(`[Seeder] Seeded ${invoicesSeed.length} invoices, ${paymentsSeed.length} payments`);

  // Populate attendance
  db.truncate('attendance_sessions');
  db.insertMany('attendance_sessions', attendanceSessionsSeed);
  db.truncate('attendance_records');
  db.insertMany('attendance_records', attendanceRecordsSeed);
  console.log(`[Seeder] Seeded ${attendanceSessionsSeed.length} sessions, ${attendanceRecordsSeed.length} attendance records`);

  // Populate gradebook
  db.truncate('grade_items');
  db.insertMany('grade_items', gradeItemsSeed);
  db.truncate('student_grades');
  db.insertMany('student_grades', studentGradesSeed);
  console.log(`[Seeder] Seeded ${gradeItemsSeed.length} grade items, ${studentGradesSeed.length} student grades`);

  // Populate tickets
  db.truncate('support_tickets');
  db.insertMany('support_tickets', ticketsSeed);
  db.truncate('ticket_replies');
  db.insertMany('ticket_replies', ticketRepliesSeed);
  console.log(`[Seeder] Seeded ${ticketsSeed.length} tickets, ${ticketRepliesSeed.length} replies`);

  // Populate announcements, notifications, settings
  db.truncate('announcements');
  db.insertMany('announcements', announcementsSeed);
  db.truncate('notifications');
  db.insertMany('notifications', notificationsSeed);
  db.truncate('system_settings');
  db.insertMany('system_settings', systemSettingsSeed);
  console.log(`[Seeder] Seeded announcements, notifications, and settings`);

  db.persistSync();
  console.log('[Seeder] Database seeding completed successfully!');
}

if (require.main === module) {
  runSeed().catch(err => {
    console.error('[Seeder] Error seeding database:', err);
    process.exit(1);
  });
}

module.exports = { runSeed };
