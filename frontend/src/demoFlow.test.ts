import { demoStepLabel, isPassengerDemoComplete, passengerDemoSteps } from "./demoFlow";

export function runPassengerDemoAssertions() {
  if (demoStepLabel("journey search") !== "Journey Search") throw new Error("Demo step labels are invalid");
  if (isPassengerDemoComplete(passengerDemoSteps.slice(0, 2))) throw new Error("Incomplete demo marked complete");
  if (!isPassengerDemoComplete(passengerDemoSteps)) throw new Error("Complete demo not recognized");
}
