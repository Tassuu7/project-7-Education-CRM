'use strict';

const FinanceView = {
  async render(container) {
    container.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
        <div>
          <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Tuition Billing & Invoicing Ledger</h2>
          <p style="color: var(--text-muted); font-size: 13px;">Track student invoices, partial payments, receipts, and outstanding dues</p>
        </div>
      </div>

      <div class="card">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Invoice #</th>
                <th>Student</th>
                <th>Title</th>
                <th>Total Billed</th>
                <th>Paid</th>
                <th>Balance Due</th>
                <th>Due Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody id="invoices-table-body">
              <tr><td colspan="9" style="text-align:center; padding:30px;"><i class="fas fa-spinner fa-spin"></i></td></tr>
            </tbody>
          </table>
        </div>
      </div>
    `;

    await this.loadInvoices();
  },

  async loadInvoices() {
    try {
      const res = await window.API.get('/finance/invoices');
      const invoices = res.data;
      const tbody = document.getElementById('invoices-table-body');

      tbody.innerHTML = invoices.map(inv => `
        <tr>
          <td><code style="font-family:var(--font-mono); font-weight:600;">${inv.invoice_number}</code></td>
          <td>
            <div style="font-weight:600;">${inv.student ? inv.student.first_name + ' ' + inv.student.last_name : 'Student'}</div>
            <div style="font-size:11px; color:var(--text-muted);">${inv.student ? inv.student.student_id_number : ''}</div>
          </td>
          <td><span style="font-size:13px;">${inv.title}</span></td>
          <td style="font-weight:700;">$${inv.total_amount.toLocaleString()}</td>
          <td style="color:var(--accent-emerald); font-weight:600;">$${inv.amount_paid.toLocaleString()}</td>
          <td style="color:${inv.balance_due > 0 ? 'var(--accent-rose)' : 'var(--text-muted)'}; font-weight:700;">
            $${inv.balance_due.toLocaleString()}
          </td>
          <td style="font-size:12px; color:var(--text-muted);">${inv.due_date}</td>
          <td>
            <span class="badge ${inv.status === 'paid' ? 'badge-success' : inv.status === 'partially_paid' ? 'badge-info' : 'badge-warning'}">
              ${inv.status.replace('_', ' ').toUpperCase()}
            </span>
          </td>
          <td>
            ${inv.balance_due > 0 ? `
              <button class="btn btn-primary btn-sm" onclick="window.FinanceView.openPaymentModal('${inv.id}', ${inv.balance_due})">
                <i class="fas fa-credit-card"></i> Pay
              </button>
            ` : `
              <span style="font-size:12px; color:var(--accent-emerald); font-weight:600;"><i class="fas fa-check-circle"></i> Paid in Full</span>
            `}
          </td>
        </tr>
      `).join('');
    } catch (err) {
      console.error(err);
    }
  },

  openPaymentModal(invoiceId, balanceDue) {
    const body = `
      <div>
        <p style="margin-bottom:16px; font-size:13px; color:var(--text-muted);">
          Enter payment transaction details to credit against invoice balance.
        </p>
        <div class="form-group">
          <label class="form-label">Payment Amount ($) *</label>
          <input type="number" id="pay-amount" class="form-control" value="${balanceDue}" max="${balanceDue}" min="1" step="0.01">
        </div>
        <div class="form-group">
          <label class="form-label">Payment Method</label>
          <select id="pay-method" class="form-control">
            <option value="bank_transfer">Direct Bank Transfer</option>
            <option value="upi">UPI / Instant Online</option>
            <option value="credit_card">Credit / Debit Card</option>
            <option value="cheque">Cheque / Demand Draft</option>
            <option value="cash">Institutional Cash Desk</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Transaction Reference Number</label>
          <input type="text" id="pay-ref" class="form-control" placeholder="e.g. TXN-994829104">
        </div>
      </div>
    `;

    const { close } = window.Modal.open({
      title: 'Record Tuition Fee Payment',
      body,
      footer: `
        <button class="btn btn-secondary btn-sm" id="pay-cancel">Cancel</button>
        <button class="btn btn-success btn-sm" id="pay-submit"><i class="fas fa-receipt"></i> Process Receipt</button>
      `
    });

    document.getElementById('pay-cancel').addEventListener('click', close);
    document.getElementById('pay-submit').addEventListener('click', async () => {
      const amount = parseFloat(document.getElementById('pay-amount').value);
      const method = document.getElementById('pay-method').value;
      const ref = document.getElementById('pay-ref').value;

      if (isNaN(amount) || amount <= 0) return window.Toast.error('Please enter valid amount');

      await window.API.post(`/finance/invoices/${invoiceId}/pay`, {
        amount,
        payment_method: method,
        transaction_reference: ref
      });

      window.Toast.success(`Payment of $${amount} recorded successfully!`);
      close();
      window.FinanceView.loadInvoices();
    });
  }
};

window.FinanceView = FinanceView;
