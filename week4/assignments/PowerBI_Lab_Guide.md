# PakFreight Week 4 — Power BI Lab Guide

**Data Warehousing & Business Intelligence · Week 4 — Dimensional Modeling · CLO2**
BS Data Science, Semesters 7 & 8 · Faculty of Computer Science & IT, The Superior University, Lahore

---

## What you are building

Six tables arrive with **no relationships between them**. By the end of this
lab they are a working star: six relationships, one of them inactive, every
cross-filter direction Single, and both Week 3 totals still reconciling to the
kilogram and the rupee.

You should have **T4 of the workbook filled in before you start.** If you do
not, stop and go and do it. The whole point of this week is that the register
comes first and the clicking comes second.

**Time:** steps 1–6 in the 40-minute lab. Steps 7–9 are homework.

---

## Setup — import the six unlinked tables

Everything is in `data/star/`:

```
FactShipment.csv    34 rows   six foreign keys, one degenerate key, three measures
DimCity.csv         15 rows   14 cities + Unknown; Province and Region as COLUMNS
DimDate.csv         28 rows   gapless February 2026
DimRoute.csv        21 rows   20 corridors + Unknown
DimMode.csv          4 rows   marine, rail, road + Unknown
DimStatus.csv        4 rows   delivered, in transit, delayed + Unknown
```

**Home → Get data → Text/CSV**, once per file. Load all six. Do **not** let
Power BI combine them, and do not open the Model view yet.

> If you would rather carry on from your own Week 3 `.pbix`, that is fine and
> the task is identical. The CSVs exist so that a broken Week 3 file cannot
> cost you Week 4.

---

## Step 1 — turn off the guessing (30 seconds, and it is the most important step)

**File → Options and settings → Options → Current File → Data Load**

Clear both:

- ☐ Autodetect new relationships after data is loaded
- ☐ Update or delete relationships when refreshing data

Autodetect wires relationships on column name and type. It is right often
enough that you stop looking, and then one wrong relationship propagates into
every visual and you spend the lab debugging a chart instead of a model.

If Power BI already created relationships on import, delete every one of them
in Model view before you continue. You are building all six yourself.

---

## Step 2 — check the keys before you draw a single line

In **Model view**, click each table and check the key columns in the
Properties pane. Every `*Key` column must be **Whole Number**.

| Table | Column | Must be |
|---|---|---|
| FactShipment | `DateKey`, `OriginCityKey`, `DestCityKey`, `RouteKey`, `ModeKey`, `StatusKey` | Whole Number |
| DimCity | `CityKey` | Whole Number |
| DimDate | `DateKey` | Whole Number |
| DimRoute | `RouteKey` | Whole Number |
| DimMode | `ModeKey` | Whole Number |
| DimStatus | `StatusKey` | Whole Number |

A text key joined to a numeric key either fails outright or coerces silently,
and silent is worse. Fix the type in **Power Query → Transform → Data Type**,
not with a calculated column.

Then confirm the dimension keys are **unique and never blank**. In Power Query,
select `CityKey` and read the **Column distribution** profile: 15 distinct, 15
unique, 0 empty. If a dimension key is not unique, Power BI will set the
cardinality to many-to-many by itself — and if that happens, the fault is
upstream in the load, not in the dialog.

---

## Step 3 — build the six relationships

**Model view → Manage relationships → New**, six times. Use the dialog every
time. Do not drag columns and accept what Power BI offers.

Each one: dimension column on the left, fact column on the right,
**Cardinality: Many to one (\*:1)**, **Cross-filter direction: Single**.

| # | One side | Many side | Active? |
|---|---|---|---|
| 1 | `DimDate[DateKey]` | `FactShipment[DateKey]` | Yes |
| 2 | `DimCity[CityKey]` | `FactShipment[OriginCityKey]` | Yes |
| 3 | `DimCity[CityKey]` | `FactShipment[DestCityKey]` | **No — inactive** |
| 4 | `DimRoute[RouteKey]` | `FactShipment[RouteKey]` | Yes |
| 5 | `DimMode[ModeKey]` | `FactShipment[ModeKey]` | Yes |
| 6 | `DimStatus[StatusKey]` | `FactShipment[StatusKey]` | Yes |

**Create relationship 3 anyway.** Power BI will accept it and mark it
inactive — a dashed line. Read the message if it warns you. That dashed line is
the model telling you the truth: with both active, a filter on `DimCity` has
two routes into the fact and no defined meaning.

When you finish, Model view should show **five solid lines and one dashed
line**, and nothing should be arrowed in both directions.

---

## Step 4 — resolve the two city roles

Pick **one** of these three and write one line in T4 part B saying why. All
three are defensible; none is defensible without a reason.

### Answer 1 — activate per measure

Leave relationship 3 inactive and switch it on inside the one measure that
needs it:

```dax
Weight to Destination City =
CALCULATE(
    [Total Weight],
    USERELATIONSHIP( FactShipment[DestCityKey], DimCity[CityKey] )
)
```

Cheapest in memory. Every destination measure needs its own `USERELATIONSHIP`,
and a report reader cannot tell from the model that it exists.

### Answer 2 — two role-playing tables (recommended for this lab)

Load `DimCity` a second time and rename both copies. In Power Query:

1. Right-click the `DimCity` query → **Reference**.
2. Rename the reference to `DimDestCity`.
3. Rename the original to `DimOriginCity`.
4. **Close & Apply.**

Then relationship 2 becomes `DimOriginCity[CityKey] → FactShipment[OriginCityKey]`
and relationship 3 becomes `DimDestCity[CityKey] → FactShipment[DestCityKey]`,
and **both can be active**.

Costs a little memory on a 15-row table, which is nothing, and the slicers
read correctly without anybody writing DAX. A slicer labelled `DimCity` that
silently means origin is a reporting bug waiting to happen.

### Answer 3 — flatten onto the fact

Put `OriginCityName` and `DestCityName` on the fact row in Power Query and drop
one relationship. Only defensible if nothing will ever group by city — which is
false here, because step 8 groups by destination province.

---

## Step 5 — make DimDate behave like a date table

Two things, and reports look broken without either.

1. Select `DimDate` → **Table tools → Mark as date table** → date column
   `FullDate`.
2. Select `DimDate[MonthName]` → **Column tools → Sort by column** →
   `MonthNumber`.

Without step 2, your months sort **April, August, December, February…** and
students lose marks every year to it. Week 3 built this dimension gapless
precisely so this works: 8 February has a row even though nothing shipped that
day, so February is a continuous axis rather than a list of the days that
happened to have freight on them.

---

## Step 6 — five measures

**Home → New measure**, five times. Explicit measures, not implicit drag-and-sum.

```dax
Total Weight     = SUM( FactShipment[WeightKG] )

Total Cost       = SUM( FactShipment[FreightCostPKR] )

Shipment Count   = SUM( FactShipment[ShipmentCount] )

Cost per KG      = DIVIDE( [Total Cost], [Total Weight] )

Distinct Cities  = DISTINCTCOUNT( FactShipment[OriginCityKey] )
```

`Cost per KG` must be `DIVIDE(SUM, SUM)` — **not** `AVERAGE` of a per-row
ratio. Week 3 proved the difference: 8.31 the right way, 8.06 the wrong way,
on the same 34 rows, with no error raised. A ratio is non-additive and cannot
be re-aggregated.

`DISTINCTCOUNT` on the fact's key column is how you answer "how many cities
appear in the data at all" **without** touching cross-filter direction. Reach
for the measure before you reach for the model.

---

## Step 7 — hide every key from Report view

In Model view, right-click each key column → **Hide in report view**:

- all six `*Key` columns on `FactShipment`
- `CityKey`, `DateKey`, `RouteKey`, `ModeKey`, `StatusKey` on the dimensions
- `OriginCityKey` and `DestCityKey` on `DimRoute`

Leave `ShipmentID` visible — it is a degenerate dimension and a user may
legitimately want to look one up.

A business user should never be offered `CityKey` as something to chart. A
summed surrogate key is a number that looks like data and means nothing.

---

## Step 8 — build the report page that proves it works

1. A **matrix**: `Province` on rows (from `DimCity` / `DimOriginCity`),
   `MonthName` on columns (from `DimDate`), `Total Weight` in values.
2. A **slicer** on `DimMode[ModeName]`.
3. Two **cards**: `Total Weight` and `Total Cost`.
4. A **table**: `ShipmentID`, `Total Weight`, `Cost per KG`.

Now click the slicer. Every visual must respond, and nothing must throw an
error or a loop warning.

**Why this matrix is the payoff:** `Province` is a *column on DimCity*, not a
table. A matrix grouped by province needs **no extra join** — which is exactly
the argument the whole first half of the session made. In a snowflaked model
the same matrix would cost two joins instead of one, and a country-level
version three instead of one.

If you chose answer 2 in step 4, also add a second matrix with
`DimDestCity[Province]` on rows, and confirm the two matrices disagree — they
should, because shipments go *from* four provinces and *to* five.

---

## Step 9 — reconcile, then fill in T7

Read these off your model and type them into T7. Thirteen checks, all thirteen
must pass.

| # | Check | Expected |
|---|---|---|
| 1 | Relationships in the model | 6 |
| 2 | Relationships with cardinality \*:1 | 6 |
| 3 | Relationships with cross-filter Single | 6 |
| 4 | Active relationships | 5 |
| 5 | Inactive relationships | 1 |
| 6 | Rows in FactShipment | 34 |
| 7 | `SUM(WeightKG)` | **578,650 kg** |
| 8 | `SUM(FreightCostPKR)` | **PKR 4,808,000** |
| 9 | Blank rows across all five dimensions | 0 |
| 10 | Distinct origin provinces in the fact | 4 |
| 11 | WeightKG for Sindh origins | 484,350 |
| 12 | WeightKG for Punjab origins | 44,100 |
| 13 | WeightKG for Balochistan origins | 44,100 |

> If you used role-playing tables, checks 1–5 become 7 relationships with 6
> active and 0 inactive. Say so in T7 and the check is marked on your register,
> not on the table above.

**Checks 7 and 8 are the ones that matter.** If they fail, the model is wrong
and the data is not. These two numbers have been true since Week 2 and were
verified against the source before any brief was written. Restructuring a
schema never changes what the business shipped.

---

## Definition of done

- [ ] Autodetect off, and no relationship you did not create yourself
- [ ] Six relationships, every one **Many to one**, every one **Single**
- [ ] Exactly one active path between any two tables (one dashed line)
- [ ] Every key column **Whole Number**; dimension keys unique and non-blank
- [ ] `DimDate` marked as a date table; `MonthName` sorted by `MonthNumber`
- [ ] Five explicit measures; `Cost per KG` uses `DIVIDE(SUM, SUM)`
- [ ] Every key hidden from Report view; `ShipmentID` left visible
- [ ] The matrix responds to the Mode slicer with no loop warning
- [ ] **578,650 kg** and **PKR 4,808,000**, exactly
- [ ] T4 register and T7 reconciliation both complete in the workbook

---

## Troubleshooting

| Symptom | Most likely cause | Fix |
|---|---|---|
| Every visual shows the same total, ignoring the slicer | No relationship, or cross-filter pointing the wrong way | Model view: is there a line at all? Then check its direction |
| Power BI refuses to create a relationship | It would close a loop or create ambiguity | Read the message. One path is already covered — leave it inactive |
| A relationship came out as \*:\* on its own | The dimension-side key is not unique | Fix it in Power Query. Do **not** override the cardinality |
| A slicer shows an empty `(Blank)` entry | An unmatched fact key, and no Unknown member | Route unmatched keys to `−1`, as Week 3 did |
| Totals right, province subtotals short | The blank-row problem — weight attributed to nothing | Same fix. Check 9 before you trust checks 7 and 8 |
| Months sort April, August, December… | `MonthName` is text and is not sorted by `MonthNumber` | Step 5 |
| The matrix is empty | Measure and grouping sit on tables with no path between them | Trace the path in Model view, dimension to fact, hop by hop |
| `Cost per KG` reads 8.06, not 8.31 | You averaged a ratio instead of dividing two sums | `DIVIDE([Total Cost], [Total Weight])` |

**Debug in this order: keys → relationships → measures → visuals.** Students
debug in exactly the reverse order and lose the lab to it. If the keys are
wrong, nothing downstream can be right, and a chart is the last place the cause
will ever be.

---

## Submission

`W4_<roll number>.pbix` on the LMS, before Week 5.

`.pbix` files are gitignored in the course repository on purpose — submit
through the LMS, not by committing. Include the step-4 justification as a text
box on the report page or in the model description, so the reason is in the
file and not only in your head.
