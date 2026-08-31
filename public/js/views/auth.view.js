'use strict';

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
