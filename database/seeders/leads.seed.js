'use strict';

/**
 * Seed data for prospective student leads across various stages and counselors
 */

const leadsSeed = [
  {
    id: 'lead_001',
    first_name: 'Vikram',
    last_name: 'Patel',
    email: 'vikram.patel@gmail.com',
    phone: '+91-9820011223',
    alternate_phone: '+91-9820011224',
    source: 'Website Inbound',
    stage: 'qualified',
    interested_course_id: 'crs_cs_01',
    assigned_counselor_id: 'usr_counselor_01',
    lead_score: 85,
    budget_range: '$10,000 - $15,000',
    preferred_intake: 'Fall 2026',
    country: 'India',
    city: 'Mumbai',
    notes: 'Strong Python background, completed 12th with 92% in PCM. Very keen on Full-Stack track.',
    qualification_status: 'High Intent',
    last_contacted_at: '2026-08-25T14:30:00Z',
    next_follow_up_date: '2026-09-02T10:00:00Z'
  },
  {
    id: 'lead_002',
    first_name: 'Pooja',
    last_name: 'Nair',
    email: 'pooja.nair@outlook.com',
    phone: '+91-9745123456',
    source: 'Google Search Ads',
    stage: 'counseling_scheduled',
    interested_course_id: 'crs_ai_01',
    assigned_counselor_id: 'usr_counselor_02',
    lead_score: 92,
    budget_range: '$15,000+',
    preferred_intake: 'Fall 2026',
    country: 'India',
    city: 'Bangalore',
    notes: 'B.Tech graduate in ECE with 2 years IT experience. Looking to pivot to AI research.',
    qualification_status: 'Eligible & High Intent',
    last_contacted_at: '2026-08-28T11:00:00Z',
    next_follow_up_date: '2026-09-01T15:00:00Z'
  },
  {
    id: 'lead_003',
    first_name: 'David',
    last_name: 'Miller',
    email: 'david.miller@yahoo.com',
    phone: '+1-555-789-0123',
    source: 'Education Fair 2026',
    stage: 'application_submitted',
    interested_course_id: 'crs_mba_01',
    assigned_counselor_id: 'usr_counselor_01',
    lead_score: 78,
    budget_range: '$18,000+',
    preferred_intake: 'Fall 2026',
    country: 'USA',
    city: 'Chicago',
    notes: 'Submitted resume and SOP. Waiting for academic transcript verification.',
    qualification_status: 'Application Under Review',
    last_contacted_at: '2026-08-29T16:00:00Z',
    next_follow_up_date: '2026-09-03T11:30:00Z'
  },
  {
    id: 'lead_004',
    first_name: 'Fatima',
    last_name: 'Al-Mansoor',
    email: 'fatima.mansoor@gmail.com',
    phone: '+971-50-1234567',
    source: 'Social Media Campaign',
    stage: 'new',
    interested_course_id: 'crs_ux_01',
    assigned_counselor_id: 'usr_counselor_02',
    lead_score: 65,
    budget_range: '$3,000 - $5,000',
    preferred_intake: 'Winter 2026',
    country: 'UAE',
    city: 'Dubai',
    notes: 'Downloaded brochure from Instagram ad. Needs intro counseling call.',
    qualification_status: 'Pending Contact',
    last_contacted_at: null,
    next_follow_up_date: '2026-09-01T14:00:00Z'
  },
  {
    id: 'lead_005',
    first_name: 'Karthik',
    last_name: 'Subramanian',
    email: 'karthik.sub@gmail.com',
    phone: '+91-9884012345',
    source: 'Alumni Referral',
    stage: 'enrolled',
    interested_course_id: 'crs_cs_01',
    assigned_counselor_id: 'usr_counselor_01',
    lead_score: 98,
    budget_range: '$12,500',
    preferred_intake: 'Fall 2026',
    country: 'India',
    city: 'Chennai',
    notes: 'Converted! Enrolled as Student ID STU-2026-003.',
    qualification_status: 'Enrolled',
    last_contacted_at: '2026-08-30T09:00:00Z',
    next_follow_up_date: null
  },
  {
    id: 'lead_006',
    first_name: 'Elena',
    last_name: 'Popova',
    email: 'elena.popova@mail.ru',
    phone: '+7-903-1234567',
    source: 'Partner Agent',
    stage: 'contacted',
    interested_course_id: 'crs_cyber_01',
    assigned_counselor_id: 'usr_counselor_01',
    lead_score: 72,
    budget_range: '$10,000 - $15,000',
    preferred_intake: 'Spring 2027',
    country: 'Germany',
    city: 'Berlin',
    notes: 'Spoke over WhatsApp. Sent curriculum outline and fee installment details.',
    qualification_status: 'Interested',
    last_contacted_at: '2026-08-27T12:00:00Z',
    next_follow_up_date: '2026-09-04T16:00:00Z'
  }
];

const leadInteractionsSeed = [
  {
    id: 'intr_001',
    lead_id: 'lead_001',
    user_id: 'usr_counselor_01',
    interaction_type: 'phone_call',
    summary: 'Introductory 20-minute discussion regarding CS program syllabus and lab infrastructure.',
    outcome: 'Interested in taking entrance assessment test next week.',
    duration_minutes: 20,
    scheduled_follow_up: '2026-09-02T10:00:00Z',
    created_at: '2026-08-25T14:30:00Z'
  },
  {
    id: 'intr_002',
    lead_id: 'lead_002',
    user_id: 'usr_counselor_02',
    interaction_type: 'campus_visit',
    summary: 'Candidate visited campus AI lab with parents. Met Prof. Ada Lovelace.',
    outcome: 'Extremely impressed with GPU cluster setup. Requested application portal link.',
    duration_minutes: 60,
    scheduled_follow_up: '2026-09-01T15:00:00Z',
    created_at: '2026-08-28T11:00:00Z'
  }
];

module.exports = { leadsSeed, leadInteractionsSeed };
