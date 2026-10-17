# Week 4 — Assignments: Dimensional Modeling

Seven tasks covering **Lecture 7** (star against snowflake) and **Lecture 8**
(relationships in Power BI).

| | |
|---|---|
| **L7** | Evaluate the normalization differences between Star and Snowflake schemas on query performance and maintenance cost — **CLO2 · Courage** |
| **L8** | Construct multi-table relational networks with correct cardinality and cross-filter directions — **CLO2 · Competence** |

The case continues from Week 3. **PakFreight** ended last week with one fact
table and five dimensions — 34 rows, 578,650 kg, PKR 4,808,000 — and not one
relationship between them.

Week 3 had a right answer. Week 4 has a **defensible** one. Both schemas you
will look at this week are legal, which is why every task below asks for a
reason as well as an answer, and why in most of them the reason carries more
marks than the verdict.

| Task | Covers | Marks |
|---|---|---|
| **T1** | Hop count: eight questions, joins counted in both schemas | 12 |
| **T2** | Snowflake `DimCity` into three tables, then justify the verdict | 15 |
| **T3** | Storage arithmetic: the bytes three ways, and in context | 12 |
| **T4** | The relationship register — six relationships, before Power BI opens | 20 |
| **T5** | Cross-filter direction: six scenarios | 12 |
| **T6** | When to snowflake: six scenarios against the four legitimate cases | 12 |
| **T7** | Reconcile. Thirteen checks, all thirteen must pass | 12 |
| | **Excel workbook total** | **95** |
| **Lab** | **Hands-on:** wire the star in Power BI | separate |

---

## Setup

The data is already in `data/`. Nothing to generate.

| File | What it is |
|---|---|
| `PakFreight_W4_SchemaLab_STUDENT.xlsx` | **Start here.** All seven tasks. Cream cells are yours to fill |
| `star/*.csv` | **Six unlinked tables** — the fact and five dimensions, nothing wired. The lab's starting point |
| `snowflake/*.csv` | `DimCity` split three ways, to check T2 against once you have done it yourself |
| `Shipments_Unified.csv` | The Week 2 output, in case your own file did not survive |

For the lab you need **Power BI Desktop**. On macOS or Linux use Power BI
Service or a lab machine, and say which in your submission.

**Requirements:** Excel, LibreOffice Calc or Google Sheets for the workbook.
Every formula in it is `COUNTIF`, `SUM` and `IF` — nothing that needs Excel 365.

> Do not open the `snowflake/` folder until T2 is finished. It is there so you
> can check your own answer, not supply it.

---

## How to work

**Teams of 3.** Name one person each:

| Role | Owns | Has to defend |
|---|---|---|
| **Modeller** | T2 and T4 | the shape of the model, to a room that disagrees |
| **Arithmetician** | T1 and T3, and may not round anything | every number, with the working shown |
| **Reconciler** | T7, with veto power over "it looks fine" | the thirteen checks |

**Do T1 before T2.** Counting the hops first is what turns the T2 verdict into
an argument instead of a preference. The workbook is ordered this way
deliberately and T2 asks you to cite your own T1 figures.

**Fill in T4 before Power BI opens.** On paper or in the sheet, but before. That
is the whole discipline of the week, and it is worth 20 marks — more than any
other task.

**Type only in cream cells.** Grey cells are source data as received from Week 3.

**T7 marks itself.** Every `✘ fix` means something earlier is still wrong.

---

## The rules

- **Count, do not assume.** T1 has eight questions and only four of them
  change between the two schemas. A student who writes a bigger number in every
  snowflake row has guessed, and scores accordingly.
- **A verdict without a mechanism is an opinion.** "Star is faster" earns
  almost nothing anywhere in this task. Name *what* is faster and *why* — hops,
  join order, compression, filter path.
- **Count the table you added.** Snowflaking costs you `DimProvince` itself.
  Forgetting it is the single most common T3 error and it inverts the answer.
- **One active path between any two tables.** Six relationships, five active.
  If all six of your Active cells say Yes, your register is wrong before you
  build anything.
- **Cross-filter is Single until you can justify otherwise, in writing.**
  Exactly like snowflaking. "It made my chart work" is not a justification.
- **The totals must not move.** 578,650 kg and PKR 4,808,000. Restructuring a
  schema never changes what the business shipped.

---

## T1 · Hop count audit  (12 marks)

Eight business questions. For each one, count the **join operations beyond
`FactShipment` itself** — in the star you already have, and in the snowflake
where `DimCity → DimProvince → DimCountry`.

Use the definition literally. "Total weight by month" touches `DimDate` only,
so it is **1 join in either schema**. Everything except the city chain is
unchanged between the two models.

**You produce:** the dimensions each question touches, two join counts, whether
the count changed, and one line on why it did or did not.

**Self-check (in the sheet):** the eight star joins total **11**, the eight
snowflake joins total **16**, and exactly **4** questions change.

> If your "changed" count is 8 you assumed instead of counting. If it is 0 you
> have not split `DimCity`. Both score zero for the counting marks.

**4 of the 12 marks** are for one written answer: the snowflake needs 5 more
joins in total — state what that number does **not** tell you about which
schema is faster.

---

## T2 · Snowflake it, then justify it  (15 marks)

Split the flat `DimCity` into three tables, then decide whether PakFreight
should actually do it.

**Part A · `DimProvince` (5).** One row per distinct province, a surrogate key
you mint yourself, the `Region` column moved across from `DimCity`, and a
foreign key up to `DimCountry`. Include the Unknown member — every dimension
gets one, for the reason Week 3 gave.

**Part B · `DimCountry` (2).** Build it. Then look hard at how many rows it has
excluding Unknown, and write that number down.

**Part C · `DimCity`, normalized (4).** The same 15 rows with `Province` and
`Region` removed and a `ProvinceKey` in their place. Two text columns out, one
integer in. Nothing about the business changed — only where the province name
is written down.

**Part D · The verdict (4).** Flatten or Snowflake, and why. **The reason
carries the marks, not the verdict.** A full-mark answer cites at least one
figure you calculated yourself in T1 or T3.

---

## T3 · Storage arithmetic  (12 marks)

The storage saving is the snowflake's only real advantage. Work out how big it
actually is.

The model: **2 bytes per character** (the way Excel and a columnar dictionary
hold text) and **4 bytes per integer key**. Count only the province and region
information — everything else is identical in both schemas.

**Part A · Three ways to hold it (6).** For five different `DimCity` row
counts, compute:

| | |
|---|---|
| **Flat, raw** | `ProvinceName` and `RegionName` written out as text on every city row. No compression — a 1990s row store |
| **Flat, encoded** | The same table in a columnar engine. Each distinct string stored **once** in a dictionary, plus a 4-byte pointer per row. Two text columns, so two pointers |
| **Snowflaked** | One 4-byte `ProvinceKey` per city row, **plus `DimProvince` itself** |

**Part B · The finding (3).** At 15 rows, is the snowflake smaller? Then state
the per-row saving once everything is encoded.

**Part C · Put it in context (3).** A real fact table runs roughly 100× its
dimensions at about 40 bytes a row. Express the saving as a percentage of
*that*, at both ends of your table. Then name the one condition under which
the storage argument is worth paying a join for.

> One of these five rows shows the snowflake being **bigger**. Find it and say
> why. If every row shows a saving, you forgot to count `DimProvince`.

---

## T4 · The relationship register  (20 marks)

**Part A · The six relationships (14).** One row each: the "one" side (always a
dimension), the "many" side (always the fact), the cardinality, the cross-filter
direction, whether it is active, and why the relationship exists. Write columns
as `Table[Column]`.

Five self-checks in the sheet carry 5 of these marks: six relationships, six at
`* : 1`, six at Single, **five active, one inactive**.

Exactly one of the six cannot be active. Find it before Power BI tells you.

**Part B · The two city roles (6).** `FactShipment` has `OriginCityKey` and
`DestCityKey` and both point at `DimCity`. Name which of the three answers from
the lecture you are using, and why:

1. Leave the second relationship inactive and activate it per measure with
   `USERELATIONSHIP`.
2. Load `DimCity` twice as `DimOriginCity` and `DimDestCity` — two active
   relationships, two slicers that read correctly.
3. Flatten both city names onto the fact and drop one relationship.

**Any of the three earns full marks with a sound reason. None earns full marks
without one.**

---

## T5 · Cross-filter direction  (12 marks)

Six situations. For each: **Single**, **Both**, or solve it at **measure level**
instead. One mark for the verdict, one for the reason — and the reason must say
what breaks if you get it wrong.

Only one of the six is a genuine case for changing anything, and even that one
is solved inside a measure rather than in the model.

> If you have written Both more than once, read the lecture again. The question
> is not whether Both works — it is what else it changes.

---

## T6 · When to snowflake  (12 marks)

Six scenarios. Verdict of **Flatten**, **Snowflake** or **Bridge**, and when you
say Snowflake, name which of the four legitimate cases it is:

1. **A genuine outrigger** — an attribute inside a dimension that is itself a
   dimension at a different grain.
2. **A huge dimension with wide, high-cardinality text** that will not compress.
3. **A sub-dimension owned elsewhere**, on a different load cadence.
4. **A multi-valued attribute** — which needs a bridge table, and is strictly
   not a snowflake at all.

Anything that is not one of these four gets flattened.

The last 2 marks: state the test in your own words. **Two conditions, both of
which must hold** before you snowflake anything.

---

## T7 · Reconcile  (12 marks)

Thirteen checks against the model you built in the lab. Read each number off
Power BI and type it in. **All thirteen must read `✔ pass`.**

| # | Check | Expected |
|---|---|---|
| 1 | Relationships in the model | 6 |
| 2 | Relationships with cardinality `* : 1` | 6 |
| 3 | Relationships with cross-filter Single | 6 |
| 4 | Active relationships | 5 |
| 5 | Inactive relationships | 1 |
| 6 | Rows in `FactShipment` | 34 |
| 7 | `SUM(WeightKG)` | **578,650 kg** |
| 8 | `SUM(FreightCostPKR)` | **PKR 4,808,000** |
| 9 | Blank rows across all five dimensions | 0 |
| 10 | Distinct origin provinces in the fact | 4 |
| 11 | `WeightKG` for Sindh origins | 484,350 |
| 12 | `WeightKG` for Punjab origins | 44,100 |
| 13 | `WeightKG` for Balochistan origins | 44,100 |

Do **not** copy the expected column across. The point of a reconciliation is
that it can fail.

**Three of these are diagnostic:**

- **Check 10 reads 5, not 4** → you counted provinces across both city roles.
  Only four provinces ever ship *from* anywhere — Sindh, Punjab, Balochistan
  and Islamabad ICT. Five *receive*.
- **Checks 11 and 12 both read 44,100** → not an error. Punjab and Balochistan
  origins genuinely both total 44,100 kg. It is a coincidence in the data.
  Verify Sindh reads 484,350 before you go hunting for a bug.
- **Check 9 reads anything but 0** → a fact key points at a dimension row that
  does not exist, so Power BI invented a blank row. The grand total will still
  be right and every breakdown will be short. Route the unmatched key to the
  Unknown member at `−1`.

> If you used role-playing tables (answer 2 in T4), checks 1–5 become 7
> relationships with 6 active and 0 inactive. Say so, and the check is marked
> against your register rather than the table above.

---

## The lab — wire the star in Power BI

Full steps, the M code, the DAX and a troubleshooting table are in
[`PowerBI_Lab_Guide.md`](PowerBI_Lab_Guide.md). In outline:

1. Import the six CSVs from `data/star/`.
2. **Turn off autodetect** — `File → Options → Current File → Data Load`.
3. Check every key is **Whole Number**, unique and non-blank on the one side.
4. Build the six relationships through the dialog, not by dragging.
5. Resolve the two city roles with your T4 part B answer.
6. Mark `DimDate` as a date table; sort `MonthName` by `MonthNumber`.
7. Five explicit measures. `Cost per KG` must be `DIVIDE(SUM, SUM)`.
8. Hide every key from Report view.
9. Build the matrix — `WeightKG` by `Province` by `Month`, plus a Mode slicer.

### Definition of done

- [ ] Autodetect off, and no relationship you did not create yourself
- [ ] Six relationships, every one **Many to one**, every one **Single**
- [ ] Exactly one active path between any two tables (one dashed line)
- [ ] Every key column Whole Number; dimension keys unique and non-blank
- [ ] `DimDate` marked as a date table; `MonthName` sorted by `MonthNumber`
- [ ] Five explicit measures; `Cost per KG` uses `DIVIDE(SUM, SUM)`
- [ ] Every key hidden from Report view; `ShipmentID` left visible
- [ ] The matrix responds to the slicer with no loop warning
- [ ] **578,650 kg** and **PKR 4,808,000**, exactly

### Why the matrix is the point

`Province` is a **column on `DimCity`**, not a table. A matrix grouped by
province therefore needs **no extra join**. That is the argument the whole
lecture made, made visible on your own screen. In the snowflaked model the same
matrix costs two joins instead of one, and a country-level version costs three.

---

## What you hand in

Due on the LMS **before Week 5**.

1. `W4_Schema_<team number>.xlsx` — all seven tasks, T7 reading **13 / 13**.
   Submitting with a single red cell loses all 12 marks for T7.
2. `W4_<roll number>.pbix` — the lab complete, with the T4 part B justification
   written on the report page or in the model description.
3. The individual quick check is done on paper in class, not submitted here.

**Marks: 95 in the workbook + 12 in the paper quick check.** These feed the
Hands-on Exercises component (20% of the course) against CLO2 and CLO3.

> `.pbix` files are gitignored in this repository on purpose. Submit through the
> LMS, not by committing.

---

## References

- **Kimball & Ross (2013)**, *The Data Warehouse Toolkit*, 3rd ed. — Ch. 2 for
  the position on snowflaking and outriggers; Ch. 11 for role-playing
  dimensions and multiple relationships to one table.
- **Ferrari & Russo (2019)**, *The Definitive Guide to DAX*, 2nd ed. — Ch. 15
  on `USERELATIONSHIP`; Ch. 18 on VertiPaq compression and dictionary encoding.
- **Microsoft Learn** — "Star schema and the importance of relevance in Power
  BI", "Create and manage relationships in Power BI Desktop", and
  "Bi-directional relationship guidance".
- **Kimball Group Design Tip No. 105** — snowflakes, outriggers and bridges.
  Short, free, and the clearest statement of the four exceptions.

---

## One sentence to leave with

Both schemas are legal, so the design is not a lookup — it is a judgement, and
the judgement is: flatten by default, snowflake only where the attribute is a
true dimension in its own right and nobody is waiting on it.
