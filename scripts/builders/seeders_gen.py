#!/usr/bin/env python3
"""
EduPulse CRM - Seeders Generator
Generates realistic seed datasets across all 15 tables with dozens of records per module.
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

    # database/seeders/users.seed.js
    write("database/seeders/users.seed.js", """'use strict';

/**
 * Seed data for system users across all roles
 */

const crypto = require('crypto');

function hashPassword(pwd) {
  return crypto.createHash('sha256').update(pwd + 'edupulse_salt_2026').digest('hex');
}

const usersSeed = [
  {
    id: 'usr_superadmin_01',
    username: 'superadmin',
    email: 'superadmin@edupulse.edu',
    password_hash: hashPassword('admin123'),
    first_name: 'Alexander',
    last_name: 'Vance',
    role: 'super_admin',
    phone: '+1-555-0100',
    avatar_url: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
    is_active: 1,
    last_login_at: new Date().toISOString()
  },
  {
    id: 'usr_admin_01',
    username: 'admin',
    email: 'admin@edupulse.edu',
    password_hash: hashPassword('admin123'),
    first_name: 'Sarah',
    last_name: 'Connor',
    role: 'admin',
    phone: '+1-555-0101',
    avatar_url: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150',
    is_active: 1,
    last_login_at: new Date().toISOString()
  },
  {
    id: 'usr_counselor_01',
    username: 'counselor_rachel',
    email: 'rachel.green@edupulse.edu',
    password_hash: hashPassword('counselor123'),
    first_name: 'Rachel',
    last_name: 'Green',
    role: 'counselor',
    phone: '+1-555-0102',
    avatar_url: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150',
    is_active: 1,
    last_login_at: new Date().toISOString()
  },
  {
    id: 'usr_counselor_02',
    username: 'counselor_ross',
    email: 'ross.geller@edupulse.edu',
    password_hash: hashPassword('counselor123'),
    first_name: 'Ross',
    last_name: 'Geller',
    role: 'counselor',
    phone: '+1-555-0103',
    avatar_url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150',
    is_active: 1,
    last_login_at: new Date().toISOString()
  },
  {
    id: 'usr_instructor_01',
    username: 'prof_alan',
    email: 'alan.turing@edupulse.edu',
    password_hash: hashPassword('faculty123'),
    first_name: 'Dr. Alan',
    last_name: 'Turing',
    role: 'instructor',
    phone: '+1-555-0104',
    avatar_url: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150',
    is_active: 1,
    last_login_at: new Date().toISOString()
  },
  {
    id: 'usr_instructor_02',
    username: 'prof_ada',
    email: 'ada.lovelace@edupulse.edu',
    password_hash: hashPassword('faculty123'),
    first_name: 'Prof. Ada',
    last_name: 'Lovelace',
    role: 'instructor',
    phone: '+1-555-0105',
    avatar_url: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150',
    is_active: 1,
    last_login_at: new Date().toISOString()
  },
  {
    id: 'usr_instructor_03',
    username: 'prof_richard',
    email: 'richard.feynman@edupulse.edu',
    password_hash: hashPassword('faculty123'),
    first_name: 'Dr. Richard',
    last_name: 'Feynman',
    role: 'instructor',
    phone: '+1-555-0106',
    avatar_url: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150',
    is_active: 1,
    last_login_at: new Date().toISOString()
  },
  {
    id: 'usr_finance_01',
    username: 'finance_elena',
    email: 'elena.rostova@edupulse.edu',
    password_hash: hashPassword('finance123'),
    first_name: 'Elena',
    last_name: 'Rostova',
    role: 'finance_officer',
    phone: '+1-555-0107',
    avatar_url: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150',
    is_active: 1,
    last_login_at: new Date().toISOString()
  },
  {
    id: 'usr_student_01',
    username: 'student_rohit',
    email: 'rohit.sharma@student.edupulse.edu',
    password_hash: hashPassword('student123'),
    first_name: 'Rohit',
    last_name: 'Sharma',
    role: 'student',
    phone: '+91-9876543210',
    avatar_url: 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150',
    is_active: 1,
    last_login_at: new Date().toISOString()
  },
  {
    id: 'usr_student_02',
    username: 'student_ananya',
    email: 'ananya.iyer@student.edupulse.edu',
    password_hash: hashPassword('student123'),
    first_name: 'Ananya',
    last_name: 'Iyer',
    role: 'student',
    phone: '+91-9876543211',
    avatar_url: 'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=150',
    is_active: 1,
    last_login_at: new Date().toISOString()
  },
  {
    id: 'usr_parent_01',
    username: 'parent_ramesh',
    email: 'ramesh.sharma@gmail.com',
    password_hash: hashPassword('parent123'),
    first_name: 'Ramesh',
    last_name: 'Sharma',
    role: 'parent',
    phone: '+91-9876500001',
    avatar_url: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150',
    is_active: 1,
    last_login_at: new Date().toISOString()
  }
];

module.exports = { usersSeed, hashPassword };
""")

    # database/seeders/courses.seed.js
    write("database/seeders/courses.seed.js", """'use strict';

/**
 * Seed data for course catalog, syllabi, and batches
 */

const coursesSeed = [
  {
    id: 'crs_cs_01',
    code: 'CS-401',
    title: 'B.Sc in Computer Science & Full-Stack Engineering',
    department: 'Computer Science & Software Engineering',
    degree_level: 'Bachelor',
    duration_months: 36,
    total_credits: 120,
    base_tuition_fee: 12500.00,
    description: 'Comprehensive software engineering program covering algorithms, cloud microservices, and modern web architectures.',
    syllabus_outline: 'Semester 1: CS Fundamentals & Python | Semester 2: Data Structures & C++ | Semester 3: Web Architectures & DBs | Semester 4: Distributed Systems | Semester 5: DevOps & Cloud | Semester 6: Capstone Project',
    is_active: 1
  },
  {
    id: 'crs_ai_01',
    code: 'AI-502',
    title: 'M.Sc in Artificial Intelligence & Machine Learning',
    department: 'Data Science & Artificial Intelligence',
    degree_level: 'Master',
    duration_months: 24,
    total_credits: 64,
    base_tuition_fee: 16000.00,
    description: 'Advanced postgraduate degree focusing on Deep Learning, Transformers, NLP, Computer Vision, and Reinforcement Learning.',
    syllabus_outline: 'Sem 1: Mathematical Foundations & Stat ML | Sem 2: Deep Neural Networks & PyTorch | Sem 3: LLMs & Generative AI | Sem 4: Thesis & Industrial Practicum',
    is_active: 1
  },
  {
    id: 'crs_ds_01',
    code: 'DS-301',
    title: 'Diploma in Data Analytics & Business Intelligence',
    department: 'Data Science & Artificial Intelligence',
    degree_level: 'Diploma',
    duration_months: 12,
    total_credits: 36,
    base_tuition_fee: 6500.00,
    description: 'Practical hands-on diploma in SQL, Python, PowerBI, Tableau, and predictive statistical analytics.',
    syllabus_outline: 'Module 1: Advanced SQL & Warehousing | Module 2: Python for Data Analysis | Module 3: PowerBI & Tableau Dashboards | Module 4: Predictive Modeling',
    is_active: 1
  },
  {
    id: 'crs_mba_01',
    code: 'MBA-601',
    title: 'Master of Business Administration (Tech Leadership)',
    department: 'Business Administration & Management',
    degree_level: 'Master',
    duration_months: 24,
    total_credits: 72,
    base_tuition_fee: 18500.00,
    description: 'Executive MBA curriculum integrating corporate strategy, product management, venture finance, and technology innovation.',
    syllabus_outline: 'Year 1: Strategic Management, Financial Accounting, Marketing | Year 2: Tech Product Strategy, Venture Capital, Corporate Governance',
    is_active: 1
  },
  {
    id: 'crs_ux_01',
    code: 'UX-201',
    title: 'Professional Certificate in UI/UX Design & Figma',
    department: 'UI/UX & Digital Media Design',
    degree_level: 'Certificate',
    duration_months: 6,
    total_credits: 18,
    base_tuition_fee: 3200.00,
    description: 'Intensive immersion into user research, wireframing, design systems, interactive Figma prototyping, and usability testing.',
    syllabus_outline: 'Month 1-2: UX Research & User Journeys | Month 3-4: UI Systems & Typography | Month 5-6: Design Systems, Micro-interactions & Portfolio',
    is_active: 1
  },
  {
    id: 'crs_cyber_01',
    code: 'CY-405',
    title: 'B.Sc in Cybersecurity & Ethical Hacking',
    department: 'Computer Science & Software Engineering',
    degree_level: 'Bachelor',
    duration_months: 36,
    total_credits: 120,
    base_tuition_fee: 13500.00,
    description: 'Hands-on offensive and defensive cybersecurity covering network defense, penetration testing, malware reverse-engineering, and incident response.',
    syllabus_outline: 'Year 1: Network Protocols & Linux | Year 2: Cryptography & Pen-testing | Year 3: Cloud Security, SOC Operations & Forensics',
    is_active: 1
  }
];

const courseModulesSeed = [
  { id: 'mod_cs_101', course_id: 'crs_cs_01', module_code: 'CS101', title: 'Data Structures & Algorithms', semester_number: 1, credits: 4, instructor_id: 'usr_instructor_01' },
  { id: 'mod_cs_102', course_id: 'crs_cs_01', module_code: 'CS102', title: 'Relational Database Management Systems', semester_number: 1, credits: 4, instructor_id: 'usr_instructor_02' },
  { id: 'mod_cs_201', course_id: 'crs_cs_01', module_code: 'CS201', title: 'Modern Full-Stack Web Development', semester_number: 2, credits: 4, instructor_id: 'usr_instructor_01' },
  { id: 'mod_cs_202', course_id: 'crs_cs_01', module_code: 'CS202', title: 'Computer Networks & Operating Systems', semester_number: 2, credits: 4, instructor_id: 'usr_instructor_03' },
  { id: 'mod_ai_501', course_id: 'crs_ai_01', module_code: 'AI501', title: 'Deep Learning & Neural Architectures', semester_number: 1, credits: 4, instructor_id: 'usr_instructor_02' },
  { id: 'mod_ai_502', course_id: 'crs_ai_01', module_code: 'AI502', title: 'Natural Language Processing & LLMs', semester_number: 1, credits: 4, instructor_id: 'usr_instructor_02' }
];

const batchesSeed = [
  {
    id: 'batch_cs_2026_a',
    course_id: 'crs_cs_01',
    batch_name: 'CS Fall 2026 - Cohort Alpha',
    cohort_code: 'CS-2026-A',
    start_date: '2026-09-01',
    end_date: '2029-06-30',
    max_capacity: 45,
    current_enrolled: 32,
    lead_instructor_id: 'usr_instructor_01',
    classroom_location: 'Science Block - Lab 301',
    status: 'active'
  },
  {
    id: 'batch_ai_2026_a',
    course_id: 'crs_ai_01',
    batch_name: 'AI Master 2026 - Evening Cohort',
    cohort_code: 'AI-2026-E',
    start_date: '2026-09-15',
    end_date: '2028-06-30',
    max_capacity: 30,
    current_enrolled: 24,
    lead_instructor_id: 'usr_instructor_02',
    classroom_location: 'AI Research Hall - Room 102',
    status: 'active'
  },
  {
    id: 'batch_ds_2026_b',
    course_id: 'crs_ds_01',
    batch_name: 'Data Analytics Weekend Batch B',
    cohort_code: 'DS-2026-WKND',
    start_date: '2026-10-01',
    end_date: '2027-09-30',
    max_capacity: 35,
    current_enrolled: 18,
    lead_instructor_id: 'usr_instructor_03',
    classroom_location: 'Digital Learning Hub 4',
    status: 'upcoming'
  }
];

module.exports = { coursesSeed, courseModulesSeed, batchesSeed };
""")

    # database/seeders/leads.seed.js
    write("database/seeders/leads.seed.js", """'use strict';

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
""")

    # database/seeders/students.seed.js
    write("database/seeders/students.seed.js", """'use strict';

/**
 * Seed data for enrolled students and admissions applications
 */

const applicationsSeed = [
  {
    id: 'app_2026_001',
    lead_id: 'lead_005',
    course_id: 'crs_cs_01',
    first_name: 'Rohit',
    last_name: 'Sharma',
    email: 'rohit.sharma@student.edupulse.edu',
    phone: '+91-9876543210',
    dob: '2005-04-30',
    gender: 'Male',
    high_school_percentage: 94.5,
    entrance_exam_score: 91.0,
    status: 'enrolled',
    reviewer_id: 'usr_admin_01',
    review_notes: 'Exceptional math and analytical aptitude. Approved for enrollment.',
    applied_at: '2026-07-10T10:00:00Z',
    decision_at: '2026-07-15T16:00:00Z'
  },
  {
    id: 'app_2026_002',
    lead_id: null,
    course_id: 'crs_ai_01',
    first_name: 'Ananya',
    last_name: 'Iyer',
    email: 'ananya.iyer@student.edupulse.edu',
    phone: '+91-9876543211',
    dob: '2002-11-15',
    gender: 'Female',
    high_school_percentage: 92.0,
    entrance_exam_score: 95.5,
    status: 'enrolled',
    reviewer_id: 'usr_admin_01',
    review_notes: 'Direct admission based on top 1% percentile in state entrance test.',
    applied_at: '2026-07-12T11:30:00Z',
    decision_at: '2026-07-18T14:00:00Z'
  }
];

const studentsSeed = [
  {
    id: 'stu_001',
    user_id: 'usr_student_01',
    student_id_number: 'STU-2026-001',
    application_id: 'app_2026_001',
    first_name: 'Rohit',
    last_name: 'Sharma',
    email: 'rohit.sharma@student.edupulse.edu',
    phone: '+91-9876543210',
    dob: '2005-04-30',
    blood_group: 'B+',
    address: 'Flat 402, Green Meadows, Andheri West',
    city: 'Mumbai',
    state: 'Maharashtra',
    guardian_name: 'Ramesh Sharma',
    guardian_phone: '+91-9876500001',
    guardian_email: 'ramesh.sharma@gmail.com',
    guardian_relation: 'Father',
    primary_course_id: 'crs_cs_01',
    current_batch_id: 'batch_cs_2026_a',
    current_semester: 1,
    enrollment_status: 'active',
    cumulative_gpa: 3.85,
    total_credits_earned: 16,
    enrolled_date: '2026-08-01'
  },
  {
    id: 'stu_002',
    user_id: 'usr_student_02',
    student_id_number: 'STU-2026-002',
    application_id: 'app_2026_002',
    first_name: 'Ananya',
    last_name: 'Iyer',
    email: 'ananya.iyer@student.edupulse.edu',
    phone: '+91-9876543211',
    dob: '2002-11-15',
    blood_group: 'O+',
    address: 'Plot 88, Indiranagar, 100ft Road',
    city: 'Bangalore',
    state: 'Karnataka',
    guardian_name: 'Venkatesh Iyer',
    guardian_phone: '+91-9876500002',
    guardian_email: 'venkat.iyer@gmail.com',
    guardian_relation: 'Father',
    primary_course_id: 'crs_ai_01',
    current_batch_id: 'batch_ai_2026_a',
    current_semester: 1,
    enrollment_status: 'active',
    cumulative_gpa: 3.95,
    total_credits_earned: 16,
    enrolled_date: '2026-08-01'
  }
];

module.exports = { applicationsSeed, studentsSeed };
""")

    # database/seeders/finance.seed.js
    write("database/seeders/finance.seed.js", """'use strict';

/**
 * Seed data for tuition fee invoices, payments, and receipts
 */

const invoicesSeed = [
  {
    id: 'inv_2026_001',
    invoice_number: 'INV-2026-8801',
    student_id: 'stu_001',
    course_id: 'crs_cs_01',
    title: 'Semester 1 Tuition & Laboratory Fee',
    amount: 4500.00,
    discount_amount: 500.00, // Merit scholarship
    tax_amount: 200.00,
    total_amount: 4200.00,
    amount_paid: 4200.00,
    balance_due: 0.00,
    due_date: '2026-08-15',
    status: 'paid',
    notes: 'Merit scholarship waiver applied ($500).'
  },
  {
    id: 'inv_2026_002',
    invoice_number: 'INV-2026-8802',
    student_id: 'stu_001',
    course_id: 'crs_cs_01',
    title: 'Semester 2 Tuition & Library Subscription',
    amount: 4500.00,
    discount_amount: 0.00,
    tax_amount: 225.00,
    total_amount: 4725.00,
    amount_paid: 2000.00,
    balance_due: 2725.00,
    due_date: '2026-12-15',
    status: 'partially_paid',
    notes: 'First installment of $2,000 received via UPI.'
  },
  {
    id: 'inv_2026_003',
    invoice_number: 'INV-2026-8803',
    student_id: 'stu_002',
    course_id: 'crs_ai_01',
    title: 'M.Sc AI Semester 1 GPU Lab & Tuition Fee',
    amount: 8000.00,
    discount_amount: 1000.00, // Dean Fellowship
    tax_amount: 350.00,
    total_amount: 7350.00,
    amount_paid: 7350.00,
    balance_due: 0.00,
    due_date: '2026-08-20',
    status: 'paid',
    notes: 'Paid in full via Bank Transfer.'
  }
];

const paymentsSeed = [
  {
    id: 'pay_2026_001',
    receipt_number: 'REC-2026-0199',
    invoice_id: 'inv_2026_001',
    student_id: 'stu_001',
    amount: 4200.00,
    payment_method: 'bank_transfer',
    transaction_reference: 'HDFC-N3920194821',
    payment_date: '2026-08-10T10:45:00Z',
    recorded_by_user_id: 'usr_finance_01',
    notes: 'Confirmed payment received in HDFC Institutional Account.'
  },
  {
    id: 'pay_2026_002',
    receipt_number: 'REC-2026-0200',
    invoice_id: 'inv_2026_002',
    student_id: 'stu_001',
    amount: 2000.00,
    payment_method: 'upi',
    transaction_reference: 'UPI-RAZORPAY-8829104',
    payment_date: '2026-08-20T15:20:00Z',
    recorded_by_user_id: 'usr_finance_01',
    notes: 'Installment 1 online gateway payment.'
  },
  {
    id: 'pay_2026_003',
    receipt_number: 'REC-2026-0201',
    invoice_id: 'inv_2026_003',
    student_id: 'stu_002',
    amount: 7350.00,
    payment_method: 'credit_card',
    transaction_reference: 'STRIPE-TXN-902184910',
    payment_date: '2026-08-18T12:15:00Z',
    recorded_by_user_id: 'usr_finance_01',
    notes: 'Processed via Stripe online gateway.'
  }
];

module.exports = { invoicesSeed, paymentsSeed };
""")

    # database/seeders/attendance.seed.js
    write("database/seeders/attendance.seed.js", """'use strict';

/**
 * Seed data for classroom sessions and attendance tracking
 */

const attendanceSessionsSeed = [
  {
    id: 'att_sess_001',
    batch_id: 'batch_cs_2026_a',
    course_id: 'crs_cs_01',
    module_id: 'mod_cs_101',
    instructor_id: 'usr_instructor_01',
    session_date: '2026-08-24',
    start_time: '09:00',
    end_time: '11:00',
    topic_covered: 'Graph Algorithms & Dijkstra Shortest Path'
  },
  {
    id: 'att_sess_002',
    batch_id: 'batch_cs_2026_a',
    course_id: 'crs_cs_01',
    module_id: 'mod_cs_102',
    instructor_id: 'usr_instructor_02',
    session_date: '2026-08-25',
    start_time: '11:30',
    end_time: '13:30',
    topic_covered: 'SQL Indexing & Query Plan Optimization'
  },
  {
    id: 'att_sess_003',
    batch_id: 'batch_ai_2026_a',
    course_id: 'crs_ai_01',
    module_id: 'mod_ai_501',
    instructor_id: 'usr_instructor_02',
    session_date: '2026-08-26',
    start_time: '14:00',
    end_time: '17:00',
    topic_covered: 'Backpropagation Calculus & Custom PyTorch Autograd'
  }
];

const attendanceRecordsSeed = [
  {
    id: 'att_rec_001',
    session_id: 'att_sess_001',
    student_id: 'stu_001',
    status: 'present',
    remarks: 'Active participation in live coding challenge.'
  },
  {
    id: 'att_rec_002',
    session_id: 'att_sess_002',
    student_id: 'stu_001',
    status: 'present',
    remarks: 'On time.'
  },
  {
    id: 'att_rec_003',
    session_id: 'att_sess_003',
    student_id: 'stu_002',
    status: 'present',
    remarks: 'Presented paper summary.'
  }
];

module.exports = { attendanceSessionsSeed, attendanceRecordsSeed };
""")

    # database/seeders/grades.seed.js
    write("database/seeders/grades.seed.js", """'use strict';

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
""")

    # database/seeders/tickets.seed.js
    write("database/seeders/tickets.seed.js", """'use strict';

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
""")

    # database/seeders/announcements.seed.js
    write("database/seeders/announcements.seed.js", """'use strict';

/**
 * Seed data for campus announcements, system settings, and notifications
 */

const announcementsSeed = [
  {
    id: 'anc_001',
    title: 'Fall 2026 Academic Orientation & Hackathon Kickoff',
    content: 'Welcome all new incoming students! Orientation commences this Friday at 10:00 AM in the Main Auditorium, followed by our 24-hour Welcome Hackathon.',
    target_audience: 'all',
    priority: 'high',
    author_id: 'usr_admin_01',
    is_pinned: 1,
    created_at: '2026-08-28T09:00:00Z'
  },
  {
    id: 'anc_002',
    title: 'Semester 1 Tuition Fee Installment Deadline Notice',
    content: 'All students opting for the monthly or split installment plan are reminded that the secondary installment is due by December 15, 2026.',
    target_audience: 'students',
    priority: 'normal',
    author_id: 'usr_finance_01',
    is_pinned: 0,
    created_at: '2026-08-29T11:00:00Z'
  }
];

const notificationsSeed = [
  {
    id: 'notif_001',
    user_id: 'usr_student_01',
    title: 'Grade Published: Data Structures Midterm',
    message: 'Dr. Alan Turing published your score: 94/100 (Grade A).',
    type: 'success',
    is_read: 0,
    link_url: '#/grades'
  },
  {
    id: 'notif_002',
    user_id: 'usr_counselor_01',
    title: 'New High-Score Lead Assigned',
    message: 'Vikram Patel (Score: 85) has been assigned to your counseling queue.',
    type: 'info',
    is_read: 0,
    link_url: '#/leads'
  },
  {
    id: 'notif_003',
    user_id: 'usr_student_02',
    title: 'Fee Payment Receipt Generated',
    message: 'Receipt REC-2026-0201 for $7,350 has been recorded.',
    type: 'success',
    is_read: 1,
    link_url: '#/finance'
  }
];

const systemSettingsSeed = [
  { key: 'institution_name', value: 'EduPulse Institute of Advanced Technology & Management', category: 'general', description: 'Institution legal display name' },
  { key: 'institution_email', value: 'contact@edupulse.edu', category: 'general', description: 'Main administrative email' },
  { key: 'institution_phone', value: '+1 (800) 555-EDUPULSE', category: 'general', description: 'Toll-free student help line' },
  { key: 'currency_symbol', value: '$', category: 'finance', description: 'Billing currency symbol' },
  { key: 'academic_term_current', value: 'Fall 2026', category: 'academic', description: 'Current active semester term' },
  { key: 'lead_auto_assign_enabled', value: 'true', category: 'leads', description: 'Enable automatic round-robin counselor assignment' }
];

module.exports = { announcementsSeed, notificationsSeed, systemSettingsSeed };
""")

    # database/seeders/seed-all.js
    write("database/seeders/seed-all.js", """'use strict';

/**
 * Master Database Seeder Script
 * Synchronizes and populates all database tables with comprehensive sample data.
 */

const db = require('../db');
const { usersSeed } = require('./users.seed');
const { coursesSeed, courseModulesSeed, batchesSeed } = require('./courses.seed');
const { leadsSeed, leadInteractionsSeed } = require('./leads.seed');
const { applicationsSeed, studentsSeed } = require('./students.seed');
const { invoicesSeed, paymentsSeed } = require('./finance.seed');
const { attendanceSessionsSeed, attendanceRecordsSeed } = require('./attendance.seed');
const { gradeItemsSeed, studentGradesSeed } = require('./grades.seed');
const { ticketsSeed, ticketRepliesSeed } = require('./tickets.seed');
const { announcementsSeed, notificationsSeed, systemSettingsSeed } = require('./announcements.seed');

async function runSeed() {
  console.log('[Seeder] Starting EduPulse CRM complete database seeding...');
  await db.init();

  // Populate users
  db.truncate('users');
  db.insertMany('users', usersSeed);
  console.log(`[Seeder] Seeded ${usersSeed.length} users`);

  // Populate courses, modules, batches
  db.truncate('courses');
  db.insertMany('courses', coursesSeed);
  db.truncate('course_modules');
  db.insertMany('course_modules', courseModulesSeed);
  db.truncate('batches');
  db.insertMany('batches', batchesSeed);
  console.log(`[Seeder] Seeded ${coursesSeed.length} courses, ${courseModulesSeed.length} modules, ${batchesSeed.length} batches`);

  // Populate leads & interactions
  db.truncate('leads');
  db.insertMany('leads', leadsSeed);
  db.truncate('lead_interactions');
  db.insertMany('lead_interactions', leadInteractionsSeed);
  console.log(`[Seeder] Seeded ${leadsSeed.length} leads, ${leadInteractionsSeed.length} interactions`);

  // Populate applications & students
  db.truncate('student_applications');
  db.insertMany('student_applications', applicationsSeed);
  db.truncate('students');
  db.insertMany('students', studentsSeed);
  console.log(`[Seeder] Seeded ${applicationsSeed.length} applications, ${studentsSeed.length} students`);

  // Populate finance (invoices & payments)
  db.truncate('invoices');
  db.insertMany('invoices', invoicesSeed);
  db.truncate('payments');
  db.insertMany('payments', paymentsSeed);
  console.log(`[Seeder] Seeded ${invoicesSeed.length} invoices, ${paymentsSeed.length} payments`);

  // Populate attendance
  db.truncate('attendance_sessions');
  db.insertMany('attendance_sessions', attendanceSessionsSeed);
  db.truncate('attendance_records');
  db.insertMany('attendance_records', attendanceRecordsSeed);
  console.log(`[Seeder] Seeded ${attendanceSessionsSeed.length} sessions, ${attendanceRecordsSeed.length} attendance records`);

  // Populate gradebook
  db.truncate('grade_items');
  db.insertMany('grade_items', gradeItemsSeed);
  db.truncate('student_grades');
  db.insertMany('student_grades', studentGradesSeed);
  console.log(`[Seeder] Seeded ${gradeItemsSeed.length} grade items, ${studentGradesSeed.length} student grades`);

  // Populate tickets
  db.truncate('support_tickets');
  db.insertMany('support_tickets', ticketsSeed);
  db.truncate('ticket_replies');
  db.insertMany('ticket_replies', ticketRepliesSeed);
  console.log(`[Seeder] Seeded ${ticketsSeed.length} tickets, ${ticketRepliesSeed.length} replies`);

  // Populate announcements, notifications, settings
  db.truncate('announcements');
  db.insertMany('announcements', announcementsSeed);
  db.truncate('notifications');
  db.insertMany('notifications', notificationsSeed);
  db.truncate('system_settings');
  db.insertMany('system_settings', systemSettingsSeed);
  console.log(`[Seeder] Seeded announcements, notifications, and settings`);

  db.persistSync();
  console.log('[Seeder] Database seeding completed successfully!');
}

if (require.main === module) {
  runSeed().catch(err => {
    console.error('[Seeder] Error seeding database:', err);
    process.exit(1);
  });
}

module.exports = { runSeed };
""")

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent.parent)
