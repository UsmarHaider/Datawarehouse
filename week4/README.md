# Week 4 — Dimensional Modeling

Datasets and assignments for Week 4.

← [Back to the course index](../README.md)

| Lecture | Topic | Outcome | CLO | 3C |
|---|---|---|---|---|
| **L7** | Star schema against snowflake schema | Evaluate the normalization differences between Star and Snowflake schemas on query performance and maintenance cost | CLO2 | Courage |
| **L8** | Relationships in Power BI | Construct multi-table relational networks with correct cardinality and cross-filter directions | CLO2 | Competence |

## The case

Week 3 produced **one fact table and five dimensions** — 34 rows, 578,650 kg,
PKR 4,808,000 — and left every one of them unconnected.

Week 3 had a right answer. This week has a *defensible* one. The session opens
on a multinational streaming platform whose correctly normalized snowflake
needs **twelve joins** to answer "total hours watched by country, by month" —
and takes the analytics server down trying. Street rolls into city, city into
state, state into country; nothing is stored twice; any textbook would pass the
design.

So you count the hops, do the storage arithmetic, and decide what shape
PakFreight's model should be. Then you wire it: six relationships, one of them
inactive, every cross-filter direction Single — and the two totals still
reconciling to the kilogram and the rupee.

No setup needed — the data is already in `assignments/data/`.

## Contents

| Path | What it is |
|---|---|
| `assignments/TASKS.md` | Seven tasks, the rules and the marking guide |
| `assignments/PowerBI_Lab_Guide.md` | The hands-on lab: nine steps, M code, DAX, relationship settings, definition of done, troubleshooting |
| `assignments/data/PakFreight_W4_SchemaLab_STUDENT.xlsx` | **Start here.** All seven tasks; cream cells to fill |
| `assignments/data/star/*.csv` | **Six unlinked tables** — the fact and five dimensions, nothing wired. The lab's starting point |
| `assignments/data/snowflake/*.csv` | `DimCity` split three ways, to check T2 against *after* you have done it |
| `assignments/data/Shipments_Unified.csv` | The Week 2 output, if your own file did not survive |

> The teacher key is **not** in this repository, and `.gitignore` blocks
> `*TEACHER*`, `*_KEY*` and `*ANSWER*` from ever being committed here.

## Assignments

| Task | Covers | Marks |
|---|---|---|
| 1 | Hop count: eight questions, joins counted in both schemas | 12 |
| 2 | Snowflake `DimCity` into three tables, then justify the verdict | 15 |
| 3 | Storage arithmetic: the bytes three ways, and in context | 12 |
| 4 | The relationship register — six relationships, before Power BI opens | 20 |
| 5 | Cross-filter direction: six scenarios | 12 |
| 6 | When to snowflake: six scenarios against the four legitimate cases | 12 |
| 7 | **Reconcile.** Thirteen checks, all thirteen must pass | 12 |
| lab | **Hands-on:** wire the star in Power BI, steps 7–9 as homework | — |

Full briefs in [`assignments/TASKS.md`](assignments/TASKS.md).

**Timing:** T1–T4 in a 180-minute session, T5–T7 as homework. In a 120-minute
session, stop after T4 and set T3 as homework too.

## The target model

```
                        DimDate (28 rows)
                              │
    DimCity ──────────  FactShipment  ────────── DimMode
   (14 + Unknown)      grain: one shipment leg   (3 + Unknown)
        │               34 rows · 10 columns          │
        └─ origin role         │                      │
           dest role      DimRoute              DimStatus
          (one inactive) (20 + Unknown)        (3 + Unknown)
```

Six relationships, five active, one dashed. Every one many-to-one, every one
cross-filtering **Single**, filters flowing only from dimension to fact.

`Province` and `Region` stay **columns on `DimCity`** — repeated for every city
in that province, on purpose. That repetition is the whole design decision this
week examines.

## Expected results

Every figure below was verified against the source data before this brief was
written. T7 checks all of them for you.

| Check | Expected |
|---|---|
| Relationships · `* : 1` · Single | 6 · 6 · 6 |
| Active / inactive | 5 / 1 |
| Rows in `FactShipment` | 34 |
| `SUM(WeightKG)` | 578,650 kg |
| `SUM(FreightCostPKR)` | PKR 4,808,000 |
| Blank rows across all dimensions | 0 |
| Distinct origin provinces | 4 |
| `WeightKG` — Sindh / Punjab / Balochistan origins | 484,350 / 44,100 / 44,100 |

Three are deliberately diagnostic. If **origin provinces reads 5** you counted
across both city roles — only four provinces ever ship *from* anywhere, though
five receive. If **Punjab and Balochistan both read 44,100** that is correct and
not a copy-paste error; it is a genuine coincidence in the data. If **blank rows
is anything but 0**, a fact key points at a dimension row that does not exist,
the grand total is still right, and every breakdown is silently short.

## The four traps

1. **T1 · only four of the eight questions change.** Writing a bigger number in
   every snowflake row is a guess, not a count. The join count rises only where
   the question actually reads a province or a country.
2. **T3 · at 15 rows, normalizing makes the model bigger.** Snowflaking saves
   two 4-byte pointers per row and costs you the whole of `DimProvince` — a net
   loss of **10 bytes** at this scale. A T3 that shows a saving everywhere has
   forgotten to count the table it added.
3. **T3 · the saving never stops being noise.** Even at **50 million**
   dimension rows the snowflake's saving is **0.1%** of the fact table beside
   it. "Snowflake saves storage" is a textbook written for row storage.
4. **T4 · six relationships, five active.** If all six Active cells say Yes,
   Power BI will refuse one and your register was wrong before you built
   anything. It is the second relationship into `DimCity`.

## One sentence to leave with

Both schemas are legal, so the design is not a lookup — it is a judgement, and
the judgement is: flatten by default, snowflake only where the attribute is a
true dimension in its own right and nobody is waiting on it.
