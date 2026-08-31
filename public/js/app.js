'use strict';

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
