'use strict';

/**
 * Seed data for classroom sessions and attendance tracking
 */

const attendanceSessionsSeed = [
  {
    id: 'att_sess_001',
    batch_id: 'batch_cs_2026_a',
    course_id: 'crs_cs_01',
    module_id: 'mod_cs_101',
    instructor_id: 'usr_instructor_01',
    session_date: '2026-08-24',
    start_time: '09:00',
    end_time: '11:00',
    topic_covered: 'Graph Algorithms & Dijkstra Shortest Path'
  },
  {
    id: 'att_sess_002',
    batch_id: 'batch_cs_2026_a',
    course_id: 'crs_cs_01',
    module_id: 'mod_cs_102',
    instructor_id: 'usr_instructor_02',
    session_date: '2026-08-25',
    start_time: '11:30',
    end_time: '13:30',
    topic_covered: 'SQL Indexing & Query Plan Optimization'
  },
  {
    id: 'att_sess_003',
    batch_id: 'batch_ai_2026_a',
    course_id: 'crs_ai_01',
    module_id: 'mod_ai_501',
    instructor_id: 'usr_instructor_02',
    session_date: '2026-08-26',
    start_time: '14:00',
    end_time: '17:00',
    topic_covered: 'Backpropagation Calculus & Custom PyTorch Autograd'
  }
];

const attendanceRecordsSeed = [
  {
    id: 'att_rec_001',
    session_id: 'att_sess_001',
    student_id: 'stu_001',
    status: 'present',
    remarks: 'Active participation in live coding challenge.'
  },
  {
    id: 'att_rec_002',
    session_id: 'att_sess_002',
    student_id: 'stu_001',
    status: 'present',
    remarks: 'On time.'
  },
  {
    id: 'att_rec_003',
    session_id: 'att_sess_003',
    student_id: 'stu_002',
    status: 'present',
    remarks: 'Presented paper summary.'
  }
];

module.exports = { attendanceSessionsSeed, attendanceRecordsSeed };
