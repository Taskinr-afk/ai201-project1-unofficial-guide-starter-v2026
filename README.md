# The Unofficial Guide

Taskin Rahman - corpus: `campus_life`

---

# Unit 1

## What This Does

This is a question answering system built on `campus_life`, a corpus of 88
short student posts about one university. The posts cover dining halls, dorm
buildings, courses and the administrative rules nobody explains properly,
written the way students actually talk about them rather than the way a course
catalog would.

You ask it a plain question like "when is the best time to do laundry in Old
Brewhouse" or "how many hours a week does CS 210 take" and it finds the
closest chunks of text, answers from those alone, and names the file it used.
If nothing close enough comes back it says it does not have enough information
instead of guessing.

It handles specific questions about a named thing well, since almost every
fact in this corpus lives in one short post. It handles comparisons between
two buildings or two dining halls less well, because that needs two documents
at once and the system was not built for it.

## Chunking Strategy

**Chunk size:** 300 characters, as a target rather than a hard limit. A chunk
closes once adding the next paragraph would take it past 300, and it never
cuts inside a paragraph.

**Overlap:** none, except that every chunk repeats its document's title line.

The starter cuts at 800 characters and my longest document is 549, so it never
cut anything and I got 88 chunks out of 88 documents. My documents average 317
characters.

I split them because some posts hold two unrelated things. The Kestrel Commons
post covers wait times in one paragraph and then opening hours in the next, so
a question about closing time was matching a chunk that was half about salad
bars.

I copy the title line onto every chunk because that is the only place these
documents name their subject. After the first line they switch to words like
"the machines are old". My corpus has eight housing buildings and eight dining
halls that read almost identically, so a chunk about laundry with no title on
it could belong to any of them.

Chunks only break at blank lines, so nothing starts or ends mid sentence.
Anything under 120 characters gets merged back into the chunk before it so I
never get a stray fragment.

This gave me 99 chunks instead of 88, averaging 285 characters. Only 11 of my
88 documents were long enough to split.

## Sample Chunks

The five that `python app.py chunks -n 5` printed. Chunks 4 and 5 are numbered
`#1`, which means their document was split, and both still name their subject
in the first line.

**Chunk 1**, from `admin_add_drop_deadline.txt#0`, produced by `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2**, from `course_biol_160_exams.txt#0`, produced by `chunker.py::split_documents`

```
BIOL 160 Cell Biology — assessment

Four unit tests and a cumulative final. Not curved.

The unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3**, from `course_math_220.txt#0`, produced by `chunker.py::split_documents`

```
MATH 220 Linear Algebra

I lived here my sophomore year. Format is chalk-and-talk lecture, weekly problem sets marked for correctness. Assessment: two midterms and a cumulative final. Curved to a b- median.

Expect 6 to 8 hours a week, almost all of it on problem sets.

The one piece of advice: the problem sets are the course; the lectures make sense afterwards rather than during.
```

**Chunk 4**, from `dining_the_atrium_followup.txt#1`, produced by `chunker.py::split_documents`

```
Re: The Atrium

Also worth saying: picked clean by 1:15 and not restocked again until the next morning. Nobody tells you this at orientation.
```

**Chunk 5**, from `housing_innisfree_hall.txt#1`, produced by `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

**Question:** If I live in Fenwick Court, is the campus shuttle reliable?

**Answer:**

```
  retrieved 4 chunks
  (best distance 0.393, cutoff 0.75)

If you live in Fenwick Court, the campus shuttle stop outside your building
is the one that gets skipped when the driver is behind schedule
(transit_shuttle.txt). Additionally, the published timetable is optimistic by
about five minutes in the morning (transit_shuttle.txt).

Source: transit_shuttle.txt

Sources retrieved: housing_fenwick_court.txt, housing_fenwick_court_noise.txt,
transit_shuttle.txt, transit_walking.txt
```

I picked this one because I wrote it in Milestone 2 expecting it to fail. The
fact that answers it is one clause buried in a document about shuttles, and
three other documents have Fenwick Court in the filename, so I thought those
would crowd it out. It came back at rank 1 instead. Splitting
`transit_shuttle.txt` on its paragraph break put the Fenwick sentence in a
chunk of its own, which is the chunker from Milestone 3 fixing a problem I had
written down before I built it.

**My relevance cutoff:** 0.75

My five questions came back between 0.180 and 0.393. The five in
`OUT_OF_SCOPE` came back between 0.825 and 0.934. That is a gap of 0.43 with
nothing at all inside it, so almost any number in the middle would pass both
tests and the midpoint of 0.61 looked like the obvious answer.

I went higher than that because my five questions are not what a real student
types. I wrote them knowing what was in the corpus, so they use the same words
the documents use. When I tried vaguer versions, "is the food any good" came
back at 0.656 and "do i need a car here" at 0.718, both with the right
document at rank 1. A cutoff of 0.6 refuses both of those. 0.75 answers them
and still sits 0.075 below the nearest out-of-scope question.

What I get wrong at 0.75 is near misses, meaning questions about campus that
my documents happen not to answer. "Is there a gym on campus?" comes back at
0.570 and gets through the gate. The grounding instruction has to catch those,
and when I tested it, it did, but that is the model's judgement rather than my
code's and it is the part I would test hardest in unit 2.

| Question | In corpus? | Best distance |
|---|---|---|
| How late in the term can I declare a course pass/fail, and what grade counts as a pass? | yes | 0.221 |
| How long is the lunch wait at Kestrel Commons between 12:15 and 1:00? | yes | 0.180 |
| When is the best time to do laundry in Old Brewhouse? | yes | 0.325 |
| How many hours a week outside class does CS 210 take? | yes | 0.300 |
| If I live in Fenwick Court, is the campus shuttle reliable? | yes | 0.393 |
| What is the capital of Mongolia? | no | 0.825 |
| How do I change the oil in a diesel engine? | no | 0.934 |
| Who won the 1994 World Cup? | no | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.849 |
| How do I write a for loop in Rust? | no | 0.891 |

**Top-k:** left at 5. The document holding the answer came back at rank 1 for
all five of my questions, so pulling back fewer would not have lost anything
and pulling back more would only add near identical documents about other
buildings.

**Grounding:** I added two rules to `GROUNDING_INSTRUCTION` in `generate.py`.
The first tells the model to name only the excerpt the fact came from, because
my corpus pairs most dining halls with a followup document that repeats the
same numbers, and criterion 5 is about citing the right file rather than just
citing something. The second tells it not to name a source when it is
refusing. The first one works. The second one gets ignored about half the
time, which is worth knowing.

## How I Used AI

**1. Designing the chunker.** I asked Claude what to do about chunking, given
that the starter had produced 88 chunks from 88 documents and never cut
anything. It suggested splitting on paragraph breaks, and then pointed out the
problem with doing that here, which is that my documents name their subject
only in the title line and then switch to "the machines are old". With eight
near identical laundry documents in the corpus, a split chunk would be
ambiguous between eight buildings. It gave me the choice of splitting with the
title copied onto every chunk or leaving one post as one chunk, and I chose to
split. I also made it measure my documents before picking a number, which is
where 300 came from rather than a round 500.

**2. Setting the relevance cutoff.** I asked where the cutoff should go given
my two groups of distances. The first answer pointed at the midpoint of my gap,
0.61, which is almost exactly the starter's default. That was not the number I
kept. Testing vaguer questions than the five I had written showed that "is the
food any good" comes back at 0.656 and "do i need a car here" at 0.718, both
with the correct document at rank 1, so a cutoff of 0.6 would refuse questions
it could answer. The cutoff went to 0.75.

I also had Claude draft the write ups in this README and cut most of them back.
The chunking section came back with a comparison table, a paragraph on what
might be wrong with my numbers, and an explanation of the option I did not
take. I removed about two thirds of it, because the milestone asks for the
size, the overlap and the reason, and the rest was padding.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
