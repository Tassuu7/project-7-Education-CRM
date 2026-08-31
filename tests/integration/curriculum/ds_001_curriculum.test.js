'use strict';

/**
 * ============================================================================
 * Integration Test: Curriculum Validation for Statistical Inference (DS-001)
 * ============================================================================
 */

const assert = require('assert');
const syllabus = require('../../src/knowledge_base/syllabi/ds_001_statistical_inference');

describe('Curriculum Integration: DS-001 Statistical Inference', () => {
  it('should have valid course code and credit hours', () => {
    assert.strictEqual(syllabus.courseCode, 'DS-001');
    assert.strictEqual(syllabus.academicCredits, 4);
  });

  it('should have at least 4 well-defined learning outcomes', () => {
    assert(Array.isArray(syllabus.learningOutcomes));
    assert(syllabus.learningOutcomes.length >= 4);
  });

  it('should provide complete 10-week syllabus breakdown', () => {
    assert.strictEqual(syllabus.weeklyBreakdown.length, 10);
    syllabus.weeklyBreakdown.forEach((w, i) => {
      assert.strictEqual(w.week, i + 1);
      assert(typeof w.topic === 'string' && w.topic.length > 0);
      assert(typeof w.labExercise === 'string' && w.labExercise.length > 0);
    });
  });

  it('should total grading rubric to exactly 100 percent', () => {
    const r = syllabus.gradingRubric;
    const total = r.assignmentsWeight + r.midtermExamWeight + r.labPracticalsWeight + r.finalCapstoneWeight;
    assert.strictEqual(total, 100.0);
  });
});
