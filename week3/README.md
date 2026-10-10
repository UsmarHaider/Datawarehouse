# Week 3 — Fact & Dimension Tables

Datasets and assignments for Week 3.

← [Back to the course index](../README.md)

| Lecture | Topic | Outcome | CLO | 3C |
|---|---|---|---|---|
| **L5** | Facts, dimensions and the grain | Differentiate fact tables from dimension tables by declaring grain configurations and surrogate keys | CLO2 | Competence |
| **L6** | Surrogate keys and the first star schema | Implement a functional relational design linking fact metrics with descriptive dimension tables in Power BI | CLO2 | Courage |

## The case

Week 2 ended with one flat table: **`Shipments_Unified`** — 34 rows,
578,650 kg, PKR 4,808,000.

It answers simple questions and fails at every interesting one. There is no
province column and no month column, so "freight cost per tonne by province,
this month vs last" cannot be asked. Karachi appears as *Karachi*,
*Karachi Port*, *Karachi Cantt*, *Port Qasim* and *Pipri Marshalling Yard*.
Nothing in it remembers what a route used to be called.

This week it becomes **one fact table and five dimensions** — and the totals
must not move by a single kilogram.

No setup needed — the data is already in `assignments/data/`.

## Contents

| Path | What it is |
|---|---|
| `assignments/TASKS.md` | Seven tasks, the rules and the marking guide |
| `assignments/PowerBI_Lab_Guide.md` | The hands-on lab: M code, DAX, relationship settings, definition of done |
| `assignments/data/PakFreight_W3_StarBuilder_STUDENT.xlsx` | **Start here.** All seven tasks; cream cells to fill |
| `assignments/data/Shipments_Unified.csv` | The Week 2 output, if your own file did not survive the week |
| `assignments/data/raw_locations.csv` | The 23 raw location strings with a blank conforming map, for Power Query |

> The teacher key is **not** in this repository, and `.gitignore` blocks
> `*TEACHER*`, `*_KEY*` and `*ANSWER*` from ever being committed here.

## Assignments

| Task | Covers | Marks |
|---|---|---|
| 1 | Classify twelve columns: fact, dimension, degenerate or neither | 12 |
| 2 | Declare the grain — for PakFreight and four new processes | 12 |
| 3 | Additivity, and the ratio that disagrees with itself by 3% | 10 |
| 4 | Build `DimCity` — conform 23 location strings, mint the surrogate keys | 20 |
| 5 | Build `DimRoute`, `DimMode`, `DimStatus`, `DimDate` | 20 |
| 6 | Build `FactShipment` — six integer keys, no descriptive text | 15 |
| 7 | **Reconcile.** Thirteen checks, all thirteen must pass | 8 |
| lab | **Hands-on:** the same star in Power BI, steps 5–7 as homework | — |

Full briefs in [`assignments/TASKS.md`](assignments/TASKS.md).

**Timing:** T1–T4 in a 180-minute session, T5–T7 as homework. In a 120-minute
session, stop after T4.

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

Six foreign keys, one degenerate dimension (`ShipmentID`), three measures
(`WeightKG`, `FreightCostPKR`, `ShipmentCount`). Ten columns, 34 rows.

## Expected results

Every figure below was verified against the source data before this brief was
written. T7 checks all of them for you.

| Check | Expected |
|---|---|
| Rows in `FactShipment` | **34** |
| Grand total, `WeightKG` | **578,650 kg** |
| Grand total, `FreightCostPKR` | **PKR 4,808,000** |
| Shipment legs (`SUM` of count) | **34** |
| Distinct `ShipmentID` | **34** |
| Rows in `DimCity`, excluding Unknown | **14** |
| Rows in `DimRoute`, excluding Unknown | **20** |
| Rows in `DimDate` | **28** |
| Sindh / Marine | **169,000 kg** |
| Punjab / Road | **44,100 kg** |
| Sindh, all modes | **484,350 kg** (83.7% of everything) |
| Fact rows on an Unknown key | **0** |
| Cost per kg, grand total | **PKR 8.31** |

Two of the thirteen are deliberately diagnostic. If Sindh/Marine reads
**206,500** you mapped one port to the wrong province. If cost per kg reads
**8.06** you averaged a ratio instead of dividing two sums — the same 3% error
T3 makes you prove on paper first.

## Traps worth knowing about

The workbook does not label these. They are listed here so the week can be
taught, not so the answers can be copied.

| Where | What the student meets |
|---|---|
| **T1** | Four of the twelve columns are not what they look like. Two are ratios wearing the clothes of a measurement; one looks like a degenerate key and earns its own dimension; one is not business data at all |
| **T2** | A fan trap: an analyst duplicates a fact row to fit a dimension, the row count goes to 35, and every weight report in the company is overstated forever |
| **T3** | `AVERAGE(Cost/Weight)` and `SUM(Cost)/SUM(Weight)` disagree by 3% on the same 34 rows. No error is raised and no cell turns red |
| **T4** | 23 raw location strings → 14 cities. One port is in a province most students assume wrongly, and getting it wrong still reconciles at the national total |
| **T5** | The lecture brief says "Remove Duplicates → 20 rows". On the raw strings it is **30**. Finding out why is worth 3 marks |
| **T6** | Until the dimensions exist, every key reads `-1`. That is the Unknown row working, not a bug — and students must say why that is better than losing the row |
| **T7** | One province in the deliverable matrix reads **zero**, correctly and misleadingly. That is the role-playing dimension, met before it is named |

## The 3C strand

| | |
|---|---|
| **Competence** | Declare a grain, classify any column, mint and defend a surrogate key |
| **Courage** | Build the model in Power BI and let thirteen checks tell you whether it is right |
| **Character** | T4's judgement questions and T7's last question. Merging two facilities into one city is a decision made *on behalf of the business*, and reconciliation proves arithmetic, never meaning |

## Where this goes next

| Week | Builds on this how |
|---|---|
| **W4** Star vs Snowflake | You built a star. Next week it gets normalised on purpose, the cost is measured, and SCD Types 1, 2 and 3 arrive |
| **W5** ETL | The conforming map built by hand becomes a repeatable pipeline with error handling |
| **W6** Optimization & Quality | Why the integer surrogate key minted this week is what makes indexing and partitioning possible at all |
