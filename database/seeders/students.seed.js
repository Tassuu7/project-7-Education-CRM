'use strict';

/**
 * Seed data for enrolled students and admissions applications
 */

const applicationsSeed = [
  {
    id: 'app_2026_001',
    lead_id: 'lead_005',
    course_id: 'crs_cs_01',
    first_name: 'Rohit',
    last_name: 'Sharma',
    email: 'rohit.sharma@student.edupulse.edu',
    phone: '+91-9876543210',
    dob: '2005-04-30',
    gender: 'Male',
    high_school_percentage: 94.5,
    entrance_exam_score: 91.0,
    status: 'enrolled',
    reviewer_id: 'usr_admin_01',
    review_notes: 'Exceptional math and analytical aptitude. Approved for enrollment.',
    applied_at: '2026-07-10T10:00:00Z',
    decision_at: '2026-07-15T16:00:00Z'
  },
  {
    id: 'app_2026_002',
    lead_id: null,
    course_id: 'crs_ai_01',
    first_name: 'Ananya',
    last_name: 'Iyer',
    email: 'ananya.iyer@student.edupulse.edu',
    phone: '+91-9876543211',
    dob: '2002-11-15',
    gender: 'Female',
    high_school_percentage: 92.0,
    entrance_exam_score: 95.5,
    status: 'enrolled',
    reviewer_id: 'usr_admin_01',
    review_notes: 'Direct admission based on top 1% percentile in state entrance test.',
    applied_at: '2026-07-12T11:30:00Z',
    decision_at: '2026-07-18T14:00:00Z'
  }
];

const studentsSeed = [
  {
    id: 'stu_001',
    user_id: 'usr_student_01',
    student_id_number: 'STU-2026-001',
    application_id: 'app_2026_001',
    first_name: 'Rohit',
    last_name: 'Sharma',
    email: 'rohit.sharma@student.edupulse.edu',
    phone: '+91-9876543210',
    dob: '2005-04-30',
    blood_group: 'B+',
    address: 'Flat 402, Green Meadows, Andheri West',
    city: 'Mumbai',
    state: 'Maharashtra',
    guardian_name: 'Ramesh Sharma',
    guardian_phone: '+91-9876500001',
    guardian_email: 'ramesh.sharma@gmail.com',
    guardian_relation: 'Father',
    primary_course_id: 'crs_cs_01',
    current_batch_id: 'batch_cs_2026_a',
    current_semester: 1,
    enrollment_status: 'active',
    cumulative_gpa: 3.85,
    total_credits_earned: 16,
    enrolled_date: '2026-08-01'
  },
  {
    id: 'stu_002',
    user_id: 'usr_student_02',
    student_id_number: 'STU-2026-002',
    application_id: 'app_2026_002',
    first_name: 'Ananya',
    last_name: 'Iyer',
    email: 'ananya.iyer@student.edupulse.edu',
    phone: '+91-9876543211',
    dob: '2002-11-15',
    blood_group: 'O+',
    address: 'Plot 88, Indiranagar, 100ft Road',
    city: 'Bangalore',
    state: 'Karnataka',
    guardian_name: 'Venkatesh Iyer',
    guardian_phone: '+91-9876500002',
    guardian_email: 'venkat.iyer@gmail.com',
    guardian_relation: 'Father',
    primary_course_id: 'crs_ai_01',
    current_batch_id: 'batch_ai_2026_a',
    current_semester: 1,
    enrollment_status: 'active',
    cumulative_gpa: 3.95,
    total_credits_earned: 16,
    enrolled_date: '2026-08-01'
  }
];

module.exports = { applicationsSeed, studentsSeed };
