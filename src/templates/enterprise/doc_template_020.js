'use strict';

/**
 * ============================================================================
 * EduPulse Official Document Template #020
 * Production Module: src/templates/enterprise/doc_template_020.js
 * ============================================================================
 */

class DocumentTemplate_020 {
  constructor() {
    this.templateId = 'DOC_TMPL_020';
    this.templateName = 'Official Institutional Document Variant 20';
  }

  generateHtml(data = {}) {
    const institutionName = data.institutionName || 'EduPulse Institute of Advanced Technology';
    const studentName = data.studentName || 'Sample Student';
    const studentId = data.studentId || 'STU-2026-001';
    const issueDate = data.issueDate || new Date().toLocaleDateString();

    return `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #1e293b; background: #ffffff; }
        .header-box { border-bottom: 3px double #4f46e5; padding-bottom: 20px; text-align: center; }
        .header-box h1 { margin: 0; color: #1e1b4b; font-size: 24px; }
        .header-box p { margin: 4px 0 0 0; color: #64748b; font-size: 13px; }
        .content-box { margin-top: 30px; line-height: 1.8; font-size: 14px; }
        .meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 24px 0; background: #f8fafc; padding: 16px; border: 1px solid #e2e8f0; border-radius: 8px; }
        .meta-item { display: flex; flex-direction: column; }
        .meta-label { font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 600; }
        .meta-value { font-size: 14px; font-weight: 700; color: #0f172a; margin-top: 2px; }
        .table-data { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .table-data th, .table-data td { border: 1px solid #cbd5e1; padding: 10px 14px; text-align: left; }
        .table-data th { background: #f1f5f9; font-weight: 600; }
        .footer-sig { margin-top: 60px; display: flex; justify-content: space-between; }
        .sig-line { width: 200px; border-top: 1px solid #0f172a; text-align: center; padding-top: 8px; font-size: 12px; font-weight: 600; }
      </style>
    </head>
    <body>
      <div class='header-box'>
        <h1>${institutionName}</h1>
        <p>Office of Academic Administration & Records | Form Series 20</p>
      </div>
      <div class='content-box'>
        <div class='meta-grid'>
          <div class='meta-item'><span class='meta-label'>Student Name</span><span class='meta-value'>${studentName}</span></div>
          <div class='meta-item'><span class='meta-label'>Student ID</span><span class='meta-value'>${studentId}</span></div>
          <div class='meta-item'><span class='meta-label'>Issue Date</span><span class='meta-value'>${issueDate}</span></div>
          <div class='meta-item'><span class='meta-label'>Verification Code</span><span class='meta-value'>VERIF-2026-0020</span></div>
        </div>
        <p>This document officially certifies and confirms the institutional records and status for the individual listed above in accordance with academic charter policy #20.</p>
        <table class='table-data'>
          <thead><tr><th>Record Attribute</th><th>Certified Evaluation</th><th>Compliance Status</th></tr></thead>
          <tbody>
            <tr><td>Academic Standard #1</td><td>Grade A / Honors Level 91.0%</td><td>VERIFIED & SEALED</td></tr>
            <tr><td>Academic Standard #2</td><td>Grade A / Honors Level 92.0%</td><td>VERIFIED & SEALED</td></tr>
            <tr><td>Academic Standard #3</td><td>Grade A / Honors Level 93.0%</td><td>VERIFIED & SEALED</td></tr>
            <tr><td>Academic Standard #4</td><td>Grade A / Honors Level 94.0%</td><td>VERIFIED & SEALED</td></tr>
            <tr><td>Academic Standard #5</td><td>Grade A / Honors Level 95.0%</td><td>VERIFIED & SEALED</td></tr>
            <tr><td>Academic Standard #6</td><td>Grade A / Honors Level 96.0%</td><td>VERIFIED & SEALED</td></tr>
            <tr><td>Academic Standard #7</td><td>Grade A / Honors Level 97.0%</td><td>VERIFIED & SEALED</td></tr>
            <tr><td>Academic Standard #8</td><td>Grade A / Honors Level 98.0%</td><td>VERIFIED & SEALED</td></tr>
            <tr><td>Academic Standard #9</td><td>Grade A / Honors Level 99.0%</td><td>VERIFIED & SEALED</td></tr>
            <tr><td>Academic Standard #10</td><td>Grade A / Honors Level 100.0%</td><td>VERIFIED & SEALED</td></tr>
          </tbody>
        </table>
        <div class='footer-sig'>
          <div class='sig-line'>Registrar & Dean of Records</div>
          <div class='sig-line'>Institutional Seal & Controller</div>
        </div>
      </div>
    </body>
    </html>
    `;
  }
}

module.exports = new DocumentTemplate_020();
