'use strict';

const { hasPermission, hasAnyPermission, ROLES } = require('../../config/permissions');

function requirePermission(permission) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ success: false, message: 'Unauthenticated.' });
    }

    if (req.user.role === ROLES.SUPER_ADMIN || req.user.role === ROLES.ADMIN) {
      return next();
    }

    if (!hasPermission(req.user.role, permission)) {
      return res.status(403).json({
        success: false,
        message: `Forbidden. Role '${req.user.role}' lacks permission '${permission}'.`
      });
    }

    next();
  };
}

function requireRoles(...roles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ success: false, message: 'Unauthenticated.' });
    }

    if (roles.includes(req.user.role) || req.user.role === ROLES.SUPER_ADMIN) {
      return next();
    }

    return res.status(403).json({
      success: false,
      message: `Forbidden. Role '${req.user.role}' is not authorized for this resource.`
    });
  };
}

module.exports = { requirePermission, requireRoles };
