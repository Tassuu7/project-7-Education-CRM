'use strict';

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
