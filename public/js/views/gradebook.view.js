'use strict';

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
