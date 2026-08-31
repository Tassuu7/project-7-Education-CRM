-- ============================================================================
-- Migration V002: Schema Expansion and Performance Partitioning Part 2
-- Target: EduPulse Relational Subsystem 2
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_partition_002 (
    partition_id TEXT PRIMARY KEY,
    batch_reference_id TEXT NOT NULL,
    entity_code TEXT NOT NULL,
    operation_type TEXT CHECK(operation_type IN ('INSERT', 'UPDATE', 'DELETE', 'EXECUTE', 'EXPORT')),
    payload_hash TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verification_status TEXT DEFAULT 'VERIFIED'
);

CREATE INDEX IF NOT EXISTS idx_audit_part_002_actor ON audit_partition_002(actor_id);
CREATE INDEX IF NOT EXISTS idx_audit_part_002_created ON audit_partition_002(created_timestamp);
