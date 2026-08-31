'use strict';

/**
 * Base Entity Model
 * Provides foundational CRUD operations, hooks, timestamping, and schema validation.
 */

const db = require('../../database/db');

class BaseModel {
  constructor(data = {}) {
    this.id = data.id || null;
    this.created_at = data.created_at || new Date().toISOString();
    this.updated_at = data.updated_at || new Date().toISOString();
  }

  static get tableName() {
    throw new Error('Static getter tableName must be implemented in sub-classes');
  }

  static find(predicate = {}) {
    const rows = db.find(this.tableName, predicate);
    return rows.map(row => new this(row));
  }

  static findOne(predicate = {}) {
    const row = db.findOne(this.tableName, predicate);
    return row ? new this(row) : null;
  }

  static findById(id) {
    const row = db.findById(this.tableName, id);
    return row ? new this(row) : null;
  }

  static count(predicate = {}) {
    return db.count(this.tableName, predicate);
  }

  static create(data) {
    const instance = new this(data);
    instance.beforeSave();
    const saved = db.insert(this.tableName, instance.toJSON());
    return new this(saved);
  }

  static updateById(id, updates) {
    const updated = db.updateById(this.tableName, id, updates);
    return updated ? new this(updated) : null;
  }

  static deleteById(id) {
    return db.deleteById(this.tableName, id);
  }

  beforeSave() {
    if (!this.id) {
      this.id = `${this.constructor.tableName.slice(0, 3)}_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
    }
    this.updated_at = new Date().toISOString();
  }

  save() {
    this.beforeSave();
    if (this.id && db.findById(this.constructor.tableName, this.id)) {
      const updated = db.updateById(this.constructor.tableName, this.id, this.toJSON());
      Object.assign(this, updated);
    } else {
      const created = db.insert(this.constructor.tableName, this.toJSON());
      Object.assign(this, created);
    }
    return this;
  }

  delete() {
    if (!this.id) return false;
    return db.deleteById(this.constructor.tableName, this.id);
  }

  toJSON() {
    const obj = {};
    for (const key of Object.keys(this)) {
      if (typeof this[key] !== 'function') {
        obj[key] = this[key];
      }
    }
    return obj;
  }
}

module.exports = BaseModel;
