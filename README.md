# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

Provenance Guard is a small Flask service that guesses whether a piece of writing was made by a person or an AI tool, and gives the writer a plain-language label they can appeal. It never decides anything on its own: it makes a guess, says how unsure it is, and keeps a record.

The path a submission takes:

1. A client sends `POST /submit` with `text` and `creator_id`. The route (`app.py`) returns HTTP 400 if either is missing or empty.
2. The text goes to the model signal. If it is too short to score (under three tokens), that is also a 400.
3. Signal one (`detector.py::model_signal`) runs GPT-2 over the first 400 tokens and turns perplexity into `model_score`, 0–1.
4. Signal two (`stylometry.py::style_signal`) measures sentence-length spread, vocabulary variety and punctuation density and returns `style_score`, 0–1.
5. `scoring.py::combine_signals` merges the two into one `combined_score`. If the signals disagree by more than 0.35, the score is held inside the unsure band.
6. `scoring.py::score_to_label` maps the score to one of three labels (human, unsure, AI) written for a non-technical reader, and the guess (`human` / `unsure` / `ai`) is set from the same ranges.
7. The route generates a `content_id` (a UUID), and `audit.py` appends the decision (ids, both signal scores, combined score, guess, label, status `decided`, timestamp) to `logs/audit.jsonl`, and the route returns `content_id`, `guess`, `confidence`, `label`, `model_score` and `style_score`.

If a writer disagrees, `POST /appeal` with the `content_id` and their `reasoning` writes a second log entry with status `under_review`. `GET /log` shows the whole history.



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model. A local GPT-2 reads the first 400 tokens (roughly 300 words) and computes perplexity. A logistic curve on log-perplexity (midpoint 45, steepness 1.6, both left at the starter defaults) maps it to `model_score`, 0–1, higher meaning more AI-like (`detector.py::model_signal`).

**Why that might differ between human and AI writing:** A language model produces the likely next word, so its output tends to be highly predictable to another language model. People reach for surprising words and odd turns more often.

**What it can't see:** Predictability is not authorship. Plain writing in common words and short sentences scores machine-like however it was produced: second-language writers, younger writers, anyone writing simply. My plain-human test ("I went to the store yesterday...") scored 0.88. It can also be fooled the other way: my lightly-edited AI input scored only 0.33. Adding a single typo ("Artifcial") to the same text moved it from 0.50 to 0.33, because a misspelt word is surprising to the model. The style signal stayed at 0.71 either way. It only reads the first 400 tokens, so the rest of a long piece is never seen, and text under three tokens can't be scored at all (the service returns a 400).

### Signal two — the style signal

**What it measures:** The shape of the text, with no understanding of it (`stylometry.py::style_signal`). Three measures, each scaled to 0–1 with a linear ramp (endpoints in `config.py`), then averaged:

| Measure | What it is | Fully AI-like at | Fully human-like at | Weight |
|---|---|---|---|---|
| Sentence-length spread | std / mean of sentence lengths in words | 0.25 | 0.80 | 0.50 |
| Type-token ratio | unique words / words, first 100 words only | 0.55 | 0.85 | 0.25 |
| Punctuation density | `, ; : ( ) — – ! ? "` per word | 0.05 | 0.25 | 0.25 |

Higher `style_score` means more AI-like, the same direction as signal one. Fewer than two sentences returns 0.5 ("no evidence"). TTR is cut to the first 100 words because it falls as text gets longer.

**Why that might differ between human and AI writing:** Generated prose tends toward even, mid-length sentences and a narrower vocabulary. Human writing is lumpier, with a three-word sentence beside a forty-word one.

**What it can't see:** Meaning. Anything that changes shape without changing substance moves it: injected typos, chopped-up sentences, a pasted quotation. In the other direction, a human who writes evenly looks AI. It is also weak on very short text. The landlord piece is two sentences, so its spread is noisy, and it scored 0.73. On my four calibration inputs it separated plain human (0.67) from clearly AI (0.76) by only 0.09.

### The combining rule

**The rule:** Take the average of the two scores. But if the two signals differ by more than 0.35, they disagree, and I don't trust the average as a verdict. The score is then forced to stay inside the unsure band. Two methods splitting is uncertainty. This follows my design decision (DESIGN.md): neither signal alone should be enough to produce an AI label, and a split goes to "unsure".

**The numbers:**

| Setting | Value | Where |
|---|---|---|
| Weight on model signal | 0.5 | `config.WEIGHT_MODEL_SIGNAL` |
| Weight on style signal | 0.5 | `config.WEIGHT_STYLE_SIGNAL` |
| Disagreement gap | 0.35 | `config.DISAGREEMENT_GAP` |
| Disagreement range | `HUMAN_THRESHOLD + 0.01` to `AI_THRESHOLD - 0.01` (currently 0.36–0.64) | `scoring.py::combine_signals` |

Equal weights, because I couldn't justify either signal as more trustworthy: they fail on different inputs (see DESIGN.md).

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

The landlord piece ("ok so my landlord finally fixed the heater at 2am...") got `model_score` 0.081 (human) and `style_score` 0.734 (AI), a gap of 0.65. The model signal likes its odd, specific content. The style signal sees only two sentences and little punctuation, and calls it even and sparse. The average is 0.408, which is inside the unsure band, so the clamp changed nothing here. The result is unsure (0.41), not accused. The clamp matters when disagreeing signals average outside the band, for example model 0.90 and style 0.50 average 0.70 and would be capped at 0.64.

The same signals split on lightly-edited AI: model 0.333, style 0.708, combined 0.520. The model signal was fooled by the typo; style still saw even sentences. Averaging with the disagreement rule keeps it out of "human".

**Calibration run** (`python calibrate.py`):

| Input | model | style | combined |
|---|---|---|---|
| clearly AI | 0.890 | 0.764 | 0.827 |
| clearly human | 0.134 | 0.309 | 0.221 |
| plain human | 0.860 | 0.672 | 0.766 |
| lightly-edited AI | 0.333 | 0.708 | 0.520 |

Clearly-AI and clearly-human land 0.61 apart. **Known limit:** plain human writing scores 0.77 because both signals agree it looks AI. The combining rule can't catch that, since it only handles disagreement. Plain human text scores above the current AI threshold of 0.65, so this has to be handled through the thresholds and the label wording, not the combining rule. Raising `AI_THRESHOLD` far enough to clear it (about 0.80 or higher) also puts clearly-AI text (0.83) on the edge of the unsure band. That is the trade, and it gets decided when I set the thresholds.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | "We think this was probably written by a person. Our check is only a guess, but nothing in it stood out to us." |
| unsure | 0.35 – 0.65 | "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece." |
| high-confidence AI | 0.65 – 1.00 | "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look." |

The text lives in `scoring.py` (`LABEL_HUMAN`, `LABEL_UNSURE`, `LABEL_AI`) and is chosen by `scoring.py::score_to_label`. The ranges come from `config.HUMAN_THRESHOLD` and `config.AI_THRESHOLD`.

**Why I worded the "unsure" one this way:**
The person reading it may have written every word themselves, so it says plainly that the check couldn't tell and that this is common for human work. It ends by saying nobody has decided anything, so it can't be read as a verdict or an accusation. It never uses "score", "confidence" or "threshold".

**Why the AI label is hedged too:** my own calibration showed plain human writing scoring 0.77, above the AI threshold. So even the strongest label says "may have been" and tells the writer how to appeal, because a real writer will sometimes see it.



---

## Sample Run

**A submission**

All three labels were reached with real submissions. Commands were run in Windows PowerShell, so the JSON body is read from a file (`--data-binary "@file"`) to avoid quoting problems.

Plain human writing, which gets the AI label. This is the detector's known blind spot, and it is the case the appeal exists for:

```bash
$ curl.exe -s -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  --data-binary "@store.json"
# store.json: {"text": "I went to the store yesterday. The store was busy, so I waited in line for a while. Then I bought some milk and bread and went home.", "creator_id": "u1"}
```

```json
{
  "combined_score": 0.8047871527611741,
  "confidence": 0.8048,
  "content_id": "64d0d52a-092d-4c85-bdda-a50ccb6c85ef",
  "guess": "ai",
  "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
  "model_score": 0.8763,
  "style_score": 0.7332743055223481
}
```

The other two labels, from the log (the same route, the same response shape):

| Input | content_id | model | style | combined | guess |
|---|---|---|---|---|---|
| landlord piece, two sentences | `b30a7028-520f-4b6a-b398-6566851e5228` | 0.081 | 0.734 | 0.408 | unsure |
| landlord piece, full version | `f1e17c71-f3a3-41c5-b79f-eaa41f803d33` | 0.129 | 0.317 | 0.223 | human |

**An appeal**

The writer of the store piece says they wrote it themselves:

```bash
$ curl.exe -s -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  --data-binary "@appeal.json"
# appeal.json: {"content_id": "64d0d52a-092d-4c85-bdda-a50ccb6c85ef", "reasoning": "I wrote this myself. It is a plain description of a trip to the shop."}
```

```json
{
  "content_id": "64d0d52a-092d-4c85-bdda-a50ccb6c85ef",
  "message": "Thanks. Your appeal has been recorded and this piece is now under review. Nothing further is needed from you.",
  "status": "under_review"
}
```

An unknown `content_id` returns HTTP 404 (`not_found`), and a missing `reasoning` returns HTTP 400 (`bad_request`). Neither writes to the log.

**What the log shows afterwards**

```bash
$ curl.exe -s "http://127.0.0.1:5000/log?limit=6"
```

The original decision keeps `"status": "decided"`. The appeal is a second entry after it with `"status": "under_review"`. The first two entries have `"label": null` because they were logged before the label was wired in.

```json
{
  "count": 6,
  "entries": [
    {
      "combined_score": 0.8047871527611741,
      "content_id": "06f528e3-09e7-4d78-9235-c32e928d2c94",
      "creator_id": "u1",
      "guess": "ai",
      "label": null,
      "model_score": 0.8763,
      "status": "decided",
      "style_score": 0.7332743055223481,
      "timestamp": "2026-10-11T18:43:01+00:00"
    },
    {
      "combined_score": 0.40778749999999997,
      "content_id": "64f96da1-399a-4aba-8d4b-361515069193",
      "creator_id": "u2",
      "guess": "human",
      "label": null,
      "model_score": 0.0812,
      "status": "decided",
      "style_score": 0.734375,
      "timestamp": "2026-10-11T18:43:07+00:00"
    },
    {
      "combined_score": 0.8047871527611741,
      "content_id": "64d0d52a-092d-4c85-bdda-a50ccb6c85ef",
      "creator_id": "u1",
      "guess": "ai",
      "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
      "model_score": 0.8763,
      "status": "decided",
      "style_score": 0.7332743055223481,
      "timestamp": "2026-10-11T20:00:57+00:00"
    },
    {
      "combined_score": 0.40778749999999997,
      "content_id": "b30a7028-520f-4b6a-b398-6566851e5228",
      "creator_id": "u2",
      "guess": "unsure",
      "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
      "model_score": 0.0812,
      "status": "decided",
      "style_score": 0.734375,
      "timestamp": "2026-10-11T20:01:06+00:00"
    },
    {
      "combined_score": 0.22309161389045523,
      "content_id": "f1e17c71-f3a3-41c5-b79f-eaa41f803d33",
      "creator_id": "u3",
      "guess": "human",
      "label": "We think this was probably written by a person. Our check is only a guess, but nothing in it stood out to us.",
      "model_score": 0.1288,
      "status": "decided",
      "style_score": 0.3173832277809105,
      "timestamp": "2026-10-11T20:03:04+00:00"
    },
    {
      "content_id": "64d0d52a-092d-4c85-bdda-a50ccb6c85ef",
      "creator_id": "u1",
      "event": "appeal",
      "reasoning": "I wrote this myself. It is a plain description of a trip to the shop.",
      "status": "under_review",
      "timestamp": "2026-10-11T20:04:01+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1: the combining rule**

- *What I asked for:* A way to combine `model_score` and `style_score` into one number, with the requirement that neither signal alone should be enough to produce an AI label (my design decision in DESIGN.md).
- *What came back:* A weighted average of the two scores, using the placeholder weights in `config.py`.
- *What I changed:* I kept equal weights (0.5 each) because I couldn't justify trusting either signal more. I added a disagreement rule: if the scores differ by more than 0.35, the result is clamped to stay inside the unsure band (0.36-0.64). That rule is in `scoring.py::combine_signals`. I then tested it on the landlord piece (model 0.081, style 0.734, gap 0.65). The result was 0.41, unsure, instead of an accusation.

**Moment 2: calibration and the labels**

- *What I asked for:* Help judging whether my two signals separated human from AI text, and wording for the three labels that a writer with no technical background could read.
- *What came back:* Calibration numbers from `calibrate.py`, and a first set of label text.
- *What I changed:* The calibration showed my plain-human input scoring 0.77, above the 0.65 AI threshold, because both signals agree it looks AI. I did not accept that the combining rule could fix this. I wrote it up as a known limit in the README. I then reworded the labels. The AI label says "may have been" and tells the writer how to appeal. The unsure label says plainly that the check couldn't tell and that nobody has decided anything. Neither uses "score", "confidence" or "threshold".

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**
A real writer submits a few pieces an hour. Even a burst of revisions is rarely
more than two or three in a minute, so 5 per minute never gets in their way and
50 per day is far more than anyone submits honestly. A script mapping my
thresholds needs hundreds of variations to find where "unsure" flips to "ai".
The per-minute cap slows that to a crawl, and the daily cap limits it to 50
probes per identity per day. I didn't go lower than 5 because a writer who
pastes in a few drafts back to back shouldn't be locked out; I didn't go higher
because 10 per minute would give a script twice the probing rate for no benefit
to real users.

**What a caller counts as:** The `creator_id` in the request body, falling back
to the caller's IP address when there isn't one (`rate_limit_key` in `app.py`).
Keying on `creator_id` means one household sharing an address doesn't share a
limit. The weakness is that the caller chooses their own `creator_id`, so a
script can rotate IDs to get a fresh allowance each time. Counts are also held
in memory, so a restart resets every limit.

**The run of status codes when I pushed past it:**

`python run_attacks.py --flood 15` (15 submissions as `flood_tester`):

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

10 of 15 were rate limited. Each rejection was written to the audit log with
`event: "rejected"`, `reason: "rate_limited"` and the limit that was hit, so a
flood shows up in `GET /log` and not as a gap. Full output is in
`results/flood_2026-10-11_2009.md`.

---

## Attack Run — Before

56 attacks sent with `python run_attacks.py --set attacks --label before`
(full output: `results/attack_run_2026-10-21_2122_before.md`). No 5xx and no
crashes, so nothing was auto-marked broke. The verdicts below are mine.

**Rule I used:** an attack **broke** if it got what it was going for. AI text
not labeled "ai" counts as broke (an "unsure" is a partial evasion). Human text
labeled "ai" is broke. A score or label that moved because of an injected
instruction is broke. Junk input that got a verdict instead of a rejection is
broke. A clean 4xx or 429, or an unchanged label, is held.

**Count: 24 broke, 32 held (of 56).**

| Family | Broke | Held |
|---|---|---|
| Evasion (10) | 8 | 2 (EV04, EV10) |
| False positive (8) | 7 | 1 (FP08) |
| Prompt injection (6) | 3 (PI02, PI03, PI06) | 3 (PI01, PI04, PI05) |
| Malformed content (8) | 6 (MF03–MF08) | 2 (MF01, MF02) |
| Malformed requests (12) | 0 | 12 |
| Flood, one creator (12) | 0 | 12 |

| ID | What came back | Verdict | Why |
|---|---|---|---|
| EV01 | unsure 0.543 | broke | Typos dropped the model score to 0.16 on AI text |
| EV02 | unsure 0.567 | broke | Broken-up sentences hid AI text |
| EV03 | unsure 0.610 | broke | Pasted quotation hid AI text |
| EV04 | ai 0.681 | held | Unusual words did not get past it |
| EV05 | unsure 0.630 | broke | Heavy human edit pass |
| EV06 | unsure 0.547 | broke | Long plus short sentence |
| EV07 | unsure 0.543 | broke | Punctuation padding |
| EV08 | unsure 0.517 | broke | 11 words of AI-sounding text. Weakest call: "unsure" on 11 words is defensible, and I'd accept held here |
| EV09 | unsure 0.628 | broke | Human opening paragraph pulled an AI body from "ai" to "unsure" |
| EV10 | ai 0.924 | held | Repeated stanza structure was caught |
| FP01 | ai 0.652 | broke | Plain human writing accused |
| FP02 | ai 0.802 | broke | Formal human writing accused |
| FP03 | ai 0.795 | broke | Careful non-native English accused |
| FP04 | ai 0.756 | broke | Rubric student essay accused |
| FP05 | ai 0.873 | broke | Human technical docs accused, highest score of any false positive |
| FP06 | ai 0.742 | broke | Human imitating a template accused |
| FP07 | ai 0.722 | broke | Deliberate repetition accused |
| FP08 | unsure 0.547 | held | Very short human text, nobody accused |
| PI01 | unsure 0.581 | held | Label same as the no-injection control (unsure 0.502), but model score fell 0.754 to 0.463 |
| PI02 | human 0.706 | **broke** | Control was unsure 0.502 (model 0.754). Fake SYSTEM line cut the model score to 0.204 and flipped the label to human |
| PI03 | unsure 0.627 | broke | Control was ai 0.707. A "note to the reviewing system" moved it to unsure |
| PI04 | unsure 0.540 | held | Same label as control (unsure 0.503). `<script>` text only appears inside the escaped field |
| PI05 | unsure 0.531 | held | Log line is valid JSON with the real values, forged fields did not appear |
| PI06 | unsure 0.615 | broke | Control was ai 0.652. Same camping text as FP01, so here the injection happened to help a human |
| MF01, MF02 | 400 | held | Whitespace-only and one-character text rejected |
| MF03–MF07 | unsure 0.640 | broke | Control characters, punctuation, one long word, emoji and RTL script each got a verdict. Model score swung from 0.00 to 0.998 on nonsense |
| MF08 | ai 0.850 | broke | 60,000 characters accepted with no length cap |
| RQ01–RQ09, RQ12 | 400 | held | Clean rejections |
| RQ10, RQ11 | 429 | held | Rejected, but with a 429 not a 400. The rate limiter runs before validation |
| FL01_01–05 | 200 | held | Served inside the limit |
| FL01_06–12 | 429 | held | Limiter engaged after 5 requests |

**PI controls.** For each injection I resubmitted the real text without the
injected line (`creator_id` `piNN_control`) to see whether the line moved
anything.

| Attack | Control (no injection) | With injection |
|---|---|---|
| PI01, PI02 | unsure 0.502 (model 0.754, style 0.25) | PI01 unsure 0.581 / PI02 human 0.706 |
| PI03 | ai 0.707 | unsure 0.627 |
| PI04 | unsure 0.503 | unsure 0.540 |
| PI06 | ai 0.652 | unsure 0.615 |

The model service reads attacker-controlled text, so an instruction at the
top of a submission changes signal one's score even though nothing obeys it.



**Ten audit log entries from the run**

Chosen for the failures, not the easy holds: the highest false accusations
(FP05, FP03), the three injections that moved a label (PI02, PI03, PI06), two
evasions (EV01, EV09), two junk inputs that got verdicts (MF05, MF08), and the
log-injection attempt that stayed contained (PI05).

```json
{"timestamp": "2026-10-22T01:22:23+00:00", "content_id": "e049aec8-280a-4ba0-9fa0-00e1e6d7ee7f", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.9457949478769414, "combined_score": 0.8731474739384707, "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.", "status": "decided"}
{"timestamp": "2026-10-22T01:22:22+00:00", "content_id": "15fc30a9-5ee8-4e89-a6d0-a329388bd96b", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.7848428958333062, "combined_score": 0.7949714479166532, "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.", "status": "decided"}
{"timestamp": "2026-10-22T01:22:23+00:00", "content_id": "af7cca0f-36c0-4df8-b4d9-844a94c55d00", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.38469543943853013, "combined_score": 0.2945477197192651, "label": "We think this was probably written by a person. Our check is only a guess, but nothing in it stood out to us.", "status": "decided"}
{"timestamp": "2026-10-22T01:22:23+00:00", "content_id": "142ee3ca-0769-49d0-a1b2-8fcdb5ed29fb", "creator_id": "attacker_PI03", "guess": "unsure", "model_score": 0.5943, "style_score": 0.6597237642295337, "combined_score": 0.6270118821147669, "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.", "status": "decided"}
{"timestamp": "2026-10-22T01:22:24+00:00", "content_id": "76b8531d-510a-4f14-9f28-81bba5efc90a", "creator_id": "attacker_PI06", "guess": "unsure", "model_score": 0.5583, "style_score": 0.6723339886831252, "combined_score": 0.6153169943415626, "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.", "status": "decided"}
{"timestamp": "2026-10-22T01:22:19+00:00", "content_id": "da1f716e-4d2a-43a4-9a9b-78a296341212", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.75, "combined_score": 0.45675, "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.", "status": "decided"}
{"timestamp": "2026-10-22T01:22:21+00:00", "content_id": "841bfea2-4efc-426e-9162-a4bba46ed8cb", "creator_id": "attacker_EV09", "guess": "unsure", "model_score": 0.7042, "style_score": 0.5522397078131156, "combined_score": 0.6282198539065578, "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.", "status": "decided"}
{"timestamp": "2026-10-22T01:22:25+00:00", "content_id": "d1d92a9b-648d-4eb4-8aba-4d406d8a9665", "creator_id": "attacker_MF05", "guess": "unsure", "model_score": 0.9976, "style_score": 0.5, "combined_score": 0.64, "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.", "status": "decided"}
{"timestamp": "2026-10-22T01:22:28+00:00", "content_id": "e0eed6ae-750d-403b-9e94-13f97273709e", "creator_id": "attacker_MF08", "guess": "ai", "model_score": 0.9876, "style_score": 0.7130005277837119, "combined_score": 0.850300263891856, "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.", "status": "decided"}
{"timestamp": "2026-10-22T01:22:24+00:00", "content_id": "41a2fccc-9f92-42fe-b8cf-b3e8705b9d9c", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.29872316291724393, "combined_score": 0.46941158145862194, "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.", "status": "decided"}
```

Things the log shows: it records scores, label and status but not the
submitted text, so a decision can't be re-checked from the log alone. Rejected
requests (400 and 429) leave no entry, so the RQ10 and RQ11 rejections are
invisible in it. The log's `combined_score` and the response's `confidence`
differ for "unsure" results (PI05: 0.469 logged, 0.531 returned).

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03.** A person writing carefully in their second language was told "our
check thinks this may have been written with an AI tool", at 0.795, with both
signals agreeing (model 0.805, style 0.785). Both signals reward plain, regular
prose, which is what careful non-native writing looks like, so the service
penalises the writer for being careful. The label is polite and offers an
appeal, but the writer still has to prove their own work is theirs. FP05 scored
higher (0.873) but a technical writer can at least see why docs read as
templated. FP03 is the one where I'd have no good answer.



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing flagged as AI | ≤ 1 of 10 `ai` | 4/10 | 4/10 | 4/10 | MISSED |
| 2. Clearly-AI and clearly-human text score apart | mean `combined_score` gap ≥ 0.25 | 0.111 | 0.111 | 0.111 | MISSED |
| 3. All three labels reachable | `human`, `unsure`, `ai` each ≥ 3 of 15, every trial | 0 / 4 / 11 | 0 / 4 / 11 | 0 / 4 / 11 | MISSED |
| 4. Appeal recorded, decision kept | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 5. Empty text refused | 400 `invalid_input`, 3 of 3 | 3/3 | 3/3 | 3/3 | MISSED (400 every time, but the code is `bad_request`, not the `invalid_input` the target names) |

Criterion 3 cells read `human / unsure / ai`. All three runs for criteria 1, 2,
3 and 5 are the three trials of one `run_eval.py --label before` invocation
(`results/run_2026-10-12_1945_before.md`). Criterion 4 is three separate runs of
`appeal_check.py --label before` (`results/appeal_2026-10-12_1945_before.md`,
`..._1954_before.md`, `..._1956_before.md`).

**The three trials were identical.** Every score matched to the last decimal in
all three trials. GPT-2 runs in evaluation mode with no sampling, so the same
input gives the same perplexity every time. The runs were real re-runs. The model
signal here simply doesn't vary, so three trials add no run-to-run evidence.

**Criterion 2 numbers.** `run_eval.py` doesn't record `combined_score`, so the
gap is computed from `logs/audit.jsonl` (written by `audit.py::log_decision`).
Mean combined score: AI pieces 0.768, human pieces 0.658, gap 0.111.

**Criterion 5.** The status is 400 in every trial, but the error code returned
is `bad_request` (`app.py::submit`), not the `invalid_input` named in
`criteria.md`.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

**Criterion 1.** The four pieces of my own writing labelled `ai` (trial 1 of
`results/run_2026-10-12_1945_before.md`, produced by `run_eval.py::main`). They
are the work message, the daily routine, the advice to a new student and the
reason for my major. The other six came back `unsure`.

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6948,
    "model_score": 0.5632,
    "style_score": 0.826388888888889,
    "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Hi, I've updated the driver for the RAFT tool, and I'm checking if eve"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8,
    "model_score": 0.8723,
    "style_score": 0.7277952880949976,
    "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "My weekdays are usually pretty similar. I wake up, get ready, and go t"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8639,
    "model_score": 0.9091,
    "style_score": 0.8187962684875102,
    "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "My advice is to take advantage of the opportunities you have in colleg"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8657,
    "model_score": 0.9002,
    "style_score": 0.8312028546252666,
    "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "I've been interested in computers since I was young. At first, I mostl"
  }
]
```

**Criterion 2.** The 10 pieces of the spread scenario (5 AI, then 5 human), from
`logs/audit.jsonl`, written by `audit.py::log_decision` (selected fields). The
first five are the AI pieces.

```json
[
  {
    "creator_id": "eval_c2 score spr_1",
    "guess": "ai",
    "model_score": 0.8613,
    "style_score": 0.7435897435897436,
    "combined_score": 0.8024448717948718
  },
  {
    "creator_id": "eval_c2 score spr_2",
    "guess": "ai",
    "model_score": 0.8081,
    "style_score": 0.6875,
    "combined_score": 0.7478
  },
  {
    "creator_id": "eval_c2 score spr_3",
    "guess": "ai",
    "model_score": 0.8961,
    "style_score": 0.6849489795918368,
    "combined_score": 0.7905244897959184
  },
  {
    "creator_id": "eval_c2 score spr_4",
    "guess": "ai",
    "model_score": 0.7583,
    "style_score": 0.7375,
    "combined_score": 0.7479
  },
  {
    "creator_id": "eval_c2 score spr_5",
    "guess": "ai",
    "model_score": 0.8904,
    "style_score": 0.6147307761984235,
    "combined_score": 0.7525653880992118
  },
  {
    "creator_id": "eval_c2 score spr_6",
    "guess": "ai",
    "model_score": 0.5632,
    "style_score": 0.826388888888889,
    "combined_score": 0.6947944444444445
  },
  {
    "creator_id": "eval_c2 score spr_7",
    "guess": "unsure",
    "model_score": 0.3193,
    "style_score": 0.7168991082411456,
    "combined_score": 0.5180995541205727
  },
  {
    "creator_id": "eval_c2 score spr_8",
    "guess": "ai",
    "model_score": 0.8723,
    "style_score": 0.7277952880949976,
    "combined_score": 0.8000476440474988
  },
  {
    "creator_id": "eval_c2 score spr_9",
    "guess": "unsure",
    "model_score": 0.5435,
    "style_score": 0.7261149616915934,
    "combined_score": 0.6348074808457966
  },
  {
    "creator_id": "eval_c2 score spr_10",
    "guess": "unsure",
    "model_score": 0.8973,
    "style_score": 0.4620818369610723,
    "combined_score": 0.64
  }
]
```

**Criterion 3.** No piece returned `human`. The lowest-scoring of the 15, a
human-written piece, is the closest it got (`run_eval.py::main`, trial 1):

```json
{
  "status": 200,
  "guess": "unsure",
  "confidence": 0.5181,
  "model_score": 0.3193,
  "style_score": 0.7168991082411456,
  "label": "We can't tell whether this was written by a person or by an AI tool. Our check looked at it and came out unsure, which happens with plenty of work that people wrote themselves. No one has decided anything about this piece.",
  "sent": "Spent 2 hours fixing a bug today just to realize I broke it myself yes"
}
```

Across all 15 pieces in that trial: 0 `human`, 4 `unsure`, 11 `ai`.

**Criterion 4.** One of the 10 appeals (`appeal_check.py::main`, from
`results/appeal_2026-10-12_1945_before.md`), showing the original `decided` entry
and the `under_review` entry for the same `content_id`:

```json
{
  "submit_status": 200,
  "content_id": "c9ee80c7-8e4c-4fcd-b9bc-cb6766c53a5d",
  "appeal_status": 200,
  "appeal_response": {
    "content_id": "c9ee80c7-8e4c-4fcd-b9bc-cb6766c53a5d",
    "message": "Thanks. Your appeal has been recorded and this piece is now under review. Nothing further is needed from you.",
    "status": "under_review"
  },
  "has_decided": true,
  "has_under_review": true,
  "pass": true,
  "log_entries": [
    {
      "combined_score": 0.8024448717948718,
      "content_id": "c9ee80c7-8e4c-4fcd-b9bc-cb6766c53a5d",
      "creator_id": "eval_appeal_194535_1",
      "guess": "ai",
      "label": "Our check thinks this may have been written with an AI tool. It can be wrong, especially on plain or simple writing. If you wrote it yourself, you can appeal and a person will take a look.",
      "model_score": 0.8613,
      "status": "decided",
      "style_score": 0.7435897435897436,
      "timestamp": "2026-10-12T23:45:38+00:00"
    },
    {
      "content_id": "c9ee80c7-8e4c-4fcd-b9bc-cb6766c53a5d",
      "creator_id": "eval_appeal_194535_1",
      "event": "appeal",
      "reasoning": "I wrote this myself.",
      "status": "under_review",
      "timestamp": "2026-10-12T23:45:38+00:00"
    }
  ]
}
```

**Criterion 5.** Empty and whitespace-only text (`run_eval.py::main`, trial 1):

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "   "
  }
]
```

The response body from `app.py::submit` for an empty `text`:

```json
{
  "error": "bad_request",
  "message": "text is required"
}
```

## Diagnoses

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

**How each verdict was decided.** Each target was compared with the numbers in
all three trials, and it has to hold in every trial. The trials were identical
(see above), so no criterion is "met on some trials".

- **1. MISSED.** 4 of 10 of my own pieces came back `ai`, against a target of at
  most 1, in all three trials.
- **2. MISSED.** The gap in mean `combined_score` is 0.111 (AI 0.768, human
  0.658) against a target of at least 0.25.
- **3. MISSED.** `human` fired for 0 of 15 pieces, against at least 3 in every
  trial. `unsure` (4) and `ai` (11) cleared the bar.
- **4. MET.** 10 of 10 appeals left both the `decided` and `under_review` entries,
  in all three runs.
- **5. MISSED.** The target says 400 `invalid_input`. The status was 400 in 3 of 3,
  but `app.py::submit` returns the code `bad_request`. The criterion names the
  code, so the code is part of the target. I had first written this as "MET on
  status", which is the generous reading, so I changed it to MISSED.

**Misses 1, 2 and 3 are one problem: signal two (`stylometry.py::style_signal`)
barely separates AI from human text, and it sits high for both.** I measured it
on the 10 pieces of the spread scenario (`logs/audit.jsonl`) and the 10 of
criterion 1:

| | AI pieces (5) | my own pieces (10) | gap |
|---|---|---|---|
| `model_score` mean | 0.843 | 0.636 | 0.207 |
| `style_score` mean | 0.694 | 0.648 | 0.046 |

- **Stage and mechanism, miss 2 (signal two).** The style signal separates the
  groups by 0.046, so it adds almost nothing beyond the model signal. It cannot
  read, and short plain human writing looks like AI to it: even, mid-length
  sentences and a narrow vocabulary. Of my 10 pieces, 7 scored 0.58 or higher on
  style (0.83, 0.72, 0.73, 0.73, 0.82, 0.83, 0.59). I have not yet separated
  which of the three sub-measures (sentence spread, type-token ratio,
  punctuation) pushes them up. That is the next thing to test, so I am not
  claiming one.
- **Stage and mechanism, miss 2 (combining rule).** `scoring.py::combine_signals`
  weights the two signals 0.5 and 0.5. That gives the weak signal half of the
  vote, so the 0.207 gap in the model signal is cut to 0.111 in the combined
  score. A flat average assumes both signals are equally informative, and they
  are not.
- **Stage and mechanism, miss 1 (signal two and the combining rule).** Four
  pieces of mine were called `ai`: the work message (model 0.56, style 0.83), the
  daily routine (0.87, 0.73), the advice (0.91, 0.82) and my reason for my
  major (0.90, 0.83). Style is 0.73 or higher in all four, and in the work
  message it carries the piece alone: 0.56 on the model signal would be `unsure`,
  but the 0.83 style score lifts the average to 0.695, over the 0.65 line. Those
  are plain, short, conventional pieces, which is the writing the model signal
  also misreads (low perplexity), so both signals fail together. The disagreement
  rule did not catch these because the gap is 0.26, below the 0.35 trigger. My
  design said neither signal alone should be enough for `ai`, and the style
  score alone was enough here.
- **Stage and mechanism, miss 3 (label mapping, caused upstream).**
  `scoring.py::score_to_label` calls `human` only at 0.35 or below. The lowest
  combined score of any of my pieces was 0.384 (model 0.46, style 0.30), just
  over the line, and the next lowest was 0.455. Reaching 0.35 needs both signals
  low at once, and style is low (under 0.35) for only one of the 10 pieces. The
  mapping is not broken. The human mean combined score (0.658) sits on the 0.65
  `AI_THRESHOLD`, and the human cutoff is out of reach for the same reason:
  signal two reads human text as AI-ish, so scores bunch between 0.38 and 0.9.
  (This also corrects the Criterion 3 note above, which calls 0.518 the lowest
  score. 0.518 is the lowest model score, not the lowest combined score.)
- **Stage and mechanism, miss 5 (the route).** `app.py::submit` rejects empty text
  correctly but returns `"error": "bad_request"`. This is a naming mismatch, not
  a logic fault. The fix is the string, in the route.

**Where it points.** Signal two is in all three of the score-based misses (1, 2
and 3), so the first fix target is the style signal's ramps in `config.py`
(`SPREAD_AI_HUMAN`, `TTR_AI_HUMAN`, `PUNCT_AI_HUMAN`), or its weight in
`combine_signals`. The route error code is an unrelated one-line fix.

**Targets: were they too low?** No. They were not met, so none was too easy.
The criterion I would tighten next is 3: it asks only for 3 of 15 per label, and
the 5 borderline pieces are not scored by it, so a service could pass while
sending every human piece to `unsure`. I am not revising any criterion in this
unit: all five were measurable, and I missed them. Lowering a number I missed
would not be a revision.

**Attacks.** The before run exists (`results/attack_run_2026-10-21_2122_before.md`,
24 broke). The per-attack diagnoses (stage and mechanism) are still to be
written here.



---

## The Improvement

**What I changed:** One edit in `config.py`: the signal weights went from
`WEIGHT_MODEL_SIGNAL = 0.5` / `WEIGHT_STYLE_SIGNAL = 0.5` to `0.8` / `0.2`.
Thresholds, disagreement gap, style ramps and the route's error code were left
alone. The signal scores are identical before and after (GPT-2 is deterministic,
e.g. EV01 is model 0.1635, style 0.75 in both runs), so every difference below
comes from the weights.

**Which diagnosis pointed at it:** Miss 2, combining rule. Style separates AI
from human by 0.046 and the model signal by 0.207, but a flat 0.5/0.5 average
gave the weak signal half the vote and cut the combined gap to 0.111.

**Prediction written before the run:** gap about 0.175 (0.8 × 0.207 + 0.2 × 0.046);
criterion 1 from 4 to about 3; `human` still not reached; injection attacks
possibly worse because the model signal, which injected text moves, now counts
for more.

### Criteria — before and after

| Criterion | Target | Before | After | Verdict |
|---|---|---|---|---|
| 1. My own writing flagged as AI | ≤ 1 of 10 `ai` | 4/10 | 3/10 | MISSED |
| 2. Clear AI vs clear human apart | gap ≥ 0.25 | 0.111 | 0.197 (AI 0.813, human 0.616) | MISSED |
| 3. All three labels reachable | each ≥ 3 of 15 | 0 / 4 / 11 | 0 / 5 / 10 | MISSED |
| 4. Appeal recorded, decision kept | 10 of 10 | 10/10 | 10/10 | MET |
| 5. Empty text refused | 400 `invalid_input` | 400 `bad_request` | 400 `bad_request` | MISSED (untouched) |

After run: `results/run_2026-10-23_2040_after.md` (criteria 1, 2, 3, 5, three
identical trials) and `results/appeal_2026-10-23_2041_after.md` (criterion 4).
Criterion 2 is computed from `logs/audit.jsonl`, as before. Criterion 1 `ai`
pieces were numbers 3, 7 and 9; the work message moved from `ai` (0.695) to
`unsure`.

### Attack Run — After

56 attacks sent with `python run_attacks.py --set attacks --label after`
(full output: `results/attack_run_2026-10-23_2040_after.md`). No 5xx and no
crashes. Same verdict rule as the before run.

**Count: 22 broke, 34 held (of 56). Before: 24 broke, 32 held.**

| Family | Broke before | Broke after |
|---|---|---|
| Evasion (10) | 8 | 8 (EV01–EV08) |
| False positive (8) | 7 | 6 (FP02–FP07) |
| Prompt injection (6) | 3 | 2 (PI02, PI03) |
| Malformed content (8) | 6 | 6 (MF03–MF08) |
| Malformed requests (12) | 0 | 0 |
| Flood, one creator (12) | 0 | 0 |

Rows whose verdict changed:

| ID | Before | After | Verdict change |
|---|---|---|---|
| FP01 | ai 0.652 | unsure | broke → held |
| EV09 | unsure 0.628 | ai 0.674 | broke → held |
| PI06 | injected `unsure`, control `ai` | injected `unsure`, control `unsure` | broke → held |
| EV04 | ai 0.681 | unsure 0.639 | held → **broke** |
| EV05 | unsure | human (combined 0.341) | still broke, now reads as human |
| PI02 | human, combined 0.295 | human, combined 0.240 | still broke, further from its control |

A diff of the two result tables shows exactly four labels changed (EV04, EV05,
EV09, FP01). PI06's label is `unsure` in both runs; its verdict changed because
its control moved. The after-state PI controls were **recomputed from the saved
signal scores** under the new weights, not re-run live (PI02 control 0.64
`unsure`, PI03 control 0.743 `ai`, PI06 control 0.632 `unsure`). PI02 and PI03
still change the label against their controls.

**Did it help, and how do I know:** A little, and it fixed no criterion.
Attacks that broke fell from 24 to 22 (three gained, one lost), the criterion 2
gap rose from 0.111 to 0.197 (target 0.25), and criterion 1 went from 4 to 3
of 10 (target 1). The trade is that I now trust the model signal more, so its
errors count more. EV04 was caught before only because its style score (0.75)
pulled the average over 0.65, and with style at 0.2 it slips to `unsure`.
EV05 (heavy human edit of AI text) now comes back `human`, and PI02's
injection pushes the score further toward `human`. FP02–FP07 and the junk
inputs did not move, because the model signal itself calls them AI. The
remaining problem is the model signal, and reweighting cannot fix that.


---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
