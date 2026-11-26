import pytest

from app.services.pnr import PNRGenerationError, format_pnr, generate_pnr


def test_format_pnr_has_fixed_railwayos_shape():
    assert format_pnr(42) == "RO00000042"
    assert len(format_pnr(99_999_999)) == 10


def test_generator_retries_existing_candidate():
    seen = {"RO00000042"}
    values = iter([42, 314])

    pnr = generate_pnr(
        lambda candidate: candidate not in seen, number_factory=lambda: next(values)
    )

    assert pnr == "RO00000314"


def test_generator_fails_after_bounded_collisions():
    with pytest.raises(PNRGenerationError):
        generate_pnr(lambda _: False, number_factory=lambda: 7, max_attempts=3)


def test_format_rejects_numbers_outside_eight_digit_range():
    with pytest.raises(ValueError):
        format_pnr(100_000_000)
