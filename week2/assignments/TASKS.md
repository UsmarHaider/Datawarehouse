# Week 2 — Assignments: DW Lifecycle & Architecture

Five tasks covering **Lecture 3** (architectural foundations) and **Lecture 4** (data ingestion).

| | |
|---|---|
| **L3** | Phases of DW development (staging, storage, presentation), roles in the BI ecosystem — **CLO1 · Competence** |
| **L4** | Hands-on: import data from Excel/CSV files into Power BI — **CLO1 · Courage** |

The case runs through all five tasks. **PakFreight** moves cargo three ways — marine, rail and road — and each mode keeps its own file, in its own format, with its own idea of what a shipment is. Three teams, three totals, zero trust.

| Task | Covers | Data |
|---|---|---|
| 1 | The three tiers, and Inmon's four properties | — |
| 2 | Inmon vs Kimball, and the lifecycle | — |
| 3 | **Data Detective** — profile the raw files, explain the four totals | all three source files |
| 4 | **Hands-on:** build the pipeline in Power BI | all three source files |
| 5 | Latency, schema drift, lineage and roles | — |

**Setup**

The data is already in `data/`. Nothing to download.

| File | Rows | Shape it arrives in |
|---|---|---|
| `marine_shipments.csv` | 12 | `dd/mm/yyyy` dates · **KG** · UPPERCASE status · IDs like `MR-1001` |
| `rail_shipments.xlsx` | 10 | 2 title rows above the header · **TONS** · numeric IDs · mixed-case status |
| `road_shipments.csv` | 15 | 12 real trips + 1 duplicate + 1 blank row + 1 TOTAL row · lowercase IDs |
| `PakFreight_Activity_STUDENT.xlsx` | — | the Data Detective workbook; yellow cells are yours to fill |

For Task 4 you need **Power BI Desktop**. On macOS or Linux use Power BI Service or a lab machine, and say which in your document.

**What you hand in**

| Task | Deliverable |
|---|---|
| 1, 2, 5 | `DWBI_W2_<RollNo>.pdf` (or `.md`), one heading per task |
| 3 | Your completed `PakFreight_Activity_<RollNo>.xlsx` — every check must turn ✔ |
| 4 | `DWBI_W2_<RollNo>.pbix`, plus screenshots of your Applied Steps and your validation card |

---

## The rules

- **Never edit a source file.** Every fix happens in Power Query as a recorded step. If you opened a CSV in Excel and saved over it, you have destroyed the evidence and the task scores zero.
- **Every number must be traceable.** For any figure you report, you must be able to name the file, the row and the transformation it came from.
- **Staging is not optional.** Raw queries load into staging and stay there. The model sees one table.
- **Say what you removed and why.** A row dropped without a stated reason is a row lost.
- **Your pipeline must be repeatable.** If you cannot press Refresh and get the same answer, you have not built a pipeline — you have cleaned a file by hand.

---

## Quick reference

**The three tiers**

```
Sources  →  TIER 1 Staging  →  TIER 2 Storage  →  TIER 3 Presentation  →  BI
            (quality            (EDW / ODS)        (data marts,
             checkpoint)                            star schemas)
```

**Inmon's four properties:** subject-oriented · integrated · time-variant · non-volatile.

**Inmon vs Kimball**

| | Inmon (top-down) | Kimball (bottom-up) |
|---|---|---|
| Builds first | the enterprise warehouse, normalised | one business process mart, dimensional |
| Then | data marts drawn from it | conformed dimensions tie marts together |
| Strength | one consistent enterprise model | delivers value early |
| Risk | slow to show value | marts can drift apart without conformance |
| Drives from | requirements (SDLC) | data (CLDS) |

**EDW vs ODS:** the EDW holds integrated history for analysis; the ODS holds current operational detail for near-real-time questions. A dispatcher needing truck positions every two minutes needs the ODS, not the EDW.

**The contract for Task 4** — the target schema every source must be bent into:

| Column | Type | Example |
|---|---|---|
| `ShipmentID` | Text | `RL-45012` |
| `ShipDate` | Date | `03-Feb-2026` |
| `Origin` | Text | `Karachi Cantt` |
| `Destination` | Text | `Lahore` |
| `WeightKG` | Decimal number | `32,500` |
| `CostPKR` | Fixed decimal | `285,000` |
| `Status` | Text | `Delivered` |
| `SourceSystem` | Text | `Rail` |

---

## Task 1 — The three tiers, and what a warehouse must be

**Do this:**

1. **Name the three tiers** and give, for each: its one-line job, one thing that happens there in the PakFreight case, and one thing that must **not** happen there.
2. **Apply Inmon's four properties to PakFreight.** For each property, give a concrete example from this case of the property being satisfied, and one of it being broken. For example, what in these three files breaks *integrated*?
3. **EDW or ODS?** Decide for each, in one line:

   | | Requirement |
   |---|---|
   | a | A dispatcher needs truck positions every 2 minutes |
   | b | The CFO compares freight cost per tonne-km across three years |
   | c | A customer service agent checks whether consignment 45017 left today |
   | d | The board reviews mode profitability since 2023 |

4. **Independent vs dependent data marts.** Operations, Finance and Sales each built their own mart straight from their own file. Draw that arrangement, then draw the dependent alternative. Explain in three sentences why the first produces three different answers to one question.
5. **One sentence:** why do raw files pass through staging rather than loading straight into the model?

**The question to answer:** we overwrite a customer's old address with their new one. Which of Inmon's properties does that break, and what should the warehouse have done instead?

---

## Task 2 — Inmon, Kimball, and the lifecycle

**Do this:**

1. **Side-by-side comparison.** Build a table comparing Inmon's top-down and Kimball's bottom-up approaches on at least five dimensions — starting point, modelling style, time to first value, risk, and how consistency is enforced.
2. **Draw both architectures yourself.** Inmon's CIF and Kimball's Bus. Label the flow of data in each. Hand-drawn and photographed is fine; do not screenshot the slide.
3. **Classify ten scenarios** as Inmon, Kimball or Hybrid, one reason each:

   | | Scenario |
   |---|---|
   | 1 | A bank must have one enterprise definition of "customer" before any reporting |
   | 2 | A startup needs a sales dashboard live within six weeks |
   | 3 | A hospital group with five systems and a three-year regulatory programme |
   | 4 | PakFreight builds the Shipments mart first, with conformed Date and Route |
   | 5 | A retailer with a normalised core warehouse feeding departmental marts |
   | 6 | A telecom moving to a lakehouse with bronze, silver and gold layers |
   | 7 | A government census programme where the model must be agreed before loading |
   | 8 | An e-commerce team adding a Returns mart that reuses the existing Product dimension |
   | 9 | A manufacturer who has built six marts and now cannot reconcile them |
   | 10 | A bank integrating a newly acquired competitor's systems |

4. **Apply the Kimball lifecycle to PakFreight Iteration 1.** Take the lifecycle phases — programme planning, business requirements, technical architecture, product selection, dimensional modelling, physical design, ETL design and development, BI application specification and development, deployment, and maintenance — and for **five** of them write what specifically happens for the Shipments iteration.
5. **Iteration 2 adds Billing.** Name two dimensions Iteration 1 should have built so Iteration 2 can reuse them, and explain what "conformed" means in that sentence.
6. **SDLC vs CLDS.** Inmon says the classic development lifecycle runs requirements → program, while warehouses run data → requirements. Explain the difference and why warehouse projects so often discover their requirements only *after* looking at the data. Give one example from these three freight files.

**The question to answer:** "We built the Shipments mart first, with conformed Date and Route dimensions." Top-down or bottom-up — and what would have had to be true for the other answer to be right?

---

## Task 3 — Data Detective (`PakFreight_Activity_STUDENT.xlsx` + the three source files)

Open the three source files and look at them **before** you touch Power BI. Fill in the yellow cells of the student workbook as you go.

**Do this:**

1. **Log every problem in the raw files.** For each one: the file, the column, an example value, and what it would do to a report. You should find faults in all three. Work through at least these categories — units, date formats, identifier formats, text casing and whitespace, duplicate rows, blank rows, non-data rows, and missing values.
2. **The Stovepipe Game — explain the four totals.** Asked for total weight shipped in February, three departments answered differently, and the staging area produced a fourth:

   | Who | Answer | |
   |---|---|---|
   | Operations | **661.65 t** | kept the TOTAL row |
   | Finance | **283.70 t** | read the rail tons as kilograms |
   | Sales | **584.75 t** | kept the duplicate |
   | One staging area | **578.65 t** | the true number |

   For each of the three wrong answers, reproduce the mistake and show the arithmetic that produces that exact figure. Then explain, in two sentences, why all three departments believed they were right.
3. **Clean all three in the staging sheets** of the workbook, using formulas — not by typing corrected values. Standardise names, convert units, fix dates, trim and case the status, and drop what must be dropped.
4. **Reconcile.** Every check in the workbook must turn ✔. Your staged totals must be:

   | Source | Raw records | Removed | Loaded | Weight (kg) |
   |---|---|---|---|---|
   | Marine | 12 | 0 | 12 | 206,500 |
   | Rail | 10 | 0 | 10 | 295,250 |
   | Road | 15 | 3 | 12 | 76,900 |
   | **Total** | **37** | **3** | **34** | **578,650** |

   If a check will not turn ✔, do not adjust the number — find the row causing it and say which it is.
5. **Trace the lineage of 578.65 t.** Write the full path from the three raw files to that single figure: every file, every transformation, every row removed, in order. This is the deliverable that proves you can answer "where did this number come from?" — the question an auditor will actually ask.
6. **Build the Kimball bus matrix** for PakFreight: business processes down the side, conformed dimensions across the top, ticks where they meet. Start with Shipments and Billing, and at least four dimensions.

**Watch out for:** the three rows removed from Road are **not** three of the same kind — one is a duplicate, one is blank, one is a TOTAL row that was never a shipment. Name each one individually. And the single largest trap in the whole week is rail weight: the column is in **tons**, so 32.5 means 32,500 kg. Finance's 283.70 t is what happens when nobody reads the header.

**The question to answer:** Operations' 661.65 t came from summing a column that included a TOTAL row. Name one control you would add to the pipeline so that this specific mistake can never reach a report again.

---

## Task 4 — Hands-on: one pipeline in Power BI

Build the staging → storage → presentation pipeline for real. Import three mismatched files, standardise them, and deliver **one** trusted table.

**Goal:** a single table named `Shipments`, **34 rows**, **8 columns**, totalling **578,650 kg**, with the three raw queries kept as hidden staging.

**Do this:**

1. **Connect — and do not Load.** Get Data → Text/CSV → `marine_shipments.csv` → **Transform Data**. Repeat for `road_shipments.csv`. Then Get Data → Excel workbook → `rail_shipments.xlsx` → tick the sheet → **Transform Data**. In one sentence in your document: why Transform and not Load?
2. **Name your staging.** Rename the three queries `marine_stg`, `rail_stg`, `road_stg`. Open Query Settings and note that every click is recorded in **Applied Steps** — screenshot this for one query.
3. **Fix the rail headers.** Delete the automatic *Promoted Headers* and *Changed Type* steps, remove the top 2 rows, then use the first row as headers. Explain why Power BI's automatic guess was wrong here.
4. **Standardise names.** Rename every column in all three queries to the contract in the Quick reference. They must match exactly — Append matches by **name**, not by position.
5. **Fix types, units and IDs.**
   - Marine `ShipDate`: Change Type → **Using Locale** → Date, English (United Kingdom).
   - Rail: add `WeightKG` = `[Weight (Tons)] * 1000`, then remove the tons column.
   - Rail `ShipmentID` → Text → add prefix `RL-`. Road `ShipmentID` → UPPERCASE.
6. **Clean rows and values.** Trim and capitalise `Status`. On Road: remove blank rows, filter out the `TOTAL` row, remove duplicates on `ShipmentID`. Add a `SourceSystem` column to each query — `Marine`, `Rail`, `Road`.
7. **Append.** Append Queries as New → all three `_stg` queries → rename the result `Shipments`. Right-click each `_stg` query and **untick Enable load**. Close & Apply. Only `Shipments` may appear in the model.
8. **Validate before you trust.** Turn on Column quality, Column distribution and Column profile, and set profiling to the **entire data set**. Then confirm and record every one of these:
   - 34 rows, 8 columns;
   - no Error or Empty in `ShipmentID`, `ShipDate` or `WeightKG`;
   - `Status` has exactly **3** distinct values;
   - a card showing `SUM(WeightKG)` = **578,650**;
   - a bar chart by `SourceSystem` giving Marine **206.5 t**, Rail **295.25 t**, Road **76.9 t**;
   - counts by status: Delivered **22**, In Transit **8**, Delayed **4**.
9. **Read the M code.** Open the Advanced Editor on `rail_stg`, paste the generated M into your document, and annotate three lines in your own words.

**Check the date trap:** `MR-1003` must show **03-Feb-2026**, not 2 March, and `MR-1012` must show **13-Feb-2026**, not an error. If either is wrong, your locale is wrong — fix the locale, do not retype the dates.

**Bonus — the folder connector.** Road files arrive daily. Instead of a new query per file, use Get Data → Folder → Combine & Transform. Explain in three sentences what Power BI builds for you, and why the folder is only ever as clean as its worst file.

**The question to answer:** you disabled load on the three `_stg` queries. Explain what that achieves, in terms of the three tiers — and what a business user would have seen in the model if you had left them loaded.

---

## Task 5 — Latency, drift, lineage and the people

**Do this:**

1. **Data latency.** For each consumer, state the freshness they actually need and justify it — real-time, near-real-time, daily batch, or weekly:

   | | Consumer |
   |---|---|
   | a | A dispatcher rerouting a truck around a blocked motorway |
   | b | The CFO's monthly cost-per-tonne report |
   | c | A customer tracking their consignment online |
   | d | The board's quarterly mode-profitability review |

   Then: why is "always real-time" the wrong answer? Give two concrete costs.

2. **Schema drift.** Next month the rail team adds a `Wagon_Type` column and renames `Freight Charges (PKR)` to `Charges_PKR`. For each change, say exactly what happens to your Task 4 pipeline on the next refresh — does it break, silently drop data, or carry on? Then give one way to detect each before it reaches a report.
3. **Data lineage.** Write the lineage of a single figure — `578,650 kg` — as a diagram or numbered chain, from three source files to the card on your report. Then answer: the CFO says the number looks too low. Using only your lineage, name the three places you would check, in order.
4. **Roles in the BI ecosystem.** Match each responsibility to the role that owns it, and say which tier they mainly work in:

   | | Responsibility |
   |---|---|
   | a | Designing the star schema for Shipments |
   | b | Writing and maintaining the Power Query pipeline |
   | c | Agreeing what "delivered" officially means |
   | d | Building the dashboard the operations team opens each morning |
   | e | Making sure the rail team's export keeps its agreed format |

   Roles to choose from: data architect, ETL/data engineer, business/data steward, BI developer, source system owner.

5. **The responsibility map.** Who owns each tier — staging, storage, presentation — and what goes wrong when nobody does? Answer with reference to the stovepipe problem in Task 3.
6. **Character — discipline.** Task 4 asked you to validate before trusting your own output. Write a short paragraph on why a freight analyst who skips that step is a risk to the business, with one specific consequence for PakFreight if the 578,650 figure were wrong and nobody checked.

**The question to answer:** you are handed a dashboard built by someone who left the company, showing a number you cannot reproduce. Using lineage, latency and schema drift, describe the order in which you would investigate.

---

## Marking guide

| | Weight |
|---|---|
| **Accuracy** — tiers, classifications, reconciliation and all Task 4 validation figures correct | 30% |
| **Logic** — architecture choices, lifecycle reasoning and lineage are justified, not asserted | 25% |
| **Application** — the Power BI pipeline is built correctly, staged, hidden and repeatable | 30% |
| **Creativity** — your own diagrams, your own examples, clear explanations in your own words | 15% |

**Automatic deductions:**

- editing a source file instead of transforming it in Power Query
- a `Shipments` table that is not exactly 34 rows / 578,650 kg, with no explanation of the discrepancy
- `_stg` queries left loaded into the model
- rail weight left in tons, or converted anywhere other than in the query
- the marine date locale left as default, so `MR-1003` reads 2 March
- rows removed without being named and justified
- a reconciliation check forced to ✔ by overtyping the number
- a screenshot of the lecture's architecture diagram submitted as your own
- the `.pbix` or the completed activity workbook missing
- committing the teacher key, if you are given one

---

## Before next week

Read **Kimball & Ross, Chapter 17** (the lifecycle), and **Inmon, Chapters 1–2**.

Week 3 takes the single `Shipments` table you just built and turns it into a dimensional model — facts, dimensions, grain and the star schema.
