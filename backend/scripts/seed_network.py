"""Seed the synthetic RailwayOS stations and routes."""

from app.db.session import SessionLocal
from app.seed.network import seed_full_network


def main() -> None:
    with SessionLocal() as session:
        counts = seed_full_network(session)
    print("Seeded " + ", ".join(f"{name}={count}" for name, count in counts.items()))


if __name__ == "__main__":
    main()
