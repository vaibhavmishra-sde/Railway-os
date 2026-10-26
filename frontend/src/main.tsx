import { StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";
import "./ui-overrides.css";
import { api, SEAT_CLASSES, type Service, type SeatClass, type Station } from "./api";
import { useQuery } from "./useQuery";
import { journeyCountLabel, journeyTimeLabel, localDateInputValue } from "./serviceBoard";
import { clearAccessToken, getAccessToken, saveAccessToken } from "./auth";

const today = localDateInputValue();
const statusLabel = (status: string) => status.replace(/_/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());

function App() {
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const [date, setDate] = useState(today);
  const [seatClass, setSeatClass] = useState<SeatClass>("ANY");
  const [suggestions, setSuggestions] = useState<Station[]>([]);
  const [destinationSuggestions, setDestinationSuggestions] = useState<Station[]>([]);
  const [bookingOpen, setBookingOpen] = useState(false);
  const [loginOpen, setLoginOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [authError, setAuthError] = useState<string | null>(null);
  const query = useQuery<Service[]>((signal) => api.services(date, signal), [date]);
  const [journeys, setJourneys] = useState<Awaited<ReturnType<typeof api.journeys>> | null>(null);
  const [journeyError, setJourneyError] = useState<string | null>(null);
  const [journeyLoading, setJourneyLoading] = useState(false);

  useEffect(() => {
    if (getAccessToken()) void api.me().then((user) => setUserEmail(user.email)).catch(() => clearAccessToken());
  }, []);

  const signIn = async (event: React.FormEvent) => {
    event.preventDefault();
    setAuthError(null);
    try {
      const session = await api.login(email, password);
      saveAccessToken(session.access_token);
      const user = await api.me();
      setUserEmail(user.email);
      setLoginOpen(false);
      setPassword("");
    } catch (error) { setAuthError(error instanceof Error ? error.message : "Unable to sign in"); }
  };

  useEffect(() => {
    if (from.length < 2) { setSuggestions([]); return; }
    const controller = new AbortController();
    const timer = setTimeout(() => void api.stations(from, controller.signal).then(setSuggestions).catch(() => setSuggestions([])), 250);
    return () => { clearTimeout(timer); controller.abort(); };
  }, [from]);

  useEffect(() => {
    if (to.length < 2) { setDestinationSuggestions([]); return; }
    const controller = new AbortController();
    const timer = setTimeout(() => void api.stations(to, controller.signal).then(setDestinationSuggestions).catch(() => setDestinationSuggestions([])), 250);
    return () => { clearTimeout(timer); controller.abort(); };
  }, [to]);

  const searchJourneys = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setJourneyError(null);
    setJourneys(null);
    setJourneyLoading(true);
    try {
      const origin = suggestions.find((station) => station.name === from)?.code ?? from;
      if (!origin.trim() || !to.trim()) throw new Error("Enter departure and arrival stations.");
      setJourneys(await api.journeys({ origin, destination: to, serviceDate: date, seatClass: seatClass === "ANY" ? undefined : seatClass }));
    } catch (error) { setJourneyError(error instanceof Error ? error.message : "Unable to search journeys"); }
    finally { setJourneyLoading(false); }
  };

  return <main className="shell">
    <header className="topbar"><a className="brand" href="#top">Railway<span>OS</span></a><nav aria-label="Primary navigation"><a href="#search">Journeys</a><a href="#services">Live services</a></nav>{userEmail ? <button className="profile" onClick={() => { clearAccessToken(); setUserEmail(null); }}>Sign out</button> : <button className="profile" onClick={() => setLoginOpen(true)}>Sign in</button>}</header>
    <section className="hero" id="top"><div><p className="eyebrow">Network control, simplified</p><h1>Plan the journey.<br /><em>Run the network.</em></h1><p className="intro">A dependable workspace for passengers and railway teams to find services, monitor movement, and act on what matters.</p></div><div className="hero-panel"><span className="panel-label">Network pulse</span><strong>98.4%</strong><p>Services running on schedule</p><div className="pulse-bar"><i /></div></div></section>
    <section className="search-card" id="search" aria-labelledby="planner-title"><span className="panel-label">Journey planner</span><h2 id="planner-title">Where are you going?</h2><form onSubmit={searchJourneys}><label>From<input aria-label="From station" value={from} onChange={(event) => setFrom(event.target.value)} placeholder="Departure station" />{suggestions.length > 0 && <span className="suggestions" role="listbox">{suggestions.map((station) => <button type="button" role="option" key={station.id} onClick={() => { setFrom(station.name); setSuggestions([]); }}>{station.name} <small>{station.code}</small></button>)}</span>}</label><label>To<input aria-label="To station" value={to} onChange={(event) => setTo(event.target.value)} placeholder="Arrival station" />{destinationSuggestions.length > 0 && <span className="suggestions" role="listbox">{destinationSuggestions.map((station) => <button type="button" role="option" key={station.id} onClick={() => { setTo(station.name); setDestinationSuggestions([]); }}>{station.name} <small>{station.code}</small></button>)}</span>}</label><label>Date<input aria-label="Travel date" name="date" type="date" value={date} onChange={(event) => setDate(event.target.value)} /></label><button className="primary" type="submit" disabled={journeyLoading}>{journeyLoading ? "Searching…" : "Search journeys"}</button></form>{journeyError && <p className="error" role="alert">{journeyError}</p>}{journeys && <div role="region" aria-label="Journey results"><p className="notice" role="status">{journeyCountLabel(journeys.total)} found from {journeys.origin} to {journeys.destination}.</p>{journeys.items.map((journey) => <article className="service" key={journey.service_id}><strong>{journey.train_name}</strong><span>{journeyTimeLabel(journey.departure_time, journey.arrival_time)}</span><small>{journey.train_number}</small></article>)}</div>}{query.error && <p className="error" role="alert">{query.error.message}</p>}</section>
    <section className="section" id="services"><div className="section-heading"><div><span className="panel-label">Services · {date}</span><h2>Live services</h2></div><a href="#services">View timetable →</a></div>{query.loading && <p className="notice">Loading live services…</p>}{!query.loading && !query.error && query.data?.length === 0 && <p className="notice">No services are scheduled for this date.</p>}<div className="service-list">{(query.data ?? []).map((service) => <article className="service" key={service.id}><div className="service-id"><span>{service.id}</span><strong>Train {service.train_id}</strong></div><div className="route"><strong>—</strong><span>Route {service.route_id}</span></div><div className="line">●━━━━●</div><div className="route"><strong>—</strong><span>{service.service_date}</span></div><span className="status good">{statusLabel(service.status)}</span><button className="book-link" onClick={() => setBookingOpen(true)}>Book</button></article>)}</div></section>
    {bookingOpen && <dialog open className="modal"><button className="close" aria-label="Close booking preview" onClick={() => setBookingOpen(false)}>×</button><span className="panel-label">Booking preview</span><h2>Start your booking</h2><p className="muted">Choose this service, then add traveller details and seats in the next step.</p><button className="primary" onClick={() => setBookingOpen(false)}>Continue</button></dialog>}
    {loginOpen && <dialog open className="modal" aria-labelledby="login-title"><button className="close" aria-label="Close sign in" onClick={() => setLoginOpen(false)}>×</button><span className="panel-label">Passenger account</span><h2 id="login-title">Sign in to RailwayOS</h2><form className="login-form" onSubmit={signIn}><label>Email<input type="email" autoComplete="email" required value={email} onChange={(event) => setEmail(event.target.value)} /></label><label>Password<input type="password" autoComplete="current-password" required value={password} onChange={(event) => setPassword(event.target.value)} /></label>{authError && <p className="error" role="alert">{authError}</p>}<button className="primary" type="submit">Sign in</button></form></dialog>}
  </main>;
}

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
