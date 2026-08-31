#!/usr/bin/env python3
"""
EduPulse CRM - CSS Stylesheets Generator
Generates modern, sleek, glassmorphic, responsive CSS stylesheets.
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

    # public/css/main.css
    write("public/css/main.css", """/* ==========================================================================
   EduPulse CRM - Core Design System & Design Tokens
   ========================================================================== */

:root {
  /* Brand Palette */
  --primary-50: #eef2ff;
  --primary-100: #e0e7ff;
  --primary-200: #c7d2fe;
  --primary-300: #a5b4fc;
  --primary-400: #818cf8;
  --primary-500: #6366f1;
  --primary-600: #4f46e5;
  --primary-700: #4338ca;
  --primary-800: #3730a3;
  --primary-900: #312e81;

  /* Accent & Gradients */
  --accent-cyan: #06b6d4;
  --accent-purple: #a855f7;
  --accent-amber: #f59e0b;
  --accent-emerald: #10b981;
  --accent-rose: #f43f5e;
  
  --grad-primary: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  --grad-surface: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(243, 244, 246, 0.8) 100%);
  --grad-accent: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
  --grad-card-dark: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);

  /* Neutrals (Light Mode Default) */
  --bg-app: #f8fafc;
  --bg-surface: #ffffff;
  --bg-sidebar: #0f172a;
  --bg-card: #ffffff;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --text-light: #94a3b8;
  --border-color: #e2e8f0;
  --border-focus: #6366f1;

  /* Glassmorphism & Elevation */
  --glass-bg: rgba(255, 255, 255, 0.85);
  --glass-border: rgba(255, 255, 255, 0.4);
  --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.08);

  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.04);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.03);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);

  /* Typography & Sizing */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', Menlo, monospace;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-full: 9999px;
  --sidebar-width: 260px;
  --navbar-height: 70px;
  --transition-fast: 0.15s ease;
  --transition-normal: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Dark Mode Theme Tokens */
[data-theme='dark'] {
  --bg-app: #090d16;
  --bg-surface: #111827;
  --bg-sidebar: #070a11;
  --bg-card: #131b2e;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --text-light: #64748b;
  --border-color: #1e293b;
  --glass-bg: rgba(17, 24, 39, 0.85);
  --glass-border: rgba(255, 255, 255, 0.08);
  --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* CSS Reset & Global Layout */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  width: 100%;
  height: 100%;
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 1.5;
  color: var(--text-main);
  background-color: var(--bg-app);
  -webkit-font-smoothing: antialiased;
}

a {
  color: var(--primary-600);
  text-decoration: none;
  transition: color var(--transition-fast);
}

a:hover {
  color: var(--primary-700);
}

button, input, select, textarea {
  font-family: inherit;
  font-size: inherit;
}

/* App Shell Structure */
#app {
  display: flex;
  width: 100vw;
  min-height: 100vh;
  overflow-x: hidden;
}

.app-sidebar {
  width: var(--sidebar-width);
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  background-color: var(--bg-sidebar);
  color: #ffffff;
  display: flex;
  flex-direction: column;
  z-index: 100;
  transition: transform var(--transition-normal);
  border-right: 1px solid rgba(255, 255, 255, 0.06);
}

.app-main {
  flex: 1;
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--bg-app);
  transition: margin-left var(--transition-normal);
}

.app-navbar {
  height: var(--navbar-height);
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  position: sticky;
  top: 0;
  z-index: 90;
}

.content-container {
  flex: 1;
  padding: 28px;
  max-width: 1600px;
  width: 100%;
  margin: 0 auto;
}
""")

    # public/css/dashboard.css
    write("public/css/dashboard.css", """/* Dashboard Analytics & Metrics Styling */

.dashboard-hero {
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
  color: #ffffff;
  padding: 32px;
  border-radius: var(--radius-lg);
  margin-bottom: 28px;
  box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.3);
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.dashboard-hero::after {
  content: '';
  position: absolute;
  right: -60px;
  top: -60px;
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 70%);
  border-radius: 50%;
  pointer-events: none;
}

.hero-text h1 {
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 8px;
}

.hero-text p {
  color: #c7d2fe;
  font-size: 14px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 28px;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 22px;
  display: flex;
  align-items: center;
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.stat-icon-wrapper {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 18px;
}

.stat-icon-blue { background: #e0f2fe; color: #0284c7; }
.stat-icon-emerald { background: #d1fae5; color: #059669; }
.stat-icon-purple { background: #f3e8ff; color: #9333ea; }
.stat-icon-amber { background: #fef3c7; color: #d97706; }
.stat-icon-rose { background: #ffe4e6; color: #e11d48; }

.stat-info .stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.2;
}

.stat-info .stat-label {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 500;
  margin-top: 2px;
}

.dashboard-charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  margin-bottom: 28px;
}

.card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.card-header {
  padding: 18px 24px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-main);
}

.card-body {
  padding: 24px;
}
""")

    # public/css/leads.css
    write("public/css/leads.css", """/* Leads Pipeline & Kanban Styling */

.leads-pipeline {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 20px;
  min-height: 600px;
}

.pipeline-col {
  flex: 0 0 290px;
  background: rgba(241, 245, 249, 0.6);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
}

[data-theme='dark'] .pipeline-col {
  background: rgba(15, 23, 42, 0.6);
}

.pipeline-col-header {
  padding: 14px 18px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 600;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.pipeline-cards-list {
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
  overflow-y: auto;
}

.lead-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 14px;
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.lead-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-400);
}

.lead-score-pill {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-weight: 700;
}

.score-hot { background: #fee2e2; color: #b91c1c; }
.score-warm { background: #fef3c7; color: #b45309; }
.score-cold { background: #e0f2fe; color: #0369a1; }
""")

    # public/css/components.css
    write("public/css/components.css", """/* Reusable UI Components */

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-weight: 500;
  border-radius: var(--radius-sm);
  padding: 8px 16px;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.btn-primary {
  background-color: var(--primary-600);
  color: #ffffff;
}

.btn-primary:hover {
  background-color: var(--primary-700);
}

.btn-secondary {
  background-color: transparent;
  border-color: var(--border-color);
  color: var(--text-main);
}

.btn-secondary:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.btn-success { background-color: var(--accent-emerald); color: #ffffff; }
.btn-danger { background-color: var(--accent-rose); color: #ffffff; }
.btn-sm { padding: 5px 10px; font-size: 12px; }
.btn-lg { padding: 12px 24px; font-size: 15px; }

/* Form Controls */
.form-group {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 6px;
}

.form-control {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  background-color: var(--bg-card);
  color: var(--text-main);
  outline: none;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.form-control:focus {
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

/* Tables */
.table-responsive {
  width: 100%;
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.table th {
  background: rgba(0, 0, 0, 0.02);
  padding: 12px 16px;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border-color);
}

.table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-main);
  vertical-align: middle;
}

.table tr:hover td {
  background-color: rgba(99, 102, 241, 0.03);
}

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 9px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 600;
}

.badge-primary { background: #e0e7ff; color: #4338ca; }
.badge-success { background: #d1fae5; color: #065f46; }
.badge-warning { background: #fef3c7; color: #92400e; }
.badge-danger { background: #fee2e2; color: #991b1b; }
.badge-info { background: #e0f2fe; color: #075985; }

/* Modals */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: all var(--transition-normal);
}

.modal-overlay.active {
  opacity: 1;
  visibility: visible;
}

.modal-dialog {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--border-color);
  transform: scale(0.95);
  transition: transform var(--transition-normal);
}

.modal-overlay.active .modal-dialog {
  transform: scale(1);
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-body {
  padding: 24px;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* Toast Notifications */
#toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 9999;
}

.toast {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-left: 4px solid var(--primary-600);
  border-radius: var(--radius-sm);
  padding: 14px 18px;
  min-width: 300px;
  box-shadow: var(--shadow-lg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  animation: slideInRight 0.3s ease;
}

.toast-success { border-left-color: var(--accent-emerald); }
.toast-error { border-left-color: var(--accent-rose); }
.toast-info { border-left-color: var(--accent-cyan); }
""")

    # public/css/animations.css
    write("public/css/animations.css", """/* Keyframe Animations & Micro-Interactions */

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideInRight {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

@keyframes pulseGlow {
  0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }
  100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
}

.fade-in {
  animation: fadeIn 0.25s ease-in-out;
}
""")

    # public/css/responsive.css
    write("public/css/responsive.css", """/* Responsive Layout Rules */

@media (max-width: 1024px) {
  .dashboard-charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .app-sidebar {
    transform: translateX(-100%);
  }

  .app-sidebar.mobile-open {
    transform: translateX(0);
  }

  .app-main {
    margin-left: 0;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .content-container {
    padding: 16px;
  }
}
""")

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent.parent)
