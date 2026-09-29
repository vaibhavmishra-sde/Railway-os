"""Seed the synthetic RailwayOS stations and routes."""

from app.db.session import SessionLocal
from app.seed.network import seed_coaches, seed_network, seed_seats, seed_service_stops, seed_services, seed_trains


def main() -> None:
    with SessionLocal() as session:
        stations, routes = seed_network(session)
        trains = seed_trains(session)
        coaches = seed_coaches(session, trains)
        seats = seed_seats(session, coaches)
        services = seed_services(session, trains, routes)
        stops = seed_service_stops(session, services)
        session.commit()
    print(f"Seeded {len(stations)} stations, {len(routes)} routes, {len(trains)} trains, {len(coaches)} coaches, {len(seats)} seats, {len(services)} services, and {len(stops)} stops.")


if __name__ == "__main__":
    main()
