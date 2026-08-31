#!/usr/bin/env python3
"""
EduPulse CRM - Views and Router Generator
Generates all Single Page Application interactive views and client router.
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

    # public/js/views/auth.view.js
    write("public/js/views/auth.view.js", """'use strict';

const AuthView = {
  render(container) {
    container.innerHTML = `
      <div style="max-width: 440px; margin: 40px auto; background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 36px; box-shadow: var(--shadow-xl);">
        <div style="text-align: center; margin-bottom: 28px;">
          <div style="width: 54px; height: 54px; border-radius: var(--radius-md); background: var(--grad-primary); display: inline-flex; align-items: center; justify-content: center; font-size: 26px; color: #fff; margin-bottom: 12px;">
            <i class="fas fa-graduation-cap"></i>
          </div>
          <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Welcome to EduPulse</h2>
          <p style="color: var(--text-muted); font-size: 13px; margin-top: 4px;">Sign in to access your portal</p>
        </div>

        <form id="login-form">
          <div class="form-group">
            <label class="form-label">Username or Institutional Email</label>
            <input type="text" id="login-username" class="form-control" placeholder="e.g. superadmin or rachel.green@edupulse.edu" required>
          </div>

          <div class="form-group">
            <label class="form-label">Password</label>
            <input type="password" id="login-password" class="form-control" placeholder="••••••••" required>
          </div>

          <button type="submit" class="btn btn-primary" style="width: 100%; padding: 12px; margin-top: 10px; font-size: 14px;">
            Sign In to Dashboard
          </button>
        </form>

        <div style="margin-top: 24px; padding-top: 20px; border-top: 1px solid var(--border-color); text-align: center;">
          <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 8px;">Quick Demo Accounts (Click to Autofill):</p>
          <div style="display: flex; flex-wrap: wrap; gap: 6px; justify-content: center;">
            <button class="btn btn-secondary btn-sm demo-fill" data-u="superadmin" data-p="admin123">Super Admin</button>
            <button class="btn btn-secondary btn-sm demo-fill" data-u="counselor_rachel" data-p="counselor123">Counselor</button>
            <button class="btn btn-secondary btn-sm demo-fill" data-u="prof_alan" data-p="faculty123">Instructor</button>
            <button class="btn btn-secondary btn-sm demo-fill" data-u="finance_elena" data-p="finance123">Finance</button>
            <button class="btn btn-secondary btn-sm demo-fill" data-u="student_rohit" data-p="student123">Student</button>
          </div>
        </div>
      </div>
    `;

    document.querySelectorAll('.demo-fill').forEach(btn => {
      btn.addEventListener('click', () => {
        document.getElementById('login-username').value = btn.dataset.u;
        document.getElementById('login-password').value = btn.dataset.p;
      });
    });

    document.getElementById('login-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const u = document.getElementById('login-username').value;
      const p = document.getElementById('login-password').value;

      try {
        const res = await window.API.post('/auth/login', { username: u, password: p });
        window.AppState.setUser(res.data.user, res.data.token);
        window.Toast.success(`Welcome back, ${res.data.user.fullName}!`);
        renderNavbar();
        renderSidebar();
        window.Router.navigate('#/');
      } catch (err) {
        // Handled by API error toast
      }
    });
  }
};

window.AuthView = AuthView;
""")

    # public/js/views/dashboard.view.js
    write("public/js/views/dashboard.view.js", """'use strict';

const DashboardView = {
  async render(container) {
    container.innerHTML = `
      <div style="display: flex; justify-content: center; padding: 50px;">
        <i class="fas fa-spinner fa-spin fa-2x" style="color: var(--primary-600);"></i>
      </div>
    `;

    try {
      const res = await window.API.get('/analytics/summary');
      const { kpis, funnel, recentActivity, announcements } = res.data;

      container.innerHTML = `
        <!-- Hero Welcome Header -->
        <div class="dashboard-hero">
          <div class="hero-text">
            <h1>Education Management Cockpit</h1>
            <p>Real-time analytics for admissions, student performance, revenue collection, and inquiries.</p>
          </div>
          <div style="display: flex; gap: 12px;">
            <button class="btn btn-primary" onclick="window.Router.navigate('#/leads')" style="background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3);">
              <i class="fas fa-plus"></i> New Lead
            </button>
            <button class="btn btn-primary" onclick="window.Router.navigate('#/admissions')" style="background: #ffffff; color: #1e1b4b;">
              <i class="fas fa-file-invoice"></i> Applications
            </button>
          </div>
        </div>

        <!-- KPI Summary Cards -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon-wrapper stat-icon-blue">
              <i class="fas fa-user-plus"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">${kpis.totalLeads}</div>
              <div class="stat-label">Total Inbound Leads</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrapper stat-icon-emerald">
              <i class="fas fa-user-graduate"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">${kpis.totalStudents}</div>
              <div class="stat-label">Enrolled Students</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrapper stat-icon-purple">
              <i class="fas fa-dollar-sign"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">$${kpis.totalRevenueCollected.toLocaleString()}</div>
              <div class="stat-label">Tuition Collected</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrapper stat-icon-amber">
              <i class="fas fa-percentage"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">${kpis.conversionRate}%</div>
              <div class="stat-label">Lead Conversion Rate</div>
            </div>
          </div>
        </div>

        <!-- Charts & Feed Grid -->
        <div class="dashboard-charts-grid">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title"><i class="fas fa-filter" style="color: var(--primary-600); margin-right: 8px;"></i> Admissions Conversion Funnel</h3>
              <span class="badge badge-primary">Live Pipeline</span>
            </div>
            <div class="card-body">
              <canvas id="funnelCanvas" style="width: 100%; height: 240px;"></canvas>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <h3 class="card-title"><i class="fas fa-bullhorn" style="color: var(--accent-amber); margin-right: 8px;"></i> Campus Bulletins</h3>
            </div>
            <div class="card-body" style="padding: 16px;">
              ${announcements.map(a => `
                <div style="padding: 12px; border-bottom: 1px solid var(--border-color); margin-bottom: 8px;">
                  <div style="font-weight: 600; font-size: 13px; color: var(--text-main); margin-bottom: 4px;">${a.title}</div>
                  <div style="font-size: 12px; color: var(--text-muted); line-height: 1.4;">${a.content}</div>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      `;

      // Render Funnel Chart
      window.ChartRenderer.drawFunnel('funnelCanvas', funnel);
    } catch (err) {
      container.innerHTML = `<div class="card card-body"><p style="color:red">Failed to load dashboard data: ${err.message}</p></div>`;
    }
  }
};

window.DashboardView = DashboardView;
""")

    # public/js/views/leads.view.js
    write("public/js/views/leads.view.js", """'use strict';

const LeadsView = {
  async render(container) {
    container.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
        <div>
          <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Leads & Admissions Pipeline</h2>
          <p style="color: var(--text-muted); font-size: 13px;">Manage prospective inquiries, follow-ups, and counselor assignments</p>
        </div>
        <button class="btn btn-primary" id="btn-add-lead">
          <i class="fas fa-plus"></i> Capture New Lead
        </button>
      </div>

      <div class="leads-pipeline" id="leads-kanban-board">
        <div style="padding: 30px; text-align: center; width: 100%;">
          <i class="fas fa-spinner fa-spin fa-2x"></i>
        </div>
      </div>
    `;

    document.getElementById('btn-add-lead').addEventListener('click', () => {
      this.openCreateLeadModal();
    });

    await this.loadLeads();
  },

  async loadLeads() {
    try {
      const res = await window.API.get('/leads');
      const leads = res.data;

      const stages = [
        { key: 'new', title: 'New Inquiries', icon: 'fa-envelope-open' },
        { key: 'contacted', title: 'Contacted', icon: 'fa-phone-volume' },
        { key: 'qualified', title: 'Qualified', icon: 'fa-check-double' },
        { key: 'counseling_scheduled', title: 'Counseling', icon: 'fa-calendar-alt' },
        { key: 'application_submitted', title: 'App Submitted', icon: 'fa-file-alt' },
        { key: 'enrolled', title: 'Enrolled', icon: 'fa-user-graduate' }
      ];

      const board = document.getElementById('leads-kanban-board');
      board.innerHTML = stages.map(st => {
        const stageLeads = leads.filter(l => l.stage === st.key);
        return `
          <div class="pipeline-col">
            <div class="pipeline-col-header">
              <span><i class="fas ${st.icon}" style="margin-right:6px;"></i> ${st.title}</span>
              <span class="badge badge-primary">${stageLeads.length}</span>
            </div>
            <div class="pipeline-cards-list">
              ${stageLeads.map(lead => {
                let scoreClass = 'score-cold';
                if (lead.lead_score >= 75) scoreClass = 'score-hot';
                else if (lead.lead_score >= 45) scoreClass = 'score-warm';

                return `
                  <div class="lead-card" onclick="window.LeadsView.openLeadDetail('${lead.id}')">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                      <span class="lead-score-pill ${scoreClass}">Score: ${lead.lead_score}</span>
                      <span style="font-size:11px; color:var(--text-muted);">${lead.source}</span>
                    </div>
                    <div style="font-weight:600; font-size:14px; color:var(--text-main);">${lead.fullName}</div>
                    <div style="font-size:12px; color:var(--text-muted); margin-top:2px;">
                      <i class="fas fa-graduation-cap" style="width:14px;"></i> ${lead.course ? lead.course.code : 'Course TBD'}
                    </div>
                    <div style="font-size:12px; color:var(--text-muted); margin-top:2px;">
                      <i class="fas fa-map-marker-alt" style="width:14px;"></i> ${lead.city || 'Global'}
                    </div>
                    <div style="margin-top:10px; padding-top:8px; border-top:1px solid var(--border-color); display:flex; justify-content:space-between; align-items:center; font-size:11px; color:var(--text-light);">
                      <span><i class="fas fa-user-tie"></i> ${lead.counselor ? lead.counselor.name.split(' ')[0] : 'Unassigned'}</span>
                      <span><i class="fas fa-comments"></i> ${lead.interactionsCount || 0}</span>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;
      }).join('');
    } catch (err) {
      console.error(err);
    }
  },

  async openLeadDetail(leadId) {
    try {
      const res = await window.API.get(`/leads/${leadId}`);
      const lead = res.data;

      const body = `
        <div>
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border-color);">
            <div>
              <h3 style="font-size: 18px; font-weight: 700; color: var(--text-main);">${lead.fullName}</h3>
              <p style="font-size: 13px; color: var(--text-muted);">${lead.email} | ${lead.phone}</p>
            </div>
            <span class="lead-score-pill ${lead.lead_score >= 75 ? 'score-hot' : 'score-warm'}" style="font-size: 13px; padding: 4px 12px;">
              Score: ${lead.lead_score} (${lead.lead_score >= 75 ? 'Hot Intent' : 'Warm'})
            </span>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
            <div>
              <label class="form-label">Current Pipeline Stage</label>
              <select class="form-control" id="lead-stage-select">
                <option value="new" ${lead.stage === 'new' ? 'selected' : ''}>New Inquiry</option>
                <option value="contacted" ${lead.stage === 'contacted' ? 'selected' : ''}>Contacted</option>
                <option value="qualified" ${lead.stage === 'qualified' ? 'selected' : ''}>Qualified</option>
                <option value="counseling_scheduled" ${lead.stage === 'counseling_scheduled' ? 'selected' : ''}>Counseling Scheduled</option>
                <option value="application_submitted" ${lead.stage === 'application_submitted' ? 'selected' : ''}>Application Submitted</option>
                <option value="enrolled" ${lead.stage === 'enrolled' ? 'selected' : ''}>Enrolled</option>
                <option value="lost" ${lead.stage === 'lost' ? 'selected' : ''}>Lost / Closed</option>
              </select>
            </div>
            <div>
              <label class="form-label">Interested Program</label>
              <input type="text" class="form-control" value="${lead.course ? lead.course.title : 'None'}" disabled>
            </div>
          </div>

          <div class="card" style="margin-bottom: 20px;">
            <div class="card-header" style="padding: 12px 18px;">
              <h4 style="font-size: 14px; font-weight: 600;">Log Call / Counseling Interaction</h4>
            </div>
            <div class="card-body" style="padding: 16px;">
              <div class="form-group">
                <textarea id="intr-summary" class="form-control" rows="2" placeholder="Enter interaction discussion notes..."></textarea>
              </div>
              <button class="btn btn-primary btn-sm" id="btn-save-intr">
                <i class="fas fa-save"></i> Record Interaction
              </button>
            </div>
          </div>
        </div>
      `;

      const { close } = window.Modal.open({
        title: `Lead Profile: ${lead.fullName}`,
        body,
        footer: `
          <button class="btn btn-secondary btn-sm" id="modal-cancel">Close</button>
          <button class="btn btn-primary btn-sm" id="modal-update-lead">Save Changes</button>
        `,
        width: '650px'
      });

      document.getElementById('modal-cancel').addEventListener('click', close);

      document.getElementById('btn-save-intr').addEventListener('click', async () => {
        const text = document.getElementById('intr-summary').value;
        if (!text) return window.Toast.error('Please enter notes');
        await window.API.post(`/leads/${lead.id}/interactions`, {
          interaction_type: 'phone_call',
          summary: text
        });
        window.Toast.success('Interaction logged!');
        close();
        window.LeadsView.loadLeads();
      });

      document.getElementById('modal-update-lead').addEventListener('click', async () => {
        const newStage = document.getElementById('lead-stage-select').value;
        await window.API.put(`/leads/${lead.id}`, { stage: newStage });
        window.Toast.success('Lead updated successfully.');
        close();
        window.LeadsView.loadLeads();
      });
    } catch (err) {
      console.error(err);
    }
  },

  openCreateLeadModal() {
    const body = `
      <form id="create-lead-form">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div class="form-group">
            <label class="form-label">First Name *</label>
            <input type="text" id="nl-first-name" class="form-control" required>
          </div>
          <div class="form-group">
            <label class="form-label">Last Name *</label>
            <input type="text" id="nl-last-name" class="form-control" required>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div class="form-group">
            <label class="form-label">Email Address *</label>
            <input type="email" id="nl-email" class="form-control" required>
          </div>
          <div class="form-group">
            <label class="form-label">Phone Number *</label>
            <input type="tel" id="nl-phone" class="form-control" required>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div class="form-group">
            <label class="form-label">Lead Source</label>
            <select id="nl-source" class="form-control">
              <option value="Website Inbound">Website Inbound</option>
              <option value="Google Search Ads">Google Search Ads</option>
              <option value="Social Media Campaign">Social Media Campaign</option>
              <option value="Education Fair 2026">Education Fair 2026</option>
              <option value="Alumni Referral">Alumni Referral</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">City</label>
            <input type="text" id="nl-city" class="form-control" placeholder="e.g. Mumbai">
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Counselor Notes / Inquiries</label>
          <textarea id="nl-notes" class="form-control" rows="2" placeholder="Student background & interests..."></textarea>
        </div>
      </form>
    `;

    const { close } = window.Modal.open({
      title: 'Capture Inbound Student Lead',
      body,
      footer: `
        <button class="btn btn-secondary btn-sm" id="nl-cancel">Cancel</button>
        <button class="btn btn-primary btn-sm" id="nl-submit">Create Lead</button>
      `
    });

    document.getElementById('nl-cancel').addEventListener('click', close);
    document.getElementById('nl-submit').addEventListener('click', async () => {
      const payload = {
        first_name: document.getElementById('nl-first-name').value,
        last_name: document.getElementById('nl-last-name').value,
        email: document.getElementById('nl-email').value,
        phone: document.getElementById('nl-phone').value,
        source: document.getElementById('nl-source').value,
        city: document.getElementById('nl-city').value,
        notes: document.getElementById('nl-notes').value
      };

      if (!payload.first_name || !payload.email || !payload.phone) {
        return window.Toast.error('Please fill required fields.');
      }

      await window.API.post('/leads', payload);
      window.Toast.success('Lead created and assigned!');
      close();
      window.LeadsView.loadLeads();
    });
  }
};

window.LeadsView = LeadsView;
""")

    # public/js/views/admissions.view.js
    write("public/js/views/admissions.view.js", """'use strict';

const AdmissionsView = {
  async render(container) {
    container.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
        <div>
          <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Admissions & Enrollment Processing</h2>
          <p style="color: var(--text-muted); font-size: 13px;">Review submitted entrance applications, verify transcripts, and issue enrollment letters</p>
        </div>
      </div>

      <div class="card">
        <div class="table-responsive">
          <table class="table" id="apps-table">
            <thead>
              <tr>
                <th>Applicant</th>
                <th>Program Applied</th>
                <th>Academic Score</th>
                <th>Submission Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody id="apps-table-body">
              <tr><td colspan="6" style="text-align:center; padding:30px;"><i class="fas fa-spinner fa-spin"></i></td></tr>
            </tbody>
          </table>
        </div>
      </div>
    `;

    await this.loadApplications();
  },

  async loadApplications() {
    try {
      const res = await window.API.get('/admissions/applications');
      const apps = res.data;

      const tbody = document.getElementById('apps-table-body');
      if (apps.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;">No applications found.</td></tr>`;
        return;
      }

      tbody.innerHTML = apps.map(app => `
        <tr>
          <td>
            <div style="font-weight:600; color:var(--text-main);">${app.first_name} ${app.last_name}</div>
            <div style="font-size:12px; color:var(--text-muted);">${app.email} | ${app.phone}</div>
          </td>
          <td>
            <div style="font-weight:500;">${app.course ? app.course.title : 'Program'}</div>
            <span class="badge badge-primary">${app.course ? app.course.code : 'CODE'}</span>
          </td>
          <td>
            <div style="font-size:13px;">High School: <strong>${app.high_school_percentage}%</strong></div>
            <div style="font-size:12px; color:var(--text-muted);">Entrance Test: ${app.entrance_exam_score}%</div>
          </td>
          <td style="font-size:12px; color:var(--text-muted);">
            ${new Date(app.applied_at).toLocaleDateString()}
          </td>
          <td>
            <span class="badge ${app.status === 'enrolled' ? 'badge-success' : 'badge-warning'}">
              ${app.status.toUpperCase()}
            </span>
          </td>
          <td>
            ${app.status !== 'enrolled' ? `
              <button class="btn btn-success btn-sm" onclick="window.AdmissionsView.enrollStudent('${app.id}')">
                <i class="fas fa-check"></i> Enroll Student
              </button>
            ` : `
              <span style="font-size:12px; color:var(--accent-emerald); font-weight:600;"><i class="fas fa-id-card"></i> Student Enrolled</span>
            `}
          </td>
        </tr>
      `).join('');
    } catch (err) {
      console.error(err);
    }
  },

  async enrollStudent(appId) {
    if (!confirm('Approve application and formally enroll student into active cohort?')) return;

    try {
      const res = await window.API.post(`/admissions/applications/${appId}/enroll`, {
        review_notes: 'Approved through Admissions Portal.'
      });
      window.Toast.success(`Student Enrolled! Student ID: ${res.data.student.student_id_number}`);
      await this.loadApplications();
    } catch (err) {
      // Handled by API error
    }
  }
};

window.AdmissionsView = AdmissionsView;
""")

    # public/js/views/students.view.js
    write("public/js/views/students.view.js", """'use strict';

const StudentsView = {
  async render(container) {
    container.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
        <div>
          <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Student Information System (SIS)</h2>
          <p style="color: var(--text-muted); font-size: 13px;">Active student registry, academic history, guardians, and GPA tracking</p>
        </div>
      </div>

      <div class="card">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Student</th>
                <th>Student ID</th>
                <th>Program & Batch</th>
                <th>Cumulative GPA</th>
                <th>Attendance</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="students-table-body">
              <tr><td colspan="6" style="text-align:center; padding:30px;"><i class="fas fa-spinner fa-spin"></i></td></tr>
            </tbody>
          </table>
        </div>
      </div>
    `;

    await this.loadStudents();
  },

  async loadStudents() {
    try {
      const res = await window.API.get('/students');
      const students = res.data;
      const tbody = document.getElementById('students-table-body');

      tbody.innerHTML = students.map(s => `
        <tr>
          <td>
            <div style="font-weight:600; color:var(--text-main);">${s.fullName}</div>
            <div style="font-size:12px; color:var(--text-muted);">${s.email}</div>
          </td>
          <td>
            <code style="font-family:var(--font-mono); font-weight:600; background:rgba(0,0,0,0.05); padding:3px 6px; border-radius:4px;">${s.student_id_number}</code>
          </td>
          <td>
            <div style="font-weight:500;">${s.course ? s.course.title : 'Program'}</div>
            <div style="font-size:12px; color:var(--text-muted);">${s.batch ? s.batch.batch_name : 'Cohort Alpha'}</div>
          </td>
          <td>
            <span style="font-weight:700; font-size:15px; color:${s.cumulative_gpa >= 3.5 ? 'var(--accent-emerald)' : 'var(--text-main)'};">
              ${s.cumulative_gpa.toFixed(2)} / 4.0
            </span>
          </td>
          <td>
            <div style="display:flex; align-items:center; gap:8px;">
              <div style="flex:1; height:6px; background:var(--border-color); border-radius:3px; overflow:hidden; width:80px;">
                <div style="width:${s.attendancePercentage}%; height:100%; background:${s.attendancePercentage >= 75 ? 'var(--accent-emerald)' : 'var(--accent-rose)'};"></div>
              </div>
              <span style="font-size:12px; font-weight:600;">${s.attendancePercentage}%</span>
            </div>
          </td>
          <td>
            <span class="badge badge-success">${s.enrollment_status.toUpperCase()}</span>
          </td>
        </tr>
      `).join('');
    } catch (err) {
      console.error(err);
    }
  }
};

window.StudentsView = StudentsView;
""")

    # public/js/views/courses.view.js
    write("public/js/views/courses.view.js", """'use strict';

const CoursesView = {
  async render(container) {
    container.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
        <div>
          <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Course Catalog & Curriculum</h2>
          <p style="color: var(--text-muted); font-size: 13px;">Degree programs, credit requirements, tuition fees, and active cohorts</p>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px;" id="courses-grid">
        <div style="padding: 40px; text-align: center;"><i class="fas fa-spinner fa-spin fa-2x"></i></div>
      </div>
    `;

    await this.loadCourses();
  },

  async loadCourses() {
    try {
      const res = await window.API.get('/courses');
      const courses = res.data;
      const grid = document.getElementById('courses-grid');

      grid.innerHTML = courses.map(c => `
        <div class="card" style="display:flex; flex-direction:column; justify-content:space-between;">
          <div class="card-body">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
              <span class="badge badge-primary">${c.code}</span>
              <span class="badge badge-info">${c.degree_level}</span>
            </div>
            <h3 style="font-size:17px; font-weight:700; color:var(--text-main); margin-bottom:8px;">${c.title}</h3>
            <p style="font-size:13px; color:var(--text-muted); line-height:1.5; margin-bottom:16px;">${c.description}</p>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; font-size:12px; color:var(--text-muted); padding:12px; background:rgba(0,0,0,0.02); border-radius:var(--radius-sm); margin-bottom:16px;">
              <div><i class="fas fa-clock"></i> <strong>${c.duration_months} Months</strong></div>
              <div><i class="fas fa-coins"></i> <strong>${c.total_credits} Credits</strong></div>
              <div><i class="fas fa-users"></i> <strong>${c.enrolledCount || 0} Enrolled</strong></div>
              <div><i class="fas fa-layer-group"></i> <strong>${c.modules ? c.modules.length : 0} Modules</strong></div>
            </div>
          </div>
          <div class="card-header" style="background:transparent; border-top:1px solid var(--border-color); display:flex; justify-content:space-between; align-items:center;">
            <div>
              <span style="font-size:11px; color:var(--text-muted); text-transform:uppercase;">Tuition Fee</span>
              <div style="font-size:18px; font-weight:800; color:var(--primary-600);">$${c.base_tuition_fee.toLocaleString()}</div>
            </div>
            <button class="btn btn-secondary btn-sm" onclick="window.Toast.info('Curriculum syllabus preview ready.')">
              <i class="fas fa-file-alt"></i> Syllabus
            </button>
          </div>
        </div>
      `).join('');
    } catch (err) {
      console.error(err);
    }
  }
};

window.CoursesView = CoursesView;
""")

    # public/js/views/finance.view.js
    write("public/js/views/finance.view.js", """'use strict';

const FinanceView = {
  async render(container) {
    container.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
        <div>
          <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Tuition Billing & Invoicing Ledger</h2>
          <p style="color: var(--text-muted); font-size: 13px;">Track student invoices, partial payments, receipts, and outstanding dues</p>
        </div>
      </div>

      <div class="card">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Invoice #</th>
                <th>Student</th>
                <th>Title</th>
                <th>Total Billed</th>
                <th>Paid</th>
                <th>Balance Due</th>
                <th>Due Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody id="invoices-table-body">
              <tr><td colspan="9" style="text-align:center; padding:30px;"><i class="fas fa-spinner fa-spin"></i></td></tr>
            </tbody>
          </table>
        </div>
      </div>
    `;

    await this.loadInvoices();
  },

  async loadInvoices() {
    try {
      const res = await window.API.get('/finance/invoices');
      const invoices = res.data;
      const tbody = document.getElementById('invoices-table-body');

      tbody.innerHTML = invoices.map(inv => `
        <tr>
          <td><code style="font-family:var(--font-mono); font-weight:600;">${inv.invoice_number}</code></td>
          <td>
            <div style="font-weight:600;">${inv.student ? inv.student.first_name + ' ' + inv.student.last_name : 'Student'}</div>
            <div style="font-size:11px; color:var(--text-muted);">${inv.student ? inv.student.student_id_number : ''}</div>
          </td>
          <td><span style="font-size:13px;">${inv.title}</span></td>
          <td style="font-weight:700;">$${inv.total_amount.toLocaleString()}</td>
          <td style="color:var(--accent-emerald); font-weight:600;">$${inv.amount_paid.toLocaleString()}</td>
          <td style="color:${inv.balance_due > 0 ? 'var(--accent-rose)' : 'var(--text-muted)'}; font-weight:700;">
            $${inv.balance_due.toLocaleString()}
          </td>
          <td style="font-size:12px; color:var(--text-muted);">${inv.due_date}</td>
          <td>
            <span class="badge ${inv.status === 'paid' ? 'badge-success' : inv.status === 'partially_paid' ? 'badge-info' : 'badge-warning'}">
              ${inv.status.replace('_', ' ').toUpperCase()}
            </span>
          </td>
          <td>
            ${inv.balance_due > 0 ? `
              <button class="btn btn-primary btn-sm" onclick="window.FinanceView.openPaymentModal('${inv.id}', ${inv.balance_due})">
                <i class="fas fa-credit-card"></i> Pay
              </button>
            ` : `
              <span style="font-size:12px; color:var(--accent-emerald); font-weight:600;"><i class="fas fa-check-circle"></i> Paid in Full</span>
            `}
          </td>
        </tr>
      `).join('');
    } catch (err) {
      console.error(err);
    }
  },

  openPaymentModal(invoiceId, balanceDue) {
    const body = `
      <div>
        <p style="margin-bottom:16px; font-size:13px; color:var(--text-muted);">
          Enter payment transaction details to credit against invoice balance.
        </p>
        <div class="form-group">
          <label class="form-label">Payment Amount ($) *</label>
          <input type="number" id="pay-amount" class="form-control" value="${balanceDue}" max="${balanceDue}" min="1" step="0.01">
        </div>
        <div class="form-group">
          <label class="form-label">Payment Method</label>
          <select id="pay-method" class="form-control">
            <option value="bank_transfer">Direct Bank Transfer</option>
            <option value="upi">UPI / Instant Online</option>
            <option value="credit_card">Credit / Debit Card</option>
            <option value="cheque">Cheque / Demand Draft</option>
            <option value="cash">Institutional Cash Desk</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Transaction Reference Number</label>
          <input type="text" id="pay-ref" class="form-control" placeholder="e.g. TXN-994829104">
        </div>
      </div>
    `;

    const { close } = window.Modal.open({
      title: 'Record Tuition Fee Payment',
      body,
      footer: `
        <button class="btn btn-secondary btn-sm" id="pay-cancel">Cancel</button>
        <button class="btn btn-success btn-sm" id="pay-submit"><i class="fas fa-receipt"></i> Process Receipt</button>
      `
    });

    document.getElementById('pay-cancel').addEventListener('click', close);
    document.getElementById('pay-submit').addEventListener('click', async () => {
      const amount = parseFloat(document.getElementById('pay-amount').value);
      const method = document.getElementById('pay-method').value;
      const ref = document.getElementById('pay-ref').value;

      if (isNaN(amount) || amount <= 0) return window.Toast.error('Please enter valid amount');

      await window.API.post(`/finance/invoices/${invoiceId}/pay`, {
        amount,
        payment_method: method,
        transaction_reference: ref
      });

      window.Toast.success(`Payment of $${amount} recorded successfully!`);
      close();
      window.FinanceView.loadInvoices();
    });
  }
};

window.FinanceView = FinanceView;
""")

    # public/js/views/attendance.view.js
    write("public/js/views/attendance.view.js", """'use strict';

const AttendanceView = {
  async render(container) {
    container.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
        <div>
          <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Daily & Lecture Attendance Logging</h2>
          <p style="color: var(--text-muted); font-size: 13px;">Mark lecture participation, monitor attendance thresholds, and trigger deficiency alerts</p>
        </div>
        <button class="btn btn-primary" onclick="window.Toast.success('Attendance session submitted successfully.')">
          <i class="fas fa-save"></i> Save Attendance Sheet
        </button>
      </div>

      <div class="card" style="margin-bottom: 24px;">
        <div class="card-body" style="display: flex; gap: 16px; align-items: center;">
          <div style="flex: 1;">
            <label class="form-label">Cohort Batch</label>
            <select class="form-control" id="att-batch-select">
              <option value="batch_cs_2026_a">CS Fall 2026 - Cohort Alpha</option>
              <option value="batch_ai_2026_a">AI Master 2026 - Evening Cohort</option>
            </select>
          </div>
          <div style="flex: 1;">
            <label class="form-label">Session Date</label>
            <input type="date" class="form-control" value="${new Date().toISOString().split('T')[0]}">
          </div>
          <div style="flex: 1;">
            <label class="form-label">Topic / Lecture</label>
            <input type="text" class="form-control" value="Advanced Full-Stack Engineering & Microservices">
          </div>
        </div>
      </div>

      <div class="card">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Student ID</th>
                <th>Student Name</th>
                <th>Current %</th>
                <th>Mark Status</th>
                <th>Remarks</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>STU-2026-001</code></td>
                <td><strong>Rohit Sharma</strong></td>
                <td><span class="badge badge-success">96%</span></td>
                <td>
                  <div style="display: flex; gap: 8px;">
                    <label><input type="radio" name="att_001" value="present" checked> Present</label>
                    <label><input type="radio" name="att_001" value="absent"> Absent</label>
                    <label><input type="radio" name="att_001" value="late"> Late</label>
                  </div>
                </td>
                <td><input type="text" class="form-control" placeholder="Optional notes..." style="padding:4px 8px; font-size:12px;"></td>
              </tr>
              <tr>
                <td><code>STU-2026-002</code></td>
                <td><strong>Ananya Iyer</strong></td>
                <td><span class="badge badge-success">98%</span></td>
                <td>
                  <div style="display: flex; gap: 8px;">
                    <label><input type="radio" name="att_002" value="present" checked> Present</label>
                    <label><input type="radio" name="att_002" value="absent"> Absent</label>
                    <label><input type="radio" name="att_002" value="late"> Late</label>
                  </div>
                </td>
                <td><input type="text" class="form-control" placeholder="Optional notes..." style="padding:4px 8px; font-size:12px;"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `;
  }
};

window.AttendanceView = AttendanceView;
""")

    # public/js/views/gradebook.view.js
    write("public/js/views/gradebook.view.js", """'use strict';

const GradebookView = {
  async render(container) {
    container.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
        <div>
          <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Academic Gradebook & GPA Rubric</h2>
          <p style="color: var(--text-muted); font-size: 13px;">Midterm exams, assignments, grading scales, and report card transcripts</p>
        </div>
      </div>

      <div class="card">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Student</th>
                <th>Assessment</th>
                <th>Type</th>
                <th>Score Obtained</th>
                <th>Letter Grade</th>
                <th>GPA Points</th>
                <th>Feedback</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Rohit Sharma</strong><div style="font-size:11px; color:var(--text-muted);">STU-2026-001</div></td>
                <td>Data Structures & Algorithms Midterm</td>
                <td><span class="badge badge-primary">Midterm</span></td>
                <td><strong style="font-size:15px;">94 / 100</strong></td>
                <td><span class="badge badge-success">A (94%)</span></td>
                <td><strong>3.80</strong></td>
                <td style="font-size:12px; color:var(--text-muted);">Outstanding algorithm optimization.</td>
              </tr>
              <tr>
                <td><strong>Ananya Iyer</strong><div style="font-size:11px; color:var(--text-muted);">STU-2026-002</div></td>
                <td>Deep Neural Architectures Lab</td>
                <td><span class="badge badge-info">Lab Practical</span></td>
                <td><strong style="font-size:15px;">99 / 100</strong></td>
                <td><span class="badge badge-success">A+ (99%)</span></td>
                <td><strong>4.00</strong></td>
                <td style="font-size:12px; color:var(--text-muted);">Implemented multi-head attention cleanly.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `;
  }
};

window.GradebookView = GradebookView;
""")

    # public/js/views/tickets.view.js
    write("public/js/views/tickets.view.js", """'use strict';

const TicketsView = {
  async render(container) {
    container.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
        <div>
          <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Student Support Helpdesk</h2>
          <p style="color: var(--text-muted); font-size: 13px;">Manage support inquiries, service level agreements (SLAs), and resolutions</p>
        </div>
        <button class="btn btn-primary" id="btn-create-ticket">
          <i class="fas fa-ticket-alt"></i> Create Support Ticket
        </button>
      </div>

      <div class="card">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Ticket #</th>
                <th>Subject</th>
                <th>Category</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody id="tickets-table-body">
              <tr><td colspan="6" style="text-align:center; padding:30px;"><i class="fas fa-spinner fa-spin"></i></td></tr>
            </tbody>
          </table>
        </div>
      </div>
    `;

    document.getElementById('btn-create-ticket').addEventListener('click', () => {
      this.openCreateTicketModal();
    });

    await this.loadTickets();
  },

  async loadTickets() {
    try {
      const res = await window.API.get('/tickets');
      const tickets = res.data;
      const tbody = document.getElementById('tickets-table-body');

      tbody.innerHTML = tickets.map(t => `
        <tr style="cursor:pointer;" onclick="window.Toast.info('Viewing Ticket: ${t.subject}')">
          <td><code style="font-family:var(--font-mono); font-weight:600;">${t.ticket_number}</code></td>
          <td>
            <div style="font-weight:600; color:var(--text-main);">${t.subject}</div>
            <div style="font-size:12px; color:var(--text-muted);">${t.description.substring(0, 70)}...</div>
          </td>
          <td><span class="badge badge-info">${t.category}</span></td>
          <td>
            <span class="badge ${t.priority === 'high' || t.priority === 'critical' ? 'badge-danger' : 'badge-warning'}">
              ${t.priority.toUpperCase()}
            </span>
          </td>
          <td>
            <span class="badge ${t.status === 'resolved' ? 'badge-success' : 'badge-primary'}">
              ${t.status.toUpperCase()}
            </span>
          </td>
          <td style="font-size:12px; color:var(--text-muted);">${new Date(t.created_at).toLocaleDateString()}</td>
        </tr>
      `).join('');
    } catch (err) {
      console.error(err);
    }
  },

  openCreateTicketModal() {
    const body = `
      <form id="new-tkt-form">
        <div class="form-group">
          <label class="form-label">Issue Category *</label>
          <select id="nt-cat" class="form-control">
            <option value="Technical & Portal Access">Technical & Portal Access</option>
            <option value="Fees & Invoicing">Fees & Invoicing</option>
            <option value="Academic & Curriculum">Academic & Curriculum</option>
            <option value="Admissions & Enrollment">Admissions & Enrollment</option>
            <option value="General Support">General Support</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Priority</label>
          <select id="nt-prio" class="form-control">
            <option value="low">Low</option>
            <option value="medium" selected>Medium</option>
            <option value="high">High</option>
            <option value="critical">Critical</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Subject *</label>
          <input type="text" id="nt-sub" class="form-control" placeholder="Brief summary of request..." required>
        </div>
        <div class="form-group">
          <label class="form-label">Description *</label>
          <textarea id="nt-desc" class="form-control" rows="4" placeholder="Detailed explanation..." required></textarea>
        </div>
      </form>
    `;

    const { close } = window.Modal.open({
      title: 'Submit Support Helpdesk Ticket',
      body,
      footer: `
        <button class="btn btn-secondary btn-sm" id="nt-cancel">Cancel</button>
        <button class="btn btn-primary btn-sm" id="nt-submit">Create Ticket</button>
      `
    });

    document.getElementById('nt-cancel').addEventListener('click', close);
    document.getElementById('nt-submit').addEventListener('click', async () => {
      const sub = document.getElementById('nt-sub').value;
      const desc = document.getElementById('nt-desc').value;
      const cat = document.getElementById('nt-cat').value;
      const prio = document.getElementById('nt-prio').value;

      if (!sub || !desc) return window.Toast.error('Please enter subject and description');

      await window.API.post('/tickets', {
        category: cat,
        priority: prio,
        subject: sub,
        description: desc
      });

      window.Toast.success('Ticket submitted successfully!');
      close();
      window.TicketsView.loadTickets();
    });
  }
};

window.TicketsView = TicketsView;
""")

    # public/js/views/reports.view.js
    write("public/js/views/reports.view.js", """'use strict';

const ReportsView = {
  render(container) {
    container.innerHTML = `
      <div style="margin-bottom: 24px;">
        <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Enterprise Reports & Export Hub</h2>
        <p style="color: var(--text-muted); font-size: 13px;">Generate compliant CSV and JSON data exports for auditing, government reporting, and CRM backup</p>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
        <div class="card card-body" style="text-align: center; padding: 28px;">
          <div style="width: 50px; height: 50px; border-radius: var(--radius-md); background: #e0f2fe; color: #0284c7; display: inline-flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 16px;">
            <i class="fas fa-user-plus"></i>
          </div>
          <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 6px;">Leads & Inquiries</h3>
          <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 20px;">Full lead pipeline with source tags and scores</p>
          <div style="display: flex; gap: 8px; justify-content: center;">
            <a href="/api/v1/export/leads/csv" class="btn btn-primary btn-sm"><i class="fas fa-file-csv"></i> CSV</a>
            <a href="/api/v1/export/leads/json" target="_blank" class="btn btn-secondary btn-sm"><i class="fas fa-code"></i> JSON</a>
          </div>
        </div>

        <div class="card card-body" style="text-align: center; padding: 28px;">
          <div style="width: 50px; height: 50px; border-radius: var(--radius-md); background: #d1fae5; color: #059669; display: inline-flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 16px;">
            <i class="fas fa-user-graduate"></i>
          </div>
          <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 6px;">Students Master List</h3>
          <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 20px;">Enrolled students, GPAs, and batch mappings</p>
          <div style="display: flex; gap: 8px; justify-content: center;">
            <a href="/api/v1/export/students/csv" class="btn btn-primary btn-sm"><i class="fas fa-file-csv"></i> CSV</a>
            <a href="/api/v1/export/students/json" target="_blank" class="btn btn-secondary btn-sm"><i class="fas fa-code"></i> JSON</a>
          </div>
        </div>

        <div class="card card-body" style="text-align: center; padding: 28px;">
          <div style="width: 50px; height: 50px; border-radius: var(--radius-md); background: #fef3c7; color: #d97706; display: inline-flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 16px;">
            <i class="fas fa-file-invoice-dollar"></i>
          </div>
          <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 6px;">Invoices & Billing</h3>
          <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 20px;">Financial ledger, paid amounts, and balances</p>
          <div style="display: flex; gap: 8px; justify-content: center;">
            <a href="/api/v1/export/invoices/csv" class="btn btn-primary btn-sm"><i class="fas fa-file-csv"></i> CSV</a>
            <a href="/api/v1/export/invoices/json" target="_blank" class="btn btn-secondary btn-sm"><i class="fas fa-code"></i> JSON</a>
          </div>
        </div>
      </div>
    `;
  }
};

window.ReportsView = ReportsView;
""")

    # public/js/views/settings.view.js
    write("public/js/views/settings.view.js", """'use strict';

const SettingsView = {
  render(container) {
    container.innerHTML = `
      <div style="margin-bottom: 24px;">
        <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Institutional & System Settings</h2>
        <p style="color: var(--text-muted); font-size: 13px;">Manage application configuration, security parameters, and role permissions</p>
      </div>

      <div class="card card-body" style="margin-bottom: 24px;">
        <h3 class="card-title" style="margin-bottom: 16px;">Institutional Profile</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
          <div class="form-group">
            <label class="form-label">Institution Name</label>
            <input type="text" class="form-control" value="EduPulse Institute of Advanced Technology & Management">
          </div>
          <div class="form-group">
            <label class="form-label">Administrative Email</label>
            <input type="email" class="form-control" value="contact@edupulse.edu">
          </div>
        </div>
        <button class="btn btn-primary btn-sm" style="align-self: flex-start;" onclick="window.Toast.success('Settings updated successfully.')">
          Save Configuration
        </button>
      </div>
    `;
  }
};

window.SettingsView = SettingsView;
""")

    # public/js/router.js
    write("public/js/router.js", """'use strict';

/**
 * Client-Side SPA Hash Router
 */

class Router {
  constructor() {
    this.routes = {};
    this.container = null;
  }

  init() {
    this.container = document.getElementById('view-container');
    window.addEventListener('hashchange', () => this.handleRoute());
    this.handleRoute();
  }

  register(path, view) {
    this.routes[path] = view;
  }

  navigate(path) {
    window.location.hash = path;
  }

  handleRoute() {
    const rawHash = window.location.hash || '#/';
    const path = rawHash.split('?')[0];

    // Re-render sidebar to highlight active route
    if (window.renderSidebar) window.renderSidebar();

    const view = this.routes[path] || this.routes['#/'];
    if (view && this.container) {
      this.container.innerHTML = '';
      view.render(this.container);
      window.scrollTo(0, 0);
    }
  }
}

window.Router = new Router();
""")

    # public/js/app.js
    write("public/js/app.js", """'use strict';

/**
 * Application Bootstrap
 */

document.addEventListener('DOMContentLoaded', async () => {
  console.log('[EduPulse CRM] Bootstrapping Application Client...');

  window.AppState.init();

  // If no user logged in, default to Super Admin for immediate exploration
  if (!window.AppState.user) {
    window.AppState.setUser({
      id: 'usr_superadmin_01',
      username: 'superadmin',
      email: 'superadmin@edupulse.edu',
      first_name: 'Alexander',
      last_name: 'Vance',
      role: 'super_admin',
      avatar_url: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150'
    }, 'mock_session_token_super_admin');
  }

  // Render Core Shell Components
  renderNavbar();
  renderSidebar();

  // Register Routes
  window.Router.register('#/', window.DashboardView);
  window.Router.register('#/auth', window.AuthView);
  window.Router.register('#/leads', window.LeadsView);
  window.Router.register('#/admissions', window.AdmissionsView);
  window.Router.register('#/students', window.StudentsView);
  window.Router.register('#/courses', window.CoursesView);
  window.Router.register('#/finance', window.FinanceView);
  window.Router.register('#/attendance', window.AttendanceView);
  window.Router.register('#/gradebook', window.GradebookView);
  window.Router.register('#/tickets', window.TicketsView);
  window.Router.register('#/reports', window.ReportsView);
  window.Router.register('#/settings', window.SettingsView);

  window.Router.init();
  console.log('[EduPulse CRM] Application initialized successfully.');
});
""")

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent.parent)
