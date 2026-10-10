# Week 3 — Assignments: Fact & Dimension Tables

Seven tasks covering **Lecture 5** (facts, dimensions and the grain) and
**Lecture 6** (surrogate keys and the first star schema).

| | |
|---|---|
| **L5** | Differentiate fact tables from dimension tables by declaring grain configurations and surrogate keys — **CLO2 · Competence** |
| **L6** | Implement a functional relational design linking fact metrics with descriptive dimension tables in Power BI — **CLO2 · Courage** |

The case continues from Week 2. **PakFreight** ended last week with one flat
table: `Shipments_Unified`, 34 rows, 578,650 kg, PKR 4,808,000.

It answers simple questions and fails at every interesting one. There is no
province column and no month column. Karachi is spelled five different ways.
Nothing in it remembers what a route used to be called.

This week you split that table into **one fact table and five dimensions** —
and the totals must not move by a single kilogram.

| Task | Covers | Marks |
|---|---|---|
| **T1** | Classify twelve columns: fact, dimension, degenerate or neither | 12 |
| **T2** | Declare the grain — for PakFreight and four new processes | 12 |
| **T3** | Additivity: additive, semi-additive, non-additive | 10 |
| **T4** | Build `DimCity` — conform 23 location strings, mint the keys | 20 |
| **T5** | Build `DimRoute`, `DimMode`, `DimStatus`, `DimDate` | 20 |
| **T6** | Build `FactShipment` — six integer keys, no text | 15 |
| **T7** | Reconcile. Thirteen checks, all thirteen must pass | 8 |
| | **Excel workbook total** | **95** |
| **Lab** | **Hands-on:** the same star built in Power BI | separate |

---

## Setup

The data is already in `data/`. Nothing to generate.

| File | What it is |
|---|---|
| `PakFreight_W3_StarBuilder_STUDENT.xlsx` | **Start here.** All seven tasks. Cream cells are yours to fill |
| `Shipments_Unified.csv` | The Week 2 output, in case your own file did not survive the week |
| `raw_locations.csv` | The 23 raw location strings with a blank conforming map, for Power Query |

For the lab you need **Power BI Desktop**. On macOS or Linux use Power BI
Service or a lab machine, and say which in your submission.

**Requirements:** Excel, LibreOffice Calc or Google Sheets for the workbook.
Every formula in it is `INDEX`/`MATCH`, `COUNTIF`, `SUMIFS` and `SUMPRODUCT` —
nothing that needs Excel 365.

---

## How to work

**Teams of 3.** Name one person each:

| Role | Owns | Has to defend |
|---|---|---|
| **Modeller** | the grain statement | why one row means exactly one thing |
| **Conformer** | `DimCity` and the 23 → 14 decision | every merge, to a person who disagrees |
| **Reconciler** | T7, with veto power over "it looks fine" | the thirteen numbers |

**Do the tasks in order.** T6 cannot be filled in before T4 and T5 exist. That
is not a quirk of the workbook — it is why dimensions are always loaded before
facts, and T7 asks you to say so in one sentence.

**Type only in cream cells.** Grey cells are source data as received.

**T7 marks itself.** Every `✘ fix` means something earlier is still wrong.

---

## The rules

- **Never put descriptive text in a fact table.** If you are tempted to add
  `OriginCityName` to `FactShipment`, stop. That column belongs in `DimCity`,
  where it is stored once instead of once per fact row.
- **Integer surrogate keys only.** Never join on a source system's own ID. T2
  question 3 is about what breaks when you do.
- **Every dimension gets a `-1` Unknown row.** A fact row whose context nobody
  recognises must land somewhere visible and countable, not vanish.
- **Store the numerator and the denominator, never the ratio.** A rate is only
  correct at the level it was computed at.
- **Declare the grain before you design a single column.** If your sentence
  needs the word "and", you have described two fact tables.
- **The totals must not move.** Reshaping is not a licence to lose a kilogram.

---

## T1 · Fact, dimension, degenerate or drop?  (12 marks)

PakFreight's operations team wants twelve more columns in the warehouse. For
each one, write **F** (fact / measure), **D** (dimension attribute), **DD**
(degenerate dimension) or **X** (belongs in neither), name the table it should
live in, and defend it in one line.

**Four of the twelve are deliberately tricky.** Two of them look like
measurements and are not safe to treat as one; one looks like a degenerate key
and is not; one does not belong in the dimensional model at all.

Then answer the three defence questions at the bottom of the sheet.

| | Marks |
|---|---|
| Twelve verdicts | 6 |
| Justifications | 3 |
| The three defence questions | 3 |

> A wrong verdict with a sharp justification scores more than a right verdict
> with none. The reasoning is the skill.

---

## T2 · Declare the grain  (12 marks)

**Part A** — write PakFreight's grain statement. The sheet checks it for the
word "and" automatically.

**Part B** — four processes PakFreight wants to add next. For each: the grain
sentence, the dimensions it implies, two measures, and the fact table type
(transaction, periodic snapshot, accumulating snapshot).

Two of the four are not plain transaction tables. One of them needs something
that is not a dimension at all.

**Part C** — a 20-second case. An analyst adds `CustomerName` to
`FactShipment`, hits a shipment billed to two customers, and duplicates the
row. Say what rule he broke, what he should have built, and which of T7's
thirteen checks would have caught it.

| | Marks |
|---|---|
| Part A grain sentence | 3 |
| Part B, 1.5 per process | 6 |
| Part C | 3 |
| Bonus: the two that are not transaction tables | 1 |

> A sentence containing "and" loses the grain mark however good the rest is.

---

## T3 · Additivity audit  (10 marks)

Ten candidate measures. Classify each as additive, semi-additive or
non-additive, say whether it is safe to `SUM` across time, and say what you
should store instead.

Then run the proof block. The sheet computes two numbers from PakFreight's own
34 rows: the average of a per-row ratio, and the ratio of two sums. **They
disagree, by about 3%, and nothing turns red.**

Answer the three questions at the bottom: which number goes on a board slide,
what the other one actually measures, and which row of the table has "delete
the column" as its correct answer.

| | Marks |
|---|---|
| Classification, 0.5 per row | 5 |
| The "store instead" column | 2 |
| The three questions | 3 |

> Full marks on question 1 require naming what the wrong number *measures*.
> "It is wrong" is not an answer — it is a real quantity, it just answers a
> different question.

---

## T4 · Build DimCity  (20 marks)

This is the editorial act of dimensional modelling, and it is yours.

**Block 1** — the conforming map. 23 raw location strings, exactly as the three
source systems wrote them. Decide what each one really is, and give it a
province, a region, a port flag and a facility type.

**Block 2** — the dimension. One row per real-world city, with a surrogate key
you mint yourself, plus the reserved `-1` Unknown row.

Three self-checks at the bottom must all pass before you start T5.

Then answer the three judgement questions. They are the marks that separate a
pass from a good grade, because none of them has a single right answer:

- You merged a facility 40 km outside the city into it. Name one business
  decision that choice quietly made for the company.
- One location is not in the province most people assume. What breaks if you
  get it wrong, and what breaks if you leave the province blank instead?
- A new file arrives next month with a spelling nobody has mapped. Walk
  through exactly what has to happen, in order, for it to appear correctly.

| | Marks |
|---|---|
| Conforming map | 8 |
| Provinces and regions correct | 4 |
| `DimCity` built, with the `-1` row reused | 4 |
| The three judgement questions | 4 |

---

## T5 · The other four dimensions  (20 marks)

`DimRoute`, `DimMode`, `DimStatus`, `DimDate`.

**Block A opens with a trap, and you must find it before you fill anything in.**
The lecture brief says "Remove Duplicates → 20 rows". Try it on the raw data
and you get a different number. Column I of the sheet lists every raw pair so
you can see why. Write down the reason, and which operation has to happen
first.

**Block C** builds `DimDate` for all 28 days of February 2026 — including the
days nothing shipped. The sheet counts them for you. Then answer why a date
dimension gets 28 rows when the fact table only ever touches 12 of them.

Four questions at the bottom, including one with no single right answer. You
should argue about it.

| | Marks |
|---|---|
| The Block A trap, explained | 3 |
| `DimRoute` | 6 |
| `DimMode` and `DimStatus`, with `-1` rows | 3 |
| `DimDate` | 4 |
| The four questions | 4 |

---

## T6 · Build FactShipment  (15 marks)

Left of the gap: `Shipments_Unified` exactly as Week 2 left it. Right of the
gap: the fact table. Row 6 is worked for you — copy it down.

**The rule you must not break: no descriptive text crosses the gap.**

Until T4 and T5 are filled in, every key in row 6 reads `-1`. That is not an
error — it is the Unknown row doing its job. Watch them turn into real keys as
you complete the dimensions.

Then answer the three questions: what `IFERROR(…, -1)` buys you and what it
costs you, why the text columns do not cross the gap, and why `ShipmentID`
stays in the fact table even though it joins to nothing.

| | Marks |
|---|---|
| Six key columns correct | 9 |
| Measures and the degenerate key | 3 |
| The three questions | 3 |

> A hard-typed key column instead of a lookup scores zero for that column. The
> point is the join, not the digit.

---

## T7 · Reconcile  (8 marks)

Thirteen checks. All thirteen must read **pass**.

The reshaping must not change a single kilogram. Reconciliation is not a
formality — it is the last moment at which you can still find the mistake
cheaply.

Two of the thirteen are deliberately diagnostic: if they come out wrong, the
sheet tells you which specific conforming decision you got wrong, and which
arithmetic mistake from T3 you repeated.

Then build the province × mode matrix, read the row that comes out as zero,
and answer the last question: **name one thing that could still be wrong with
this model that no check on the sheet would ever catch.**

| | Marks |
|---|---|
| Thirteen checks passing (all or nothing) | 5 |
| The matrix | 1 |
| The last question | 2 |

> Submitting with a single red cell loses all 8 marks. Thirteen out of
> thirteen, or it is not done.

---

## The lab — build the same star in Power BI

Full walkthrough in [`PowerBI_Lab_Guide.md`](PowerBI_Lab_Guide.md).

Steps 1–4 in class; **steps 5–7 are homework, due before Week 4**, because
Week 4 starts by assuming your star works.

### Definition of done

- [ ] Six tables: `FactShipment` + five dimensions
- [ ] Six relationships, all many-to-one, all single-direction, **exactly one inactive**
- [ ] Every key column hidden from report view
- [ ] Five explicit measures, with `Cost per KG` as `DIVIDE` of two sums
- [ ] `DimDate` marked as a date table, `MonthName` sorted by `MonthNumber`
- [ ] A `-1` Unknown row in all five dimensions
- [ ] The grain statement typed into the `FactShipment` description
- [ ] A matrix of Province × Mode totalling **578,650 kg** exactly
- [ ] No column anywhere in `FactShipment` holding descriptive text

### Bonus · role-playing dimensions

Your matrix is built on `OriginCityKey`, and one province reads **zero** —
correctly, and misleadingly. Fix it twice: once with `USERELATIONSHIP` in DAX,
once with a second physical role table. Then say in one paragraph which you
would choose and why. There is a defensible answer either way; what is marked
is whether you name the trade-off.

---

## What you hand in

Due on the LMS **before Week 4**.

| | Deliverable |
|---|---|
| Workbook | `W3_Star_<team number>.xlsx` — all seven tasks, T7 reading **13 / 13** |
| Power BI | `W3_<RollNo>.pbix` — lab steps 5–7 complete, five measures, keys hidden, grain in the table description |

> `.pbix` files are gitignored. Submit through the LMS, not by committing here.

---

## References

- **Kimball, R. & Ross, M. (2013).** *The Data Warehouse Toolkit*, 3rd ed.
  Wiley. Ch. 1 (the four-step design process), Ch. 2 (grain, additivity, fact
  table types, degenerate dimensions), Ch. 3 (the retail-sales example this
  case is modelled on), Ch. 19 (surrogate key management).
- **Inmon, W. H. (2005).** *Building the Data Warehouse*, 4th ed. Ch. 2 on
  granularity — the counterpoint to Kimball's dimensional grain.
- **Ferrari, A. & Russo, M. (2019).** *The Definitive Guide to DAX*, 2nd ed.
  Ch. 3 on date tables, Ch. 15 on `USERELATIONSHIP` and role-playing dimensions.
- **Microsoft Learn** — "Star schema and the importance of relevance in
  Power BI", and "Create date tables in Power BI Desktop".
- **Kimball Group Design Tips** No. 21 (declaring the grain) and No. 147
  (durable surrogate keys). Short, free, and worth reading before Week 4.

---

## One sentence to leave with

A fact table records what happened; a dimension table records what it was
about; and the grain is the promise that every row means the same thing. Get
those three right and the rest of the course is detail.
