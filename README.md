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

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->



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

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



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
