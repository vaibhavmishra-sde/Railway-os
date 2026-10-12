import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function App() {
  return (
    <main className="shell">
      <p className="eyebrow">RailwayOS</p>
      <h1>Plan the journey. Run the network.</h1>
      <p className="intro">A synthetic railway operations platform for passenger and staff workflows.</p>
      <div className="cards">
        <section><span>Passenger</span><h2>Find a journey</h2><p>Search timetables and manage upcoming travel.</p></section>
        <section><span>Operations</span><h2>Monitor services</h2><p>Track service status and operational updates.</p></section>
      </div>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
