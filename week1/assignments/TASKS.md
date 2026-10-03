# Week 1 — Assignments: Introduction to DW & BI

Five tasks covering **Lecture 1** (fundamentals) and **Lecture 2** (your first live Power BI connection).

| | |
|---|---|
| **L1** | Overview of Data Warehousing & BI, importance in decision-making — **CLO1 · Competence** |
| **L2** | Connecting Power BI to sample datasets and exploring interface layouts — **CLO1 · Courage** |

| Task | Covers | Data |
|---|---|---|
| 1 | The messy sales log — why the raw export cannot answer the CEO | `DWBI_W1_Messy_Sales_Log.csv` |
| 2 | OLTP vs OLAP — two different jobs | — |
| 3 | No history, no single truth | — |
| 4 | The DW/BI architecture — place each item in its stage | — |
| 5 | **Hands-on:** your first live connection | `DWBI_W1_Regional_Sales.xlsx` |

**Setup**

```bash
cd week1/assignments
python3 generate_week1_data.py
```

Needs `pandas` and `openpyxl`. Both files are generated with a fixed seed, so everyone's data is identical and your answers can be compared. **Do not change the seed.**

For Task 5 you need **Power BI Desktop** (free, Windows). If you are on macOS or Linux, use Power BI Service (`app.powerbi.com`) in a browser, or a Windows lab machine — say in your notebook which you used.

**What you hand in**

| Task | Deliverable |
|---|---|
| 1–4 | One document, `DWBI_W1_<RollNo>.pdf` (or `.md`), with a clear heading per task |
| 5 | `DWBI_W1_<RollNo>.pbix`, **plus** a screenshot of your report page in the document |

Answer in your own words. An answer copied from the slides earns nothing — the point is whether *you* can explain it.

---

## The rules

- **Every claim needs its evidence.** If you say a number is wrong, show the right one and how you got it.
- **Name who fixes it.** For every data problem you find, say whether it belongs to the source system, to ETL, or to the business — this is the habit the whole course is built on.
- **No screenshots of the slides.** Diagrams must be your own, even if they are drawn on paper and photographed.
- **State your assumptions.** Several questions here have more than one defensible answer. The reasoning is marked, not the verdict.

---

## Quick reference

**Inmon's definition.** A data warehouse is a **subject-oriented**, **integrated**, **time-variant**, **non-volatile** collection of data in support of management's decisions.

**Business Intelligence** is the set of processes, tools and reports that turn that data into decisions.

**OLTP vs OLAP**

| | OLTP | OLAP |
|---|---|---|
| Job | run the business | understand the business |
| Touches | a few rows, right now | millions of rows, over time |
| Optimised for | fast writes | fast reads and aggregation |
| Example | a cashier scans a packet of chips | the CEO compares 12 months of sales |

**The DW/BI architecture (Kimball)** — four components, in order:

```
Source Systems  →  ETL / Staging  →  Presentation Area  →  BI Applications
```

The restaurant metaphor: **source systems** are the farms, **ETL** is the kitchen, the **presentation area** is the serving counter, and **BI applications** are the diners' tables. Nobody eats in the kitchen.

---

## Task 1 — The messy sales log (`DWBI_W1_Messy_Sales_Log.csv`)

38 rows: one morning's orders from three branches, exactly as the branch systems exported them.

Columns: `OrderID`, `Branch`, `Date`, `Product`, `Category`, `Qty`, `Amount`.

**Do this:**

1. **Find at least six distinct problems** in this file. For each one give: the problem, one `OrderID` that shows it, and why it would break a report. "The data is messy" is not a problem; "the same branch is written four different ways, so `GROUP BY Branch` returns six branches instead of three" is.
2. **Say who fixes each one.** For every problem, assign it to exactly one owner and justify the choice in a sentence:

   | Owner | Fixes |
   |---|---|
   | Source system | faults that should never have been recorded in the first place |
   | ETL / staging | faults that can be corrected consistently on the way in |
   | The business | faults that need a human decision or a rule nobody has written yet |

3. **Answer the question the branch manager actually asked: what was the total Beverages revenue this morning?** Show your working. You will have to make decisions about the duplicate, the blank category, the return, and at least one amount that is obviously wrong. State every decision and its effect on the total.
4. **Give your answer a confidence level** — high, medium or low — and say what you would need in order to raise it.
5. **One sentence:** why can this file not simply be loaded into a dashboard as it is?

**Watch out for:** `Amount` is not a number in every row — some values carry `Rs` or a thousands separator, so a naive `SUM` either fails or silently skips them. Also look carefully at order `1008` against order `1001`: same product, same quantity, very different amount. One of them is wrong, and you must decide which.

**The question to answer:** two of your six problems could have been prevented at the point of data entry. Which two, and what single change to the branch system would have prevented each?

---

## Task 2 — OLTP or OLAP?

**Do this:**

1. **Classify all eight** of the following as OLTP or OLAP, with a one-line reason each. The reason matters more than the label.

   | # | Scenario |
   |---|---|
   | 1 | A cashier scans a packet of chips and prints the bill |
   | 2 | The CEO compares sales by category over the last 12 months |
   | 3 | A customer updates her phone number in the store app |
   | 4 | Marketing compares Eid week with a normal week, across all branches |
   | 5 | You withdraw Rs 5,000 from an ATM |
   | 6 | A bank finds customers whose balance fell three months in a row |
   | 7 | A rider marks a food order as delivered |
   | 8 | Head office ranks all branches by returns this quarter |

   Use the two-question test from the lecture: **how many records does it touch?** and **right now, or over time?**

2. **Write two scenarios of your own** from a Pakistani business you actually know — one clearly OLTP, one clearly OLAP — and explain what makes each one obvious.
3. **Write one genuinely borderline scenario** and argue both sides. Then say which system you would put it on and why. Borderline cases are where the real design decisions live.

**The question to answer:** the Superstore ran the CEO's report on the live checkout database and every billing counter in the country slowed down. In terms of what OLTP systems are optimised for, explain precisely *why* that happened — not just that it did.

---

## Task 3 — No history, and no single truth

Two separate failures of a live operational database. Both were demonstrated in the lecture.

**Do this:**

1. **No history — "Where did Ali's sales go?"** A salesperson, Ali, moved from the Lahore branch to Karachi in March. The live `Employee` table stores one row per employee with a single `Branch` column, which was overwritten on the day he moved. In April, the Lahore manager runs a report of last year's sales by branch and finds Ali's entire history has moved to Karachi.
   - Explain exactly which of Inmon's four properties this breaks, and why.
   - Describe, in plain words, what the warehouse does differently so that last year's report still credits Lahore.
   - Name one other business situation where silently overwriting a value would rewrite history.
2. **No single truth — three departments, three numbers.** Asked for "sales last month", Operations reports Rs 661.65 m, Finance reports Rs 283.70 m, and Sales reports Rs 584.75 m.
   - Give one plausible reason each department could arrive at a different figure while *no one is lying and no one has made an arithmetic error*.
   - Explain what a single staging area changes about this situation.
   - Who should own the definition of "sales last month" — and why not simply let each department keep its own?
3. **One paragraph:** a manager says, "we already have all this data in our systems, so why build a warehouse at all?" Answer them using the two failures above.

**The question to answer:** "non-volatile" is often explained as "we never delete anything". That is not quite what it means. Give a better one-sentence definition, and one example of data a warehouse *would* legitimately change.

---

## Task 4 — Place each item in the right stage

The four components of the DW/BI architecture: **Source Systems**, **ETL / Staging**, **Presentation Area**, **BI Applications**.

**Do this:**

1. **Place each of these eight items** in exactly one stage, with a one-line justification:

   | | Item |
   |---|---|
   | A | Removing duplicate orders |
   | B | CEO dashboard on a phone |
   | C | Branch POS billing system |
   | D | Sales star schema by date, branch, product |
   | E | HR team's staff Excel sheet |
   | F | Converting `CL-150` to `Cola 1.5L` |
   | G | Weekly PDF report emailed to managers |
   | H | Finance data mart |

   Two items belong in each stage.

2. **Draw the architecture yourself** — four boxes, arrows in the right direction, and your eight items placed in them. Hand-drawn and photographed is fine. Do not screenshot the slide.
3. **Extend the restaurant metaphor.** The lecture compared the architecture to a restaurant: farms, kitchen, serving counter, tables. Describe what each of these corresponds to, and what goes wrong in a real warehouse when it happens:
   - a diner wandering into the kitchen to grab food off the stove
   - the kitchen serving a dish without tasting it
   - two kitchens cooking the same dish to different recipes
4. **Kimball's goals.** Pick **three** of the goals a DW/BI system must meet and, for each, name something concrete in the Superstore case that would violate it.

**The question to answer:** item E is the HR team's own Excel sheet. Argue the case for treating it as a legitimate source system, and the case against. Which would you choose, and what would you require before trusting it?

---

## Task 5 — Hands-on: your first live connection (`DWBI_W1_Regional_Sales.xlsx`)

Three tables, January to June 2026:

| Sheet | Rows | Columns |
|---|---|---|
| `Sales` | 480 | `SaleID`, `SaleDate`, `ProductID`, `RegionID`, `Quantity`, `UnitPrice`, `SalesAmount` |
| `Products` | 15 | `ProductID`, `ProductName`, `Category`, `UnitPrice` |
| `Regions` | 4 | `RegionID`, `RegionName`, `HeadOffice`, `RegionalManager` |

**Before you load — answer these three in your document, before opening Power BI:**

1. Which column tells us *what product* was sold?
2. Where does the region's *name* live?
3. Your slicer is Product Category. Which table must it come from, and why not from `Sales`?

**Then do this:**

1. **Connect.** Get Data → Excel workbook → select all three sheets → **Load**. Confirm you have 480 / 15 / 4 rows. If a sheet loads with the wrong header row, fix it in Power Query, not by editing the file.
2. **Check the relationships.** Open Model view. Power BI will usually detect `ProductID` and `RegionID` itself. Verify both, and for each one write down: which table is the *one* side, which is the *many* side, and how you can tell. Fix any relationship it got wrong.
3. **Visualise.** A bar chart of **Total Sales by Region**. Region *name*, not `RegionID`. Sort it, and give it a title that states what you found rather than naming the axes.
4. **Slice.** Add a slicer on **Product Category** and a card showing **Total Sales**. Click through each category and watch both the chart and the card update.
5. **Validate** — and write the result of each check in your document:
   - the card with no slicer selected equals the sum of `SalesAmount` across all 480 rows;
   - selecting every category one at a time adds back up to that same total;
   - the underlying source file has not changed — slicing filters the view, it does not edit the data;
   - no error or blank values appear in any visual.
6. **Explore the interface.** Name the four main panes of Power BI Desktop and say in one line what each is for. Then name the three views down the left-hand side and when you would use each.

**Watch out for:** `UnitPrice` exists in both `Sales` and `Products`. Decide which one your report should use and justify it — in a real warehouse this is exactly the kind of duplication that produces two different "correct" answers. Also note that **Total Sales by Region** only works once the relationship to `Regions` exists; without it every region shows the same number, which is the single most common mistake in this task.

**Submit:** `DWBI_W1_<RollNo>.pbix`, plus a screenshot of the finished report page in your document.

**The question to answer:** you have just answered "which region sells most?" in about a minute, without anyone queuing at a checkout. Referring to Task 2, explain what made that possible — and what would have happened if you had run the same query against the live branch database at 6pm on a Friday.

---

## Marking guide

| | Weight |
|---|---|
| **Accuracy** — problems correctly identified, classifications right, totals and validations correct | 30% |
| **Logic** — reasoning is sound and the owner of each fix is justified, not guessed | 30% |
| **Application** — Power BI report connects, relates and validates correctly | 25% |
| **Creativity** — your own examples, your own diagram, a title that states a finding | 15% |

**Automatic deductions:**

- an answer copied from the lecture slides
- a data problem named without an `OrderID` that demonstrates it
- a total given without its working
- a report built on `RegionID` instead of `RegionName`
- a card total that does not reconcile with the source rows
- a screenshot of the lecture's architecture diagram submitted as your own
- the `.pbix` file missing, or saved without the report page
- changing `SEED` in `generate_week1_data.py`

---

## Before next week

Read **Kimball & Ross, *The Data Warehouse Toolkit*, Chapter 1**, and **Inmon, *Building the Data Warehouse*, Chapter 1**.

Week 2 takes the architecture you placed in Task 4 and builds it for real: three mismatched freight files, one staging area, and a single trusted table at the end.
