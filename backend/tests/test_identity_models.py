from sqlalchemy import inspect

from app.models.identity import AuditEvent, Role, User, UserRole


def test_identity_tables_are_registered():
    assert {
        User.__tablename__,
        Role.__tablename__,
        UserRole.__tablename__,
        AuditEvent.__tablename__,
    } <= {table.name for table in User.metadata.tables.values()}


def test_audit_event_has_security_indexes():
    indexes = {index.name for index in inspect(AuditEvent).mapper.local_table.indexes}
    assert "ix_audit_actor_created" in indexes
    assert "ix_audit_resource_created" in indexes
