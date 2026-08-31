'use strict';

function requestLogger(req, res, next) {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`[HTTP] ${req.method} ${req.originalUrl} | Status: ${res.statusCode} | Duration: ${duration}ms | User: ${req.user ? req.user.username : 'Anonymous'}`);
  });
  next();
}

module.exports = requestLogger;
