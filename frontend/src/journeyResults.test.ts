import { describe, expect, it } from "vitest";
import { classLabel, durationLabel, fareLabel } from "./journeyResults";

describe("journey result formatting", () => {
  it("formats duration and unavailable values", () => {
    expect(durationLabel(145)).toBe("2h 25m");
    expect(durationLabel(null)).toBe("Duration unavailable");
  });

  it("formats known and unknown classes", () => {
    expect(classLabel("AC")).toBe("Third AC");
    expect(classLabel("CUSTOM")).toBe("CUSTOM");
  });

  it("formats fares with readable class names", () => {
    expect(fareLabel({ SLEEPER: 120, AC: 240 })).toBe("Sleeper ₹120 · Third AC ₹240");
  });
});
