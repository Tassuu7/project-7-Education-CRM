'use strict';

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
