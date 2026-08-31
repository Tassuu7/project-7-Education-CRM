'use strict';

/**
 * ============================================================================
 * EduPulse Statistical Grading Curves & Honors Roll Classifier
 * Feature Branch: feature/academic-gradebook
 * ============================================================================
 */

const db = require('../../database/db');

class AcademicGradeCurvingService {
  computeGaussianCurvedGrades(gradeItemId, targetMean = 80.0, targetStdDev = 10.0) {
    const rawGrades = db.find('student_grades', { grade_item_id: gradeItemId });
    if (rawGrades.length === 0) return { count: 0, message: 'No grade records found.' };

    const rawScores = rawGrades.map(g => Number(g.score_obtained) || 0);
    const mean = rawScores.reduce((a, b) => a + b, 0) / rawScores.length;
    const variance = rawScores.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / rawScores.length;
    const stdDev = Math.sqrt(variance) || 1.0;

    const curvedResults = rawGrades.map(g => {
      const raw = Number(g.score_obtained) || 0;
      const zScore = (raw - mean) / stdDev;
      const curvedScore = Math.min(100, Math.max(0, targetMean + (zScore * targetStdDev)));

      let letterGrade = 'F';
      let gpa = 0.0;
      if (curvedScore >= 95) { letterGrade = 'A+'; gpa = 4.0; }
      else if (curvedScore >= 90) { letterGrade = 'A'; gpa = 3.8; }
      else if (curvedScore >= 85) { letterGrade = 'B+'; gpa = 3.4; }
      else if (curvedScore >= 80) { letterGrade = 'B'; gpa = 3.0; }
      else if (curvedScore >= 75) { letterGrade = 'C+'; gpa = 2.5; }
      else if (curvedScore >= 70) { letterGrade = 'C'; gpa = 2.0; }
      else if (curvedScore >= 60) { letterGrade = 'D'; gpa = 1.0; }

      return {
        studentId: g.student_id,
        rawScore: raw,
        zScore: Number(zScore.toFixed(3)),
        curvedScore: Number(curvedScore.toFixed(2)),
        letterGrade,
        gpa
      };
    });

    return {
      gradeItemId,
      originalMean: Number(mean.toFixed(2)),
      originalStdDev: Number(stdDev.toFixed(2)),
      curvedResults
    };
  }
}

module.exports = new AcademicGradeCurvingService();
