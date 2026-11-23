warning: in the working copy of 'backend/app/seed/network.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'backend/tests/test_network_seed.py', LF will be replaced by CRLF the next time Git touches it
[1mdiff --git a/backend/app/seed/network.py b/backend/app/seed/network.py[m
[1mindex e4d2f07..53c8745 100644[m
[1m--- a/backend/app/seed/network.py[m
[1m+++ b/backend/app/seed/network.py[m
[36m@@ -242,6 +242,7 @@[m [mdef seed_service_stops([m
 [m
 def seed_full_network(session: Session) -> dict[str, int]:[m
     """Seed the complete demo catalog and return inserted/catalog counts."""[m
[32m+[m[32m    roles = seed_roles(session)[m
     stations, routes = seed_network(session)[m
     trains = seed_trains(session)[m
     coaches = seed_coaches(session, trains)[m
[36m@@ -249,7 +250,9 @@[m [mdef seed_full_network(session: Session) -> dict[str, int]:[m
     services = seed_services(session, trains, routes)[m
     stops = seed_service_stops(session, services)[m
     session.commit()[m
[32m+[m
     return {[m
[32m+[m[32m        "roles": len(roles),[m
         "stations": len(stations),[m
         "routes": len(routes),[m
         "trains": len(trains),[m
[1mdiff --git a/backend/tests/test_network_seed.py b/backend/tests/test_network_seed.py[m
[1mindex 2a63e0e..bd436d3 100644[m
[1m--- a/backend/tests/test_network_seed.py[m
[1m+++ b/backend/tests/test_network_seed.py[m
[36m@@ -1,6 +1,7 @@[m
 from sqlalchemy import create_engine, select[m
 from sqlalchemy.orm import Session[m
[31m-[m
[32m+[m[32mfrom app.models.identity import Role[m
[32m+[m[32mfrom app.seed.network import seed_roles[m
 from app.db.session import Base[m
 from app.models.route import Route, RouteStop[m
 from app.models.seat import Seat[m
[36m@@ -19,6 +20,18 @@[m [mfrom app.seed.network import ([m
 )[m
 [m
 [m
[32m+[m[32mdef test_role_seed_is_idempotent(db_session):[m
[32m+[m[32m    first = seed_roles(db_session)[m
[32m+[m[32m    db_session.commit()[m
[32m+[m
[32m+[m[32m    second = seed_roles(db_session)[m
[32m+[m[32m    db_session.commit()[m
[32m+[m
[32m+[m[32m    assert len(first) == 4[m
[32m+[m[32m    assert len(second) == 4[m
[32m+[m[32m    assert db_session.query(Role).count() == 4[m
[32m+[m
[32m+[m
 def test_network_seed_is_idempotent():[m
     engine = create_engine("sqlite://")[m
     Base.metadata.create_all(engine)[m
