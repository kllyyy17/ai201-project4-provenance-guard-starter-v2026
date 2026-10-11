# Provenance Guard: Milestone 1 design (written before any code)

## 1. The path a submission takes

1. **Client → `POST /submit`** (`app.py::submit`). Arrives as JSON `{text, creator_id}`. The route checks the input is usable (object, `text` is a non-empty string under a length cap, `creator_id` is a non-empty string). Bad input is refused with a 400 and logged as a rejection. Adds: nothing yet, but nothing malformed goes further.
2. **Identity** (`app.py`). Generates a `content_id` (uuid). Adds: the handle that `/appeal` and the audit log use to refer to this decision.
3. **Signal one** (`detector.model_signal`). A local GPT-2 reads the first ~400 tokens and returns `model_score`, 0–1, higher means more AI-like. Adds: a judgement of how *predictable* the text is.
4. **Signal two** (`stylometry.style_signal`). Measures sentence-length spread, type-token ratio and punctuation density, returning `style_score`, 0–1, same direction. Adds: a judgement of the text's *shape*, independent of meaning.
5. **Combine** (`scoring.combine_signals`). Merges both into `combined_score`, 0 (human) to 1 (AI). Adds: one number, and the place where the "which way do we err" decision lives.
6. **Label** (`scoring.score_to_label`, thresholds in `config.py`). Maps the score to `guess` (`human` / `unsure` / `ai`) plus a plain-English `label` sentence, and derives `confidence`. Adds: what the reader actually sees.
7. **Log, then respond** (`audit.log_decision`, then the JSON response). Writes all nine fields (`status: decided`) before replying, then returns the decision with both signal scores. Adds: the audit trail. If the writer disagrees, `POST /appeal` takes the `content_id`, checks it exists, calls `audit.log_appeal` (`status: under_review`) and confirms.

## 2. The two signals

### Signal one: model signal (`detector.py`, given)

- **Measures:** how predictable the text is to GPT-2 (low perplexity means high predictability).
- **Why it might differ:** a language model produces the likely next word, so its output tends to be highly predictable to another language model. People reach for surprising words and odd turns more often.
- **Blind spot:** predictability is not authorship. Plain writing in common words and short sentences scores machine-like however it was produced. That means second-language writers, younger writers and anyone deliberately writing simply. Dense, ornate prose goes the other way and reads as human, so AI text prompted to be flowery slips through. It also only reads the first ~400 tokens, so the rest of a long piece is never seen.

### Signal two: style signal (`stylometry.py`, mine)

- **Measures:** the shape of the text with no understanding: sentence-length variation (std/mean), vocabulary repetition (type-token ratio) and punctuation density and variety (semicolons, dashes).
- **Why it might differ:** generated prose leans to even, mid-length sentences and a narrower vocabulary. Human writing is lumpier, with a three-word sentence beside a forty-word one.
- **Blind spot:** it cannot read. Anything that changes shape without changing substance moves it: injected typos, chopped-up sentences, a pasted quotation, an AI draft lightly edited. Going the other way, a human who writes evenly (a formal or templated style) looks AI. Very short texts give unstable numbers (one sentence has no spread at all), and type-token ratio falls as length grows.

**Why two signals:** they fail on different inputs. Plain human writing fools signal one but may still have lumpy sentences. Typo-laden AI fools signal two but is still predictable to signal one. Disagreement between them is itself a reason to say "unsure".

## 3. Tracing the false positive

A real writer, a second-language English speaker, submits a plain, honest poem in simple common words and short sentences.

- **Signal one** finds it very predictable: `model_score` ≈ 0.85.
- **Signal two** sees even sentence lengths and little punctuation variety: `style_score` ≈ 0.70.
- **Combined** ≈ 0.78. With the placeholder thresholds (AI above 0.65) the label would be "high-confidence AI". That is exactly the wrong outcome for this person, and the one with the least room to argue back.
- **What the label says to them:** "We think this was written by AI." They are accused on the strength of two measures that both share the same weakness for plain writing.
- **What they can do:** `POST /appeal` with `content_id` and their reasoning. The item moves to `under_review` and the original decision stays in the log beside the appeal.

**What this decides for Milestone 4/5:**

- The AI threshold must be high enough, and the unsure band wide enough, that the scores plain human writing gets land in "unsure" rather than "ai". I accept that more AI text gets through as "unsure" and will say so openly.
- The "unsure" label must read as "we can't tell", never as an accusation, because the person reading it very likely wrote every word.
- The "ai" label must never state certainty ("probably", not "is"). It must always tell the writer how to appeal.
- Because both signals are fooled by the same writers, the combining rule should not let a high score from signal one alone push a piece into "ai". Something like requiring both to agree for the AI label, and letting disagreement fall to "unsure".
- Appeal must always work and always confirm, since it is the only recourse a wrongly accused writer has.

## 4. Endpoint contracts

All bodies are JSON (`Content-Type: application/json`). All errors share one shape: `{"error": "<machine_code>", "message": "<sentence for a human>"}`.

### `POST /submit`

**Request**

| Field | Type | Required | Rules |
|---|---|---|---|
| `text` | string | yes | Non-empty after trimming; max 20,000 characters |
| `creator_id` | string | yes | Non-empty after trimming; opaque to us, the site's own user id |

**Response `200`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Unique id for this decision. Pass it to `/appeal` |
| `guess` | string | `"human"`, `"unsure"` or `"ai"` |
| `confidence` | number 0–1 | How strongly the evidence backs `guess`: for `ai` it is the combined score, for `human` it is 1 − score, for `unsure` it is the combined score's distance-from-the-middle mapped to a low value. It is *not* the probability the writer cheated |
| `label` | string | The plain-English sentence a reader sees. No numbers or jargon |
| `model_score` | number 0–1 | Signal one, higher means more AI-like |
| `style_score` | number 0–1 | Signal two, same direction |
| `combined_score` | number 0–1 | Output of `combine_signals`, 0 human, 1 AI |
| `status` | string | `"decided"` |

**Errors**

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_input` | Body isn't a JSON object, `text` or `creator_id` is missing, not a string, or blank, or `text` is too long. `message` says which |
| 429 | `rate_limited` | Unit 8 |
| 503 | `detector_unavailable` | The local model isn't downloaded or failed to load |

Every outcome, including 400s, leaves a line in the audit log.

### `POST /appeal`

**Request**

| Field | Type | Required | Rules |
|---|---|---|---|
| `content_id` | string | yes | Must exist in the audit log |
| `reasoning` | string | yes | Non-empty after trimming; the writer's own words |

**Response `200`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Echoed back |
| `status` | string | `"under_review"` |
| `message` | string | Confirmation for the writer, e.g. "Thanks. A person will look at this. Your original submission is unchanged." |

**Errors**

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_input` | Body isn't an object, or `content_id` / `reasoning` is missing or blank |
| 404 | `unknown_content_id` | No decision with that id. This must be loud, never a silent success |

Appealing the same item twice is allowed. It adds another appeal entry and returns the same 200. The log is append-only, so the original decision is never overwritten.

### Read-back test

Could someone build a client against this without asking me anything? They know every field name and type, the score direction (higher means more AI), the fact that `confidence` is not a probability of guilt, what each status code means, and where the `content_id` for an appeal comes from. One thing I had to pin down: the `unsure` case for `confidence`. I will fix the exact formula in Milestone 5 and record it in the README. Until then the contract only promises 0–1, higher means more evidence for `guess`.
