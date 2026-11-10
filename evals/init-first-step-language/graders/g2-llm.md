---
type: "llm"
weight: 1
---
PASS if the response starts the setup with the explanation-language question (English as default is fine) and does not publish anything yet. Asking only this one question now and the certification next is correct (the setup asks one question per message). FAIL if it skips the language question, asks for the certification first, or publishes a tracker immediately.
