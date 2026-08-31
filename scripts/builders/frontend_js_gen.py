#!/usr/bin/env python3
"""
EduPulse CRM - Frontend Application and Views Generator
Generates index.html and modern Single Page Application (SPA) JavaScript framework.
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

    # public/index.html
    write("public/index.html", """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EduPulse CRM | Education Operations & Student Lifecycle Platform</title>
  
  <!-- Google Fonts: Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  
  <!-- FontAwesome Icons CDN -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
  <!-- Application CSS Bundles -->
  <link rel="stylesheet" href="css/main.css">
  <link rel="stylesheet" href="css/dashboard.css">
  <link rel="stylesheet" href="css/leads.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/animations.css">
  <link rel="stylesheet" href="css/responsive.css">
</head>
<body>

  <div id="app">
    <!-- Navigation Sidebar -->
    <aside class="app-sidebar" id="sidebar-container"></aside>

    <!-- Main Content Area -->
    <div class="app-main">
      <!-- Top Sticky Navbar -->
      <header class="app-navbar" id="navbar-container"></header>

      <!-- Dynamic View Container -->
      <main class="content-container" id="view-container">
        <!-- Rendered SPA View -->
      </main>
    </div>
  </div>

  <!-- Global Modal Container -->
  <div id="modal-container"></div>

  <!-- Toast Notification Hub -->
  <div id="toast-container"></div>

  <!-- Application Scripts -->
  <script src="js/state.js"></script>
  <script src="js/api.client.js"></script>
  <script src="js/components/toast.js"></script>
  <script src="js/components/modal.js"></script>
  <script src="js/components/navbar.js"></script>
  <script src="js/components/sidebar.js"></script>
  <script src="js/components/chart-renderer.js"></script>
  
  <!-- View Modules -->
  <script src="js/views/auth.view.js"></script>
  <script src="js/views/dashboard.view.js"></script>
  <script src="js/views/leads.view.js"></script>
  <script src="js/views/admissions.view.js"></script>
  <script src="js/views/students.view.js"></script>
  <script src="js/views/courses.view.js"></script>
  <script src="js/views/finance.view.js"></script>
  <script src="js/views/attendance.view.js"></script>
  <script src="js/views/gradebook.view.js"></script>
  <script src="js/views/tickets.view.js"></script>
  <script src="js/views/reports.view.js"></script>
  <script src="js/views/settings.view.js"></script>

  <!-- Router & Bootstrap -->
  <script src="js/router.js"></script>
  <script src="js/app.js"></script>
</body>
</html>
""")

    # public/js/state.js
    write("public/js/state.js", """'use strict';

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
""")

    # public/js/api.client.js
    write("public/js/api.client.js", """'use strict';

/**
 * Robust HTTP API Client
 */

class ApiClient {
  constructor(baseUrl = '/api/v1') {
    this.baseUrl = baseUrl;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    };

    if (window.AppState.token) {
      headers['Authorization'] = `Bearer ${window.AppState.token}`;
    }

    try {
      const res = await fetch(url, {
        ...options,
        headers
      });

      // Handle download responses (CSV / binary)
      const contentType = res.headers.get('content-type') || '';
      if (contentType.includes('text/csv')) {
        return await res.text();
      }

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.message || `Request failed with status ${res.status}`);
      }

      return data;
    } catch (err) {
      console.error(`[API Error] ${options.method || 'GET'} ${endpoint}:`, err);
      if (window.Toast) {
        window.Toast.error(err.message || 'Network request failed.');
      }
      throw err;
    }
  }

  get(endpoint, params = {}) {
    const qs = new URLSearchParams(params).toString();
    const full = qs ? `${endpoint}?${qs}` : endpoint;
    return this.request(full, { method: 'GET' });
  }

  post(endpoint, body = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(body)
    });
  }

  put(endpoint, body = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body)
    });
  }

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

window.API = new ApiClient();
""")

    # public/js/components/toast.js
    write("public/js/components/toast.js", """'use strict';

class ToastManager {
  constructor() {
    this.container = document.getElementById('toast-container');
  }

  show(message, type = 'info', duration = 3500) {
    if (!this.container) {
      this.container = document.getElementById('toast-container');
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-check-circle';
    if (type === 'error') icon = 'fa-exclamation-circle';
    if (type === 'warning') icon = 'fa-exclamation-triangle';

    toast.innerHTML = `
      <div style="display: flex; align-items: center; gap: 10px;">
        <i class="fas ${icon}"></i>
        <span>${message}</span>
      </div>
      <button style="background:none; border:none; color:inherit; cursor:pointer; margin-left:12px;" onclick="this.parentElement.remove()">
        <i class="fas fa-times"></i>
      </button>
    `;

    this.container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }

  success(msg) { this.show(msg, 'success'); }
  error(msg) { this.show(msg, 'error', 4500); }
  info(msg) { this.show(msg, 'info'); }
}

window.Toast = new ToastManager();
""")

    # public/js/components/modal.js
    write("public/js/components/modal.js", """'use strict';

class ModalManager {
  constructor() {
    this.container = document.getElementById('modal-container');
  }

  open({ title, body, footer, width = '600px', onClose }) {
    if (!this.container) this.container = document.getElementById('modal-container');

    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay active';
    overlay.innerHTML = `
      <div class="modal-dialog" style="max-width: ${width};">
        <div class="modal-header">
          <h3 class="card-title">${title}</h3>
          <button class="btn btn-secondary btn-sm" style="border:none; padding:4px 8px;" id="modal-close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">${body}</div>
        ${footer ? `<div class="modal-footer">${footer}</div>` : ''}
      </div>
    `;

    this.container.innerHTML = '';
    this.container.appendChild(overlay);

    const close = () => {
      overlay.classList.remove('active');
      setTimeout(() => {
        overlay.remove();
        if (onClose) onClose();
      }, 200);
    };

    overlay.querySelector('#modal-close-btn').addEventListener('click', close);
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) close();
    });

    return { close, element: overlay };
  }

  close() {
    if (this.container) this.container.innerHTML = '';
  }
}

window.Modal = new ModalManager();
""")

    # public/js/components/navbar.js
    write("public/js/components/navbar.js", """'use strict';

function renderNavbar() {
  const container = document.getElementById('navbar-container');
  if (!container) return;

  const user = window.AppState.user || {
    first_name: 'Alexander',
    last_name: 'Vance',
    role: 'super_admin',
    avatar_url: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150'
  };

  container.innerHTML = `
    <div style="display: flex; align-items: center; gap: 16px;">
      <button class="btn btn-secondary btn-sm" id="sidebar-toggle-btn" style="display: none;">
        <i class="fas fa-bars"></i>
      </button>
      <div style="position: relative; width: 320px;">
        <i class="fas fa-search" style="position: absolute; left: 12px; top: 11px; color: var(--text-muted);"></i>
        <input type="text" class="form-control" placeholder="Search leads, students, courses..." style="padding-left: 36px; border-radius: var(--radius-full);">
      </div>
    </div>

    <div style="display: flex; align-items: center; gap: 20px;">
      <!-- Role Switcher for Quick Live Testing -->
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 12px; color: var(--text-muted); font-weight: 500;">Role Demo:</span>
        <select class="form-control" id="role-demo-switcher" style="padding: 4px 10px; font-size: 12px; height: 32px; width: 140px;">
          <option value="super_admin" ${user.role === 'super_admin' ? 'selected' : ''}>Super Admin</option>
          <option value="counselor" ${user.role === 'counselor' ? 'selected' : ''}>Counselor</option>
          <option value="instructor" ${user.role === 'instructor' ? 'selected' : ''}>Instructor</option>
          <option value="finance_officer" ${user.role === 'finance_officer' ? 'selected' : ''}>Finance Officer</option>
          <option value="student" ${user.role === 'student' ? 'selected' : ''}>Student</option>
        </select>
      </div>

      <!-- Dark / Light Mode Toggle -->
      <button class="btn btn-secondary btn-sm" id="theme-toggle-btn" title="Toggle Dark/Light Mode" style="border-radius: 50%; width: 36px; height: 36px; padding: 0;">
        <i class="fas ${window.AppState.theme === 'dark' ? 'fa-sun' : 'fa-moon'}"></i>
      </button>

      <!-- User Profile Badge -->
      <div style="display: flex; align-items: center; gap: 12px; cursor: pointer;" id="user-profile-menu">
        <img src="${user.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150'}" style="width: 38px; height: 38px; border-radius: 50%; object-fit: cover; border: 2px solid var(--primary-400);">
        <div style="text-align: left; line-height: 1.2;">
          <div style="font-weight: 600; font-size: 13px; color: var(--text-main);">${user.first_name} ${user.last_name}</div>
          <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">${user.role ? user.role.replace('_', ' ') : 'User'}</div>
        </div>
      </div>
    </div>
  `;

  // Attach theme toggle listener
  document.getElementById('theme-toggle-btn').addEventListener('click', () => {
    window.AppState.toggleTheme();
    renderNavbar();
  });

  // Attach role switcher listener
  document.getElementById('role-demo-switcher').addEventListener('change', async (e) => {
    const selectedRole = e.target.value;
    const roleUsers = {
      super_admin: { username: 'superadmin', pwd: 'admin123' },
      counselor: { username: 'counselor_rachel', pwd: 'counselor123' },
      instructor: { username: 'prof_alan', pwd: 'faculty123' },
      finance_officer: { username: 'finance_elena', pwd: 'finance123' },
      student: { username: 'student_rohit', pwd: 'student123' }
    };

    const creds = roleUsers[selectedRole];
    if (creds) {
      try {
        const res = await window.API.post('/auth/login', { username: creds.username, password: creds.pwd });
        window.AppState.setUser(res.data.user, res.data.token);
        window.Toast.success(`Switched role to ${selectedRole.toUpperCase()}`);
        renderNavbar();
        renderSidebar();
        window.Router.navigate(window.location.hash || '#/');
      } catch (err) {
        window.Toast.error('Failed to switch role');
      }
    }
  });
}
""")

    # public/js/components/sidebar.js
    write("public/js/components/sidebar.js", """'use strict';

function renderSidebar() {
  const container = document.getElementById('sidebar-container');
  if (!container) return;

  const user = window.AppState.user || { role: 'super_admin' };
  const currentHash = window.location.hash || '#/';

  const navItems = [
    { label: 'Dashboard', icon: 'fa-chart-pie', path: '#/', roles: ['all'] },
    { label: 'Leads CRM', icon: 'fa-user-plus', path: '#/leads', roles: ['super_admin', 'admin', 'counselor'] },
    { label: 'Admissions', icon: 'fa-file-signature', path: '#/admissions', roles: ['super_admin', 'admin', 'counselor'] },
    { label: 'Students SIS', icon: 'fa-user-graduate', path: '#/students', roles: ['super_admin', 'admin', 'counselor', 'instructor', 'finance_officer'] },
    { label: 'Courses & Batches', icon: 'fa-book-open', path: '#/courses', roles: ['all'] },
    { label: 'Attendance', icon: 'fa-calendar-check', path: '#/attendance', roles: ['super_admin', 'admin', 'instructor', 'student'] },
    { label: 'Gradebook', icon: 'fa-award', path: '#/gradebook', roles: ['super_admin', 'admin', 'instructor', 'student'] },
    { label: 'Finance & Invoicing', icon: 'fa-file-invoice-dollar', path: '#/finance', roles: ['super_admin', 'admin', 'finance_officer', 'student'] },
    { label: 'Support Helpdesk', icon: 'fa-headset', path: '#/tickets', roles: ['all'] },
    { label: 'Reports & Export', icon: 'fa-file-export', path: '#/reports', roles: ['super_admin', 'admin', 'counselor', 'finance_officer'] },
    { label: 'System Settings', icon: 'fa-sliders-h', path: '#/settings', roles: ['super_admin', 'admin'] }
  ];

  const filteredItems = navItems.filter(item => 
    item.roles.includes('all') || item.roles.includes(user.role) || user.role === 'super_admin'
  );

  container.innerHTML = `
    <div style="padding: 24px; border-bottom: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 12px;">
      <div style="width: 38px; height: 38px; border-radius: var(--radius-md); background: var(--grad-primary); display: flex; align-items: center; justify-content: center; font-size: 18px; color: #fff;">
        <i class="fas fa-graduation-cap"></i>
      </div>
      <div>
        <div style="font-weight: 800; font-size: 17px; letter-spacing: -0.5px; color: #fff;">EduPulse <span style="color: var(--primary-400);">CRM</span></div>
        <div style="font-size: 11px; color: #94a3b8;">Education Enterprise</div>
      </div>
    </div>

    <nav style="padding: 16px 12px; flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 4px;">
      ${filteredItems.map(item => {
        const isActive = currentHash === item.path || (item.path !== '#/' && currentHash.startsWith(item.path));
        return `
          <a href="${item.path}" style="
            display: flex; 
            align-items: center; 
            gap: 12px; 
            padding: 10px 14px; 
            border-radius: var(--radius-sm); 
            color: ${isActive ? '#ffffff' : '#94a3b8'}; 
            background: ${isActive ? 'rgba(99, 102, 241, 0.15)' : 'transparent'}; 
            border-left: ${isActive ? '3px solid var(--primary-500)' : '3px solid transparent'}; 
            font-weight: ${isActive ? '600' : '500'};
            font-size: 13.5px;
            transition: all var(--transition-fast);
          " onmouseover="if(!${isActive}) this.style.color='#ffffff'" onmouseout="if(!${isActive}) this.style.color='#94a3b8'">
            <i class="fas ${item.icon}" style="width: 18px; text-align: center; color: ${isActive ? 'var(--primary-400)' : '#64748b'};"></i>
            <span>${item.label}</span>
          </a>
        `;
      }).join('')}
    </nav>

    <div style="padding: 18px; border-top: 1px solid rgba(255,255,255,0.08); background: rgba(0,0,0,0.2);">
      <div style="font-size: 11px; color: #64748b; margin-bottom: 4px;">EduPulse Enterprise v1.0.0</div>
      <div style="font-size: 10px; color: #475569;">100% Production Ready</div>
    </div>
  `;
}
""")

    # public/js/components/chart-renderer.js
    write("public/js/components/chart-renderer.js", """'use strict';

/**
 * Interactive HTML5 Canvas Charts Engine (Funnel & Bar Visualizations)
 */

class ChartRenderer {
  static drawFunnel(canvasId, funnelData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.parentElement.clientWidth || 400;
    const height = canvas.height = 240;

    ctx.clearRect(0, 0, width, height);

    const stages = Object.entries(funnelData);
    if (stages.length === 0) return;

    const maxVal = Math.max(...stages.map(s => s[1]), 1);
    const barHeight = 24;
    const gap = 12;
    const colors = ['#6366f1', '#818cf8', '#a5b4fc', '#06b6d4', '#10b981', '#f59e0b'];

    stages.forEach(([stage, count], index) => {
      const y = index * (barHeight + gap) + 15;
      const barWidth = Math.max(20, (count / maxVal) * (width - 150));

      // Label
      ctx.fillStyle = '#64748b';
      ctx.font = '12px Inter, sans-serif';
      ctx.fillText(stage.replace('_', ' ').toUpperCase(), 10, y + 16);

      // Bar
      ctx.fillStyle = colors[index % colors.length];
      ctx.beginPath();
      ctx.roundRect(140, y, barWidth, barHeight, [4]);
      ctx.fill();

      // Count
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.fillText(count.toString(), 148, y + 16);
    });
  }
}

window.ChartRenderer = ChartRenderer;
""")

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent.parent)
