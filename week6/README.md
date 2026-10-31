# Week 6 — Query Optimization & Data Quality

Datasets and assignments for Week 6.

← [Back to the course index](../README.md)

| Lecture | Topic | Outcome | CLO | 3C |
|---|---|---|---|---|
| **L11** | Indexing, and what a query plan is telling you | Apply indexing strategies to optimize analytic read speeds and pinpoint slow join paths | CLO3 | Competence |
| **L12** | Data quality, deduplication and error routing | Design error-routing workflows that isolate corrupt rows without crashing the pipeline, and eliminate duplicates while keeping historical query validity | CLO3 | Competence |

## The case

March closed. The same three systems wrote the same three files and the volume
went up thirty-five times.

Three things are now true at once. The 08:00 dashboard takes minutes to open.
The board has been told PakFreight served **46 customers** in March, and
PakFreight has **40**. And some rows in tonight's files cannot be fixed by any
transform the course has taught — not by trimming, not by casting, not by
conforming. They are simply not loadable, and last month there were none of
them.

Week 5's rule was that **nothing is dropped silently.** This week that rule
becomes arithmetic —

```
rows extracted  =  rows loaded  +  rows rejected  +  rows deduplicated
     1,284      =     1,200     +       24        +         60
```

— and the audit table that proves it is a deliverable, marked as heavily as the
fact table.

**This week is also a checkpoint.** Week 8 is the midterm — a pipeline and a
star, under time. T1 is fifteen claims drawn from every week of the course, and
it is where a student finds out which of the first five weeks they are still
carrying.

No setup needed — the data is already in `assignments/data/`.

## Contents

| Path | What it is |
|---|---|
| `assignments/TASKS.md` | Seven tasks, the rules and the marking guide |
| `assignments/data/PakFreight_W6_QualityLab_STUDENT.xlsx` | **Start here.** All seven tasks; cream cells to fill |
| `assignments/data/march/*` | **The three dirty files.** 1,284 data rows. The input |
| `assignments/data/customers_master.csv` | The customer registry — 46 rows, and fewer customers than that |
| `assignments/data/alias_lookup.csv` | The Week 5 alias map, **unchanged**: 23 raw strings → 14 cities |
| `assignments/data/dims/*.csv` | The Week 4 star, carried forward. **One of the five is stale and it is not labelled** |

`FactShipment_March.csv`, `RejectLog.csv` and `DimCustomer.csv` are
deliberately **not** here. Producing all three is the week.

> There is **no lab guide this week, by design.** Week 5 handed over seventeen
> named steps; Week 6 hands over the targets and nothing else. The teacher key,
> the generator, the file-level verifier and the quick-check answers are not in
> this repository either — `.gitignore` blocks `*TEACHER*`, `*_KEY*` and
> `*ANSWER*` from ever being committed here.

## Assignments

| Task | Covers | Marks |
|---|---|---|
| 1 | **The carry-forward audit:** fifteen claims, one from every week, true or false, with the number | 15 |
| 2 | Profile the eight contract columns before you transform anything | 12 |
| 3 | **The reject contract:** nine classes of row, four verdicts, and a reject schema you specify | 18 |
| 4 | The reconciliation identity, and four wrong totals read back to their cause | 15 |
| 5 | Four readings of the word duplicate, and the customer count the board was given | 12 |
| 6 | Selectivity, the index you would build, what it costs on write, and the join path | 15 |
| 7 | **Definition of done.** Ten checks, all ten must pass | 8 |
| lab | **Hands-on:** the dual-route load | — |

Full briefs in [`assignments/TASKS.md`](assignments/TASKS.md).

**Individual work.** No team roles this week, and nothing to hand to anybody
else to check.

**Timing:** T1–T4 in a 180-minute session, T5–T7 as homework. In a 120-minute
session, stop after T3 and set T4 as homework too — T3 is the week and it is
worth 18 marks.

## The pipeline you are building

```
  THREE SOURCES          STAGING                 TWO ROUTES            THE STAR

  marine .csv  ──┐    land, log, profile    ┌─► RejectLog    24    DimDate     90
  rail   .xlsx ──┼──► trim · type · reject  ┤                      DimCity     15
  road   .csv  ──┘    dedup · conform · key └─► FactShipment 1,200 DimCustomer 41
                                                                   DimRoute    21
  1,284 rows          1,260 loadable             60 removed         DimMode      4
  105 rule failures   24 unloadable              21 routed to -1    DimStatus    4
```

**Reject, route and remove are three different decisions**, and telling them
apart is most of what this week marks.

- **Reject** — the row cannot be loaded at all. It goes to `RejectLog` with a
  reason, a file, and a line number.
- **Route to Unknown** — the row loads. A lookup failed, the key is `-1`, and
  the count is **published**.
- **Remove as duplicate** — the row is not a second shipment, so taking it out
  restores the grain.

**Power Query, Excel or pandas — your choice, same marks.** Every number is a
fact about the data, not about the tool.

## Expected results

Every figure below was derived from the committed files and asserted before
this brief was written. T7 checks all ten for you.

| # | Check | Expected |
|---|---|---|
| 1 | Rows extracted into staging | **1,284** |
| 2 | Rows in `RejectLog` | **24** |
| 3 | Rows removed as duplicates | **60** |
| 4 | Rows in `FactShipment_March` | **1,200** |
| 5 | `SUM(WeightKG)` | **17,542,050 kg** |
| 6 | `SUM(FreightCostPKR)` | **PKR 147,037,000** |
| 7 | Rows on the Unknown **city** member | **14** |
| 8 | Rows on the Unknown **status** member | **7** |
| 9 | Rows in `DimCustomer`, excluding Unknown | **40** |
| 10 | Rows in `DimDate` | **90** |

**Checks 1 to 4 are the identity** and must satisfy `1 = 2 + 3 + 4` before any
of the others mean anything. **Checks 5 and 6 are the famous ones and the
weakest on the sheet** — four different wrong pipelines pass check 5 exactly.
**Checks 9 and 10 cannot be passed by cleaning the March files at all**; they
are Week 3 and Week 4 arriving to be marked.

PKR 8.38 per kilogram, against February's 8.31 — a sanity check that costs
nothing and catches a unit error instantly.

## The six traps

1. **Three rows look exactly like faults and are not.** A negative *weight* is
   impossible and is rejected; a negative *cost* is a credit note, and Week 1
   already met one in the Superstore log. Reject on "any negative" and you
   delete three real shipments. A reject count of 27 is this mistake; 38 means
   the unresolved cities went too.

2. **Checks 7 and 8 expect 14 and 7, not zero.** They are the only two checks
   on the sheet satisfied by *admitting* something. Zero was available — delete
   the fourteen rows and the count is 1,186, the dashboard is green, and
   **195,150 kg** of freight the company actually moved is gone from the
   quarter. Nobody would have found it.

3. **Check 5 passes for four different wrong pipelines.** The sharpest: let the
   nine text weights load and they land as nulls, `SUM` skips a null, and the
   weight is right to the kilogram with nine rows in the fact table that are
   not shipments. 1,209 rows at 17,542,050 kg. This is why the ladder is marked
   on rows as well as on weight.

4. **The customer count is wrong and the fact table has no duplicates.** The
   duplication is in the *dimension*: six businesses are in the registry twice
   under a second ID and a different spelling. A duplicate fact row inflates
   weight and revenue; a duplicate dimension row inflates counts and leaves
   every additive total exactly right — which is how this one reached the
   board.

5. **The "natural" business key deletes real history.** Deduplicate on day +
   lane + weight + customer and you get 1,198: two pairs of genuinely different
   `RD-` consignments match on all four columns. It sounds more rigorous than
   the right answer, which is why it survives review. A business key is a claim
   about the data — test it before you deduplicate on it.

6. **`dims/DimDate.csv` is February's 28 rows and nothing says so.** Every
   March row would land on a date key that does not exist and the weight total
   would still be exactly right. It is the clearest case all week of a failure
   that reconciles perfectly, and it is carried in from Week 4 rather than
   caused by anything in these files.

## One sentence to leave with

Week 5 built the pipeline, so this week the deliverable is not the fact table
either: it is the fact table **and** the audit table beside it, because a
warehouse is trusted for what it admits it could not load, and 1,284 has to
equal 1,200 + 24 + 60 before any number downstream is worth reading.
