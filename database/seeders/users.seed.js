'use strict';

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
