import { journeySearchPath, normalizeStationCode } from "./api";

export function runJourneySearchPathAssertions() {
  if (normalizeStationCode("  ndls ") !== "NDLS") throw new Error("Station normalization is invalid");
  const path = journeySearchPath({
    origin: " ndls ",
    destination: "bct",
    serviceDate: "2026-10-22",
    seatClass: "SLEEPER",
    offset: 20,
    limit: 10,
    sort: "fare",
    descending: true,
  });
  if (!path.includes("origin=NDLS") || !path.includes("seat_class=SLEEPER") || !path.includes("sort=fare") || !path.includes("descending=true")) {
    throw new Error("Journey search query mapping is invalid");
  }
  if (!path.includes("service_date=2026-10-22")) throw new Error("Travel date mapping is invalid");
}
