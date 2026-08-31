'use strict';

/**
 * Database connection and configuration helper
 */

const path = require('path');
const config = require('./app.config');

module.exports = {
  client: 'sqlite3',
  connection: {
    filename: config.database.filePath
  },
  useNullAsDefault: true,
  pool: {
    min: 2,
    max: 10
  }
};
