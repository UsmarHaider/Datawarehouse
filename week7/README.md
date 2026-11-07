# Week 7 — Integration, History & OLAP

Datasets and assignments for Week 7.

← [Back to the course index](../README.md)

| Lecture | Topic | Outcome | CLO | 3C |
|---|---|---|---|---|
| **L13** | Slowly changing dimensions, and what each type does to a report you already published | Implement slowly changing dimension logic that absorbs source changes without invalidating previously published reports | CLO3 | Competence |
| **L14** | OLAP navigation on the finished star, and when an aggregate table earns its keep | Answer executive questions by navigating a dimensional model through roll-up, drill-down, slice, dice and pivot, and justify an aggregate table against its maintenance cost | CLO1 | Courage |

## The case

April closed, and three things happened at once.

**A fourth carrier.** PakFreight signed **ShaheenEx**, a courier partner that
consolidates parcels and sub-contracts PakFreight's own trucks when a load
fills. ShaheenEx does not file a spreadsheet. It files **JSON** — one object
per consignment, weight in **grams**, status as an **integer code**, the
customer nested inside the record, and a booking **timestamp** instead of a
date.

**The dimension moved.** Six customers changed during April: three moved head
office across a provincial border, two were re-classified, one was renamed
after an acquisition. Each change arrives with an **effective date**.

**The board asked for one table.** Weight by the customer's head-office
province, by month, February to April. March's Punjab figure was published in
April at **7,566,850 kg**, and after you load April it must still read
7,566,850 kg.

That last sentence is the week. Overwrite the three relocated customers and
every total still reconciles to the kilogram — and **883,350 kg of March's
freight quietly changes province.** The reject log does not catch it. The
identity does not catch it. The number the board already has is simply wrong.

**This is the last week before the midterm.** Week 8 is a pipeline and a star
under time, built from these same four sources.

No setup needed — the data is already in `assignments/data/`.

## Contents

| Path | What it is |
|---|---|
| `assignments/TASKS.md` | Eight tasks, the rules and the marking guide |
| `assignments/data/PakFreight_W7_IntegrationLab_STUDENT.xlsx` | **Start here.** All eight tasks; cream cells to fill |
| `assignments/data/april/*` | **The four dirty sources.** 1,805 data rows. The input |
| `assignments/data/customer_changes.csv` | **The six changes, with effective dates.** T5 starts here |
| `assignments/data/customers_master.csv` | The registry — 46 rows, 40 businesses, unchanged since Week 6 |
| `assignments/data/alias_lookup.csv` | The Week 5 alias map, **unchanged**: 23 raw strings → 14 cities |
| `assignments/data/dims/*.csv` | The Week 4 star carried forward. `DimDate` is Q1 only, `DimRoute` has 20 lanes and `DimMode` has three modes |
| `assignments/data/carryforward/FactShipment_Feb.csv` | **34 rows, 578,650 kg.** Week 2's one number, as a fact table |
| `assignments/data/carryforward/FactShipment_March.csv` | **1,200 rows, 17,542,050 kg.** Week 6's deliverable, verified |
| `assignments/data/carryforward/DimCustomer.csv` | **41 rows.** Week 6's customer dimension, with **no history columns at all** |

`FactShipment_April.csv`, `RejectLog_April.csv`, the Type 2 `DimCustomer.csv`
and `FactShipment_FebToApril.csv` are deliberately **not** here. Producing all
four, without moving February or March, is the week.

> February and March are handed over **verified**, so nobody is blocked by last
> week. There is **no lab guide**, by design, for the second week running. The
> teacher key, the generator, the file-level verifier and the quick-check
> answers are not in this repository either — `.gitignore` blocks `*TEACHER*`,
> `*_KEY*` and `*ANSWER*` from ever being committed here.

## Assignments

| Task | Covers | Marks |
|---|---|---|
| 1 | The warehouse end to end: a fourth source placed across the tiers | 10 |
| 2 | Profile four sources against one contract | 12 |
| 3 | **Reject, route, remove** — and a reject schema that survives JSON | 14 |
| 4 | The reconciliation identity across four sources, and four wrong totals | 12 |
| 5 | **Slowly changing dimensions, and the 883,350 kg that moves if you overwrite** | 18 |
| 6 | OLAP navigation: roll-up, drill-down, slice, dice, pivot | 14 |
| 7 | Selectivity, the index, and the aggregate table | 12 |
| 8 | **Definition of done.** Twelve checks, all twelve must pass | 8 |
| lab | **Hands-on:** the integrated load | — |

Full briefs in [`assignments/TASKS.md`](assignments/TASKS.md).

**Individual work.** No team roles, nothing to hand to anybody else to check.

**Timing:** T1–T4 in a 180-minute session, T5–T8 as homework. In a 120-minute
session, do T1–T3 in class and set the rest as homework — but do **T5 before
T6**, because T6 reads numbers off the model T5 makes correct.

## The pipeline you are building

```
  FOUR SOURCES              STAGING                  THREE ROUTES              THE MODEL

  marine  .csv   256  ─┐  land, log, profile     ┌─► RejectLog      35    DimDate      120
  rail    .xlsx  318  ─┼─► trim · unit · reject  ┤                        DimCity       15
  road    .csv   739  ─┼─► dedup · conform       ├─► dropped as dup  70   DimCustomer   47
  courier .json  492  ─┘  key by DATE + ID       └─► FactApril    1,700   DimRoute      25
                                                                          DimMode        5
  1,805 rows             74 rule failures             38 routed to -1     DimStatus      4
  2 structural rows      35 unloadable                383,600 kg admitted
```

**A fifth decision joins the four from Week 6: leave history alone.** Reject,
route, remove and load all act on April. The fifth acts on March, and it acts
by doing nothing.

**Power Query, Excel or pandas — your choice, same marks.** Every number is a
fact about the data, not about the tool.

## Expected results

Every figure below was derived from the committed files and asserted before
this brief was written. T8 checks all twelve for you.

| # | Check | Expected |
|---|---|---|
| 1 | Rows extracted into staging, all four files | **1,805** |
| 2 | Rows in `RejectLog_April` | **35** |
| 3 | Rows removed as duplicates | **70** |
| 4 | Rows in `FactShipment_April` | **1,700** |
| 5 | `SUM(WeightKG)`, April | **17,915,700 kg** |
| 6 | `SUM(FreightCostPKR)`, April | **PKR 158,037,000** |
| 7 | April rows on the Unknown **city** member | **18** |
| 8 | April rows on the Unknown **status** member | **9** |
| 9 | April rows on the Unknown **customer** member | **11** |
| 10 | Rows in `DimCustomer`, all versions (41 current) | **47** |
| 11 | Rows in `DimDate` | **120** |
| 12 | **Punjab, March, read off the integrated model** | **7,566,850 kg** |

**Checks 1 to 4 are the identity** and must satisfy `1 = 2 + 3 + 4` before any
of the others mean anything. **Check 12 is the only check in this course that
is passed by not doing something** — it is not about April at all.

Integrated, February to April: **2,934 rows · 36,036,400 kg · PKR 309,882,000 ·
8.60 per kg.**

| Month | Rows | Weight | Cost | Per kg |
|---|---|---|---|---|
| February | 34 | 578,650 kg | PKR 4,808,000 | 8.31 |
| March | 1,200 | 17,542,050 kg | PKR 147,037,000 | 8.38 |
| April | 1,700 | 17,915,700 kg | PKR 158,037,000 | **8.82** |

## The seven traps

1. **883,350 kg moves and every total stays right.** Three customers crossed a
   provincial border in April. Overwrite them — Type 1, the default in almost
   every tool — and March's province table re-allocates itself: Punjab
   −222,450, Sindh +284,400, Islamabad ICT +268,500, Khyber Pakhtunkhwa
   −330,450. The column still totals 17,542,050 kg. This is the week.

   The gross movement is 883,350 kg and the province column only shows
   **552,900** of it, because CU-116 moved *into* Punjab while CU-105 and
   CU-120 moved out. Reporting the net figure understates the damage by a
   third, which is the second mistake available here.

2. **The asymmetry is what hides it.** Islamabad ICT's March figure rises 79%
   and Punjab's falls 2.9%. The glaring error is in the province nobody reads;
   the invisible one is in the province the board cares about.

3. **The customer lookup is no longer a lookup.** Under Type 2 it is
   `CustomerID` **and the shipment date** → `CustomerKey`. Ignore the date and
   a handful of early-April shipments land in the wrong province, with every
   total correct and no error raised. CU-116 is the one that bites: 21 of its
   37 April rows fall **before** its 19 April effective date.

4. **A business key is the right tool this month and was the wrong one last
   month.** Fifteen rows are one consignment filed by both ShaheenEx and
   PakFreight Trucking under different IDs — only a business key finds those.
   Nine further **pairs** of rows share a business key and are genuinely
   different shipments. Dedup on it unscoped and you hand in 1,691 rows,
   17,882,150 kg, and nine destroyed consignments. The answer is the **scope**,
   not the key.

5. **The cost column failed for the first time.** Four rows have no price.
   `SUM` skips a null, so the weight total is perfect, the cost total is quietly
   short, and a pipeline that only ever validated weight loads all four.

6. **`SUM` is still the weakest check on the sheet.** Let the ten text weights
   through and they land as nulls: 1,710 rows at exactly 17,915,700 kg. Right
   to the kilogram, right to the rupee, ten rows in the fact table that are not
   shipments.

7. **Two of the unresolved statuses are integers, and they are not dirty.**
   `7` and `9` are perfectly clean values from a code table the warehouse was
   never told about — the block is sitting at the top of
   `courier_april.json`. Routing them to Unknown is correct. Guessing what they
   mean is not, and the fix is a conversation rather than a transform.

## One sentence to leave with

Week 6's deliverable was the fact table and the audit table beside it. This
week there is a third thing to deliver and it is the hardest to see, because it
is the February and March numbers **still reading what they read before you
started** — a warehouse is trusted for what it refuses to change as much as for
what it loads, and 7,566,850 kg has to survive April.
