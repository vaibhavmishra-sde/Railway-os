export const serviceStatusClass = (status: string) => status === "On time" ? "good" : "warn";

export function runServiceBoardAssertions() {
  if (serviceStatusClass("On time") !== "good" || serviceStatusClass("Delayed 12m") !== "warn") {
    throw new Error("Service status mapping is invalid");
  }
}
