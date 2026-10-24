# Week 5 — The ETL Process

Datasets and assignments for Week 5.

← [Back to the course index](../README.md)

| Lecture | Topic | Outcome | CLO | 3C |
|---|---|---|---|---|
| **L9** | Extract, transform, load — and what each stage guarantees | Formulate structured ETL workflows and identify where each stage fails | CLO3 | Competence |
| **L10** | Power Query, live | Build reusable transformation steps that clean, restructure and load dimensional data | CLO3 | Courage |

## The case

A commercial bank pulls a regional currency-dealing log every night at 02:00 —
one file per region, written by a system nobody at the bank controls. By 08:00
the treasury desk needs one number on screen.

Last night the file came in with eleven empty rows, branch codes typed as
`LHR-04`, `lhr-04` and `Lhr 04`, and amounts carrying thousands separators and a
stray en-dash where a minus sign belonged. **The load did not fail. It
succeeded, partly.** At 08:00 the desk read a position short by one region and
spent the morning trading against it. Nobody was told, because nothing crashed.

Then the same story in your own data. **Week 2** opened three PakFreight files,
fixed them by hand, and pasted the result into one sheet — a correct table and
zero reusable work. **Week 4** wired an empty star and left it waiting.

This week those two halves meet: you build the machine that loads the star. The
deliverable is **not the table** — Week 2 already produced the table. It is the
**seventeen steps, in order, with their names on them**, and the test of it is
that tomorrow night it runs without you.

No setup needed — the data is already in `assignments/data/`.

## Contents

| Path | What it is |
|---|---|
| `assignments/TASKS.md` | Seven tasks, the rules and the marking guide |
| `assignments/PowerQuery_Lab_Guide.md` | The hands-on lab: nine steps, the M code for all three queries, the refresh test, definition of done, troubleshooting — **plus a Python appendix** with the whole pipeline in pandas |
| `assignments/data/PakFreight_W5_ETLLab_STUDENT.xlsx` | **Start here.** All seven tasks; cream cells to fill |
| `assignments/data/source/*` | **The three dirty files, unmodified.** 37 rows, ten defects. The input |
| `assignments/data/source/night2/*` | **The refresh test.** Same marine and rail; a road file your pipeline has never seen |
| `assignments/data/dims/*.csv` | The five dimensions from the Week 4 star. Import them; do not rebuild them |
| `assignments/data/alias_lookup.csv` | The 23-row alias map, to **check** your own against — not to import |

`FactShipment.csv` is deliberately **not** here. Week 4 handed it over as a
starting point; this week it is the finish line.

> The teacher key is **not** in this repository, and `.gitignore` blocks
> `*TEACHER*`, `*_KEY*` and `*ANSWER*` from ever being committed here.

## Assignments

| Task | Covers | Marks |
|---|---|---|
| 1 | Defect census: ten defects, each tied to a step and to loud or quiet | 12 |
| 2 | Stage ownership: twelve activities, and the four that are violations | 12 |
| 3 | **Order the seventeen steps,** and defend the three constraints | 20 |
| 4 | Row arithmetic: 37 → 35 → 34, and every wrong total read from its gap | 15 |
| 5 | The locale trap: twelve date strings, two locales | 12 |
| 6 | Loud or quiet: six failures, and the check that converts each | 12 |
| 7 | **Definition of done.** Eight checks, all eight must pass | 12 |
| lab | **Hands-on:** rebuild the Week 2 merge as a pipeline that reruns | — |

Full briefs in [`assignments/TASKS.md`](assignments/TASKS.md).

**Timing:** T1–T4 in a 180-minute session, T5–T7 as homework. In a 120-minute
session, stop after T3 and set T4 as homework too — but do not cut T3, and do
not cut the paper design that feeds it.

## The pipeline you are building

```
  THREE SOURCES              STAGING                   THE STAR
  (read-only)                (never user-facing)       (everybody)

  marine .csv  ──┐        E1-E3  land, log            DimDate   28
  road   .csv  ──┼──────► T1-T7  per source   ──────► DimCity   15
  rail   .xlsx ──┘        T8-T10 once, combined       DimMode    4
                                                      DimStatus  4
  37 rows                 35 appended                 DimRoute  21
  10 defects              34 after dedup              FactShipment 34
```

**Shape, then text, then type, then keys.** Four words in that order will get
you through most of the lab and most of the midterm practical.

**Power Query or Python — your choice, same marks.** Deck slides 33–37 are a
Python track and the lab guide has a pandas appendix. Every number you have to
hit is identical, because the defects are facts about the data and not about
the tool. The trade-offs, and the four things required in place of named
applied steps, are in [`assignments/TASKS.md`](assignments/TASKS.md).

Three stages, three responsibilities, and the part that gets skipped is what
each one **must not** do: extract must not clean, transform must not write to
the source, load must not decide anything.

## Expected results

Every figure below was verified against the source data before this brief was
written. T7 checks all of them for you.

| Check | Expected |
|---|---|
| Contract columns in each of the three queries | 7 |
| Rail subtotal, in kilograms | 295,250 |
| Distinct values in `StatusRaw` | 3 (from 17) |
| Latest day in `ShipDate` | 13 February 2026 |
| Rows in `FactShipment` | 34 |
| Rows carrying a `-1` city key | 0 |
| `SUM(WeightKG)` | 578,650 kg |
| `SUM(FreightCostPKR)` | PKR 4,808,000 |

**Checks 1 to 4 come first, and that is not an ordering accident.** The last two
are the famous ones and they are the weakest on the sheet — a locale bug and a
status casing bug both pass them to the rupee. A pipeline that reconciles is not
the same as a pipeline that is right.

### After the refresh test, against `night2`

| | Expected |
|---|---|
| Rows in `FactShipment` | 35 |
| `SUM(WeightKG)` / `SUM(FreightCostPKR)` | 584,950 kg / PKR 4,860,000 |
| Rows carrying a `-1` key | **1** — and you name the city |
| Rows with status `Delayed` | 5 |
| *If you deduplicated before trimming* | *36 rows, 591,550 kg* |

## The five traps

1. **T1 · only one of the ten defects fails loudly.** Teams mark five or six as
   loud because they are confident they would notice. The test is not whether a
   careful person would spot it — it is whether the **pipeline tells somebody**.
   Exactly one does. The other nine lie with a straight face.

2. **T3 · the dedup constraint cannot be proved on tonight's file.** The two
   `RD-505` rows are **byte-identical**, so both dedup rules give 34 rows and
   578,650 kg. Noticing that is **correct and earns marks** — and then the rule
   still holds, for reasons the task asks you to find. `night2` is the file that
   proves it.

3. **T5 · the totals pass and every report is wrong.** Under US regional
   settings ten of the twelve marine dates land in the wrong month, one is right
   by accident and one errors — and `SUM(WeightKG)` is still 578,650 to the
   kilogram. Answering T6 with "the reconciliation totals would catch it" misses
   the week.

4. **T7 · check 6 expects zero, and zero is the trap.** The `-1` count is 0 only
   because the alias map happens to cover all 23 spellings these files contain.
   "0" typed without looking is the same answer as "0" typed after looking,
   which is why the sheet asks *how you know*. On `night2` the same pipeline
   reports **1**.

5. **Marine should have fewer applied steps than road, not the same.** Road
   needs 11, marine 9 (no blank row, no `TOTAL` footer), rail 13 (navigate,
   skip, prefix, convert). A marine query with eleven steps has two that do
   nothing — and a filter that removes nothing is worse than no filter, because
   the next person reads it as evidence that the file has junk rows.

## One sentence to leave with

Week 2 cleaned a file and Week 5 built the thing that cleans it, so the
deliverable was never the table: it is the seventeen steps, in order, with
their names on them — because those are what still work tomorrow night at two
in the morning when nobody is watching.
