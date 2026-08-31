'use strict';

function renderSidebar() {
  const container = document.getElementById('sidebar-container');
  if (!container) return;

  const user = window.AppState.user || { role: 'super_admin' };
  const currentHash = window.location.hash || '#/';

  const navItems = [
    { label: 'Dashboard', icon: 'fa-chart-pie', path: '#/', roles: ['all'] },
    { label: 'Leads CRM', icon: 'fa-user-plus', path: '#/leads', roles: ['super_admin', 'admin', 'counselor'] },
    { label: 'Admissions', icon: 'fa-file-signature', path: '#/admissions', roles: ['super_admin', 'admin', 'counselor'] },
    { label: 'Students SIS', icon: 'fa-user-graduate', path: '#/students', roles: ['super_admin', 'admin', 'counselor', 'instructor', 'finance_officer'] },
    { label: 'Courses & Batches', icon: 'fa-book-open', path: '#/courses', roles: ['all'] },
    { label: 'Attendance', icon: 'fa-calendar-check', path: '#/attendance', roles: ['super_admin', 'admin', 'instructor', 'student'] },
    { label: 'Gradebook', icon: 'fa-award', path: '#/gradebook', roles: ['super_admin', 'admin', 'instructor', 'student'] },
    { label: 'Finance & Invoicing', icon: 'fa-file-invoice-dollar', path: '#/finance', roles: ['super_admin', 'admin', 'finance_officer', 'student'] },
    { label: 'Support Helpdesk', icon: 'fa-headset', path: '#/tickets', roles: ['all'] },
    { label: 'Reports & Export', icon: 'fa-file-export', path: '#/reports', roles: ['super_admin', 'admin', 'counselor', 'finance_officer'] },
    { label: 'System Settings', icon: 'fa-sliders-h', path: '#/settings', roles: ['super_admin', 'admin'] }
  ];

  const filteredItems = navItems.filter(item => 
    item.roles.includes('all') || item.roles.includes(user.role) || user.role === 'super_admin'
  );

  container.innerHTML = `
    <div style="padding: 24px; border-bottom: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 12px;">
      <div style="width: 38px; height: 38px; border-radius: var(--radius-md); background: var(--grad-primary); display: flex; align-items: center; justify-content: center; font-size: 18px; color: #fff;">
        <i class="fas fa-graduation-cap"></i>
      </div>
      <div>
        <div style="font-weight: 800; font-size: 17px; letter-spacing: -0.5px; color: #fff;">EduPulse <span style="color: var(--primary-400);">CRM</span></div>
        <div style="font-size: 11px; color: #94a3b8;">Education Enterprise</div>
      </div>
    </div>

    <nav style="padding: 16px 12px; flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 4px;">
      ${filteredItems.map(item => {
        const isActive = currentHash === item.path || (item.path !== '#/' && currentHash.startsWith(item.path));
        return `
          <a href="${item.path}" style="
            display: flex; 
            align-items: center; 
            gap: 12px; 
            padding: 10px 14px; 
            border-radius: var(--radius-sm); 
            color: ${isActive ? '#ffffff' : '#94a3b8'}; 
            background: ${isActive ? 'rgba(99, 102, 241, 0.15)' : 'transparent'}; 
            border-left: ${isActive ? '3px solid var(--primary-500)' : '3px solid transparent'}; 
            font-weight: ${isActive ? '600' : '500'};
            font-size: 13.5px;
            transition: all var(--transition-fast);
          " onmouseover="if(!${isActive}) this.style.color='#ffffff'" onmouseout="if(!${isActive}) this.style.color='#94a3b8'">
            <i class="fas ${item.icon}" style="width: 18px; text-align: center; color: ${isActive ? 'var(--primary-400)' : '#64748b'};"></i>
            <span>${item.label}</span>
          </a>
        `;
      }).join('')}
    </nav>

    <div style="padding: 18px; border-top: 1px solid rgba(255,255,255,0.08); background: rgba(0,0,0,0.2);">
      <div style="font-size: 11px; color: #64748b; margin-bottom: 4px;">EduPulse Enterprise v1.0.0</div>
      <div style="font-size: 10px; color: #475569;">100% Production Ready</div>
    </div>
  `;
}
