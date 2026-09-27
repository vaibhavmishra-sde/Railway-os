"""Day 21 checks for core schema constraints and model relationships."""

from sqlalchemy import inspect


def test_seat_schema_has_foreign_key_and_index(test_engine):
    inspector = inspect(test_engine)

    foreign_keys = inspector.get_foreign_keys("seats")
    assert any(
        fk["referred_table"] == "coaches"
        and fk["constrained_columns"] == ["coach_id"]
        for fk in foreign_keys
    )

    indexes = inspector.get_indexes("seats")
    assert any(index["column_names"] == ["coach_id"] for index in indexes)


def test_core_tables_have_expected_unique_constraints(test_engine):
    inspector = inspect(test_engine)

    expected = {
        "coaches": {"train_id", "coach_number"},
        "seats": {"coach_id", "seat_number"},
    }
    for table, columns in expected.items():
        constraints = inspector.get_unique_constraints(table)
        assert any(set(item["column_names"]) == columns for item in constraints)

    train_indexes = inspector.get_indexes("trains")
    assert any(index["unique"] and index["column_names"] == ["number"] for index in train_indexes)
