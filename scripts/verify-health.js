'use strict';

const http = require('http');

const req = http.get('http://localhost:4050/api/v1/health', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log('[Health Check] Status Code:', res.statusCode);
    console.log('[Health Check] Response:', data);
    process.exit(res.statusCode === 200 ? 0 : 1);
  });
});

req.on('error', (err) => {
  console.error('[Health Check Error] Server is not reachable:', err.message);
  process.exit(1);
});
