---
type: "llm"
weight: 1
---
PASS if the question asked is about a concept from a completed module only (c2-m1 Introducing Google Cloud, c2-m2 Resources and Access, c4-m2 IAM). Topics from uncompleted modules c2-m3 (VPC networking, Compute Engine) and c4-m3 (Cloud SQL, storage) must not be asked. Given the open misconception on service accounts, asking about service accounts / attached service accounts with new wording is the ideal choice. FAIL if the question targets VPC networking, Compute Engine VM creation, Cloud SQL or other storage services.
