# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Human writing is rarely accused

Of 10 human-written pieces, at most 1 gets `guess: "ai"`.

**Why this target:** On a writing site a wrong accusation costs the writer far
more than a missed detection costs the site, so 1 in 10 is the most I will
accept.

---

## 2. Clearly-AI and clearly-human text score apart

The mean `combined_score` of 5 AI-generated pieces is at least 0.25 higher than
the mean of 5 human-written pieces.

**Why this target:** If the two groups score close together, any threshold is
arbitrary. 0.25 is a quarter of the scale, which is enough for the labels to
mean something without demanding more than two weak signals can give.

---

## 3. All three labels are reachable

Submitting 15 pieces through `/submit` (5 AI-generated, 5 human-written, and 5
borderline) returns each of `human`, `unsure` and `ai` for at least 3 of the 15 pieces, in every trial.

The 5 borderline pieces are chosen by origin, not by score: 3 AI-written
pieces I edited by hand, and 2 mixed pieces (half mine, half AI). The same 15
pieces are used in every trial.

**Why this target:** A label that can never fire is a lie in the interface, and
`unsure` is the label my design relies on to protect plain-writing humans.
`ai` is the hardest to reach, because my design requires both signals to agree.

---

## 4. An appeal is recorded without overwriting the decision

After `POST /appeal` on a valid `content_id`, the audit log holds both the
original `decided` entry and a new `under_review` entry for that id, and this
is true for 10 of 10 appeals.

**Why this target:** The appeal is the only recourse for a wrongly labelled
writer, so there is no acceptable failure rate. The log is append-only so the
original decision stays visible beside the appeal.

---

## 5. Empty text is refused

A `POST /submit` with `text` set to an empty string or only spaces returns 400
`invalid_input` in 3 of 3 tries, never a 200 or a 500.

**Why this target:** An empty string gives my style signal nothing to measure
(it falls back to 0.5, "no evidence") and my model signal nothing to read, so
any score would be invented and could still land on a label a writer could be
held to. Refusing it with a 400 is the only honest answer, and 3 of 3 is the
bar because there is no input where a made-up label is acceptable.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
