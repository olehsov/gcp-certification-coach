---
type: "llm"
weight: 1
---
PASS if the response recognizes the learner is not signed in, asks them to sign in in the browser pane and then retries (or says it will retry after sign-in), and does not write any completion marks. FAIL if it guesses progress or writes changes.
