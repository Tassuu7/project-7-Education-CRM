-- ============================================================================
-- Migration V015: Schema Expansion and Performance Partitioning Part 15
-- Target: EduPulse Relational Subsystem 15
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_partition_015 (
    partition_id TEXT PRIMARY KEY,
    batch_reference_id TEXT NOT NULL,
    entity_code TEXT NOT NULL,
    operation_type TEXT CHECK(operation_type IN ('INSERT', 'UPDATE', 'DELETE', 'EXECUTE', 'EXPORT')),
    payload_hash TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verification_status TEXT DEFAULT 'VERIFIED'
);

CREATE INDEX IF NOT EXISTS idx_audit_part_015_actor ON audit_partition_015(actor_id);
CREATE INDEX IF NOT EXISTS idx_audit_part_015_created ON audit_partition_015(created_timestamp);
