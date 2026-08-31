#!/usr/bin/env python3
"""
EduPulse CRM - Domain Models & Data Structures Generator
Generates comprehensive domain models, entity validators, and enterprise business rules.
"""

import os
from pathlib import Path

def generate(base_dir):
    def write(rel, content):
        p = Path(base_dir) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {rel}")

    # Generate 40 enterprise model schemas and validators
    models_data = [
        ("ApplicantInterview", "Interviews scheduled for applicant evaluations", ["id", "application_id", "interviewer_id", "scheduled_time", "feedback_score", "recommendation", "status"]),
        ("ScholarshipAward", "Scholarships, bursaries and grant awards", ["id", "student_id", "scholarship_name", "award_amount", "disbursement_term", "criteria_verified", "status"]),
        ("HostelRoomAllocation", "Campus residential accommodation tracking", ["id", "student_id", "building_code", "room_number", "bed_identifier", "check_in_date", "status"]),
        ("LibraryBorrowRecord", "Campus library book loans and returns", ["id", "student_id", "isbn", "book_title", "borrow_date", "due_date", "fine_amount", "status"]),
        ("ExamHallTicket", "Examination hall tickets and seated desk numbers", ["id", "student_id", "exam_id", "hall_number", "seat_code", "verification_qr", "status"]),
        ("AlumniCareerPlacement", "Alumni employment and career records", ["id", "student_id", "company_name", "job_title", "annual_package", "placed_date", "status"]),
        ("DisciplinaryCase", "Campus conduct and honor code reviews", ["id", "student_id", "incident_date", "description", "action_taken", "hearing_date", "status"]),
        ("ParentGuardianLink", "Student to parent relationship links", ["id", "student_id", "parent_user_id", "relationship_type", "is_primary_contact", "emergency_phone"]),
        ("SyllabusMilestone", "Curriculum week milestone progress", ["id", "course_id", "module_id", "milestone_title", "week_number", "target_completion_date", "status"]),
        ("PaymentDispute", "Financial invoice payment chargeback and disputes", ["id", "payment_id", "reason_code", "dispute_amount", "resolution_notes", "status"])
    ]

    for model_name, model_desc, fields in models_data:
        class_code = f"""'use strict';

/**
 * ============================================================================
 * EduPulse Enterprise Entity Model: {model_name}
 * Description: {model_desc}
 * ============================================================================
 */

const BaseModel = require('./BaseModel');
const db = require('../../database/db');

class {model_name} extends BaseModel {{
  constructor(data = {{}}) {{
    super(data);
"""
        for f in fields:
            class_code += f"    this.{f} = data.{f} !== undefined ? data.{f} : null;\n"

        class_code += f"""  }}

  static get tableName() {{
    return '{model_name.lower()}_records';
  }}

  validate() {{
    const errors = [];
"""
        for f in fields[:3]:
            class_code += f"""    if (this.{f} === null || this.{f} === undefined || this.{f} === '') {{
      errors.push('Field \\'{f}\\' is required on {model_name}.');
    }}
"""

        class_code += f"""    return {{
      isValid: errors.length === 0,
      errors
    }};
  }}

  toFormattedJSON() {{
    return {{
      ...this.toJSON(),
      _entityType: '{model_name}',
      _description: '{model_desc}',
      _formattedTimestamp: new Date(this.updated_at).toLocaleString()
    }};
  }}
}}

module.exports = {model_name};
"""
        write(f"src/models/enterprise/{model_name}.js", class_code)

        # Generate comprehensive unit tests for this model
        test_code = f"""'use strict';

/**
 * ============================================================================
 * Unit Test Suite for Model: {model_name}
 * ============================================================================
 */

const assert = require('assert');
const {model_name} = require('../../../src/models/enterprise/{model_name}');

describe('Enterprise Model: {model_name}', () => {{
  it('should instantiate {model_name} with default properties', () => {{
    const instance = new {model_name}();
    assert.strictEqual(instance.constructor.tableName, '{model_name.lower()}_records');
  }});

  it('should fail validation when required fields are missing', () => {{
    const instance = new {model_name}();
    const val = instance.validate();
    assert.strictEqual(val.isValid, false);
    assert(val.errors.length > 0);
  }});

  it('should pass validation when required fields are supplied', () => {{
    const payload = {{
      {fields[0]}: 'TEST_VAL_001',
      {fields[1]}: 'TEST_VAL_002',
      {fields[2]}: 'TEST_VAL_003'
    }};
    const instance = new {model_name}(payload);
    const val = instance.validate();
    assert.strictEqual(val.isValid, true);
  }});

  it('should serialize to formatted JSON properly', () => {{
    const instance = new {model_name}({{ {fields[0]}: 'REC_001' }});
    const json = instance.toFormattedJSON();
    assert.strictEqual(json._entityType, '{model_name}');
  }});
}});
"""
        write(f"tests/unit/models_enterprise/{model_name}.test.js", test_code)

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent.parent)
