import importlib.util
from pathlib import Path

from sqlalchemy import inspect

from app.db.session import create_db_engine


def load_migration_module():
    migration_path = Path(__file__).resolve().parents[1] / "app" / "db" / "migrations" / "001_init.py"
    spec = importlib.util.spec_from_file_location("migration_001_init", migration_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_T01_initial_database_schema_is_created():
    engine = create_db_engine("sqlite:///:memory:")
    migration = load_migration_module()

    migration.upgrade(engine)

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    assert "slots" in tables
    assert "bookings" in tables
    assert "audit_logs" in tables

    bookings_columns = {column["name"] for column in inspector.get_columns("bookings")}
    assert "hn" in bookings_columns
    assert "national_id" not in bookings_columns

    slots_columns = {column["name"] for column in inspector.get_columns("slots")}
    assert "remaining" in slots_columns

    audit_columns = {column["name"] for column in inspector.get_columns("audit_logs")}
    assert "actor_id" in audit_columns
    assert "accessed_at" in audit_columns
