# Privacy policy

This policy covers the GCP Certification Coach plugin (`gcp-cert-coach`) in this repository. Not affiliated with or endorsed by Google or Anthropic.

## Personal data

The plugin reads personal data only to do its job and never stores it. It may see:

- your name, on your own course progress page, if you ask for the optional check in the Claude desktop app's built-in browser;
- email addresses or Google Cloud project ids in command output that you paste into a challenge.

Challenge grading redacts these, and nothing of that is saved.

## Stored data

Only your study progress: levels, the answer log, misconceptions, plan settings and snapshots. It lives in the database of your own tracker artifact on claude.ai, under your account and your control. You can reset the progress or delete the artifact at any time.

## Sending data

No data is sent to any third-party service. The plugin only fetches public pages (Google Cloud documentation and the Google Skills learning path) and runs a local seeding script in the Claude sandbox.

## Retention

The maintainer runs no server and receives or retains no data. There are no analytics and no telemetry.

## Age

The plugin is not intended for users under 18.

## Contact

Open an issue in this repository: https://github.com/olehsov/gcp-certification-coach/issues
