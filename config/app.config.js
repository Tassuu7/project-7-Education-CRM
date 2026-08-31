'use strict';

/**
 * EduPulse CRM Application Configuration
 * Enterprise multi-environment configuration module.
 */

const path = require('path');

const CONFIG = {
  app: {
    name: 'EduPulse Education CRM',
    version: '1.0.0',
    tagline: 'Next-Gen Student Lifecycle & Educational Operations Platform',
    environment: process.env.NODE_ENV || 'production',
    port: parseInt(process.env.PORT || '4050', 10),
    host: process.env.HOST || '0.0.0.0',
    baseUrl: process.env.BASE_URL || 'http://localhost:4050',
    apiPrefix: '/api/v1',
    timezone: 'Asia/Kolkata',
    defaultLocale: 'en-US'
  },

  security: {
    jwtSecret: 'edupulse_crm_jwt_secure_session_key_production_2026',
    tokenExpirySeconds: 86400 * 7, // 7 days
    refreshTokenExpirySeconds: 86400 * 30, // 30 days
    bcryptRounds: 10,
    rateLimitWindowMs: 15 * 60 * 1000, // 15 minutes
    rateLimitMaxRequests: 1000,
    corsOrigins: ['http://localhost:4050', 'http://127.0.0.1:4050'],
    sessionCookieName: 'edupulse_session',
    csrfEnabled: false
  },

  paths: {
    root: path.resolve(__dirname, '..'),
    public: path.resolve(__dirname, '../public'),
    database: path.resolve(__dirname, '../database'),
    storage: path.resolve(__dirname, '../storage'),
    uploads: path.resolve(__dirname, '../storage/uploads'),
    exports: path.resolve(__dirname, '../storage/exports'),
    logs: path.resolve(__dirname, '../logs')
  },

  database: {
    type: 'sqlite_in_memory_persistent',
    filePath: path.resolve(__dirname, '../database/edupulse.db'),
    jsonBackupPath: path.resolve(__dirname, '../database/edupulse_data.json'),
    autoSyncIntervalMs: 60000, // 1 minute auto backup
    enableSeedOnStartup: true,
    maxPoolSize: 20
  },

  leads: {
    defaultAssignmentStrategy: 'round_robin', // 'round_robin' | 'score_weighted' | 'manual'
    leadScoreThresholds: {
      hot: 75,
      warm: 45,
      cold: 0
    },
    staleLeadDays: 14,
    autoFollowUpReminderHours: 24,
    qualificationStages: [
      'new',
      'contacted',
      'qualified',
      'counseling_scheduled',
      'application_submitted',
      'enrolled',
      'unqualified',
      'lost'
    ]
  },

  admissions: {
    applicationFee: 50.00,
    defaultAcademicYear: '2026-2027',
    termPeriods: ['Fall 2026', 'Spring 2027', 'Summer 2027'],
    documentRequirements: [
      'high_school_transcript',
      'photo_id',
      'recommendation_letter',
      'statement_of_purpose'
    ]
  },

  academic: {
    attendanceThresholdWarning: 75.0, // Low attendance below 75%
    attendanceThresholdCritical: 60.0,
    gradingScale: {
      'A+': { min: 95, max: 100, gpa: 4.0 },
      'A':  { min: 90, max: 94.9, gpa: 3.8 },
      'B+': { min: 85, max: 89.9, gpa: 3.4 },
      'B':  { min: 80, max: 84.9, gpa: 3.0 },
      'C+': { min: 75, max: 79.9, gpa: 2.5 },
      'C':  { min: 70, max: 74.9, gpa: 2.0 },
      'D':  { min: 60, max: 69.9, gpa: 1.0 },
      'F':  { min: 0,  max: 59.9, gpa: 0.0 }
    },
    creditHoursPerSemesterMax: 24,
    creditHoursPerSemesterMin: 12
  },

  finance: {
    currency: 'USD',
    currencySymbol: '$',
    taxRatePercentage: 5.0,
    lateFeeDailyAmount: 5.00,
    lateFeeGraceDays: 5,
    installmentPlans: {
      lump_sum: { installments: 1, discountPercent: 5.0 },
      semester_bi: { installments: 2, discountPercent: 0.0 },
      monthly_plan: { installments: 4, surchargePercent: 2.5 }
    }
  },

  support: {
    defaultSlaHours: {
      critical: 4,
      high: 12,
      medium: 24,
      low: 48
    },
    categories: [
      'Admissions',
      'Fee & Billing',
      'Course Registration',
      'Attendance & Grades',
      'Technical Support',
      'Hostel & Transport',
      'General Inquiry'
    ]
  },

  notifications: {
    enableEmailSimulation: true,
    enableSmsSimulation: true,
    channels: ['in_app', 'email', 'sms']
  }
};

module.exports = CONFIG;
