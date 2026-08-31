'use strict';

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
