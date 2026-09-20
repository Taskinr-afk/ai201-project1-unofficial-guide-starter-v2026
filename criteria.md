# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** Four of my five questions point at a fact that lives in
exactly one document with the subject in its title line — the pass/fail
deadline, the Old Brewhouse laundry times, the CS 210 workload, the Kestrel
Commons lunch wait — so retrieval only has to land on an obvious match. The
fifth is the Fenwick Court shuttle question, and I expect that one to miss:
`campus_life` has three documents with "Fenwick Court" in the name (the hall,
its laundry, its noise) and the shuttle fact is one clause buried in
`transit_shuttle.txt`, which never says "Fenwick" in its title. Those three
decoys should crowd out the one chunk that actually answers it. I set 4 of 5
rather than 5 of 5 because I'd rather name the question I think is hard than
pretend all five are easy — and rather than 3 of 5, because a second miss
would mean something is wrong with retrieval, not with one awkward question.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** All five and not four, because nothing here depends on
luck. There are only two ways out of `app.py ask`: the gate refuses before the
model is ever called, or `answer_from_chunks` runs with a prompt that labels
every excerpt `[from <filename>]` and a system instruction that says to name
the file. The retrieved chunks are also printed with their sources regardless
of what the model writes. So the only way to miss this is for the model to
ignore a direct instruction while the filenames sit in its context — a real
failure, not an unlucky one. If it happens even once I want it to count
against me.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:** Four of the five `OUT_OF_SCOPE` questions are from
domains my corpus has no vocabulary for at all — Mongolia, diesel engines, the
1994 World Cup, Rust for loops — so their nearest chunk should be far away and
easy to cut off. The fifth is the ibuprofen dosage question, and that one
worries me: `health_center.txt` is in the corpus and talks about walk-in hours
and urgent problems, so a medical question has something to be near without
having anything to be answered by. That is exactly the kind of near-miss that
sits on the wrong side of a single global cutoff. One allowed failure is for
that question. I'll record the actual distance spread when I set the cutoff in
Milestone 4 and note here whether the two groups separated cleanly or
overlapped.

---

## 4. Chunks stand on their own

For 5 sampled chunks: none begins or ends mid-sentence, and each one names its
own subject — the hall, course, dining hall, or office it is about — inside
the chunk text, without relying on a neighbouring chunk. Target: 5 of 5 on
both.

**Why this target:** When I read the documents in Milestone 1, almost every
one of them opens with a title line that is the only place the subject is
named — "Laundry in Old Brewhouse", "Workload for CS 210 Data Structures" —
and then switches to bare pronouns: "the machines are old", "it's
front-loaded". The corpus also has near-identical documents for eight housing
buildings and eight dining halls, so a chunk that says "best time is Tuesday
or Wednesday morning" without the building name is not just vague, it is
genuinely ambiguous between eight buildings and will be retrieved for the
wrong one. That makes subject-naming the thing worth counting here, more than
chunk length. I set 5 of 5 rather than 4 of 5 because the documents average
around 300 characters — most of them should fit in one chunk and keep their
title line for free, so even one orphaned chunk means my split is cutting in
the wrong place.

---

## 5. The named source is the right source

For all 5 of my test questions, the document the answer names is a document
that actually contains the fact stated in the answer, checked by reading the
file. Target: 5 of 5.

**Why this target:** Criterion 2 only asks whether a source is printed, and a
confidently wrong citation passes it. That is the failure I actually care
about, because the whole promise of this system is "here is where I got it"
— an answer with the wrong filename attached is worse than no answer, since
someone would go read the wrong document and trust it. My corpus gives the
model plenty of chances to get it wrong: the dining halls each have a `_followup.txt`
that repeats the same figures as the main file, and five chunks go into every
prompt, so the model has several plausible-looking files to pick from and only
some of them say what it just said. I set 5 of 5 because, unlike retrieval, there is no hard case here — every
filename is sitting in the prompt right next to the text it belongs to, so
attaching the wrong one is a grounding failure, not bad luck.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
