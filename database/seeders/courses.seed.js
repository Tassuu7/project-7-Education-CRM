'use strict';

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
