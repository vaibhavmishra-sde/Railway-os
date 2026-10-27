export const classLabel = (value: string) => ({ FIRST: "First AC", AC: "Third AC", SLEEPER: "Sleeper", SECOND: "Second AC", GENERAL: "General" }[value] ?? value);

export const fareLabel = (fares: Record<string, number>) => Object.entries(fares).map(([seatClass, fare]) => `${classLabel(seatClass)} ₹${fare}`).join(" · ");

export const durationLabel = (minutes: number | null) => minutes == null ? "Duration unavailable" : `${Math.floor(minutes / 60)}h ${minutes % 60}m`;
