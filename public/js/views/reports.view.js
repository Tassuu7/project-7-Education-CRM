'use strict';

const ReportsView = {
  render(container) {
    container.innerHTML = `
      <div style="margin-bottom: 24px;">
        <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Enterprise Reports & Export Hub</h2>
        <p style="color: var(--text-muted); font-size: 13px;">Generate compliant CSV and JSON data exports for auditing, government reporting, and CRM backup</p>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
        <div class="card card-body" style="text-align: center; padding: 28px;">
          <div style="width: 50px; height: 50px; border-radius: var(--radius-md); background: #e0f2fe; color: #0284c7; display: inline-flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 16px;">
            <i class="fas fa-user-plus"></i>
          </div>
          <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 6px;">Leads & Inquiries</h3>
          <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 20px;">Full lead pipeline with source tags and scores</p>
          <div style="display: flex; gap: 8px; justify-content: center;">
            <a href="/api/v1/export/leads/csv" class="btn btn-primary btn-sm"><i class="fas fa-file-csv"></i> CSV</a>
            <a href="/api/v1/export/leads/json" target="_blank" class="btn btn-secondary btn-sm"><i class="fas fa-code"></i> JSON</a>
          </div>
        </div>

        <div class="card card-body" style="text-align: center; padding: 28px;">
          <div style="width: 50px; height: 50px; border-radius: var(--radius-md); background: #d1fae5; color: #059669; display: inline-flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 16px;">
            <i class="fas fa-user-graduate"></i>
          </div>
          <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 6px;">Students Master List</h3>
          <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 20px;">Enrolled students, GPAs, and batch mappings</p>
          <div style="display: flex; gap: 8px; justify-content: center;">
            <a href="/api/v1/export/students/csv" class="btn btn-primary btn-sm"><i class="fas fa-file-csv"></i> CSV</a>
            <a href="/api/v1/export/students/json" target="_blank" class="btn btn-secondary btn-sm"><i class="fas fa-code"></i> JSON</a>
          </div>
        </div>

        <div class="card card-body" style="text-align: center; padding: 28px;">
          <div style="width: 50px; height: 50px; border-radius: var(--radius-md); background: #fef3c7; color: #d97706; display: inline-flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 16px;">
            <i class="fas fa-file-invoice-dollar"></i>
          </div>
          <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 6px;">Invoices & Billing</h3>
          <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 20px;">Financial ledger, paid amounts, and balances</p>
          <div style="display: flex; gap: 8px; justify-content: center;">
            <a href="/api/v1/export/invoices/csv" class="btn btn-primary btn-sm"><i class="fas fa-file-csv"></i> CSV</a>
            <a href="/api/v1/export/invoices/json" target="_blank" class="btn btn-secondary btn-sm"><i class="fas fa-code"></i> JSON</a>
          </div>
        </div>
      </div>
    `;
  }
};

window.ReportsView = ReportsView;
