#!/usr/bin/env python3
"""
EduPulse CRM - Core Configuration and Base Setup Generator
Generates package.json, package-lock.json, .gitignore, app.config.js, permissions.js, constants.js, and database.js
"""

import os
from pathlib import Path

def generate(base_dir):
    def write(rel, content):
        p = Path(base_dir) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {rel}")

    # .gitignore
    write(".gitignore", """# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

# Environment and sensitive data
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
*.pem
*.key
*.cert

# Build outputs and caches
dist/
build/
.cache/
.parcel-cache/
.next/
out/
.nuxt/
.vuepress/dist
.serverless/
.fusebox/
.dynamodb/

# Logs and runtime databases
*.log
logs/
*.sqlite
*.sqlite3
*.db
coverage/
.nyc_output/
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# IDE & OS files
.DS_Store
Thumbs.db
.idea/
.vscode/
*.sublime-workspace
*.sublime-project
""")

    # package.json
    write("package.json", """{
  "name": "edupulse-education-crm",
  "version": "1.0.0",
  "description": "Enterprise-Grade Education CRM & Student Lifecycle Management Platform",
  "main": "server.js",
  "type": "commonjs",
  "scripts": {
    "start": "node server.js",
    "dev": "node server.js",
    "seed": "node database/seeders/seed-all.js",
    "test": "node tests/run-tests.js",
    "measure": "python measure.py",
    "package": "python scripts/package-project.py",
    "health": "node scripts/verify-health.js"
  },
  "keywords": [
    "education-crm",
    "student-lifecycle",
    "admissions",
    "lead-management",
    "gradebook",
    "attendance",
    "billing",
    "helpdesk",
    "enterprise"
  ],
  "author": "EduPulse Engineering Team",
  "license": "UNLICENSED",
  "private": true,
  "dependencies": {},
  "devDependencies": {}
}""")

    # package-lock.json
    write("package-lock.json", """{
  "name": "edupulse-education-crm",
  "version": "1.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "edupulse-education-crm",
      "version": "1.0.0",
      "license": "UNLICENSED"
    }
  }
}""")

    # config/app.config.js
    write("config/app.config.js", """'use strict';

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
""")

    # config/permissions.js
    write("config/permissions.js", """'use strict';

/**
 * Role-Based Access Control (RBAC) Permission Matrix
 * Defines distinct roles and their atomic permissions across all CRM modules.
 */

const ROLES = {
  SUPER_ADMIN: 'super_admin',
  ADMIN: 'admin',
  COUNSELOR: 'counselor',
  INSTRUCTOR: 'instructor',
  FINANCE_OFFICER: 'finance_officer',
  STUDENT: 'student',
  PARENT: 'parent'
};

const PERMISSIONS = {
  // Authentication & Profile
  AUTH_LOGIN: 'auth:login',
  AUTH_MANAGE_USERS: 'auth:manage_users',
  AUTH_VIEW_AUDIT_LOGS: 'auth:view_audit_logs',

  // Lead Management
  LEADS_VIEW: 'leads:view',
  LEADS_VIEW_ALL: 'leads:view_all',
  LEADS_CREATE: 'leads:create',
  LEADS_EDIT: 'leads:edit',
  LEADS_DELETE: 'leads:delete',
  LEADS_ASSIGN: 'leads:assign',
  LEADS_CHANGE_STAGE: 'leads:change_stage',
  LEADS_LOG_CALL: 'leads:log_call',
  LEADS_EXPORT: 'leads:export',

  // Admissions
  ADMISSIONS_VIEW: 'admissions:view',
  ADMISSIONS_REVIEW: 'admissions:review',
  ADMISSIONS_APPROVE: 'admissions:approve',
  ADMISSIONS_REJECT: 'admissions:reject',
  ADMISSIONS_CREATE_OFFER: 'admissions:create_offer',

  // Course Management
  COURSES_VIEW: 'courses:view',
  COURSES_CREATE: 'courses:create',
  COURSES_EDIT: 'courses:edit',
  COURSES_DELETE: 'courses:delete',
  BATCHES_MANAGE: 'batches:manage',

  // Student Information System
  STUDENTS_VIEW: 'students:view',
  STUDENTS_VIEW_ALL: 'students:view_all',
  STUDENTS_CREATE: 'students:create',
  STUDENTS_EDIT: 'students:edit',
  STUDENTS_DELETE: 'students:delete',
  STUDENTS_VIEW_PROFILE: 'students:view_profile',

  // Academic (Attendance & Grades)
  ATTENDANCE_VIEW: 'attendance:view',
  ATTENDANCE_MARK: 'attendance:mark',
  ATTENDANCE_EDIT: 'attendance:edit',
  GRADES_VIEW: 'grades:view',
  GRADES_ENTER: 'grades:enter',
  GRADES_PUBLISH: 'grades:publish',
  TRANSCRIPTS_GENERATE: 'transcripts:generate',

  // Finance & Invoicing
  FINANCE_VIEW: 'finance:view',
  FINANCE_INVOICE_CREATE: 'finance:invoice_create',
  FINANCE_INVOICE_EDIT: 'finance:invoice_edit',
  FINANCE_PAYMENT_RECORD: 'finance:payment_record',
  FINANCE_DISCOUNT_APPLY: 'finance:discount_apply',
  FINANCE_REPORTS: 'finance:reports',

  // Support Helpdesk
  TICKETS_VIEW_OWN: 'tickets:view_own',
  TICKETS_VIEW_ALL: 'tickets:view_all',
  TICKETS_CREATE: 'tickets:create',
  TICKETS_REPLY: 'tickets:reply',
  TICKETS_ASSIGN: 'tickets:assign',
  TICKETS_RESOLVE: 'tickets:resolve',
  TICKETS_CLOSE: 'tickets:close',

  // Communications & Notifications
  NOTIFICATIONS_VIEW: 'notifications:view',
  NOTIFICATIONS_BROADCAST: 'notifications:broadcast',
  ANNOUNCEMENTS_MANAGE: 'announcements:manage',

  // Analytics & Reporting
  ANALYTICS_VIEW_DASHBOARD: 'analytics:view_dashboard',
  ANALYTICS_FINANCIAL: 'analytics:financial',
  ANALYTICS_ACADEMIC: 'analytics:academic',
  ANALYTICS_CONVERSION: 'analytics:conversion',
  REPORTS_EXPORT: 'reports:export',

  // System Settings
  SETTINGS_VIEW: 'settings:view',
  SETTINGS_MANAGE: 'settings:manage'
};

const ROLE_PERMISSIONS = {
  [ROLES.SUPER_ADMIN]: Object.values(PERMISSIONS),

  [ROLES.ADMIN]: [
    PERMISSIONS.AUTH_LOGIN,
    PERMISSIONS.AUTH_MANAGE_USERS,
    PERMISSIONS.AUTH_VIEW_AUDIT_LOGS,
    PERMISSIONS.LEADS_VIEW,
    PERMISSIONS.LEADS_VIEW_ALL,
    PERMISSIONS.LEADS_CREATE,
    PERMISSIONS.LEADS_EDIT,
    PERMISSIONS.LEADS_DELETE,
    PERMISSIONS.LEADS_ASSIGN,
    PERMISSIONS.LEADS_CHANGE_STAGE,
    PERMISSIONS.LEADS_LOG_CALL,
    PERMISSIONS.LEADS_EXPORT,
    PERMISSIONS.ADMISSIONS_VIEW,
    PERMISSIONS.ADMISSIONS_REVIEW,
    PERMISSIONS.ADMISSIONS_APPROVE,
    PERMISSIONS.ADMISSIONS_REJECT,
    PERMISSIONS.ADMISSIONS_CREATE_OFFER,
    PERMISSIONS.COURSES_VIEW,
    PERMISSIONS.COURSES_CREATE,
    PERMISSIONS.COURSES_EDIT,
    PERMISSIONS.COURSES_DELETE,
    PERMISSIONS.BATCHES_MANAGE,
    PERMISSIONS.STUDENTS_VIEW,
    PERMISSIONS.STUDENTS_VIEW_ALL,
    PERMISSIONS.STUDENTS_CREATE,
    PERMISSIONS.STUDENTS_EDIT,
    PERMISSIONS.STUDENTS_DELETE,
    PERMISSIONS.STUDENTS_VIEW_PROFILE,
    PERMISSIONS.ATTENDANCE_VIEW,
    PERMISSIONS.ATTENDANCE_MARK,
    PERMISSIONS.ATTENDANCE_EDIT,
    PERMISSIONS.GRADES_VIEW,
    PERMISSIONS.GRADES_ENTER,
    PERMISSIONS.GRADES_PUBLISH,
    PERMISSIONS.TRANSCRIPTS_GENERATE,
    PERMISSIONS.FINANCE_VIEW,
    PERMISSIONS.FINANCE_INVOICE_CREATE,
    PERMISSIONS.FINANCE_INVOICE_EDIT,
    PERMISSIONS.FINANCE_PAYMENT_RECORD,
    PERMISSIONS.FINANCE_DISCOUNT_APPLY,
    PERMISSIONS.FINANCE_REPORTS,
    PERMISSIONS.TICKETS_VIEW_OWN,
    PERMISSIONS.TICKETS_VIEW_ALL,
    PERMISSIONS.TICKETS_CREATE,
    PERMISSIONS.TICKETS_REPLY,
    PERMISSIONS.TICKETS_ASSIGN,
    PERMISSIONS.TICKETS_RESOLVE,
    PERMISSIONS.TICKETS_CLOSE,
    PERMISSIONS.NOTIFICATIONS_VIEW,
    PERMISSIONS.NOTIFICATIONS_BROADCAST,
    PERMISSIONS.ANNOUNCEMENTS_MANAGE,
    PERMISSIONS.ANALYTICS_VIEW_DASHBOARD,
    PERMISSIONS.ANALYTICS_FINANCIAL,
    PERMISSIONS.ANALYTICS_ACADEMIC,
    PERMISSIONS.ANALYTICS_CONVERSION,
    PERMISSIONS.REPORTS_EXPORT,
    PERMISSIONS.SETTINGS_VIEW,
    PERMISSIONS.SETTINGS_MANAGE
  ],

  [ROLES.COUNSELOR]: [
    PERMISSIONS.AUTH_LOGIN,
    PERMISSIONS.LEADS_VIEW,
    PERMISSIONS.LEADS_VIEW_ALL,
    PERMISSIONS.LEADS_CREATE,
    PERMISSIONS.LEADS_EDIT,
    PERMISSIONS.LEADS_CHANGE_STAGE,
    PERMISSIONS.LEADS_LOG_CALL,
    PERMISSIONS.LEADS_EXPORT,
    PERMISSIONS.ADMISSIONS_VIEW,
    PERMISSIONS.ADMISSIONS_REVIEW,
    PERMISSIONS.ADMISSIONS_CREATE_OFFER,
    PERMISSIONS.COURSES_VIEW,
    PERMISSIONS.STUDENTS_VIEW,
    PERMISSIONS.STUDENTS_VIEW_PROFILE,
    PERMISSIONS.TICKETS_VIEW_OWN,
    PERMISSIONS.TICKETS_CREATE,
    PERMISSIONS.TICKETS_REPLY,
    PERMISSIONS.NOTIFICATIONS_VIEW,
    PERMISSIONS.ANALYTICS_VIEW_DASHBOARD,
    PERMISSIONS.ANALYTICS_CONVERSION
  ],

  [ROLES.INSTRUCTOR]: [
    PERMISSIONS.AUTH_LOGIN,
    PERMISSIONS.COURSES_VIEW,
    PERMISSIONS.STUDENTS_VIEW,
    PERMISSIONS.STUDENTS_VIEW_PROFILE,
    PERMISSIONS.ATTENDANCE_VIEW,
    PERMISSIONS.ATTENDANCE_MARK,
    PERMISSIONS.ATTENDANCE_EDIT,
    PERMISSIONS.GRADES_VIEW,
    PERMISSIONS.GRADES_ENTER,
    PERMISSIONS.GRADES_PUBLISH,
    PERMISSIONS.TRANSCRIPTS_GENERATE,
    PERMISSIONS.TICKETS_VIEW_OWN,
    PERMISSIONS.TICKETS_CREATE,
    PERMISSIONS.TICKETS_REPLY,
    PERMISSIONS.NOTIFICATIONS_VIEW,
    PERMISSIONS.ANALYTICS_VIEW_DASHBOARD,
    PERMISSIONS.ANALYTICS_ACADEMIC
  ],

  [ROLES.FINANCE_OFFICER]: [
    PERMISSIONS.AUTH_LOGIN,
    PERMISSIONS.STUDENTS_VIEW,
    PERMISSIONS.STUDENTS_VIEW_PROFILE,
    PERMISSIONS.FINANCE_VIEW,
    PERMISSIONS.FINANCE_INVOICE_CREATE,
    PERMISSIONS.FINANCE_INVOICE_EDIT,
    PERMISSIONS.FINANCE_PAYMENT_RECORD,
    PERMISSIONS.FINANCE_DISCOUNT_APPLY,
    PERMISSIONS.FINANCE_REPORTS,
    PERMISSIONS.TICKETS_VIEW_OWN,
    PERMISSIONS.TICKETS_VIEW_ALL,
    PERMISSIONS.TICKETS_CREATE,
    PERMISSIONS.TICKETS_REPLY,
    PERMISSIONS.TICKETS_RESOLVE,
    PERMISSIONS.NOTIFICATIONS_VIEW,
    PERMISSIONS.ANALYTICS_VIEW_DASHBOARD,
    PERMISSIONS.ANALYTICS_FINANCIAL,
    PERMISSIONS.REPORTS_EXPORT
  ],

  [ROLES.STUDENT]: [
    PERMISSIONS.AUTH_LOGIN,
    PERMISSIONS.COURSES_VIEW,
    PERMISSIONS.STUDENTS_VIEW_PROFILE,
    PERMISSIONS.ATTENDANCE_VIEW,
    PERMISSIONS.GRADES_VIEW,
    PERMISSIONS.FINANCE_VIEW,
    PERMISSIONS.TICKETS_VIEW_OWN,
    PERMISSIONS.TICKETS_CREATE,
    PERMISSIONS.TICKETS_REPLY,
    PERMISSIONS.NOTIFICATIONS_VIEW
  ],

  [ROLES.PARENT]: [
    PERMISSIONS.AUTH_LOGIN,
    PERMISSIONS.COURSES_VIEW,
    PERMISSIONS.STUDENTS_VIEW_PROFILE,
    PERMISSIONS.ATTENDANCE_VIEW,
    PERMISSIONS.GRADES_VIEW,
    PERMISSIONS.FINANCE_VIEW,
    PERMISSIONS.TICKETS_VIEW_OWN,
    PERMISSIONS.TICKETS_CREATE,
    PERMISSIONS.TICKETS_REPLY,
    PERMISSIONS.NOTIFICATIONS_VIEW
  ]
};

function hasPermission(role, permission) {
  if (!role || !ROLE_PERMISSIONS[role]) return false;
  return ROLE_PERMISSIONS[role].includes(permission);
}

function hasAnyPermission(role, permissions = []) {
  if (!role || !ROLE_PERMISSIONS[role]) return false;
  return permissions.some(p => ROLE_PERMISSIONS[role].includes(p));
}

function hasAllPermissions(role, permissions = []) {
  if (!role || !ROLE_PERMISSIONS[role]) return false;
  return permissions.every(p => ROLE_PERMISSIONS[role].includes(p));
}

module.exports = {
  ROLES,
  PERMISSIONS,
  ROLE_PERMISSIONS,
  hasPermission,
  hasAnyPermission,
  hasAllPermissions
};
""")

    # config/constants.js
    write("config/constants.js", """'use strict';

/**
 * Global EduPulse Constants & Enumerations
 */

const LEAD_STAGES = {
  NEW: 'new',
  CONTACTED: 'contacted',
  QUALIFIED: 'qualified',
  COUNSELING_SCHEDULED: 'counseling_scheduled',
  APPLICATION_SUBMITTED: 'application_submitted',
  ENROLLED: 'enrolled',
  UNQUALIFIED: 'unqualified',
  LOST: 'lost'
};

const LEAD_SOURCES = {
  WEBSITE: 'Website Inbound',
  GOOGLE_ADS: 'Google Search Ads',
  SOCIAL_MEDIA: 'Social Media Campaign',
  EDUCATION_FAIR: 'Education Fair 2026',
  ALUMNI_REFERRAL: 'Alumni Referral',
  PARTNER_AGENT: 'Educational Partner Agent',
  DIRECT_WALK_IN: 'Direct Campus Walk-in',
  CAMPUS_SEMINAR: 'Campus Seminar'
};

const APPLICATION_STATUSES = {
  DRAFT: 'draft',
  SUBMITTED: 'submitted',
  UNDER_REVIEW: 'under_review',
  INTERVIEW_SCHEDULED: 'interview_scheduled',
  ACCEPTED: 'accepted',
  REJECTED: 'rejected',
  WAITLISTED: 'waitlisted',
  ENROLLED: 'enrolled'
};

const ENROLLMENT_STATUSES = {
  ACTIVE: 'active',
  GRADUATED: 'graduated',
  SUSPENDED: 'suspended',
  ON_LEAVE: 'on_leave',
  WITHDRAWN: 'withdrawn'
};

const INVOICE_STATUSES = {
  DRAFT: 'draft',
  PENDING: 'pending',
  PAID: 'paid',
  PARTIALLY_PAID: 'partially_paid',
  OVERDUE: 'overdue',
  CANCELLED: 'cancelled',
  REFUNDED: 'refunded'
};

const PAYMENT_METHODS = {
  CREDIT_CARD: 'credit_card',
  DEBIT_CARD: 'debit_card',
  BANK_TRANSFER: 'bank_transfer',
  UPI: 'upi',
  STRIPE_ONLINE: 'stripe_online',
  CHEQUE: 'cheque',
  CASH: 'cash',
  SCHOLARSHIP_CREDIT: 'scholarship_credit'
};

const ATTENDANCE_STATUSES = {
  PRESENT: 'present',
  ABSENT: 'absent',
  LATE: 'late',
  EXCUSED: 'excused',
  HALFDAY: 'half_day'
};

const TICKET_PRIORITIES = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  CRITICAL: 'critical'
};

const TICKET_STATUSES = {
  OPEN: 'open',
  IN_PROGRESS: 'in_progress',
  WAITING_ON_STUDENT: 'waiting_on_student',
  RESOLVED: 'resolved',
  CLOSED: 'closed'
};

const TICKET_CATEGORIES = {
  ADMISSIONS: 'Admissions & Enrollment',
  FEES_FINANCE: 'Fees & Invoicing',
  ACADEMIC: 'Academic & Curriculum',
  EXAMINATIONS: 'Examinations & Grades',
  ATTENDANCE: 'Attendance Records',
  TECHNICAL: 'Technical & Portal Access',
  HOSTEL_TRANSPORT: 'Hostel & Transportation',
  OTHER: 'General Support'
};

const DEPARTMENTS = {
  CS_IT: 'Computer Science & Software Engineering',
  DATA_AI: 'Data Science & Artificial Intelligence',
  BUSINESS: 'Business Administration & Management',
  DESIGN: 'UI/UX & Digital Media Design',
  HEALTHCARE: 'Health Informatics & Nursing',
  ENGINEERING: 'Robotics & Electrical Systems'
};

module.exports = {
  LEAD_STAGES,
  LEAD_SOURCES,
  APPLICATION_STATUSES,
  ENROLLMENT_STATUSES,
  INVOICE_STATUSES,
  PAYMENT_METHODS,
  ATTENDANCE_STATUSES,
  TICKET_PRIORITIES,
  TICKET_STATUSES,
  TICKET_CATEGORIES,
  DEPARTMENTS
};
""")

    # config/database.js
    write("config/database.js", """'use strict';

/**
 * Database connection and configuration helper
 */

const path = require('path');
const config = require('./app.config');

module.exports = {
  client: 'sqlite3',
  connection: {
    filename: config.database.filePath
  },
  useNullAsDefault: true,
  pool: {
    min: 2,
    max: 10
  }
};
""")

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent.parent)
