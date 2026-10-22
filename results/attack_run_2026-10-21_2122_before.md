# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-10-21 21:22
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `da1f716e-4d2a-43a4-9a9b-78a296341212` | unsure | 0.543 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `797c1b75-d20e-4188-810a-df7cbed9d2a4` | unsure | 0.567 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `69c64da5-dca5-4ff5-89e3-3e25e9530811` | unsure | 0.610 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `38bc0c3c-e9d3-41fd-a5f9-8693d11333a9` | ai | 0.681 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `2b209726-c6d6-4029-9782-d3b056dc9eda` | unsure | 0.630 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `10b2ff2a-5b85-438d-8705-4c1be4af7df5` | unsure | 0.547 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `bd64e0a6-e91a-49b9-b37b-6239220fcb2a` | unsure | 0.543 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `be55cdc7-5e96-4d4c-9a9c-9bfa9bab67eb` | unsure | 0.517 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `841bfea2-4efc-426e-9162-a4bba46ed8cb` | unsure | 0.628 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `2712ca54-0b50-421e-9fe1-406400f79ae1` | ai | 0.924 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `be892a95-f3d2-4a09-8e0a-cef9d80ea7c2` | ai | 0.652 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `bebf2296-b52d-4f30-8ae2-a539f2bc14ec` | ai | 0.802 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `15fc30a9-5ee8-4e89-a6d0-a329388bd96b` | ai | 0.795 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `ba0e5309-fb33-473d-8a4f-4933211018e9` | ai | 0.756 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `e049aec8-280a-4ba0-9fa0-00e1e6d7ee7f` | ai | 0.873 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `1312b9a4-c9d8-462b-a961-c9ccf476effe` | ai | 0.742 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `834e6d58-03b5-4540-8e9e-cd633915d824` | ai | 0.722 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `104e7f14-1c86-4ff6-8ad3-db01a252b52a` | unsure | 0.547 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `1d9da6d4-79dc-46ed-a3d8-4db45913c31f` | unsure | 0.581 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `af7cca0f-36c0-4df8-b4d9-844a94c55d00` | human | 0.706 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `142ee3ca-0769-49d0-a1b2-8fcdb5ed29fb` | unsure | 0.627 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `3528121e-eda6-4088-b262-0d519b17d384` | unsure | 0.540 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `41a2fccc-9f92-42fe-b8cf-b3e8705b9d9c` | unsure | 0.531 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `76b8531d-510a-4f14-9f28-81bba5efc90a` | unsure | 0.615 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `ccdff2fa-b38b-4b4f-a98c-360a5285eb83` | unsure | 0.640 |  |
| MF04 | malformed | text is only punctuation | 200 | `4047b9cc-d2e2-49ad-8137-299296674cf8` | unsure | 0.640 |  |
| MF05 | malformed | text is a very long single word | 200 | `d1d92a9b-648d-4eb4-8aba-4d406d8a9665` | unsure | 0.640 |  |
| MF06 | malformed | text is emoji only | 200 | `c0628dad-86e2-4966-8ba7-acaab10decda` | unsure | 0.640 |  |
| MF07 | malformed | text is right-to-left script | 200 | `3fbd21d9-ec27-4d35-be71-23da9b639b78` | unsure | 0.640 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `e0eed6ae-750d-403b-9e94-13f97273709e` | ai | 0.850 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7a860e85-516b-4c3d-a610-dd062c91c946` | unsure | 0.640 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ba59614c-6212-4e86-b426-db26c9f007ea` | unsure | 0.640 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `81d7b3a2-72a8-4ad6-ba62-1c2baea885dc` | unsure | 0.640 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f39069fe-c0b5-45d1-8f72-1d8422024fc3` | unsure | 0.640 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f5acc4e0-7265-4cc9-8759-63ac069b5427` | unsure | 0.640 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "da1f716e-4d2a-43a4-9a9b-78a296341212",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5433,
  "model_score": 0.1635,
  "style_score": 0.75,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "797c1b75-d20e-4188-810a-df7cbed9d2a4",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5671,
  "model_score": 0.5943,
  "style_score": 0.27152014652014655,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "69c64da5-dca5-4ff5-89e3-3e25e9530811",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.6102,
  "model_score": 0.6662,
  "style_score": 0.55415632682449,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "38bc0c3c-e9d3-41fd-a5f9-8693d11333a9",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.6807,
  "model_score": 0.6114,
  "style_score": 0.75,
  "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "2b209726-c6d6-4029-9782-d3b056dc9eda",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.6305,
  "model_score": 0.3212,
  "style_score": 0.4177682246900017,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "10b2ff2a-5b85-438d-8705-4c1be4af7df5",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.547,
  "model_score": 0.5727,
  "style_score": 0.3333333333333333,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "bd64e0a6-e91a-49b9-b37b-6239220fcb2a",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5431,
  "model_score": 0.5862,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "be55cdc7-5e96-4d4c-9a9c-9bfa9bab67eb",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.5173,
  "model_score": 0.2452,
  "style_score": 0.7201429886594373,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "841bfea2-4efc-426e-9162-a4bba46ed8cb",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6282,
  "model_score": 0.7042,
  "style_score": 0.5522397078131156,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "2712ca54-0b50-421e-9fe1-406400f79ae1",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9242,
  "model_score": 0.9792,
  "style_score": 0.8691773544117198,
  "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "be892a95-f3d2-4a09-8e0a-cef9d80ea7c2",
  "creator_id": "attacker_FP01",
  "guess": "ai",
  "confidence": 0.6519,
  "model_score": 0.6175,
  "style_score": 0.686359757145689,
  "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "bebf2296-b52d-4f30-8ae2-a539f2bc14ec",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.8025,
  "model_score": 0.7387,
  "style_score": 0.8662280701754386,
  "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "15fc30a9-5ee8-4e89-a6d0-a329388bd96b",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.795,
  "model_score": 0.8051,
  "style_score": 0.7848428958333062,
  "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "ba0e5309-fb33-473d-8a4f-4933211018e9",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7556,
  "model_score": 0.8329,
  "style_score": 0.6782415447526647,
  "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "e049aec8-280a-4ba0-9fa0-00e1e6d7ee7f",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8731,
  "model_score": 0.8005,
  "style_score": 0.9457949478769414,
  "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "1312b9a4-c9d8-462b-a961-c9ccf476effe",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7415,
  "model_score": 0.8814,
  "style_score": 0.6016596290008669,
  "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "834e6d58-03b5-4540-8e9e-cd633915d824",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7222,
  "model_score": 0.8816,
  "style_score": 0.5628065848730068,
  "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "104e7f14-1c86-4ff6-8ad3-db01a252b52a",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.547,
  "model_score": 0.3223,
  "style_score": 0.5836248164616189,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "1d9da6d4-79dc-46ed-a3d8-4db45913c31f",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.5813,
  "model_score": 0.4625,
  "style_score": 0.3748594598890096,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "af7cca0f-36c0-4df8-b4d9-844a94c55d00",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.7055,
  "model_score": 0.2044,
  "style_score": 0.38469543943853013,
  "label": "We think this was probably written by a person. Our check is only a guess, but nothing in it stood out to us.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "142ee3ca-0769-49d0-a1b2-8fcdb5ed29fb",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.627,
  "model_score": 0.5943,
  "style_score": 0.6597237642295337,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "3528121e-eda6-4088-b262-0d519b17d384",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5404,
  "model_score": 0.4998,
  "style_score": 0.5810920165063929,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "41a2fccc-9f92-42fe-b8cf-b3e8705b9d9c",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5306,
  "model_score": 0.6401,
  "style_score": 0.29872316291724393,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "76b8531d-510a-4f14-9f28-81bba5efc90a",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.6153,
  "model_score": 0.5583,
  "style_score": 0.6723339886831252,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "ccdff2fa-b38b-4b4f-a98c-360a5285eb83",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "4047b9cc-d2e2-49ad-8137-299296674cf8",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "d1d92a9b-648d-4eb4-8aba-4d406d8a9665",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "c0628dad-86e2-4966-8ba7-acaab10decda",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "3fbd21d9-ec27-4d35-be71-23da9b639b78",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "e0eed6ae-750d-403b-9e94-13f97273709e",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.8503,
  "model_score": 0.9876,
  "style_score": 0.7130005277837119,
  "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "7a860e85-516b-4c3d-a610-dd062c91c946",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "ba59614c-6212-4e86-b426-db26c9f007ea",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "81d7b3a2-72a8-4ad6-ba62-1c2baea885dc",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "f39069fe-c0b5-45d1-8f72-1d8422024fc3",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "f5acc4e0-7265-4cc9-8759-63ac069b5427",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
