-- ============================================================================
-- EduPulse Enterprise Education CRM Database Schema
-- Standard Relational Schema for Academic, Financial, and Lead Management
-- ============================================================================

PRAGMA foreign_keys = ON;

-- 1. Users & Authentication
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('super_admin', 'admin', 'counselor', 'instructor', 'finance_officer', 'student', 'parent')),
    phone TEXT,
    avatar_url TEXT,
    is_active INTEGER DEFAULT 1,
    last_login_at TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 2. Prospective Leads Management
CREATE TABLE IF NOT EXISTS leads (
    id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    alternate_phone TEXT,
    source TEXT NOT NULL,
    stage TEXT NOT NULL CHECK(stage IN ('new', 'contacted', 'qualified', 'counseling_scheduled', 'application_submitted', 'enrolled', 'unqualified', 'lost')),
    interested_course_id TEXT,
    assigned_counselor_id TEXT,
    lead_score INTEGER DEFAULT 0,
    budget_range TEXT,
    preferred_intake TEXT,
    country TEXT DEFAULT 'India',
    city TEXT,
    notes TEXT,
    qualification_status TEXT,
    last_contacted_at TEXT,
    next_follow_up_date TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (assigned_counselor_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (interested_course_id) REFERENCES courses(id) ON DELETE SET NULL
);

-- 3. Lead Interaction Logs
CREATE TABLE IF NOT EXISTS lead_interactions (
    id TEXT PRIMARY KEY,
    lead_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    interaction_type TEXT NOT NULL CHECK(interaction_type IN ('phone_call', 'email', 'whatsapp', 'in_person_meeting', 'campus_visit', 'note')),
    summary TEXT NOT NULL,
    outcome TEXT,
    duration_minutes INTEGER DEFAULT 0,
    scheduled_follow_up TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Course Catalog & Programs
CREATE TABLE IF NOT EXISTS courses (
    id TEXT PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    department TEXT NOT NULL,
    degree_level TEXT NOT NULL CHECK(degree_level IN ('Certificate', 'Diploma', 'Bachelor', 'Master', 'Doctorate', 'Bootcamp')),
    duration_months INTEGER NOT NULL,
    total_credits INTEGER NOT NULL,
    base_tuition_fee REAL NOT NULL,
    description TEXT,
    syllabus_outline TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 5. Course Modules & Syllabi
CREATE TABLE IF NOT EXISTS course_modules (
    id TEXT PRIMARY KEY,
    course_id TEXT NOT NULL,
    module_code TEXT NOT NULL,
    title TEXT NOT NULL,
    semester_number INTEGER NOT NULL,
    credits INTEGER NOT NULL,
    instructor_id TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 6. Batches & Cohorts
CREATE TABLE IF NOT EXISTS batches (
    id TEXT PRIMARY KEY,
    course_id TEXT NOT NULL,
    batch_name TEXT NOT NULL,
    cohort_code TEXT UNIQUE NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    max_capacity INTEGER DEFAULT 40,
    current_enrolled INTEGER DEFAULT 0,
    lead_instructor_id TEXT,
    classroom_location TEXT,
    status TEXT DEFAULT 'upcoming' CHECK(status IN ('upcoming', 'active', 'completed', 'cancelled')),
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (lead_instructor_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 7. Student Applications & Admissions
CREATE TABLE IF NOT EXISTS student_applications (
    id TEXT PRIMARY KEY,
    lead_id TEXT,
    course_id TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    dob TEXT NOT NULL,
    gender TEXT,
    high_school_percentage REAL,
    entrance_exam_score REAL,
    status TEXT NOT NULL CHECK(status IN ('draft', 'submitted', 'under_review', 'interview_scheduled', 'accepted', 'rejected', 'waitlisted', 'enrolled')),
    reviewer_id TEXT,
    review_notes TEXT,
    applied_at TEXT DEFAULT (datetime('now')),
    decision_at TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE SET NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 8. Enrolled Students Information System
CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    student_id_number TEXT UNIQUE NOT NULL,
    application_id TEXT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    dob TEXT,
    blood_group TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    guardian_name TEXT,
    guardian_phone TEXT,
    guardian_email TEXT,
    guardian_relation TEXT,
    primary_course_id TEXT NOT NULL,
    current_batch_id TEXT,
    current_semester INTEGER DEFAULT 1,
    enrollment_status TEXT DEFAULT 'active' CHECK(enrollment_status IN ('active', 'graduated', 'suspended', 'on_leave', 'withdrawn')),
    cumulative_gpa REAL DEFAULT 0.0,
    total_credits_earned INTEGER DEFAULT 0,
    enrolled_date TEXT DEFAULT (datetime('now')),
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (primary_course_id) REFERENCES courses(id) ON DELETE RESTRICT,
    FOREIGN KEY (current_batch_id) REFERENCES batches(id) ON DELETE SET NULL,
    FOREIGN KEY (application_id) REFERENCES student_applications(id) ON DELETE SET NULL
);

-- 9. Invoices & Billing
CREATE TABLE IF NOT EXISTS invoices (
    id TEXT PRIMARY KEY,
    invoice_number TEXT UNIQUE NOT NULL,
    student_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    title TEXT NOT NULL,
    amount REAL NOT NULL,
    discount_amount REAL DEFAULT 0.0,
    tax_amount REAL DEFAULT 0.0,
    total_amount REAL NOT NULL,
    amount_paid REAL DEFAULT 0.0,
    balance_due REAL NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('draft', 'pending', 'paid', 'partially_paid', 'overdue', 'cancelled', 'refunded')),
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE RESTRICT
);

-- 10. Payments & Transaction Logs
CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY,
    receipt_number TEXT UNIQUE NOT NULL,
    invoice_id TEXT NOT NULL,
    student_id TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_method TEXT NOT NULL CHECK(payment_method IN ('credit_card', 'debit_card', 'bank_transfer', 'upi', 'stripe_online', 'cheque', 'cash', 'scholarship_credit')),
    transaction_reference TEXT,
    payment_date TEXT DEFAULT (datetime('now')),
    recorded_by_user_id TEXT,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (recorded_by_user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 11. Attendance Sessions & Records
CREATE TABLE IF NOT EXISTS attendance_sessions (
    id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    module_id TEXT,
    instructor_id TEXT NOT NULL,
    session_date TEXT NOT NULL,
    start_time TEXT,
    end_time TEXT,
    topic_covered TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (batch_id) REFERENCES batches(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS attendance_records (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    student_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'late', 'excused', 'half_day')),
    remarks TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (session_id) REFERENCES attendance_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- 12. Gradebook & Examinations
CREATE TABLE IF NOT EXISTS grade_items (
    id TEXT PRIMARY KEY,
    course_id TEXT NOT NULL,
    module_id TEXT,
    batch_id TEXT NOT NULL,
    title TEXT NOT NULL,
    assessment_type TEXT NOT NULL CHECK(assessment_type IN ('Quiz', 'Assignment', 'Midterm', 'Final Exam', 'Project', 'Lab Practical')),
    max_score REAL NOT NULL,
    weight_percentage REAL NOT NULL,
    due_date TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (batch_id) REFERENCES batches(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS student_grades (
    id TEXT PRIMARY KEY,
    grade_item_id TEXT NOT NULL,
    student_id TEXT NOT NULL,
    score_obtained REAL NOT NULL,
    letter_grade TEXT,
    gpa_points REAL,
    feedback TEXT,
    graded_by_user_id TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (grade_item_id) REFERENCES grade_items(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (graded_by_user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 13. Helpdesk Support Tickets
CREATE TABLE IF NOT EXISTS support_tickets (
    id TEXT PRIMARY KEY,
    ticket_number TEXT UNIQUE NOT NULL,
    user_id TEXT NOT NULL,
    category TEXT NOT NULL,
    priority TEXT NOT NULL CHECK(priority IN ('low', 'medium', 'high', 'critical')),
    status TEXT NOT NULL CHECK(status IN ('open', 'in_progress', 'waiting_on_student', 'resolved', 'closed')),
    subject TEXT NOT NULL,
    description TEXT NOT NULL,
    assigned_to_user_id TEXT,
    resolution_notes TEXT,
    resolved_at TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to_user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ticket_replies (
    id TEXT PRIMARY KEY,
    ticket_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    is_staff_reply INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (ticket_id) REFERENCES support_tickets(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 14. Broadcast Announcements & Notifications
CREATE TABLE IF NOT EXISTS announcements (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    target_audience TEXT NOT NULL CHECK(target_audience IN ('all', 'students', 'counselors', 'instructors', 'finance')),
    priority TEXT DEFAULT 'normal',
    author_id TEXT NOT NULL,
    is_pinned INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS notifications (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT DEFAULT 'info',
    is_read INTEGER DEFAULT 0,
    link_url TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 15. Audit Logs & System Activity
CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT,
    ip_address TEXT,
    details TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- 16. System Settings
CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    description TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Indexes for lightning fast lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_leads_stage ON leads(stage);
CREATE INDEX IF NOT EXISTS idx_leads_counselor ON leads(assigned_counselor_id);
CREATE INDEX IF NOT EXISTS idx_students_course ON students(primary_course_id);
CREATE INDEX IF NOT EXISTS idx_students_batch ON students(current_batch_id);
CREATE INDEX IF NOT EXISTS idx_invoices_student ON invoices(student_id);
CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status);
CREATE INDEX IF NOT EXISTS idx_attendance_session ON attendance_records(session_id);
CREATE INDEX IF NOT EXISTS idx_grades_student ON student_grades(student_id);
CREATE INDEX IF NOT EXISTS idx_tickets_user ON support_tickets(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
