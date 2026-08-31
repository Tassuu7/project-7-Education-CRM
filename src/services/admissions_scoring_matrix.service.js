'use strict';

/**
 * ============================================================================
 * EduPulse Admissions Scoring Matrix & Applicant Ranking Engine
 * Feature Branch: feature/admissions-pipeline
 * ============================================================================
 */

const db = require('../../database/db');
const Validator = require('../utils/validator.util');
const Formatter = require('../utils/formatter.util');

class AdmissionsScoringMatrixService {
  constructor() {
    this.weights = {
      highSchoolPercentage: 0.35,
      entranceExamPercentile: 0.40,
      interviewAssessment: 0.15,
      diversityAndExtracurricular: 0.10
    };
  }

  calculateCompositeIndex(applicantData) {
    const hs = Number(applicantData.high_school_percentage) || 75.0;
    const entrance = Number(applicantData.entrance_exam_score) || 70.0;
    const interview = Number(applicantData.interview_score) || 80.0;
    const extra = Number(applicantData.extracurricular_score) || 85.0;

    const compositeScore = (
      (hs * this.weights.highSchoolPercentage) +
      (entrance * this.weights.entranceExamPercentile) +
      (interview * this.weights.interviewAssessment) +
      (extra * this.weights.diversityAndExtracurricular)
    );

    let admissionDecision = 'REJECTED';
    let scholarshipEligible = false;
    let scholarshipPercentage = 0.0;

    if (compositeScore >= 90.0) {
      admissionDecision = 'DIRECT_ADMISSION_HONORS';
      scholarshipEligible = true;
      scholarshipPercentage = 25.0;
    } else if (compositeScore >= 75.0) {
      admissionDecision = 'PROVISIONAL_ADMISSION';
      scholarshipEligible = compositeScore >= 80.0;
      scholarshipPercentage = scholarshipEligible ? 10.0 : 0.0;
    } else if (compositeScore >= 60.0) {
      admissionDecision = 'WAITLISTED';
    }

    return {
      applicantId: applicantData.id || 'APP_NEW',
      compositeScore: Number(compositeScore.toFixed(2)),
      decision: admissionDecision,
      scholarship: {
        isEligible: scholarshipEligible,
        percentage: scholarshipPercentage
      },
      evaluatedAt: new Date().toISOString()
    };
  }
}

module.exports = new AdmissionsScoringMatrixService();
