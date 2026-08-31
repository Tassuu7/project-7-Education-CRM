'use strict';

/**
 * Seed data for campus announcements, system settings, and notifications
 */

const announcementsSeed = [
  {
    id: 'anc_001',
    title: 'Fall 2026 Academic Orientation & Hackathon Kickoff',
    content: 'Welcome all new incoming students! Orientation commences this Friday at 10:00 AM in the Main Auditorium, followed by our 24-hour Welcome Hackathon.',
    target_audience: 'all',
    priority: 'high',
    author_id: 'usr_admin_01',
    is_pinned: 1,
    created_at: '2026-08-28T09:00:00Z'
  },
  {
    id: 'anc_002',
    title: 'Semester 1 Tuition Fee Installment Deadline Notice',
    content: 'All students opting for the monthly or split installment plan are reminded that the secondary installment is due by December 15, 2026.',
    target_audience: 'students',
    priority: 'normal',
    author_id: 'usr_finance_01',
    is_pinned: 0,
    created_at: '2026-08-29T11:00:00Z'
  }
];

const notificationsSeed = [
  {
    id: 'notif_001',
    user_id: 'usr_student_01',
    title: 'Grade Published: Data Structures Midterm',
    message: 'Dr. Alan Turing published your score: 94/100 (Grade A).',
    type: 'success',
    is_read: 0,
    link_url: '#/grades'
  },
  {
    id: 'notif_002',
    user_id: 'usr_counselor_01',
    title: 'New High-Score Lead Assigned',
    message: 'Vikram Patel (Score: 85) has been assigned to your counseling queue.',
    type: 'info',
    is_read: 0,
    link_url: '#/leads'
  },
  {
    id: 'notif_003',
    user_id: 'usr_student_02',
    title: 'Fee Payment Receipt Generated',
    message: 'Receipt REC-2026-0201 for $7,350 has been recorded.',
    type: 'success',
    is_read: 1,
    link_url: '#/finance'
  }
];

const systemSettingsSeed = [
  { key: 'institution_name', value: 'EduPulse Institute of Advanced Technology & Management', category: 'general', description: 'Institution legal display name' },
  { key: 'institution_email', value: 'contact@edupulse.edu', category: 'general', description: 'Main administrative email' },
  { key: 'institution_phone', value: '+1 (800) 555-EDUPULSE', category: 'general', description: 'Toll-free student help line' },
  { key: 'currency_symbol', value: '$', category: 'finance', description: 'Billing currency symbol' },
  { key: 'academic_term_current', value: 'Fall 2026', category: 'academic', description: 'Current active semester term' },
  { key: 'lead_auto_assign_enabled', value: 'true', category: 'leads', description: 'Enable automatic round-robin counselor assignment' }
];

module.exports = { announcementsSeed, notificationsSeed, systemSettingsSeed };
