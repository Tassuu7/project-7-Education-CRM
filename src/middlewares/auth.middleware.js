'use strict';

const authService = require('../services/auth.service');
const User = require('../models/User');

function authenticate(req, res, next) {
  const authHeader = req.headers.authorization || '';
  let token = null;

  if (authHeader.startsWith('Bearer ')) {
    token = authHeader.substring(7);
  } else if (req.headers['x-access-token']) {
    token = req.headers['x-access-token'];
  } else if (req.cookies && req.cookies.edupulse_session) {
    token = req.cookies.edupulse_session;
  }

  if (!token) {
    // Check if development guest bypass or default
    return next();
  }

  const payload = authService.verifyToken(token);
  if (payload && payload.userId) {
    const user = User.findById(payload.userId);
    if (user && user.is_active) {
      req.user = user.toSafeJSON();
    }
  }

  next();
}

function requireAuth(req, res, next) {
  if (!req.user) {
    return res.status(401).json({
      success: false,
      message: 'Unauthorized. Authentication token is missing or expired.'
    });
  }
  next();
}

module.exports = { authenticate, requireAuth };
