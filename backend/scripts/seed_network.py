"""Seed the synthetic RailwayOS stations and routes."""

from app.db.session import SessionLocal
from app.seed.network import seed_network


def main() -> None:
    with SessionLocal() as session:
        stations, routes = seed_network(session)
    print(f"Seeded {len(stations)} stations and {len(routes)} routes.")


if __name__ == "__main__":
    main()
