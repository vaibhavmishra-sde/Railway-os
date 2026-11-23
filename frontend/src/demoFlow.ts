export const passengerDemoSteps = ["registration", "login", "journey search"] as const;
export type PassengerDemoStep = (typeof passengerDemoSteps)[number];

export const demoStepLabel = (step: PassengerDemoStep) => step.replace(/\b\w/g, (letter) => letter.toUpperCase());

export function isPassengerDemoComplete(completed: readonly PassengerDemoStep[]) {
  return passengerDemoSteps.every((step) => completed.includes(step));
}
