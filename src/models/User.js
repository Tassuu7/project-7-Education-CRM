'use strict';

const BaseModel = require('./BaseModel');
const crypto = require('crypto');

class User extends BaseModel {
  constructor(data = {}) {
    super(data);
    this.username = data.username || '';
    this.email = data.email || '';
    this.password_hash = data.password_hash || '';
    this.first_name = data.first_name || '';
    this.last_name = data.last_name || '';
    this.role = data.role || 'student';
    this.phone = data.phone || '';
    this.avatar_url = data.avatar_url || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150';
    this.is_active = data.is_active !== undefined ? Number(data.is_active) : 1;
    this.last_login_at = data.last_login_at || null;
  }

  static get tableName() {
    return 'users';
  }

  static hashPassword(password) {
    return crypto.createHash('sha256').update(password + 'edupulse_salt_2026').digest('hex');
  }

  verifyPassword(password) {
    const hashed = User.hashPassword(password);
    return this.password_hash === hashed;
  }

  get fullName() {
    return `${this.first_name} ${this.last_name}`.trim();
  }

  toSafeJSON() {
    const safe = this.toJSON();
    delete safe.password_hash;
    safe.fullName = this.fullName;
    return safe;
  }
}

module.exports = User;
