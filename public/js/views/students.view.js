'use strict';

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
