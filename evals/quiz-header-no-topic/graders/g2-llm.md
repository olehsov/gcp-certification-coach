---
type: "llm"
weight: 1
---
Look only at the header line of the question (the line that says which question this is). PASS if it contains only the question number and total and the difficulty (for example 'Question 1 of 5 · medium') and names no concept, module, section or service, and the message has no other line that announces the topic or concept being tested. The question text itself may of course mention services. FAIL if the header or any label line reveals a concept, module or topic such as 'Service accounts', 'IAM', 'Resource hierarchy'.
