'use strict';

/**
 * Seed data for support helpdesk tickets and replies
 */

const ticketsSeed = [
  {
    id: 'tkt_001',
    ticket_number: 'TKT-2026-1042',
    user_id: 'usr_student_01',
    category: 'Technical & Portal Access',
    priority: 'medium',
    status: 'resolved',
    subject: 'Unable to access GPU lab JupyterHub cluster',
    description: 'When logging into the AI sandbox JupyterHub with my university SSO, I receive a 403 Forbidden error.',
    assigned_to_user_id: 'usr_admin_01',
    resolution_notes: 'Permissions provisioned on Kubernetes namespace. Verified access.',
    resolved_at: '2026-08-27T16:00:00Z'
  },
  {
    id: 'tkt_002',
    ticket_number: 'TKT-2026-1043',
    user_id: 'usr_student_02',
    category: 'Fees & Invoicing',
    priority: 'low',
    status: 'open',
    subject: 'Request for official fee tax exemption receipt',
    description: 'Need an official stamped receipt for tax filing under section 80E.',
    assigned_to_user_id: 'usr_finance_01',
    resolution_notes: null,
    resolved_at: null
  },
  {
    id: 'tkt_003',
    ticket_number: 'TKT-2026-1044',
    user_id: 'usr_counselor_01',
    category: 'Admissions & Enrollment',
    priority: 'high',
    status: 'in_progress',
    subject: 'Urgent document verification for international candidate Elena Popova',
    description: 'Candidate needs express verification for German embassy visa appointment next Tuesday.',
    assigned_to_user_id: 'usr_admin_01',
    resolution_notes: null,
    resolved_at: null
  }
];

const ticketRepliesSeed = [
  {
    id: 'rep_001',
    ticket_id: 'tkt_001',
    user_id: 'usr_admin_01',
    message: 'Hello Rohit, we have synced your LDAP groups with the GPU cluster. Please try logging in again.',
    is_staff_reply: 1,
    created_at: '2026-08-27T15:30:00Z'
  },
  {
    id: 'rep_002',
    ticket_id: 'tkt_001',
    user_id: 'usr_student_01',
    message: 'Works perfectly now! Thank you so much for the quick resolution.',
    is_staff_reply: 0,
    created_at: '2026-08-27T15:55:00Z'
  }
];

module.exports = { ticketsSeed, ticketRepliesSeed };
