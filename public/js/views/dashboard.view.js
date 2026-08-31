'use strict';

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
