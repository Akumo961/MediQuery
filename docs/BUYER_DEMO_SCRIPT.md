# MediQuery — Buyer Demonstration Script

## Demo rules

- Use synthetic data only.
- Do not claim diagnosis, clinical validation, or autonomous medical AI.
- Show the source PDF beside the extracted values when possible.
- Demonstrate both successful extraction and the extraction-attention warning.

## 8-minute demo

### 1. Login — 45 seconds

Create or use a synthetic demo account. Show that authentication is required before reports are accessible.

### 2. Upload PDF — 60 seconds

Upload a synthetic laboratory PDF containing Hemoglobin, WBC, Platelets, glucose, reference ranges, and flags.

Call out that WBC/Platelets use `10^3/uL`, a real CBC notation supported by the current parser.

### 3. Processing — 45 seconds

Show the processing result and report creation. Explain that the current pipeline is deterministic `pypdf + regex`, not an LLM.

### 4. Extracted values — 90 seconds

Show:

- name
- value
- unit
- reference range
- flag

Emphasize that unsupported content is not invented.

### 5. Evidence — 60 seconds

Open a finding and show its page number and evidence text derived from the PDF source text.

### 6. Report history/detail — 60 seconds

Refresh/list reports, open the report detail, and show persistence.

### 7. Security / isolation — 60 seconds

If two demo accounts are prepared, attempt cross-account report access and show that it is denied without revealing report existence.

### 8. Account management — 60 seconds

Delete the demo account. Show that subsequent login fails and protected report access is rejected.

## Closing message

“MediQuery is a secure software foundation for medical-document organization and evidence-preserving extraction. The current release deliberately avoids claiming clinical AI. A buyer can extend the replaceable architecture with validated retrieval or AI capabilities under appropriate clinical, privacy, security, and regulatory controls.”
