'use strict';

const requestCounts = new Map();

function rateLimiter(options = { windowMs: 60000, max: 200 }) {
  return (req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress || 'unknown';
    const now = Date.now();

    if (!requestCounts.has(ip)) {
      requestCounts.set(ip, { count: 1, resetTime: now + options.windowMs });
      return next();
    }

    const tracker = requestCounts.get(ip);
    if (now > tracker.resetTime) {
      tracker.count = 1;
      tracker.resetTime = now + options.windowMs;
      return next();
    }

    tracker.count++;
    if (tracker.count > options.max) {
      return res.status(429).json({
        success: false,
        message: 'Too many requests. Please slow down and try again shortly.'
      });
    }

    next();
  };
}

module.exports = rateLimiter;
