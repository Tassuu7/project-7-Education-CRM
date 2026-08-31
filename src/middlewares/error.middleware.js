'use strict';

function errorHandler(err, req, res, next) {
  console.error('[Error Middleware]', err.stack || err.message);

  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';

  res.status(status).json({
    success: false,
    error: {
      message,
      statusCode: status,
      timestamp: new Date().toISOString()
    }
  });
}

function notFoundHandler(req, res) {
  res.status(404).json({
    success: false,
    message: `Resource not found at ${req.originalUrl}`
  });
}

module.exports = { errorHandler, notFoundHandler };
