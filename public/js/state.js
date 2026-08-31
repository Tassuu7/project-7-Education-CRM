'use strict';

/**
 * Global State Manager & Pub/Sub Event Bus
 */

class StateManager {
  constructor() {
    this.user = null;
    this.token = localStorage.getItem('edupulse_token') || null;
    this.theme = localStorage.getItem('edupulse_theme') || 'light';
    this.listeners = new Map();
  }

  init() {
    document.documentElement.setAttribute('data-theme', this.theme);
    const savedUser = localStorage.getItem('edupulse_user');
    if (savedUser) {
      try {
        this.user = JSON.parse(savedUser);
      } catch {
        this.user = null;
      }
    }
  }

  setUser(user, token) {
    this.user = user;
    this.token = token;
    if (user && token) {
      localStorage.setItem('edupulse_user', JSON.stringify(user));
      localStorage.setItem('edupulse_token', token);
    } else {
      localStorage.removeItem('edupulse_user');
      localStorage.removeItem('edupulse_token');
    }
    this.emit('userChange', this.user);
  }

  toggleTheme() {
    this.theme = this.theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', this.theme);
    localStorage.setItem('edupulse_theme', this.theme);
    this.emit('themeChange', this.theme);
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(cb => cb(data));
    }
  }
}

window.AppState = new StateManager();
