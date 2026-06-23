---
name: check-jp-names
description: Check japanese names in `raw/researchers_YYYY.json`
model: sonnet
arguments: [reseracher_id]
argument-hint: "researcher ID is used to specify from what line in `raw/researchers_YYYY.json` we should start checking."
---

# Workflow: Identifying JP Researchers from researchers_YYYY.json

## Goal

Enumerate Japanese researcher names from `raw/researchers_YYYY.json`, starting from the specified line entry, and name the found japanese names.

both `raw/researchers_YYYY.json` and `raw/japanese_researchers_YYYY.json` follow this schema:
```json
{
  "researcher name A": `citation count of A (int)`,
  "researcher name B": `citation count of B (int)`,
  ...
}
```

## Rules
- Do NOT edit files under `raw/` directly.
- Focus on japanese names only. No chinese names.
- Include any ambiguous names.
  - Japanese surnames (Yamamoto, Tanaka, Suzuki, Nakamura, …): INCLUDE
  - Chinese surnames (Chen, Wang, Li, Zhang, …): EXCLUDE
  - Korean surnames (Kim, Park, Lee, Choi, …): EXCLUDE
  - When ambiguous between Japanese and Chinese: INCLUDE
- Pass the batch data via a file (not inline in the prompt) to avoid accidental truncation or wrong content.

## Steps

### 1. Assess current state

```bash
# Count researcher names.
python3 -c "import json; data=json.load(open('raw/researchers_YYYY.json')); print(len(data))"
python3 -c "import json; data=json.load(open('raw/japanese_researchers_YYYY.json')); print(len(data))"
```

Check the last few entries in `japanese_researchers_YYYY.json` to confirm where the previous run stopped.

### 2. Extract the unchecked slice

```python
import json
data = json.load(open('raw/researchers_YYYY.json'))
items = list(data.items())
# For example, if we need to check from the researcher 8000.
batch = items[8000:]   # 0-indexed: index 8000 = researcher 8001
```

### 3. Split into batches for parallel agents

Divide the slice into N equal batches (4 worked well for ~1400 names) and save each as a JSON file in a temp directory.

```python
size = len(batch) // 4
for i in range(4):
    start = i * size
    end = (i+1)*size if i < 3 else len(batch)
    chunk = dict(batch[start:end])
    json.dump(chunk, open(f'batch_{i+1}.json', 'w'), ensure_ascii=False, indent=2)
```

### 4. Launch parallel agents (one per batch)

Each agent receives:
- Path to its batch file.
- Rules of this skill.
- A reference list of common Japanese surnames.

Agents read the file and return only the found japanese names.

### 5. Validate agent results

For each name returned by the agents:
1. Verify it exists in the target slice of `researchers_YYYY.json` (guards against hallucination)
2. Check it is not already in `japanese_researchers_YYYY.json` (deduplication)

```python
found_items = dict(list(researchers.items())[start_id:])
truly_new = {k: v for k, v in found.items() if k in found_items and k not in existing_jp}
```

### 6. Report the found names.

Simply report the found names.
