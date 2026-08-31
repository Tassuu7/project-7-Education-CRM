'use strict';

/**
 * ============================================================================
 * EduPulse Academic Curriculum Syllabus: AI-004
 * Discipline: Artificial Intelligence
 * Subject: Reinforcement Learning
 * ============================================================================
 */

const SYLLABUS_DEFINITION = {
  courseCode: 'AI-004',
  courseTitle: 'Reinforcement Learning in Artificial Intelligence',
  academicCredits: 4,
  prerequisites: ['AI-101', 'MATH-201'],
  targetAudience: 'Undergraduate / Postgraduate STEM Students',
  courseOverview: 'An in-depth, rigorous exploration into theoretical foundations, practical applications, and industry-standard best practices in Reinforcement Learning.',
  
  learningOutcomes: [
    'Master core principles, algorithmic paradigms, and implementation techniques in Reinforcement Learning.',
    'Design, implement, and benchmark scalable solutions for enterprise scenarios.',
    'Formulate quantitative models and evaluate edge cases in production deployments.',
    'Present technical architecture papers and deliver milestone-driven capstone projects.'
  ],

  weeklyBreakdown: [
    { week: 1, topic: 'Introduction & Foundations of Reinforcement Learning', labExercise: 'Environment Setup and Hello World Benchmark' },
    { week: 2, topic: 'Mathematical Foundations & Data Structures', labExercise: 'Algorithmic Complexity Profiling' },
    { week: 3, topic: 'Core Design Patterns & Architecture', labExercise: 'Modular Component Refactoring' },
    { week: 4, topic: 'State Management & Concurrency Controls', labExercise: 'Thread Safety & Mutex Benchmarks' },
    { week: 5, topic: 'Distributed Storage & Serialization', labExercise: 'Schema Design & Index Optimization' },
    { week: 6, topic: 'Midterm Review & Project Milestone 1', labExercise: 'Interim Architecture Defense' },
    { week: 7, topic: 'Advanced Topics in Reinforcement Learning', labExercise: 'Performance Profiling & Bottleneck Elimination' },
    { week: 8, topic: 'Cloud Microservices & Containerization', labExercise: 'Docker & Kubernetes Cluster Deployment' },
    { week: 9, topic: 'Security Policies & Cryptographic Verification', labExercise: 'Vulnerability Scanning & Penetration Defense' },
    { week: 10, topic: 'Final Capstone Project Defense & Review', labExercise: 'Production Rollout & Live Demonstration' }
  ],

  gradingRubric: {
    assignmentsWeight: 25.0,
    midtermExamWeight: 25.0,
    labPracticalsWeight: 20.0,
    finalCapstoneWeight: 30.0
  }
};

module.exports = SYLLABUS_DEFINITION;
