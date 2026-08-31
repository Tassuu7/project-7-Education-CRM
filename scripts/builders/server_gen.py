#!/usr/bin/env python3
"""
EduPulse CRM - Main Express Server Entrypoint Generator
"""

import os
from pathlib import Path

def generate(base_dir):
    def write(rel, content):
        p = Path(base_dir) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {rel}")

    # server.js
    write("server.js", """'use strict';

/**
 * ============================================================================
 * EduPulse Education CRM & Student Lifecycle Management Platform
 * Main HTTP Application Server
 * ============================================================================
 */

const express = require('express');
const http = require('http');
const path = require('path');
const config = require('./config/app.config');
const db = require('./database/db');
const { runSeed } = require('./database/seeders/seed-all');
const apiRouter = require('./src/routes/api.router');
const { authenticate } = require('./src/middlewares/auth.middleware');
const requestLogger = require('./src/middlewares/logger.middleware');
const rateLimiter = require('./src/middlewares/rate-limiter.middleware');
const { errorHandler } = require('./src/middlewares/error.middleware');

const app = express();
const server = http.createServer(app);

// 1. Basic Middlewares & Parsers
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// 2. CORS Headers
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, PATCH');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization, x-access-token');
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }
  next();
});

// 3. Security & Logging Middlewares
app.use(rateLimiter({ windowMs: 60000, max: 500 }));
app.use(requestLogger);
app.use(authenticate);

// 4. Mount REST API Subsystems
app.use('/api/v1', apiRouter);
app.use('/api', apiRouter); // Alias for convenience

// 5. Serve Frontend Static Assets
app.use(express.static(path.join(__dirname, 'public')));

// 6. SPA Client-Side Routing Fallback
app.use((req, res, next) => {
  if (req.method === 'GET' && !req.path.startsWith('/api')) {
    return res.sendFile(path.join(__dirname, 'public', 'index.html'));
  }
  next();
});

// 7. Global Error Handler
app.use(errorHandler);

// Bootstrap Function
async function startServer() {
  try {
    console.log('================================================================');
    console.log('         EDUPULSE ENTERPRISE EDUCATION CRM SYSTEM               ');
    console.log('================================================================');
    
    // Initialize Database
    await db.init();

    // Auto-seed if users table is empty
    if (db.count('users') === 0) {
      console.log('[Server] Database is empty. Running initial system seeds...');
      await runSeed();
    } else {
      console.log(`[Server] Database connected with ${db.count('users')} users, ${db.count('leads')} leads, ${db.count('students')} students.`);
    }

    const PORT = config.app.port || 4050;
    const HOST = '0.0.0.0';

    server.listen(PORT, HOST, () => {
      console.log(`[Server] EduPulse CRM is LIVE and running on:`);
      console.log(`  -> Local:   http://localhost:${PORT}`);
      console.log(`  -> Network: http://${HOST}:${PORT}`);
      console.log(`  -> Environment: ${config.app.environment}`);
      console.log('================================================================');
    });
  } catch (err) {
    console.error('[Server] Critical startup failure:', err);
    process.exit(1);
  }
}

// Start application
if (require.main === module) {
  startServer();
}

module.exports = { app, server, startServer };
""")

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent.parent)
