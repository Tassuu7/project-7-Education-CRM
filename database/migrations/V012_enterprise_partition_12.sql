-- ============================================================================
-- Migration V012: Schema Expansion and Performance Partitioning Part 12
-- Target: EduPulse Relational Subsystem 12
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_partition_012 (
    partition_id TEXT PRIMARY KEY,
    batch_reference_id TEXT NOT NULL,
    entity_code TEXT NOT NULL,
    operation_type TEXT CHECK(operation_type IN ('INSERT', 'UPDATE', 'DELETE', 'EXECUTE', 'EXPORT')),
    payload_hash TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verification_status TEXT DEFAULT 'VERIFIED'
);

CREATE INDEX IF NOT EXISTS idx_audit_part_012_actor ON audit_partition_012(actor_id);
CREATE INDEX IF NOT EXISTS idx_audit_part_012_created ON audit_partition_012(created_timestamp);
