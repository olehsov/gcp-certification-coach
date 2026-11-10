---
type: "llm"
weight: 1
---
PASS if all hold: (1) it reads the hedged answer 'probably A' as confidence 1 without asking for a confidence (and may say so); (2) A is wrong, and it explains why the key B is right and why each other option is wrong; (3) concept c4-m2-k2 goes from level 50 to 46.0 (wrong, medium, confidence 1: 50 - 0.08 x 50), or it applies the same formula with a clearly stated different difficulty; (4) it does NOT create a misconception for this answer. FAIL if it creates a misconception, treats the confidence as 2 or 3, or asks for the confidence instead of scoring.
