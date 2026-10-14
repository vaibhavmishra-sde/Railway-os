import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const services = [
  ["RX 204", "Coastal Express", "06:40", "Mumbai Central", "10:05", "Pune Junction", "On time"],
  ["RX 817", "Deccan Intercity", "08:15", "Pune Junction", "16:20", "Hyderabad", "Boarding"],
  ["RX 531", "Western Link", "09:30", "Ahmedabad", "15:10", "Mumbai Central", "Delayed 12m"],
];

function App() {
  return <main className="shell">
    <header className="topbar"><a className="brand" href="#top">Railway<span>OS</span></a><nav><a href="#search">Journeys</a><a href="#services">Live services</a><a href="#operations">Operations</a></nav><button className="profile">Demo account</button></header>
    <section className="hero" id="top"><div><p className="eyebrow">Network control, simplified</p><h1>Plan the journey.<br /><em>Run the network.</em></h1><p className="intro">A dependable workspace for passengers and railway teams to find services, monitor movement, and act on what matters.</p></div><div className="hero-panel"><span className="panel-label">Network pulse</span><strong>98.4%</strong><p>Services running on schedule</p><div className="pulse-bar"><i /></div></div></section>
    <section className="search-card" id="search"><span className="panel-label">Journey planner</span><h2>Where are you going?</h2><form onSubmit={(event) => event.preventDefault()}><label>From<input aria-label="From station" placeholder="Departure station" /></label><label>To<input aria-label="To station" placeholder="Arrival station" /></label><label>Date<input aria-label="Travel date" type="date" defaultValue="2026-10-14" /></label><button className="primary" type="submit">Search journeys</button></form></section>
    <section className="section" id="services"><div className="section-heading"><div><span className="panel-label">Today · 14 October 2026</span><h2>Live services</h2></div><a href="#services">View timetable →</a></div><div className="service-list">{services.map(([number, name, departure, from, arrival, to, status]) => <article className="service" key={number}><div className="service-id"><span>{number}</span><strong>{name}</strong></div><div className="route"><strong>{departure}</strong><span>{from}</span></div><div className="line">●━━━━●</div><div className="route"><strong>{arrival}</strong><span>{to}</span></div><span className={status === "On time" ? "status good" : "status warn"}>{status}</span></article>)}</div></section>
    <section className="operations" id="operations"><div><span className="panel-label">For railway teams</span><h2>One clear view of the network.</h2><p>Give every team the context they need, from platform allocation to service updates and passenger impact.</p></div><button className="secondary">Open operations view <span>→</span></button></section>
  </main>;
}

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
