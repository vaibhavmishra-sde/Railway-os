import { StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";
import "./ui-overrides.css";
import { api, type Service, type Station } from "./api";
import { useQuery } from "./useQuery";

const today = new Date().toISOString().slice(0, 10);
const statusLabel = (status: string) => status.replace(/_/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());

function App() {
  const [from, setFrom] = useState("");
  const [date, setDate] = useState(today);
  const [suggestions, setSuggestions] = useState<Station[]>([]);
  const [bookingOpen, setBookingOpen] = useState(false);
  const query = useQuery<Service[]>(() => api.services(date), [date]);

  useEffect(() => {
    if (from.length < 2) { setSuggestions([]); return; }
    const timer = setTimeout(() => void api.stations(from).then(setSuggestions).catch(() => setSuggestions([])), 250);
    return () => clearTimeout(timer);
  }, [from]);

  return <main className="shell">
    <header className="topbar"><a className="brand" href="#top">Railway<span>OS</span></a><nav><a href="#search">Journeys</a><a href="#services">Live services</a><a href="#operations">Operations</a></nav><button className="profile">Sign in</button></header>
    <section className="hero" id="top"><div><p className="eyebrow">Network control, simplified</p><h1>Plan the journey.<br /><em>Run the network.</em></h1><p className="intro">A dependable workspace for passengers and railway teams to find services, monitor movement, and act on what matters.</p></div><div className="hero-panel"><span className="panel-label">Network pulse</span><strong>98.4%</strong><p>Services running on schedule</p><div className="pulse-bar"><i /></div></div></section>
    <section className="search-card" id="search"><span className="panel-label">Journey planner</span><h2>Where are you going?</h2><form onSubmit={(event) => { event.preventDefault(); setDate(new FormData(event.currentTarget).get("date") as string); }}><label>From<input aria-label="From station" value={from} onChange={(event) => setFrom(event.target.value)} placeholder="Departure station" />{suggestions.length > 0 && <span className="suggestions">{suggestions.map((station) => <button type="button" key={station.id} onClick={() => { setFrom(station.name); setSuggestions([]); }}>{station.name} <small>{station.code}</small></button>)}</span>}</label><label>To<input aria-label="To station" placeholder="Arrival station" /></label><label>Date<input aria-label="Travel date" name="date" type="date" value={date} onChange={(event) => setDate(event.target.value)} /></label><button className="primary" type="submit">Search journeys</button></form>{query.error && <p className="error" role="alert">{query.error.message}</p>}</section>
    <section className="section" id="services"><div className="section-heading"><div><span className="panel-label">Services · {date}</span><h2>Live services</h2></div><a href="#services">View timetable →</a></div>{query.loading && <p className="notice">Loading live services…</p>}{!query.loading && !query.error && query.data?.length === 0 && <p className="notice">No services are scheduled for this date.</p>}<div className="service-list">{(query.data ?? []).map((service) => <article className="service" key={service.id}><div className="service-id"><span>{service.id}</span><strong>Train {service.train_id}</strong></div><div className="route"><strong>—</strong><span>Route {service.route_id}</span></div><div className="line">●━━━━●</div><div className="route"><strong>—</strong><span>{service.service_date}</span></div><span className="status good">{statusLabel(service.status)}</span><button className="book-link" onClick={() => setBookingOpen(true)}>Book</button></article>)}</div></section>
    <section className="operations" id="operations"><div><span className="panel-label">For railway teams</span><h2>One clear view of the network.</h2><p>Give every team the context they need, from platform allocation to service updates and passenger impact.</p></div></section>
    {bookingOpen && <dialog open className="modal"><button className="close" onClick={() => setBookingOpen(false)}>×</button><span className="panel-label">Booking preview</span><h2>Start your booking</h2><p className="muted">Choose this service, then add traveller details and seats in the next step.</p><button className="primary" onClick={() => setBookingOpen(false)}>Continue</button></dialog>}
  </main>;
}

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
