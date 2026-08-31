'use strict';

/**
 * Seed data for tuition fee invoices, payments, and receipts
 */

const invoicesSeed = [
  {
    id: 'inv_2026_001',
    invoice_number: 'INV-2026-8801',
    student_id: 'stu_001',
    course_id: 'crs_cs_01',
    title: 'Semester 1 Tuition & Laboratory Fee',
    amount: 4500.00,
    discount_amount: 500.00, // Merit scholarship
    tax_amount: 200.00,
    total_amount: 4200.00,
    amount_paid: 4200.00,
    balance_due: 0.00,
    due_date: '2026-08-15',
    status: 'paid',
    notes: 'Merit scholarship waiver applied ($500).'
  },
  {
    id: 'inv_2026_002',
    invoice_number: 'INV-2026-8802',
    student_id: 'stu_001',
    course_id: 'crs_cs_01',
    title: 'Semester 2 Tuition & Library Subscription',
    amount: 4500.00,
    discount_amount: 0.00,
    tax_amount: 225.00,
    total_amount: 4725.00,
    amount_paid: 2000.00,
    balance_due: 2725.00,
    due_date: '2026-12-15',
    status: 'partially_paid',
    notes: 'First installment of $2,000 received via UPI.'
  },
  {
    id: 'inv_2026_003',
    invoice_number: 'INV-2026-8803',
    student_id: 'stu_002',
    course_id: 'crs_ai_01',
    title: 'M.Sc AI Semester 1 GPU Lab & Tuition Fee',
    amount: 8000.00,
    discount_amount: 1000.00, // Dean Fellowship
    tax_amount: 350.00,
    total_amount: 7350.00,
    amount_paid: 7350.00,
    balance_due: 0.00,
    due_date: '2026-08-20',
    status: 'paid',
    notes: 'Paid in full via Bank Transfer.'
  }
];

const paymentsSeed = [
  {
    id: 'pay_2026_001',
    receipt_number: 'REC-2026-0199',
    invoice_id: 'inv_2026_001',
    student_id: 'stu_001',
    amount: 4200.00,
    payment_method: 'bank_transfer',
    transaction_reference: 'HDFC-N3920194821',
    payment_date: '2026-08-10T10:45:00Z',
    recorded_by_user_id: 'usr_finance_01',
    notes: 'Confirmed payment received in HDFC Institutional Account.'
  },
  {
    id: 'pay_2026_002',
    receipt_number: 'REC-2026-0200',
    invoice_id: 'inv_2026_002',
    student_id: 'stu_001',
    amount: 2000.00,
    payment_method: 'upi',
    transaction_reference: 'UPI-RAZORPAY-8829104',
    payment_date: '2026-08-20T15:20:00Z',
    recorded_by_user_id: 'usr_finance_01',
    notes: 'Installment 1 online gateway payment.'
  },
  {
    id: 'pay_2026_003',
    receipt_number: 'REC-2026-0201',
    invoice_id: 'inv_2026_003',
    student_id: 'stu_002',
    amount: 7350.00,
    payment_method: 'credit_card',
    transaction_reference: 'STRIPE-TXN-902184910',
    payment_date: '2026-08-18T12:15:00Z',
    recorded_by_user_id: 'usr_finance_01',
    notes: 'Processed via Stripe online gateway.'
  }
];

module.exports = { invoicesSeed, paymentsSeed };
