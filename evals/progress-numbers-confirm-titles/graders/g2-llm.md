---
type: "llm"
weight: 1
---
PASS if all hold: (1) it resolves the numbers to titles and asks a confirmation question that names the course title (Essential Google Cloud Infrastructure: Core Services) and the module title (Storage and Database Services), in the form 'Do you mean course 4 <title>, module <title>?'; (2) it does not write or claim to have saved or marked anything before the learner says yes (showing the planned change as pending is fine). FAIL if it marks the module completed, says it is saved, or confirms without naming the titles.
