'use strict';

const TicketsView = {
  async render(container) {
    container.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
        <div>
          <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Student Support Helpdesk</h2>
          <p style="color: var(--text-muted); font-size: 13px;">Manage support inquiries, service level agreements (SLAs), and resolutions</p>
        </div>
        <button class="btn btn-primary" id="btn-create-ticket">
          <i class="fas fa-ticket-alt"></i> Create Support Ticket
        </button>
      </div>

      <div class="card">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Ticket #</th>
                <th>Subject</th>
                <th>Category</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody id="tickets-table-body">
              <tr><td colspan="6" style="text-align:center; padding:30px;"><i class="fas fa-spinner fa-spin"></i></td></tr>
            </tbody>
          </table>
        </div>
      </div>
    `;

    document.getElementById('btn-create-ticket').addEventListener('click', () => {
      this.openCreateTicketModal();
    });

    await this.loadTickets();
  },

  async loadTickets() {
    try {
      const res = await window.API.get('/tickets');
      const tickets = res.data;
      const tbody = document.getElementById('tickets-table-body');

      tbody.innerHTML = tickets.map(t => `
        <tr style="cursor:pointer;" onclick="window.Toast.info('Viewing Ticket: ${t.subject}')">
          <td><code style="font-family:var(--font-mono); font-weight:600;">${t.ticket_number}</code></td>
          <td>
            <div style="font-weight:600; color:var(--text-main);">${t.subject}</div>
            <div style="font-size:12px; color:var(--text-muted);">${t.description.substring(0, 70)}...</div>
          </td>
          <td><span class="badge badge-info">${t.category}</span></td>
          <td>
            <span class="badge ${t.priority === 'high' || t.priority === 'critical' ? 'badge-danger' : 'badge-warning'}">
              ${t.priority.toUpperCase()}
            </span>
          </td>
          <td>
            <span class="badge ${t.status === 'resolved' ? 'badge-success' : 'badge-primary'}">
              ${t.status.toUpperCase()}
            </span>
          </td>
          <td style="font-size:12px; color:var(--text-muted);">${new Date(t.created_at).toLocaleDateString()}</td>
        </tr>
      `).join('');
    } catch (err) {
      console.error(err);
    }
  },

  openCreateTicketModal() {
    const body = `
      <form id="new-tkt-form">
        <div class="form-group">
          <label class="form-label">Issue Category *</label>
          <select id="nt-cat" class="form-control">
            <option value="Technical & Portal Access">Technical & Portal Access</option>
            <option value="Fees & Invoicing">Fees & Invoicing</option>
            <option value="Academic & Curriculum">Academic & Curriculum</option>
            <option value="Admissions & Enrollment">Admissions & Enrollment</option>
            <option value="General Support">General Support</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Priority</label>
          <select id="nt-prio" class="form-control">
            <option value="low">Low</option>
            <option value="medium" selected>Medium</option>
            <option value="high">High</option>
            <option value="critical">Critical</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Subject *</label>
          <input type="text" id="nt-sub" class="form-control" placeholder="Brief summary of request..." required>
        </div>
        <div class="form-group">
          <label class="form-label">Description *</label>
          <textarea id="nt-desc" class="form-control" rows="4" placeholder="Detailed explanation..." required></textarea>
        </div>
      </form>
    `;

    const { close } = window.Modal.open({
      title: 'Submit Support Helpdesk Ticket',
      body,
      footer: `
        <button class="btn btn-secondary btn-sm" id="nt-cancel">Cancel</button>
        <button class="btn btn-primary btn-sm" id="nt-submit">Create Ticket</button>
      `
    });

    document.getElementById('nt-cancel').addEventListener('click', close);
    document.getElementById('nt-submit').addEventListener('click', async () => {
      const sub = document.getElementById('nt-sub').value;
      const desc = document.getElementById('nt-desc').value;
      const cat = document.getElementById('nt-cat').value;
      const prio = document.getElementById('nt-prio').value;

      if (!sub || !desc) return window.Toast.error('Please enter subject and description');

      await window.API.post('/tickets', {
        category: cat,
        priority: prio,
        subject: sub,
        description: desc
      });

      window.Toast.success('Ticket submitted successfully!');
      close();
      window.TicketsView.loadTickets();
    });
  }
};

window.TicketsView = TicketsView;
