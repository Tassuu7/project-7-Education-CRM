'use strict';

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
