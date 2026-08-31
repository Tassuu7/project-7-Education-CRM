'use strict';

function getAdmissionOfferEmail(applicantName, courseName, term, depositAmount) {
  return `
  <!DOCTYPE html>
  <html>
  <head>
    <style>
      body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f7fc; margin: 0; padding: 20px; }
      .card { max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 32px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
      .header { border-bottom: 2px solid #4f46e5; padding-bottom: 16px; margin-bottom: 24px; }
      .header h1 { color: #1e1b4b; margin: 0; font-size: 24px; }
      .content { color: #334155; line-height: 1.6; font-size: 15px; }
      .highlight-box { background: #eef2ff; border-left: 4px solid #4f46e5; padding: 16px; border-radius: 6px; margin: 20px 0; }
      .btn { display: inline-block; background: #4f46e5; color: #ffffff; padding: 12px 28px; border-radius: 8px; text-decoration: none; font-weight: 600; }
      .footer { margin-top: 32px; font-size: 12px; color: #94a3b8; text-align: center; }
    </style>
  </head>
  <body>
    <div class="card">
      <div class="header">
        <h1>EduPulse Institute - Offer of Admission</h1>
      </div>
      <div class="content">
        <p>Dear <strong>${applicantName}</strong>,</p>
        <p>Congratulations! On behalf of the Academic Admissions Committee, we are delighted to offer you provisional admission to:</p>
        <div class="highlight-box">
          <p><strong>Program:</strong> ${courseName}</p>
          <p><strong>Intake Term:</strong> ${term}</p>
          <p><strong>Initial Deposit Due:</strong> $${depositAmount}</p>
        </div>
        <p>Please log in to your student portal to accept your offer and complete registration formalities.</p>
        <p style="text-align: center; margin-top: 24px;">
          <a href="http://localhost:4050" class="btn">Access Student Portal</a>
        </p>
      </div>
      <div class="footer">
        <p>EduPulse Institute of Advanced Technology & Management | Office of Admissions</p>
      </div>
    </div>
  </body>
  </html>
  `;
}

module.exports = { getAdmissionOfferEmail };
