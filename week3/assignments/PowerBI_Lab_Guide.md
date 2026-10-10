# PakFreight Week 3 — Power BI Lab Guide

**Steps 1–4 in class · steps 5–7 as homework, due before Week 4**
Submit as `W3_<roll number>.pbix`

---

## Where you start

Open your **Week 2 `.pbix`**. It already contains `Stg_Marine`, `Stg_Rail`,
`Stg_Road` and the appended `Shipments_Unified` query.

- `Shipments_Unified` is your fact source: 34 rows, eight text-and-number
  columns, no keys. By the end of this lab it becomes `FactShipment` with six
  integer keys.
- **Nothing from Week 2 gets deleted.** The staging queries stay, disabled
  from load, exactly as you left them. That is Week 2's architecture doing its
  job.

If your Week 2 file did not survive the week, start from
`data/Shipments_Unified.csv` in this folder and say so in your submission.

Before you touch anything: **File ▸ Options ▸ Current File ▸ Data Load ▸
uncheck "Autodetect new relationships after data is loaded".** Power BI
guesses from column names and will happily join `DimCity` to `DimRoute`. You
are drawing all six relationships by hand.

---

## Step 1 · DimDate — a blank query, not a source file

**New Source ▸ Blank Query ▸ Advanced Editor**, and paste this:

```m
let
    Start = #date(2026, 2, 1),
    N     = Duration.Days(#date(2026, 2, 28) - Start) + 1,
    Dates = List.Dates(Start, N, #duration(1, 0, 0, 0)),
    T     = Table.FromList(Dates, Splitter.SplitByNothing(), {"FullDate"}),
    Typed = Table.TransformColumnTypes(T, {{"FullDate", type date}}),
    Keyed = Table.AddColumn(Typed, "DateKey", each
                Date.Year([FullDate]) * 10000
              + Date.Month([FullDate]) * 100
              + Date.Day([FullDate]), Int64.Type)
in
    Keyed
```

Then add the rest by clicking:

- **Add Column ▸ Date ▸** Year, Quarter, Month, Day, Day of Week, Name of
  Month, Name of Day.
- **Add Column ▸ Conditional Column ▸** `IsWeekend` = `Yes` if *Name of Day*
  is Saturday or Sunday, else `No`.
- **Add Column ▸ Conditional Column ▸** `IsHoliday` = `Yes` if *FullDate*
  equals 5 February 2026 (Kashmir Day), else `No`.

Two settings that are **not optional**:

| Do this | Where | What silently breaks if you skip it |
|---|---|---|
| **Mark as date table**, on `FullDate` | Model view ▸ select DimDate ▸ Table tools | Every DAX time-intelligence function returns wrong results with no warning |
| **Sort MonthName by MonthNumber** | Select MonthName ▸ Column tools ▸ Sort by column | Your charts run April, August, December… |

**Expect 28 rows.** If you get 12, you generated only the dates that appear in
the fact table — rebuild from the M code. A date dimension with holes is not a
date dimension.

---

## Step 2 · DimCity — four clicks and one judgement call

1. **Reference, do not duplicate.** Right-click `Shipments_Unified` ▸
   **Reference**. A reference reads the same source once; a duplicate re-reads
   the three files.
2. **Keep two columns, then unpivot.** Keep `Origin` and `Destination` ▸
   select both ▸ **Unpivot Columns** ▸ remove the `Attribute` column, keep
   `Value`. Every location string from either column is now one row.
3. **Remove duplicates, then conform.** *Remove Duplicates* gives **23** rows.
   Add a **Conditional Column** mapping each raw string to its conformed
   `CityName`, then *Remove Duplicates* again → **14** rows.
   This is the judgement call, and it is yours. The decisions that matter:
   - Karachi Port, Port Qasim, Karachi Cantt and Pipri Marshalling Yard are
     four facilities in **one city**.
   - Gwadar Port is in **Balochistan**, not Sindh. Getting this wrong makes
     Sindh/Marine read 206,500 kg instead of 169,000 kg.
   - Islamabad is **Islamabad ICT**, not Punjab.
4. **Add the index, starting at 1.** Add Column ▸ Index Column ▸ **From 1**.
   Rename to `CityKey`, set type to Whole Number. You have just minted your
   first surrogate keys.
5. Add `Province`, `Region`, `IsPortCity` and `FacilityType` as conditional
   columns. A 14-row dimension costs nothing — be generous.
6. **Add the `-1` Unknown row.** Home ▸ Enter Data for a one-row table, then
   Append it. Every dimension in this model gets one.

---

## Step 3 · DimRoute — and the trap in the brief

Reference `Shipments_Unified` again, keep `Origin` and `Destination`, and
*Remove Duplicates*.

**You will get 30 rows, not 20.** The lecture brief says 20.

Stop here and work out why before you go on. Task **T5 Block A** in the Excel
workbook asks you to write the reason down in your own words, and it is worth
3 marks — so do that task first, or at least commit to an answer now.

Then build it in this order:

1. Merge against `DimCity` on `Origin` → expand `CityKey` → rename
   `OriginCityKey`. Merge again on `Destination` → `DestCityKey`.
2. Also expand the conformed `CityName` both times, as `OriginCity` and
   `DestCity`.
3. *Now* Remove Duplicates on `OriginCityKey` + `DestCityKey` → **20 rows**.
4. Add a custom column: `RouteName = [OriginCity] & " -> " & [DestCity]`.
5. Remove the raw `Origin` and `Destination` columns.
6. Add Index from 1 → `RouteKey`. Add `Corridor` and `DistanceBand` as
   conditional columns — neither was in the source data, and inferring them is
   exactly the editorial work a dimension designer does.
7. Append the `-1` Unknown row.

If step 3 still gives you 30, you have done the operations in the wrong order.
Check what each row of `DimRoute` is supposed to mean before you add the index
— a surrogate key minted for something that is not a real thing is a row that
will sit in every report from now on, and nothing in the model will flag it.

---

## Step 4 · DimMode and DimStatus — typed by hand

**Home ▸ Enter Data.** These are *reference data*, not source data. Four rows
each, including Unknown.

**DimMode**

| ModeKey | ModeName | Carrier | TonnageClass | CostProfile | IsContainerised |
|---|---|---|---|---|---|
| 1 | Marine | PakFreight Shipping Ltd | Heavy (10–25 t) | Low cost / slow | Yes |
| 2 | Rail | Pakistan Railways Freight | Bulk (25–35 t) | Medium cost / medium | Partial |
| 3 | Road | PakFreight Trucking | Light (5–8 t) | High cost / fast | No |
| −1 | Unknown | Unknown | Unknown | Unknown | Unknown |

**DimStatus**

| StatusKey | StatusName | IsClosed | IsException | DisplayOrder |
|---|---|---|---|---|
| 1 | Delivered | Yes | No | 1 |
| 2 | In Transit | No | No | 2 |
| 3 | Delayed | No | Yes | 3 |
| −1 | Unknown | No | Yes | 99 |

`DisplayOrder` is not decoration: set `StatusName` to **Sort by column
DisplayOrder** and every visual in the report orders itself correctly without
anyone thinking about it.

---

## Step 5 · Merge the keys into the fact  *(homework)*

Select `Shipments_Unified` ▸ **Home ▸ Merge Queries**, once per dimension:

| Merge against | On | Expand | Rename to |
|---|---|---|---|
| DimCity | `Origin` → raw-string column | `CityKey` | `OriginCityKey` |
| DimCity | `Destination` → raw-string column | `CityKey` | `DestCityKey` |
| DimRoute | `OriginCityKey` + `DestCityKey` | `RouteKey` | `RouteKey` |
| DimMode | `SourceSystem` → `ModeName` | `ModeKey` | `ModeKey` |
| DimStatus | `Status` → `StatusName` | `StatusKey` | `StatusKey` |

Add `DateKey` as a custom column rather than a merge:
`Date.Year([ShipDate])*10000 + Date.Month([ShipDate])*100 + Date.Day([ShipDate])`

### The three merge settings that matter

| Setting | Choose | Why | What breaks if you get it wrong |
|---|---|---|---|
| **Join kind** | **Left Outer** | Keep all 34 fact rows whatever happens on the lookup side | An inner join drops unmatched rows and your total silently falls below 578,650 kg |
| **Fuzzy matching** | **Off** | Conforming is an explicit, auditable mapping — not a guess | "Karachi" fuzzy-matches "Karachi Cantt" today and something else tomorrow |
| **Columns to expand** | **the key only** | The dimension owns the descriptive text, not the fact | Expanding `CityName` puts text back in the fact table and defeats the whole exercise |

Then **Replace Errors with −1** on every key column. A row whose context
nobody recognised must land somewhere visible and countable, not vanish.

---

## Step 6 · Clean up before you load  *(homework)*

Remove `Origin`, `Destination`, `SourceSystem` and `Status` from
`Shipments_Unified`. Add `ShipmentCount = 1` as a custom column. Rename the
query to `FactShipment`.

Confirm the column list reads exactly:

```
DateKey · OriginCityKey · DestCityKey · RouteKey · ModeKey · StatusKey
ShipmentID · WeightKG · FreightCostPKR · ShipmentCount
```

Six keys, one degenerate dimension, three measures. Ten columns, 34 rows. Then
**Close & Apply**.

If any column holding a city name, a mode name or a status word is still
there, you have not finished step 6.

---

## Step 7 · Wire the relationships  *(homework)*

Model view. Draw all six by hand.

| From (fact) | To (dimension) | Cardinality | Cross-filter | Active? | Why |
|---|---|---|---|---|---|
| `FactShipment[DateKey]` | `DimDate[DateKey]` | * : 1 | Single | **Yes** | The only date relationship; time intelligence needs it active |
| `FactShipment[OriginCityKey]` | `DimCity[CityKey]` | * : 1 | Single | **Yes** | The primary city role — filters default to origin |
| `FactShipment[DestCityKey]` | `DimCity[CityKey]` | * : 1 | Single | **No** | Second role on the same table, so it must be **inactive** — reach it with `USERELATIONSHIP` |
| `FactShipment[RouteKey]` | `DimRoute[RouteKey]` | * : 1 | Single | **Yes** | Independent of DimCity — keeps the star flat rather than snowflaked |
| `FactShipment[ModeKey]` | `DimMode[ModeKey]` | * : 1 | Single | **Yes** | Four rows on the one side; Power BI warns if they are not unique |
| `FactShipment[StatusKey]` | `DimStatus[StatusKey]` | * : 1 | Single | **Yes** | Same pattern; `DisplayOrder` controls the sort on every visual |

### The two settings students get wrong

- **Never set cross-filter to Both.** It is offered, it looks harmless, and it
  creates ambiguous filter paths the moment you add a second fact table.
  Single direction, always.
- **Never let Power BI auto-detect.** You turned that off at the start of this
  guide. Keep it off.

### The five measures

```dax
Total Weight KG = SUM ( FactShipment[WeightKG] )

Total Freight   = SUM ( FactShipment[FreightCostPKR] )

Shipment Legs   = SUM ( FactShipment[ShipmentCount] )

Shipments       = DISTINCTCOUNT ( FactShipment[ShipmentID] )

Cost per KG     = DIVIDE ( [Total Freight], [Total Weight KG] )
```

`Cost per KG` must be `DIVIDE` of two sums. If you write
`AVERAGEX(FactShipment, DIVIDE([FreightCostPKR], [WeightKG]))` you get 8.06
instead of 8.31 — the 3% error from T3, now wearing a dashboard.

### Hide the plumbing

Select every key column in the fact **and** in all five dimensions and set
**Hide in report view**. A business user should never see `DateKey` or
`CityKey`; they should see Month, Province and Mode. A model that needs
explaining is a model that will be used wrongly.

### Write the grain into the model

Select `FactShipment` ▸ Properties ▸ **Description**, and type your grain
statement:

> One row per shipment leg dispatched by PakFreight.

This is marked. A model whose grain exists only in someone's memory is a model
whose grain will be broken by the next person to touch it.

---

## Validate before you trust

Build a **matrix**: `Province` on rows, `ModeName` on columns,
`Total Weight KG` in values. Then check every one of these.

| Check | Expected | If you get something else |
|---|---|---|
| Row count of FactShipment | **34** | A merge used Inner instead of Left Outer |
| Grand total, Total Weight KG | **578,650 kg** | Rail is still in tonnes, or the rd-505 duplicate is back |
| Grand total, Total Freight | **PKR 4,808,000** | Same causes, or a blank/TOTAL row survived staging |
| Shipment Legs | **34** | A measure problem — check `ShipmentCount = 1` on every row |
| Rows in DimCity | **14** (+ Unknown) | Your conforming map is incomplete |
| Rows in DimRoute | **20** (+ Unknown) | You deduped raw strings instead of conformed keys |
| Rows in DimDate | **28** | You generated only the dates in the fact table |
| Sindh / Marine | **169,000 kg** | 206,500 means you mapped Gwadar Port to Karachi |
| Punjab / Road | **44,100 kg** | Check Islamabad is *not* mapped to Punjab |
| Sindh, all modes | **484,350 kg** | 83.7% of everything. Lower means a Karachi alias is still its own city |
| Cost per KG, grand total | **PKR 8.31** | 8.06 means you averaged a ratio |
| Blank row in any dimension | **none** | A null key slipped through — map blanks to −1 |

Reconciliation is not a formality. It is the only moment at which you can
still find the mistake cheaply.

---

## Bonus · role-playing dimensions

Your matrix is built on `OriginCityKey`. Read the **Khyber Pakhtunkhwa** row:
it is **zero**. PakFreight moved 61,900 kg *into* Peshawar and Abbottabad in
February and nothing out of them. The number is correct; the conclusion a
reader draws from it — "KP is not part of our network" — is false.

Fix it two ways and compare.

**Option A · `USERELATIONSHIP` in DAX**

```dax
Weight to Destination =
CALCULATE (
    [Total Weight KG],
    USERELATIONSHIP ( FactShipment[DestCityKey], DimCity[CityKey] )
)
```

One measure, one model, both questions answerable. Now rebuild the matrix with
`Weight to Destination` and KP reads 61,900 kg.

**Option B · two physical role tables**

Duplicate `DimCity` as `DimDestinationCity`, both active. Simpler for users to
understand, and it costs you a second copy of the dimension and a second place
for the conforming map to drift out of date.

**Which would you choose, and why?** One paragraph in your submission. There
is a defensible answer either way — what is marked is whether you name the
trade-off.

---

## Definition of done

- [ ] Six tables in the model view: `FactShipment` + five dimensions
- [ ] Six relationships, all many-to-one, all single-direction, exactly one inactive
- [ ] Every key column hidden from report view
- [ ] Five explicit measures, with `Cost per KG` using `DIVIDE` of two sums
- [ ] `DimDate` marked as a date table, `MonthName` sorted by `MonthNumber`
- [ ] A `-1` Unknown row in all five dimensions
- [ ] Grain statement typed into the `FactShipment` description
- [ ] A matrix of Province × Mode totalling **578,650 kg** exactly
- [ ] No column anywhere in `FactShipment` holding descriptive text
- [ ] Saved as `W3_<roll number>.pbix`
