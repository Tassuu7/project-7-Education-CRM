'use strict';

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
