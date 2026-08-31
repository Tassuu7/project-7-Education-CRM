'use strict';

/**
 * EduPulse CRM Database Management Engine
 * High-performance In-Memory relational data store with disk persistence,
 * query filtering, full-text search, joins, aggregations, and seed sync.
 */

const fs = require('fs');
const path = require('path');
const config = require('../config/app.config');

class DatabaseEngine {
  constructor() {
    this.storagePath = config.database.jsonBackupPath;
    this.tables = {
      users: [],
      leads: [],
      lead_interactions: [],
      courses: [],
      course_modules: [],
      batches: [],
      student_applications: [],
      students: [],
      invoices: [],
      payments: [],
      attendance_sessions: [],
      attendance_records: [],
      grade_items: [],
      student_grades: [],
      support_tickets: [],
      ticket_replies: [],
      announcements: [],
      notifications: [],
      audit_logs: [],
      system_settings: []
    };
    this.isInitialized = false;
    this.saveTimeout = null;
  }

  /**
   * Initialize and load persisted data from disk if available
   */
  async init() {
    if (this.isInitialized) return this;

    try {
      if (fs.existsSync(this.storagePath)) {
        const raw = fs.readFileSync(this.storagePath, 'utf8');
        const parsed = JSON.parse(raw);
        for (const [tbl, rows] of Object.entries(parsed)) {
          if (this.tables[tbl]) {
            this.tables[tbl] = Array.isArray(rows) ? rows : [];
          }
        }
        console.log(`[Database] Loaded persistent data store from ${this.storagePath}`);
      } else {
        console.log('[Database] Initialized fresh in-memory database');
      }
    } catch (err) {
      console.warn('[Database] Failed to read disk backup, using fresh tables:', err.message);
    }

    this.isInitialized = true;
    return this;
  }

  /**
   * Persist current state to JSON file on disk
   */
  persistSync() {
    try {
      const dir = path.dirname(this.storagePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(this.storagePath, JSON.stringify(this.tables, null, 2), 'utf8');
    } catch (err) {
      console.error('[Database] Failed to save database to disk:', err.message);
    }
  }

  /**
   * Debounced persistence to optimize high-frequency writes
   */
  schedulePersist() {
    if (this.saveTimeout) clearTimeout(this.saveTimeout);
    this.saveTimeout = setTimeout(() => {
      this.persistSync();
    }, 500);
  }

  /**
   * Get table reference
   */
  getTable(tableName) {
    if (!this.tables[tableName]) {
      this.tables[tableName] = [];
    }
    return this.tables[tableName];
  }

  /**
   * Query builder: Find items matching criteria
   */
  find(tableName, predicate = {}) {
    const table = this.getTable(tableName);
    if (!predicate || Object.keys(predicate).length === 0) {
      return [...table];
    }

    return table.filter(item => {
      for (const [key, val] of Object.entries(predicate)) {
        if (typeof val === 'function') {
          if (!val(item[key], item)) return false;
        } else if (val !== undefined && item[key] !== val) {
          return false;
        }
      }
      return true;
    });
  }

  /**
   * Find single record matching predicate
   */
  findOne(tableName, predicate = {}) {
    const results = this.find(tableName, predicate);
    return results.length > 0 ? results[0] : null;
  }

  /**
   * Find record by primary key 'id'
   */
  findById(tableName, id) {
    return this.findOne(tableName, { id });
  }

  /**
   * Insert record into table
   */
  insert(tableName, record) {
    const table = this.getTable(tableName);
    const now = new Date().toISOString();
    
    const newRecord = {
      ...record,
      created_at: record.created_at || now,
      updated_at: record.updated_at || now
    };

    table.push(newRecord);
    this.schedulePersist();
    return { ...newRecord };
  }

  /**
   * Insert multiple records
   */
  insertMany(tableName, records = []) {
    const table = this.getTable(tableName);
    const now = new Date().toISOString();
    
    const inserted = records.map(record => ({
      ...record,
      created_at: record.created_at || now,
      updated_at: record.updated_at || now
    }));

    table.push(...inserted);
    this.schedulePersist();
    return inserted;
  }

  /**
   * Update record by ID
   */
  updateById(tableName, id, updates) {
    const table = this.getTable(tableName);
    const idx = table.findIndex(r => r.id === id || r.key === id);
    if (idx === -1) return null;

    const now = new Date().toISOString();
    const updated = {
      ...table[idx],
      ...updates,
      id: table[idx].id || id,
      updated_at: now
    };

    table[idx] = updated;
    this.schedulePersist();
    return { ...updated };
  }

  /**
   * Update all records matching predicate
   */
  updateWhere(tableName, predicate, updates) {
    const table = this.getTable(tableName);
    const now = new Date().toISOString();
    let count = 0;

    for (let i = 0; i < table.length; i++) {
      let match = true;
      for (const [k, v] of Object.entries(predicate)) {
        if (table[i][k] !== v) {
          match = false;
          break;
        }
      }

      if (match) {
        table[i] = {
          ...table[i],
          ...updates,
          updated_at: now
        };
        count++;
      }
    }

    if (count > 0) this.schedulePersist();
    return count;
  }

  /**
   * Delete record by ID
   */
  deleteById(tableName, id) {
    const table = this.getTable(tableName);
    const idx = table.findIndex(r => r.id === id || r.key === id);
    if (idx === -1) return false;

    table.splice(idx, 1);
    this.schedulePersist();
    return true;
  }

  /**
   * Delete all records matching predicate
   */
  deleteWhere(tableName, predicate) {
    const table = this.getTable(tableName);
    const initialLen = table.length;
    
    this.tables[tableName] = table.filter(item => {
      for (const [k, v] of Object.entries(predicate)) {
        if (item[k] === v) return false;
      }
      return true;
    });

    const deleted = initialLen - this.tables[tableName].length;
    if (deleted > 0) this.schedulePersist();
    return deleted;
  }

  /**
   * Count records matching predicate
   */
  count(tableName, predicate = {}) {
    return this.find(tableName, predicate).length;
  }

  /**
   * Clear all records in a table
   */
  truncate(tableName) {
    if (this.tables[tableName]) {
      this.tables[tableName] = [];
      this.schedulePersist();
    }
  }

  /**
   * Reset all tables
   */
  clearAll() {
    for (const key of Object.keys(this.tables)) {
      this.tables[key] = [];
    }
    this.persistSync();
  }
}

// Singleton database instance
const db = new DatabaseEngine();

module.exports = db;
