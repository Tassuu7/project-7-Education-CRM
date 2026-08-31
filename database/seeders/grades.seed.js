'use strict';

/**
 * Seed data for grade items, tests, and student grades
 */

const gradeItemsSeed = [
  {
    id: 'grd_item_001',
    course_id: 'crs_cs_01',
    module_id: 'mod_cs_101',
    batch_id: 'batch_cs_2026_a',
    title: 'Midterm Exam - Algorithms & Data Structures',
    assessment_type: 'Midterm',
    max_score: 100.0,
    weight_percentage: 30.0,
    due_date: '2026-08-20'
  },
  {
    id: 'grd_item_002',
    course_id: 'crs_cs_01',
    module_id: 'mod_cs_102',
    batch_id: 'batch_cs_2026_a',
    title: 'Project 1: Relational Schema & Indexing Benchmark',
    assessment_type: 'Project',
    max_score: 100.0,
    weight_percentage: 25.0,
    due_date: '2026-08-28'
  },
  {
    id: 'grd_item_003',
    course_id: 'crs_ai_01',
    module_id: 'mod_ai_501',
    batch_id: 'batch_ai_2026_a',
    title: 'Lab 1: Implementing Transformer Attention from Scratch',
    assessment_type: 'Lab Practical',
    max_score: 100.0,
    weight_percentage: 20.0,
    due_date: '2026-08-25'
  }
];

const studentGradesSeed = [
  {
    id: 'grd_rec_001',
    grade_item_id: 'grd_item_001',
    student_id: 'stu_001',
    score_obtained: 94.0,
    letter_grade: 'A',
    gpa_points: 3.8,
    feedback: 'Outstanding solution for Red-Black tree rebalancing question.',
    graded_by_user_id: 'usr_instructor_01'
  },
  {
    id: 'grd_rec_002',
    grade_item_id: 'grd_item_002',
    student_id: 'stu_001',
    score_obtained: 98.0,
    letter_grade: 'A+',
    gpa_points: 4.0,
    feedback: 'Flawless normalization and query profiling benchmarks.',
    graded_by_user_id: 'usr_instructor_02'
  },
  {
    id: 'grd_rec_003',
    grade_item_id: 'grd_item_003',
    student_id: 'stu_002',
    score_obtained: 99.0,
    letter_grade: 'A+',
    gpa_points: 4.0,
    feedback: 'Implemented multi-head flash attention with clean matrix vectorization.',
    graded_by_user_id: 'usr_instructor_02'
  }
];

module.exports = { gradeItemsSeed, studentGradesSeed };
