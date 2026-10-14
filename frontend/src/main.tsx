import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";
import "./ui-overrides.css";
import { api, type Station, type Service } from "./api";
import { useEffect, useState } from "react";

const demoServices = [
  ["RX 204", "Coastal Express", "06:40", "Mumbai Central", "10:05", "Pune Junction", "On time"],
  ["RX 817", "Deccan Intercity", "08:15", "Pune Junction", "16:20", "Hyderabad", "Boarding"],
  ["RX 531", "Western Link", "09:30", "Ahmedabad", "15:10", "Mumbai Central", "Delayed 12m"],
];

function App() {
  const [from, setFrom] = useState("");
  const [suggestions, setSuggestions] = useState<Station[]>([]);
  const [serviceData, setServiceData] = useState<Service[] | null>(null);
  const [serviceError, setServiceError] = useState("");
  const [loading, setLoading] = useState(false);
  const [authOpen, setAuthOpen] = useState(false);
  const [bookingOpen, setBookingOpen] = useState(false);
  useEffect(() => { if (from.length < 2) { setSuggestions([]); return; } const timer = setTimeout(() => { api.stations(from).then(setSuggestions).catch(() => setSuggestions([])); }, 250); return () => clearTimeout(timer); }, [from]);
  const search = async (event: React.FormEvent) => { event.preventDefault(); setLoading(true); setServiceError(""); try { setServiceData(await api.services("2026-10-14")); } catch { setServiceError("We could not load journeys. Check that the API is running and try again."); } finally { setLoading(false); } };
  return <main className="shell">
    <header className="topbar"><a className="brand" href="#top">Railway<span>OS</span></a><nav><a href="#search">Journeys</a><a href="#services">Live services</a><a href="#operations">Operations</a></nav><button className="profile" onClick={() => setAuthOpen(true)}>Sign in</button></header>
    <section className="hero" id="top"><div><p className="eyebrow">Network control, simplified</p><h1>Plan the journey.<br /><em>Run the network.</em></h1><p className="intro">A dependable workspace for passengers and railway teams to find services, monitor movement, and act on what matters.</p></div><div className="hero-panel"><span className="panel-label">Network pulse</span><strong>98.4%</strong><p>Services running on schedule</p><div className="pulse-bar"><i /></div></div></section>
    <section className="search-card" id="search"><span className="panel-label">Journey planner</span><h2>Where are you going?</h2><form onSubmit={search}><label>From<input aria-label="From station" value={from} onChange={(event) => setFrom(event.target.value)} placeholder="Departure station" />{suggestions.length > 0 && <span className="suggestions">{suggestions.map((station) => <button type="button" key={station.id} onClick={() => { setFrom(station.name); setSuggestions([]); }}>{station.name} <small>{station.code}</small></button>)}</span>}</label><label>To<input aria-label="To station" placeholder="Arrival station" /></label><label>Date<input aria-label="Travel date" type="date" defaultValue="2026-10-14" /></label><button className="primary" type="submit">{loading ? "Searching…" : "Search journeys"}</button></form>{serviceError && <p className="error" role="alert">{serviceError}</p>}</section>
    <section className="section" id="services"><div className="section-heading"><div><span className="panel-label">Today · 14 October 2026</span><h2>Live services</h2></div><a href="#services">View timetable →</a></div>{loading && <p className="notice">Loading live services…</p>}<div className="service-list">{(serviceData ? serviceData.map((service) => [service.id, service.train_id, "—", "Scheduled", "—", "", service.status]) : demoServices).map(([number, name, departure, from, arrival, to, status]) => <article className="service" key={number}><div className="service-id"><span>{number}</span><strong>{name}</strong></div><div className="route"><strong>{departure}</strong><span>{from}</span></div><div className="line">●━━━━●</div><div className="route"><strong>{arrival}</strong><span>{to}</span></div><span className="status good">{status}</span><button className="book-link" onClick={() => setBookingOpen(true)}>Book</button></article>)}</div></section>
    <section className="operations" id="operations"><div><span className="panel-label">For railway teams</span><h2>One clear view of the network.</h2><p>Give every team the context they need, from platform allocation to service updates and passenger impact.</p></div><button className="secondary">Open operations view <span>→</span></button></section>{authOpen && <dialog open className="modal"><button className="close" onClick={() => setAuthOpen(false)}>×</button><span className="panel-label">Passenger account</span><h2>Welcome back</h2><form onSubmit={(event) => { event.preventDefault(); setAuthOpen(false); }}><input aria-label="Email" type="email" placeholder="Email address" required /><input aria-label="Password" type="password" placeholder="Password" required /><button className="primary">Sign in</button></form><p className="muted">Your account keeps bookings and journeys in one place.</p></dialog>}{bookingOpen && <dialog open className="modal"><button className="close" onClick={() => setBookingOpen(false)}>×</button><span className="panel-label">Booking preview</span><h2>Start your booking</h2><p className="muted">Choose this service, then add traveller details and seats in the next step.</p><button className="primary" onClick={() => setBookingOpen(false)}>Continue</button></dialog>}
  </main>;
}

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
