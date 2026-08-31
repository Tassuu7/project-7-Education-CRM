'use strict';

const authService = require('../services/auth.service');
const auditService = require('../services/audit.service');

class AuthController {
  async login(req, res) {
    try {
      const { username, password } = req.body || {};
      const result = await authService.login(username, password);
      
      auditService.logAction(result.user.id, 'USER_LOGIN', 'users', result.user.id, { ip: req.ip }, req.ip);
      
      return res.status(200).json({
        success: true,
        message: 'Login successful.',
        data: result
      });
    } catch (err) {
      return res.status(401).json({
        success: false,
        message: err.message || 'Authentication failed.'
      });
    }
  }

  async register(req, res) {
    try {
      const result = await authService.register(req.body);
      auditService.logAction(result.user.id, 'USER_REGISTER', 'users', result.user.id, { role: result.user.role }, req.ip);

      return res.status(201).json({
        success: true,
        message: 'Registration successful.',
        data: result
      });
    } catch (err) {
      return res.status(400).json({
        success: false,
        message: err.message || 'Registration failed.'
      });
    }
  }

  async me(req, res) {
    if (!req.user) {
      return res.status(401).json({ success: false, message: 'Unauthenticated.' });
    }
    return res.status(200).json({
      success: true,
      data: req.user
    });
  }

  async logout(req, res) {
    if (req.user) {
      auditService.logAction(req.user.id, 'USER_LOGOUT', 'users', req.user.id, {}, req.ip);
    }
    return res.status(200).json({
      success: true,
      message: 'Logged out successfully.'
    });
  }
}

module.exports = new AuthController();
