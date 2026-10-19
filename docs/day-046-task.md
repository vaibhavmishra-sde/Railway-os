# Day 46 — Journey schedule calculations

Extend direct journey search with derived schedule information. Each result
now reports its effective departure and arrival times, elapsed duration in
minutes, and the distinct coach classes available on the train.

Duration calculations support services that cross midnight. Missing timetable
boundary times remain `null` rather than being guessed.
