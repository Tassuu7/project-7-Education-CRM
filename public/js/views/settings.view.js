'use strict';

const SettingsView = {
  render(container) {
    container.innerHTML = `
      <div style="margin-bottom: 24px;">
        <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Institutional & System Settings</h2>
        <p style="color: var(--text-muted); font-size: 13px;">Manage application configuration, security parameters, and role permissions</p>
      </div>

      <div class="card card-body" style="margin-bottom: 24px;">
        <h3 class="card-title" style="margin-bottom: 16px;">Institutional Profile</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
          <div class="form-group">
            <label class="form-label">Institution Name</label>
            <input type="text" class="form-control" value="EduPulse Institute of Advanced Technology & Management">
          </div>
          <div class="form-group">
            <label class="form-label">Administrative Email</label>
            <input type="email" class="form-control" value="contact@edupulse.edu">
          </div>
        </div>
        <button class="btn btn-primary btn-sm" style="align-self: flex-start;" onclick="window.Toast.success('Settings updated successfully.')">
          Save Configuration
        </button>
      </div>
    `;
  }
};

window.SettingsView = SettingsView;
