'use strict';

const LeadsView = {
  async render(container) {
    container.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
        <div>
          <h2 style="font-size: 22px; font-weight: 700; color: var(--text-main);">Leads & Admissions Pipeline</h2>
          <p style="color: var(--text-muted); font-size: 13px;">Manage prospective inquiries, follow-ups, and counselor assignments</p>
        </div>
        <button class="btn btn-primary" id="btn-add-lead">
          <i class="fas fa-plus"></i> Capture New Lead
        </button>
      </div>

      <div class="leads-pipeline" id="leads-kanban-board">
        <div style="padding: 30px; text-align: center; width: 100%;">
          <i class="fas fa-spinner fa-spin fa-2x"></i>
        </div>
      </div>
    `;

    document.getElementById('btn-add-lead').addEventListener('click', () => {
      this.openCreateLeadModal();
    });

    await this.loadLeads();
  },

  async loadLeads() {
    try {
      const res = await window.API.get('/leads');
      const leads = res.data;

      const stages = [
        { key: 'new', title: 'New Inquiries', icon: 'fa-envelope-open' },
        { key: 'contacted', title: 'Contacted', icon: 'fa-phone-volume' },
        { key: 'qualified', title: 'Qualified', icon: 'fa-check-double' },
        { key: 'counseling_scheduled', title: 'Counseling', icon: 'fa-calendar-alt' },
        { key: 'application_submitted', title: 'App Submitted', icon: 'fa-file-alt' },
        { key: 'enrolled', title: 'Enrolled', icon: 'fa-user-graduate' }
      ];

      const board = document.getElementById('leads-kanban-board');
      board.innerHTML = stages.map(st => {
        const stageLeads = leads.filter(l => l.stage === st.key);
        return `
          <div class="pipeline-col">
            <div class="pipeline-col-header">
              <span><i class="fas ${st.icon}" style="margin-right:6px;"></i> ${st.title}</span>
              <span class="badge badge-primary">${stageLeads.length}</span>
            </div>
            <div class="pipeline-cards-list">
              ${stageLeads.map(lead => {
                let scoreClass = 'score-cold';
                if (lead.lead_score >= 75) scoreClass = 'score-hot';
                else if (lead.lead_score >= 45) scoreClass = 'score-warm';

                return `
                  <div class="lead-card" onclick="window.LeadsView.openLeadDetail('${lead.id}')">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                      <span class="lead-score-pill ${scoreClass}">Score: ${lead.lead_score}</span>
                      <span style="font-size:11px; color:var(--text-muted);">${lead.source}</span>
                    </div>
                    <div style="font-weight:600; font-size:14px; color:var(--text-main);">${lead.fullName}</div>
                    <div style="font-size:12px; color:var(--text-muted); margin-top:2px;">
                      <i class="fas fa-graduation-cap" style="width:14px;"></i> ${lead.course ? lead.course.code : 'Course TBD'}
                    </div>
                    <div style="font-size:12px; color:var(--text-muted); margin-top:2px;">
                      <i class="fas fa-map-marker-alt" style="width:14px;"></i> ${lead.city || 'Global'}
                    </div>
                    <div style="margin-top:10px; padding-top:8px; border-top:1px solid var(--border-color); display:flex; justify-content:space-between; align-items:center; font-size:11px; color:var(--text-light);">
                      <span><i class="fas fa-user-tie"></i> ${lead.counselor ? lead.counselor.name.split(' ')[0] : 'Unassigned'}</span>
                      <span><i class="fas fa-comments"></i> ${lead.interactionsCount || 0}</span>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;
      }).join('');
    } catch (err) {
      console.error(err);
    }
  },

  async openLeadDetail(leadId) {
    try {
      const res = await window.API.get(`/leads/${leadId}`);
      const lead = res.data;

      const body = `
        <div>
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border-color);">
            <div>
              <h3 style="font-size: 18px; font-weight: 700; color: var(--text-main);">${lead.fullName}</h3>
              <p style="font-size: 13px; color: var(--text-muted);">${lead.email} | ${lead.phone}</p>
            </div>
            <span class="lead-score-pill ${lead.lead_score >= 75 ? 'score-hot' : 'score-warm'}" style="font-size: 13px; padding: 4px 12px;">
              Score: ${lead.lead_score} (${lead.lead_score >= 75 ? 'Hot Intent' : 'Warm'})
            </span>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
            <div>
              <label class="form-label">Current Pipeline Stage</label>
              <select class="form-control" id="lead-stage-select">
                <option value="new" ${lead.stage === 'new' ? 'selected' : ''}>New Inquiry</option>
                <option value="contacted" ${lead.stage === 'contacted' ? 'selected' : ''}>Contacted</option>
                <option value="qualified" ${lead.stage === 'qualified' ? 'selected' : ''}>Qualified</option>
                <option value="counseling_scheduled" ${lead.stage === 'counseling_scheduled' ? 'selected' : ''}>Counseling Scheduled</option>
                <option value="application_submitted" ${lead.stage === 'application_submitted' ? 'selected' : ''}>Application Submitted</option>
                <option value="enrolled" ${lead.stage === 'enrolled' ? 'selected' : ''}>Enrolled</option>
                <option value="lost" ${lead.stage === 'lost' ? 'selected' : ''}>Lost / Closed</option>
              </select>
            </div>
            <div>
              <label class="form-label">Interested Program</label>
              <input type="text" class="form-control" value="${lead.course ? lead.course.title : 'None'}" disabled>
            </div>
          </div>

          <div class="card" style="margin-bottom: 20px;">
            <div class="card-header" style="padding: 12px 18px;">
              <h4 style="font-size: 14px; font-weight: 600;">Log Call / Counseling Interaction</h4>
            </div>
            <div class="card-body" style="padding: 16px;">
              <div class="form-group">
                <textarea id="intr-summary" class="form-control" rows="2" placeholder="Enter interaction discussion notes..."></textarea>
              </div>
              <button class="btn btn-primary btn-sm" id="btn-save-intr">
                <i class="fas fa-save"></i> Record Interaction
              </button>
            </div>
          </div>
        </div>
      `;

      const { close } = window.Modal.open({
        title: `Lead Profile: ${lead.fullName}`,
        body,
        footer: `
          <button class="btn btn-secondary btn-sm" id="modal-cancel">Close</button>
          <button class="btn btn-primary btn-sm" id="modal-update-lead">Save Changes</button>
        `,
        width: '650px'
      });

      document.getElementById('modal-cancel').addEventListener('click', close);

      document.getElementById('btn-save-intr').addEventListener('click', async () => {
        const text = document.getElementById('intr-summary').value;
        if (!text) return window.Toast.error('Please enter notes');
        await window.API.post(`/leads/${lead.id}/interactions`, {
          interaction_type: 'phone_call',
          summary: text
        });
        window.Toast.success('Interaction logged!');
        close();
        window.LeadsView.loadLeads();
      });

      document.getElementById('modal-update-lead').addEventListener('click', async () => {
        const newStage = document.getElementById('lead-stage-select').value;
        await window.API.put(`/leads/${lead.id}`, { stage: newStage });
        window.Toast.success('Lead updated successfully.');
        close();
        window.LeadsView.loadLeads();
      });
    } catch (err) {
      console.error(err);
    }
  },

  openCreateLeadModal() {
    const body = `
      <form id="create-lead-form">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div class="form-group">
            <label class="form-label">First Name *</label>
            <input type="text" id="nl-first-name" class="form-control" required>
          </div>
          <div class="form-group">
            <label class="form-label">Last Name *</label>
            <input type="text" id="nl-last-name" class="form-control" required>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div class="form-group">
            <label class="form-label">Email Address *</label>
            <input type="email" id="nl-email" class="form-control" required>
          </div>
          <div class="form-group">
            <label class="form-label">Phone Number *</label>
            <input type="tel" id="nl-phone" class="form-control" required>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div class="form-group">
            <label class="form-label">Lead Source</label>
            <select id="nl-source" class="form-control">
              <option value="Website Inbound">Website Inbound</option>
              <option value="Google Search Ads">Google Search Ads</option>
              <option value="Social Media Campaign">Social Media Campaign</option>
              <option value="Education Fair 2026">Education Fair 2026</option>
              <option value="Alumni Referral">Alumni Referral</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">City</label>
            <input type="text" id="nl-city" class="form-control" placeholder="e.g. Mumbai">
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Counselor Notes / Inquiries</label>
          <textarea id="nl-notes" class="form-control" rows="2" placeholder="Student background & interests..."></textarea>
        </div>
      </form>
    `;

    const { close } = window.Modal.open({
      title: 'Capture Inbound Student Lead',
      body,
      footer: `
        <button class="btn btn-secondary btn-sm" id="nl-cancel">Cancel</button>
        <button class="btn btn-primary btn-sm" id="nl-submit">Create Lead</button>
      `
    });

    document.getElementById('nl-cancel').addEventListener('click', close);
    document.getElementById('nl-submit').addEventListener('click', async () => {
      const payload = {
        first_name: document.getElementById('nl-first-name').value,
        last_name: document.getElementById('nl-last-name').value,
        email: document.getElementById('nl-email').value,
        phone: document.getElementById('nl-phone').value,
        source: document.getElementById('nl-source').value,
        city: document.getElementById('nl-city').value,
        notes: document.getElementById('nl-notes').value
      };

      if (!payload.first_name || !payload.email || !payload.phone) {
        return window.Toast.error('Please fill required fields.');
      }

      await window.API.post('/leads', payload);
      window.Toast.success('Lead created and assigned!');
      close();
      window.LeadsView.loadLeads();
    });
  }
};

window.LeadsView = LeadsView;
