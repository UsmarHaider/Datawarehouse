# Week 5 — Assignments: The ETL Process

Seven tasks covering **Lecture 9** (what the three stages guarantee) and
**Lecture 10** (Power Query, live).

| | |
|---|---|
| **L9** | Formulate structured extract–transform–load workflows and identify where each stage fails — **CLO3 · Competence** |
| **L10** | Build reusable transformation steps that clean, restructure and load dimensional data — **CLO3 · Courage** |

The case continues from Week 2 and Week 4. **Week 2** opened three files, fixed
them by hand, and pasted the result into one sheet — a correct table and zero
reusable work. **Week 4** wired an empty star and left it waiting.

This week those two halves meet: you build the machine that loads the star.

The deliverable is **not the table**. Week 2 already produced the table. It is
the **seventeen steps, in order, with their names on them** — and the test of
it is that tomorrow night it runs without you. Tonight's file arrives at 02:00
and nobody is awake to paste it.

| Task | Covers | Marks |
|---|---|---|
| **T1** | Defect census: ten defects, each tied to a step and to loud or quiet | 12 |
| **T2** | Stage ownership: twelve activities, and the four that are violations | 12 |
| **T3** | Order the seventeen steps, and defend the three constraints | 20 |
| **T4** | Row arithmetic: 37 → 35 → 34, and every wrong total read from its gap | 15 |
| **T5** | The locale trap: twelve date strings, two locales | 12 |
| **T6** | Loud or quiet: six failures, and the check that converts each | 12 |
| **T7** | Definition of done. Eight checks, all eight must pass | 12 |
| | **Excel workbook total** | **95** |
| **Lab** | **Hands-on:** rebuild the Week 2 merge as a pipeline that reruns | separate |

---

## Setup

The data is already in `data/`. Nothing to generate.

| File | What it is |
|---|---|
| `PakFreight_W5_ETLLab_STUDENT.xlsx` | **Start here.** All seven tasks. Cream cells are yours to fill |
| `source/*` | **The three dirty files, unmodified.** 37 rows, ten defects. This is the input |
| `source/night2/*` | **The refresh test.** Same marine and rail; a road file your pipeline has never seen |
| `dims/*.csv` | The five dimensions from the Week 4 star. **Import them; do not rebuild them** |
| `alias_lookup.csv` | The 23-row alias map — to **check** your own against, not to import |

`FactShipment.csv` is deliberately **not** in this folder. Week 4 handed it to
you as a starting point; this week it is the finish line. Producing it is the
lab.

For the lab you need **Power BI Desktop**. On macOS or Linux use Power BI
Service or a lab machine, and say which in your submission. Power Query also
ships inside Excel (**Data → Get Data**) and every step in the lab guide works
there — say so if that is what you used.

**Or do it in Python.** See *The Python track* below. `pip install pandas
openpyxl`.

**Requirements:** Excel, LibreOffice Calc or Google Sheets for the workbook.
Every formula in it is `COUNTIF`, `COUNTA`, `SUM` and `IF` — nothing that needs
Excel 365.

> Do not open `night2/` until T7 part A is finished and all eight checks pass.
> It is there to test a pipeline, not to help you build one.

---

## How to work

**Teams of 3.** Name one person each:

| Role | Owns | Has to defend |
|---|---|---|
| **Extractor** | T1 and T2, and may not fix anything while reading | the census, and that extract corrected nothing |
| **Sequencer** | T3 | the run order, to a room that will disagree about it |
| **Reconciler** | T4 and T7, with veto power over "it looks fine" | every number, and the −1 count |

**Do T1 before T3.** You cannot order a pipeline against a mess you have not
counted. The workbook is ordered this way deliberately, and so is the session:
fifty-five minutes before anybody opens a tool.

**T3 is worth 20 marks** — more than any other task, and nine of them are the
three constraints. Ordering is the whole discipline of the week.

**Type only in cream cells.** Grey cells are given to you: the defect list, the
step list, the raw date strings, the alias map.

**T7 marks itself.** Every `✘ fix` means something earlier is still wrong. Go
and find it; do not adjust the check.

**Every number in the workbook came out of `data/source`.** So can yours. Open
the files and count — nothing here has to be taken on trust.

---

## The rules

- **Extract corrects nothing.** Thirty-seven rows arrive and thirty-seven rows
  land, blank line and `TOTAL` footer included. Fix anything on the way in and
  you have no untouched copy to prove the source against, and no way to tell a
  source problem from your own.
- **Shape, then text, then type, then keys.** Four words in that order. Every
  team that gets stuck this week will have tried to look up a key before
  trimming the value it is looking up.
- **Order is a mechanism, not a style.** Three orderings are forbidden and
  everything else is taste. Know which three, and know the number that each one
  costs you when you break it.
- **Name every step.** `RemovedTotalRow` tells the next person what
  `FilteredRows1` never will. It takes two seconds, it is the only
  documentation the pipeline will ever have, and it is marked.
- **A pipeline that reconciles is not the same as a pipeline that is right.**
  578,650 kg and PKR 4,808,000 are the weakest checks you have — a locale bug
  and a status casing bug both pass them to the rupee.
- **Nothing is dropped silently.** A row you cannot resolve goes to the Unknown
  member at `-1` and is **counted**. Deleting it is an answer, and you have to
  defend it in writing.
- **The totals must not move.** Cleaning data never changes what the business
  shipped.

---

## T1 · Defect census  (12 marks)

Ten defects across three files totalling thirty-seven lines. For each one:
which of the **four transform classes** fixes it (Structural, String, Type &
Unit, Conform), **which step** clears it, and whether ignoring it fails
**loudly or quietly**.

Use these definitions literally:

- **Loud** — the refresh errors, or a step fails outright, and somebody is told.
- **Quiet** — the load succeeds and a published number is wrong.

**You produce:** a class, a step and a verdict for all ten rows, plus one line
each on what breaks if you ignore it.

**Self-check (in the sheet):** exactly **1** of the ten fails loudly, **7**
fail quietly, and **1** does both.

> If your Loud count is 5 or 6 you are marking "I would notice that" as loud.
> The test is not whether a careful person would spot it — it is whether the
> **pipeline tells somebody**.

**One of the ten rows is not a defect at all.** Find it and say why it is on the
list. **4 of the 12 marks** are for that answer and for one on why defects 8 and
9 — the `TOTAL` footer and the repeated consignment — are judgements rather than
errors.

---

## T2 · Stage ownership  (12 marks)

Twelve activities. For each: **Extract**, **Transform**, **Load** — or
**Violation**, meaning one stage is doing another's job, or a job no stage may
do at all.

The value of the three-word name is that it **divides the blame**: when a
pipeline breaks you should be able to say which of the three stages broke. A
stage doing another stage's job makes that impossible, which is why the three
"must nots" are the part that gets skipped:

- Extract must not clean.
- Transform must not write to the source.
- Load must not decide anything.

**You produce:** a verdict and a reason for all twelve. One mark for the
verdict, one for the reason.

**Self-check (in the sheet):** **4** of the twelve are violations, and
**Transform** owns more of the rest than either other stage — which is not an
accident of how the list was written.

> The four violations are there to be found by argument, not by elimination.
> The other eight are real work that a real stage really owns.

**4 of the 12 marks** are for one paragraph on why staging is never
user-facing, naming the Power Query setting that enforces it.

---

## T3 · Order the seventeen steps  (20 marks)

The seventeen steps are listed **alphabetically**, not in run order. Put them in
an order that works, and for each one say which stage owns it and whether it
runs **per source** or **once** on the combined table.

**You produce:** a run-order number 1–17 used exactly once each, a stage, a
cadence, the defects that step clears, and one line on why it sits where you
put it.

**Self-check (in the sheet):** 3 extract + 10 transform + 4 load, and **10 run
per source** while **7 run once**.

> Getting the cadence column wrong is how a team ends up appending three
> already-deduplicated tables and still finding a duplicate. Ask of every step:
> *does this need information that only exists before the append?*

### The three constraints — 9 of the 20 marks

Three orderings are not negotiable. Name what each one costs you, **as a
number**:

| | Constraint | What breaking it costs |
|---|---|---|
| 1 | Rename before append | a fact table of **20 columns** |
| 2 | Trim before deduplicate | a duplicate that survives the dedup step |
| 3 | Convert before append | **283,695.25 kg** instead of 578,650 kg |

### And the question that separates a rule from a habit — 4 of the 20 marks

Run the dedup step **before** the trim step on tonight's road file and you
**still get 34 rows**. So why is "trim before dedup" a constraint and not a
preference?

> This is the hardest question in the workbook and it is worth answering
> properly. Look at the two `RD-505` rows before you answer it.

---

## T4 · Row arithmetic  (15 marks)

Every wrong total this week is 578,650 plus or minus something specific, and
the something tells you which step failed. Learn to read the gap.

### Part A · The ladder — 6 marks

Fill it in **from the files**, not from the slides.

| Stage | Rows | SUM(WeightKG) | SUM(FreightCostPKR) |
|---|---|---|---|
| marine, as extracted | ? | ? | ? |
| rail, as extracted | ? | ? | ? |
| road, as extracted | ? | ? | ? |
| raw rows landed in staging | ? | — | — |
| appended | ? | ? | ? |
| loaded into `FactShipment` | ? | **578,650** | **4,808,000** |

> The road row is the one that catches people: **fifteen rows land and thirteen
> survive**, and the road subtotal still has the duplicate inside it. That is
> why the road rung and the loaded rung differ by 6,100 kg and not by nothing.

### Part B · Read the gap — 9 marks

Three real totals a student has handed in. Work out the arithmetic that
produced each, then name the step that was missing or misplaced:

```
SUM(WeightKG) = 283,695.25 kg
SUM(WeightKG) = 584,750 kg
SUM(WeightKG) = 661,650 kg
```

Then two more symptoms that move **no total at all** — headers reading
`Column1, Column2, …`, and a fact table of 35 rows whose totals are both
exactly right. Name the cause of each.

> A row count is not a total, and a total is not a row count. That second
> symptom is the entire reason check 5 exists separately from checks 7 and 8.

---

## T5 · The locale trap  (12 marks)

The marine file writes its dates as text in `dd/MM/yyyy`. On a machine set to
United States regional settings, Power Query reads `01/02/2026` as the **second
of January**.

Fill in all twelve strings read **both ways**, then classify each row as
**Right by luck**, **Wrong month** or **Error**.

**Self-check (in the sheet):** **10** wrong, **1** right by accident, **1**
error — and the eleven readable rows land in **eleven different months**.

> August never appears, because nobody shipped on the 8th. If you can say why
> that matters, you have understood that "check the month list" and "check the
> range" are not the same check.

**6 of the 12 marks** are for three written answers:

1. Which of the three files is exposed to this, and how many loaded rows that
   puts at risk. (The other two are not exposed, and for two different
   reasons.)
2. Both reconciliation totals are exact and every monthly report is still
   wrong. Explain why the totals **cannot** catch it.
3. The single click that prevents it, and the check that catches it if you
   forget.

> This is the only defect of the ten that produces a plausible, confidently
> wrong answer with **no error message anywhere**. "The dates were wrong" earns
> nothing without naming the click.

---

## T6 · Loud or quiet  (12 marks)

Six failures — four scheduling accidents and two defects. For each: loud or
quiet, which of the eight checks would catch it, and what makes it safe.

A **loud** failure stops the run: a job goes red, somebody is paged, the
warehouse is unchanged, and the 08:00 report shows yesterday's number with a
stale-as-of stamp on it. Embarrassing, bounded, fixable before anyone trades on
it.

A **quiet** failure succeeds. Eleven rows went to Unknown, one region is
missing, the dates landed in the wrong month, and the dashboard is green.
Nobody finds out until a quarter closes.

**Self-check (in the sheet):** only **1** of the six is loud — and it is the one
you have no work to do about.

**4 of the 12 marks** are for the answer that is not the obvious one. Everybody
says they would rather have the loud failure. State what follows from that about
**where the engineering effort in a pipeline actually goes**.

> A pipeline that never fails is not reliable. It is unmonitored.

---

## T7 · Definition of done  (12 marks)

Refresh your model, read each number off it, and type it in. **All eight must
read "pass".** Submitting with a single `✘ fix` loses all 12 marks.

| # | Check | Expected |
|---|---|---|
| 1 | Contract columns in each of the three queries | 7 |
| 2 | Rail subtotal, in kilograms | **295,250** |
| 3 | Distinct values in `StatusRaw` | **3** |
| 4 | Latest day in `ShipDate` | **13** February 2026 |
| 5 | Rows in `FactShipment` | **34** |
| 6 | Rows carrying a `-1` city key | **0** |
| 7 | `SUM(WeightKG)` | **578,650 kg** |
| 8 | `SUM(FreightCostPKR)` | **PKR 4,808,000** |

**Checks 1 to 4 come first, and that is not an ordering accident.** Checks 7 and
8 are the famous ones and they are the weakest on the sheet. Work them in order
— if 7 fails, fix 2 and 5 first, because they cause it.

### Check 6 is the character question

Check 6 expects **0**, and that is the trap. Zero is right here only because the
alias map happens to cover all 23 spellings these three files contain. It is not
a law of nature, and **"0" typed without looking is the same answer as "0" typed
after looking.**

So the sheet asks *how you know* — and then asks what the same pipeline reports
on `night2`.

> Integrity is logging the rows you could not fix. Routing a row to Unknown is
> not forgiveness; dropping it quietly so the dashboard looks complete is a
> statement about you, not about the data.

### Part B · The refresh test

Point your three queries at `data/source/night2/` and press **Refresh**.
Nothing should need fixing. Then fill in six more numbers.

That folder holds the same marine and rail files and a road file you have never
seen: an extra consignment, a second copy of `RD-508` that differs from the
first by **one trailing space**, a status typed as `  DELAYED  `, and a shipment
from a city no alias resolves.

> If you get **36 rows and 591,550 kg**, you deduplicated before you trimmed.
> That is the T3 constraint arriving as a number, and nothing on the first
> night's file would ever have told you.

---

## The Python track

**You may do this lab in pandas instead of Power Query, and you are marked the
same.** Deck slides **33 to 37** are the Python section, and
[`PowerQuery_Lab_Guide.md`](PowerQuery_Lab_Guide.md) ends with an appendix
carrying the whole pipeline, ready to run.

Nothing about the task changes. The ten defects, the four transform classes,
the three ordering constraints and all eight checks are facts about **the
data**, not about the tool — so every number you have to hit is identical, and
T1 to T7 in the workbook were tool-agnostic to begin with.

The traps are all still there:

| Trap | In pandas |
|---|---|
| The locale | `pd.to_datetime("01/02/2026")` → **2026-01-02**. pandas guesses month-first and makes the exact mistake. Naive parsing spreads these 12 rows over **eleven months** |
| Append before rename | `pd.concat` of three un-renamed frames → **20 columns**, only `Status` shared, **no error** |
| Dedup before trim | night two loads **36 rows / 591,550 kg** instead of 35 / 584,950 |
| Tons before append | **283,695.25 kg**, short by 294,954.75 |

### What you must do instead of naming applied steps

There is no applied-steps pane, so four things are required in its place. Each
one loses the same mark its Power Query equivalent would:

| | Required | Instead of |
|---|---|---|
| 1 | A named `STEPS` list, keeping each intermediate frame so you can look at step 7 | renaming applied steps |
| 2 | `format="%d/%m/%Y"` stated explicitly — a bare `pd.to_datetime` loses the mark | Change Type **Using Locale** |
| 3 | `drop_duplicates(subset=["ShipmentID"])` — never bare | the Remove Duplicates dialog |
| 4 | `how="left"` then `fillna(-1)` — `how="inner"` drops the row and moves the total | Merge Queries, Left Outer |

Plus one that replaces **"Enable load, off"**: say which frames are
intermediate and which are published. No setting marks the staging boundary
for you, so you mark it yourself.

### What does not translate

- **Query folding** has no analogue. It is inert this week anyway — flat files
  have no engine to push work to — but it is the whole of Weeks 12 and 14, so
  read slide 23 regardless.
- **`Text.Clean`** has no single equivalent. Collapse whitespace with
  `.str.replace(r"\s+", " ", regex=True)`.
- **`dayfirst=True` is not the same as stating a format.** It is a hint pandas
  may override. State the format.

### Before you choose

The **Week 8 midterm practical** is an ingestion pipeline and a star, **under
time**, and Weeks 9 and 10 are Power BI visualization and DAX. A pandas
pipeline earns full marks here — and leaves you meeting Power Query cold in the
exam.

**The workbook's 95 marks are tool-agnostic. The lab is not.** If you are
unsure: do the workbook in either, and the lab in Power Query.

---

## The lab · Rebuild Week 2's merge as a pipeline

Full walkthrough in
[`PowerQuery_Lab_Guide.md`](PowerQuery_Lab_Guide.md) — nine steps, the M code
for all three queries, where every click lives, and a troubleshooting table
that reads a wrong total back to the step that caused it.

In outline:

| Step | What you do |
|---|---|
| 1 | Shape the rail workbook first: skip two title rows, **then** promote headers |
| 2 | Drop the road file's blank line and `TOTAL` footer — two named steps, not one |
| 3 | Rename all three into the seven-name contract |
| 4 | Trim, clean, Proper Case, uppercase, `RL-` prefix; dates **Using Locale**; tons × 1,000; `ModeKey` by source |
| 5 | Append the three, then deduplicate on `ShipmentID` — 35 in, 34 out |
| 6 | Split `RawAliases` into rows, merge **left outer** twice, expand, nulls → `-1` |
| 7 | Staging queries to connection-only, refresh, clear all eight checks |
| 8 | **The refresh test** against `night2` |
| 9 | If you finish early: `DateKey`, `StatusKey`, `RouteKey`, and build `DimRoute` yourself |

### How many applied steps you should have

| Query | Steps | Why it differs |
|---|---|---|
| `Road` | **11** | the reference query |
| `Marine` | **9** | no blank row and no `TOTAL` footer, so two filters do not exist |
| `Rail` | **13** | adds navigate-to-sheet, skip title rows, the `RL-` prefix, the tons conversion |
| `FactStaging` | **5** | append, dedup, merge, expand, replace nulls |

> If your marine query has eleven steps you have added two that do nothing, and
> a filter that removes nothing is **worse** than no filter: the next person
> reads it as evidence that the file has junk rows.

### Definition of done

- [ ] Three source queries, step counts as above, every step **named**
- [ ] `Marine`, `Rail`, `Road`, `AliasLookup` all connection-only
- [ ] Six tables in the model; ten queries behind it
- [ ] `AliasLookup` has **23** rows and **14** distinct keys, not 24
- [ ] Every date typed **Using Locale**, English (United Kingdom) — never plain
      Change Type
- [ ] Rail subtotal **295,250 kg** *before* the append
- [ ] All eight checks pass
- [ ] The `-1` count written down **as a number**, for both nights
- [ ] The refresh test run against `night2`, with a before-and-after screenshot
- [ ] **578,650 kg** and **PKR 4,808,000**, exactly

### Why the refresh is the point

Replace the three source files with next week's three, click **Refresh**, and
all sixteen steps replay: headers promoted, junk dropped, names conformed, tons
converted, duplicates removed, keys assigned, Unknown routed, star loaded.

Week 2 produced a table. Today you produce **the thing that produces the
table** — and if anything needs fixing by hand, your pipeline is still a
one-off.

---

## What you hand in

Due on the LMS **before Week 6**.

1. `W5_ETL_<team number>.xlsx` — all seven tasks, T7 reading **8 / 8** on the
   checks and **6 / 6** on the refresh test. Submitting with a single red cell
   loses all 12 marks for T7.
2. `W5_<roll number>.pbix` — the pipeline complete: three source queries with
   named applied steps, staging queries connection-only, six tables in the
   model, 34 fact rows, both totals exact.
   **Python track:** `W5_<roll number>.py` instead, with the named `STEPS` list,
   the eight checks as assertions, and the `-1` count printed.
3. **The written part, which carries more than the clicks:**
   - what makes two rows a duplicate, and why that test cannot run before the
     trim;
   - what happens to a row whose city you cannot resolve, and why that is not
     "delete it";
   - the `-1` count, as a number, for both the first night and `night2`;
   - the before-and-after screenshot of the refresh test.
4. The individual quick check is done on paper in class, not submitted here.

**Marks: 95 in the workbook + 12 in the paper quick check.** These feed the
Hands-on Exercises component (20% of the course) against CLO3.

> `.pbix` files are gitignored in this repository on purpose. Submit through the
> LMS, not by committing.

---

## References

- **Kimball & Ross (2013)**, *The Data Warehouse Toolkit*, 3rd ed. — Ch. 19 on
  the ETL subsystems, of which this week builds about nine; Ch. 20 on staging,
  dependency order and the audit columns Week 6 adds; Ch. 3 §"Dimension Table
  Attributes" for conformed values and the Unknown member from first
  principles.
- **Kimball & Caserta (2004)**, *The Data Warehouse ETL Toolkit* — the whole
  book on this one week. Chapters 4 and 5 on cleaning, conforming and
  error-event handling are the source of the reject-table argument.
- **Inmon (2005)**, *Building the Data Warehouse*, 4th ed. — the normalized,
  enterprise-first counterpoint, and a much stronger case for the staging layer
  than Kimball bothers to make.
- **Microsoft Learn** — "Power Query M formula language reference", "Query
  folding guidance", "Best practices when working with Power Query", "Shape and
  combine data in Power BI Desktop".
- **Kimball Group** — "The 34 Subsystems of ETL". The short article version,
  and the clearest one-page map of everything a production pipeline eventually
  needs.

---

## One sentence to leave with

Week 2 cleaned a file and Week 5 built the thing that cleans it, so the
deliverable was never the table: it is the seventeen steps, in order, with
their names on them — because those are what still work tomorrow night at two
in the morning when nobody is watching.
