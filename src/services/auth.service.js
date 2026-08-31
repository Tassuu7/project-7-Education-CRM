'use strict';

/**
 * Authentication and Session Management Service
 */

const crypto = require('crypto');
const db = require('../../database/db');
const User = require('../models/User');
const config = require('../../config/app.config');

class AuthService {
  /**
   * Authenticate user with credentials
   */
  async login(usernameOrEmail, password) {
    if (!usernameOrEmail || !password) {
      throw new Error('Username/Email and Password are required.');
    }

    const cleanInput = usernameOrEmail.trim().toLowerCase();
    const userRow = db.findOne('users', (val, item) => 
      item.email.toLowerCase() === cleanInput || item.username.toLowerCase() === cleanInput
    );

    if (!userRow) {
      throw new Error('Invalid credentials or account does not exist.');
    }

    const user = new User(userRow);
    if (!user.verifyPassword(password)) {
      throw new Error('Invalid credentials.');
    }

    if (!user.is_active) {
      throw new Error('Account is inactive. Please contact your system administrator.');
    }

    // Update last login timestamp
    user.last_login_at = new Date().toISOString();
    user.save();

    // Generate token payload
    const token = this.generateToken(user);

    return {
      token,
      user: user.toSafeJSON()
    };
  }

  /**
   * Register a new user account
   */
  async register(userData) {
    const { username, email, password, first_name, last_name, role = 'student', phone } = userData;

    if (!username || !email || !password || !first_name || !last_name) {
      throw new Error('All required registration fields must be provided.');
    }

    // Check uniqueness
    const existingEmail = db.findOne('users', { email: email.trim().toLowerCase() });
    if (existingEmail) {
      throw new Error('Email address is already in use.');
    }

    const existingUser = db.findOne('users', { username: username.trim().toLowerCase() });
    if (existingUser) {
      throw new Error('Username is already taken.');
    }

    const passwordHash = User.hashPassword(password);
    const newUser = User.create({
      id: `usr_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
      username: username.trim().toLowerCase(),
      email: email.trim().toLowerCase(),
      password_hash: passwordHash,
      first_name: first_name.trim(),
      last_name: last_name.trim(),
      role,
      phone: phone ? phone.trim() : '',
      is_active: 1,
      last_login_at: new Date().toISOString()
    });

    const token = this.generateToken(newUser);
    return {
      token,
      user: newUser.toSafeJSON()
    };
  }

  /**
   * Generate simple signed token
   */
  generateToken(user) {
    const payload = {
      userId: user.id,
      email: user.email,
      role: user.role,
      issuedAt: Date.now(),
      expiresAt: Date.now() + (config.security.tokenExpirySeconds * 1000)
    };

    const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url');
    const body = Buffer.from(JSON.stringify(payload)).toString('base64url');
    const signature = crypto.createHmac('sha256', config.security.jwtSecret)
      .update(`${header}.${body}`)
      .digest('base64url');

    return `${header}.${body}.${signature}`;
  }

  /**
   * Verify token integrity and expiration
   */
  verifyToken(token) {
    if (!token) return null;
    const parts = token.split('.');
    if (parts.length !== 3) return null;

    const [header, body, signature] = parts;
    const expectedSignature = crypto.createHmac('sha256', config.security.jwtSecret)
      .update(`${header}.${body}`)
      .digest('base64url');

    if (signature !== expectedSignature) {
      return null;
    }

    try {
      const payload = JSON.parse(Buffer.from(body, 'base64url').toString('utf8'));
      if (payload.expiresAt && Date.now() > payload.expiresAt) {
        return null; // Expired
      }
      return payload;
    } catch {
      return null;
    }
  }

  /**
   * Fetch current authenticated user by ID
   */
  async getCurrentUser(userId) {
    const user = User.findById(userId);
    if (!user) return null;
    return user.toSafeJSON();
  }
}

module.exports = new AuthService();
