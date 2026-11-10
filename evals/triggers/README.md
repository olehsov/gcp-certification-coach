# Trigger eval sets

Query sets for the skill-creator trigger evaluation (`scripts/run_eval.py` of the skill-creator skill): 8 queries that should trigger the skill and 8 that should not (requests for sibling skills, and same-keyword requests unrelated to Google Cloud certification prep). All queries are invented. Results are summarized in [../RESULTS.md](../RESULTS.md).

The runner tests one skill in isolation, so the negatives check over-triggering, not disambiguation between sibling skills; the plugin eval's `skill-fired` graders cover that.
