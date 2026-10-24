# PakFreight Week 5 — Power Query Lab Guide

**Data Warehousing & Business Intelligence · Week 5 — The ETL Process · CLO3**
BS Data Science, Semesters 7 & 8 · Faculty of Computer Science & IT, The Superior University, Lahore

---

## What you are building

Three dirty files go in. One clean, keyed, 34-row fact table comes out — and
then you point the same queries at a file you have never seen, press
**Refresh**, and nothing needs fixing.

Week 2 produced the table. This week you produce **the thing that produces the
table**, and that is the entire difference between an answer and a pipeline.

The deliverable is **sixteen named applied steps**: eleven on each source
query and five on the combined one. Not the clicks — the steps, with names you
would be happy to defend in a review.

**Before you start:** T3 of the workbook should be filled in. If it is not,
stop and go and do it. Fifty-five minutes before anybody opens a tool, and the
reason is on slide 5 — a student who starts clicking first builds a pipeline
shaped like the mess in front of them, and a student who designs first builds
one shaped like the destination.

**Time:** steps 1–7 in the 40-minute lab. Steps 8 and 9 are homework.

---

## Setup — what to import, and what not to

| What | Where | How |
|---|---|---|
| The three sources | `data/source/` | **unmodified** — this is the input, not a working copy |
| The five dimensions | `data/dims/` | import them; **do not rebuild them** |
| `alias_lookup.csv` | `data/` | **do not import.** You build this yourself in step 6 — the file is there so you can check you got 23 rows and 14 keys |

**Home → Get data → Text/CSV** for the four CSVs, **Excel workbook** for the
rail file. Then **Transform Data** to open Power Query, and do not close it
again until step 7.

> `FactShipment.csv` is deliberately **not** in this folder. Producing it is
> the entire lab. If you find a copy of it, you have found the answer and
> skipped the week.

Four things to set before you touch a query:

1. **File → Options → Current File → Data Load**: clear *Autodetect new
   relationships*. You will build relationships from your Week 4 register.
2. **File → Options → Global → Regional Settings**: note what it says. If it
   is anything other than English (United Kingdom), step 4 is about to matter
   to you personally.
3. **File → Options → Global → Power Query Editor**: tick *Display the
   formula bar*. You cannot learn M from dialogs you cannot see.
4. Rename the three source queries `Marine`, `Rail`, `Road`. Not `Query1`.

---

## Step 1 — shape the rail workbook first, because it is the awkward one

Start with the hard file. If you start with marine you will build a habit that
the rail file then breaks.

The rail sheet has **two title rows above the real header**:

```
Column1                                      Column2
Pakistan Railways Freight — Consignment …    null
Period: February 2026   |   Weights in TONS  null
Consignment No                               Dispatch Date      <- the real header
45012                                        2026-02-03
```

Promote headers now and `Pakistan Railways Freight — Consignment Register`
becomes a column name. So:

1. **Home → Remove Rows → Remove Top Rows → 2**
2. **Transform → Use First Row as Headers**

```m
Skipped  = Table.Skip(Sheet, 2),
Promoted = Table.PromoteHeaders(Skipped)
```

Rename the steps **`SkippedTitleRows`** and **`PromotedHeaders`**. Do this for
every step from here on — it takes two seconds, it is the only documentation
the pipeline will ever have, and it is marked.

Then do the marine and road queries: **Transform → Use First Row as Headers**,
and nothing else structural, because neither file has title rows.

---

## Step 2 — drop the junk rows, and only in the file that has them

The **road** file alone carries a blank line and a `TOTAL` footer. The TOTAL
row holds 83,000 kg, and if it loads it is counted as a shipment — slide 42's
661,650 kg.

Filter the ID column twice:

```m
NoBlanks = Table.SelectRows(Renamed, each
             [ShipmentID] <> null and [ShipmentID] <> ""),
NoTotal  = Table.SelectRows(NoBlanks, each
             Text.Upper(Text.Trim([ShipmentID])) <> "TOTAL")
```

Name them **`RemovedBlankRows`** and **`RemovedTotalRow`**. `FilteredRows1`
tells the next person nothing.

> **Why two steps and not one?** Because they are two different decisions. A
> blank row is dirt in every pipeline that will ever read this file. A TOTAL
> footer is a *grain* problem — it is information to a human reading the
> spreadsheet and a different grain to a fact table at one-row-per-shipment.
> Two reasons, two named steps, and the names say which is which.

Row count after this step: **marine 12, rail 10, road 13.**

---

## Step 3 — rename all three into the seven-name contract

This is the step that makes the append on step 5 work, and it has to happen
**before** it.

| The contract | marine | road | rail |
|---|---|---|---|
| `ShipmentID` | `Shipment_ID` | `trip_id` | `Consignment No` |
| `ShipDate` | `Ship_Date` | `trip_date` | `Dispatch Date` |
| `OriginRaw` | `Origin_Port` | `from_city` | `From Station` |
| `DestRaw` | `Dest_Port` | `to_city` | `To Station` |
| `WeightKG` | `Weight_KG` | `weight_kg` | `Weight (Tons)` ← **not kg** |
| `FreightCostPKR` | `Cost_PKR` | `cost_pkr` | `Freight Charges (PKR)` |
| `StatusRaw` | `Status` | `status` | `Status` |

Double-click each header, or do them all at once in the formula bar:

```m
Renamed = Table.RenameColumns(NoTotal, {
    {"trip_id","ShipmentID"}, {"trip_date","ShipDate"},
    {"from_city","OriginRaw"}, {"to_city","DestRaw"},
    {"weight_kg","WeightKG"}, {"cost_pkr","FreightCostPKR"},
    {"status","StatusRaw"} })
```

Name it **`RenamedToContract`**.

On the rail query, rename `Weight (Tons)` to **`WeightTons`**, not `WeightKG`.
Naming it `WeightKG` while it still holds tons is how a pipeline lies to the
person maintaining it.

> **If you skip this step and append anyway:** seven names each, and only
> `Status` shared by marine and rail, so you get a fact table of **twenty
> columns** with two thirds of every one of them empty. No error. No warning.
> Append keeps a column present in one table and missing in another and fills
> it with null.

---

## Step 4 — text, then types and units, in that order

### 4a · Trim, clean, case

**Transform → Format**, four operations:

| Column | Operation | Why |
|---|---|---|
| `OriginRaw`, `DestRaw` | Trim | they feed a lookup in step 6 |
| `StatusRaw` | Clean, then Trim, then Capitalize Each Word | 17 strings → 3 |
| `ShipmentID` | UPPERCASE | `rd-505` → `RD-505`, matching the star |

```m
Trimmed = Table.TransformColumns(Renamed, {
    {"OriginRaw",  Text.Trim},
    {"DestRaw",    Text.Trim},
    {"StatusRaw",  each Text.Proper(Text.Trim(Text.Clean(_)))},
    {"ShipmentID", Text.Upper} })
```

Two things students get wrong here:

- **Trim does not touch interior whitespace.** `In  Transit` survives it and
  still fails the lookup. That is what **Replace Values** is for.
- **Clean and Trim are not the same operation,** and a tab character is
  invisible on screen. If a value looks right and still will not match, it is
  one of these two.

On the rail query only, add the `RL-` prefix:

```m
Prefixed = Table.TransformColumns(Trimmed, {
    {"ShipmentID", each "RL-" & Text.From(_), type text} })
```

Rail consignment numbers arrive as bare integers — `45012` — and the star
stores `RL-45012`. This is the one place all week where you **change a value's
meaning on purpose**, so name the step **`PrefixedRailIDs`** and be able to say
why.

### 4b · Dates, with the locale stated out loud

**Transform → Data Type → Using Locale → Date → English (United Kingdom).**

Never plain **Change Type** on a date column. Not once, not on the road file
that happens to be ISO, not ever — because the habit is the whole lesson.

```m
Typed = Table.TransformColumnTypes(Prefixed, {
    {"ShipDate", type date},
    {"FreightCostPKR", Int64.Type} }, "en-GB")
```

The `"en-GB"` is a literal argument in the M. That is what makes the query
correct on **any** machine in any regional setting, and it is why the step is
worth a click more than the alternative.

What it is defending you against, on the twelve marine rows:

```
'01/02/2026'   en-GB -> 2026-02-01  correct
'01/02/2026'   en-US -> 2026-01-02  WRONG, and silent
'02/02/2026'   en-US -> 2026-02-02  right by luck
'13/02/2026'   en-US -> Error       no month 13
```

Ten rows in the wrong month, one right by accident, one error — and **both
reconciliation totals still pass to the rupee.** Only every date-based report
is wrong.

### 4c · Tons to kilograms, in a step of its own

On the rail query, **Add Column → Custom Column**, or:

```m
ToKg    = Table.AddColumn(Typed, "WeightKG",
            each [WeightTons] * 1000, Int64.Type),
Dropped = Table.RemoveColumns(ToKg, {"WeightTons"})
```

Name it **`ConvertedTonsToKG`**. Do not fold it into the typing step and do not
do it after the append — the rail subtotal must read **295,250 kg** before
anything is combined, and that is check 2.

### 4d · ModeKey, which no source carries

**Add Column → Custom Column**, one constant per query:

```m
WithMode = Table.AddColumn(Typed, "ModeKey", each 1, Int64.Type)   // marine
                                             each 2               // rail
                                             each 3               // road
```

This is defect 10 and it is not a defect: no file carries a transport mode, so
the pipeline assigns one from **which query the row came through**. Some
warehouse columns are produced by the pipeline rather than carried by the
source.

> **Why ModeKey is added per source and not once on the combined table:** once
> the three queries are appended there is nothing left to tell you where a row
> came from. The information exists only before the append, which is exactly
> why the step has to run there.

### How many steps you should have, and why the three queries differ

Slide 22 counts **eleven applied steps on each source query**. That is exactly
right for the **road** query — the one slide 31 prints in full — and your other
two should *not* match it:

| Query | Steps | Why it differs from road's eleven |
|---|---|---|
| `Road` | **11** | the reference query: source, promote, rename, 2 junk filters, trim, case, upper, 2 type steps, mode |
| `Marine` | **9** | no blank row and no TOTAL footer, so the two junk filters do not exist |
| `Rail` | **13** | adds navigate-to-sheet, skip title rows, the `RL-` prefix and the tons conversion |

If your marine query has eleven steps you have added two that do nothing, and a
filter that removes nothing is worse than no filter: the next person reads it
as evidence that this file has junk rows.

Read all three in **View → Advanced Editor** before you go on. You will never
debug a pipeline from the dialogs alone, and the midterm asks you to explain a
step, not to find it in a menu.

---

## Step 5 — append, then deduplicate, in that order

**Home → Append Queries as New → Three or more tables** → Marine, Rail, Road.
Name the new query `FactStaging`.

Row count: **35**. Thirty-seven raw rows, less the blank line and the TOTAL
footer.

Then **Home → Remove Rows → Remove Duplicates** — but not on the whole row.
Select the `ShipmentID` column first:

```m
NoDupes = Table.Distinct(Appended, {"ShipmentID"})
```

Row count: **34**. That is the star's fact row count, and it is check 5.

> **Read this even if your number is already 34.** On tonight's road file the
> two `RD-505` rows are byte-identical, so an exact whole-row comparison
> catches them too, and both rules give 34. **That is luck, not correctness.**
> Deduplicate on a business key, after the trim and the uppercase, for two
> reasons: the IDs themselves need the trim and the case before they compare at
> all, and the moment one copy of a repeated row differs by a space, a case or
> a reformatted date, whole-row comparison keeps both and the total goes up.
> `data/source/night2` is that file. Step 9 is where you find out.

---

## Step 6 — conform the names, then trade them for keys

A fact row must carry **integer keys** — never a city name, never a status
word. Twenty-three spellings go in; fourteen keys and an Unknown come out.

### 6a · Build the alias lookup

`DimCity` already carries the mapping, in `RawAliases`:

```
CityKey  CityName   RawAliases
1        Karachi    Karachi Port | Port Qasim | Karachi Cantt |
                    Pipri Marshalling Yard | Karachi
3        Lahore     Lahore Dry Port | Lahore
-1       Unknown    (empty — this is the catch-all)
```

Reference `DimCity` into a new query called `AliasLookup`, then:

1. **Home → Choose Columns** → `CityKey` and `RawAliases` only.
2. **Transform → Split Column → By Delimiter → Custom `" | "` → Advanced
   options → Split into *Rows*.**
3. Trim the result, and **filter out the blank** the Unknown row leaves behind.

```m
Split   = Table.ExpandListColumn(
            Table.TransformColumns(Kept, {
              {"RawAliases", Splitter.SplitTextByDelimiter(" | ")}}),
            "RawAliases"),
Trimmed = Table.TransformColumns(Split, {{"RawAliases", Text.Trim}}),
NoBlank = Table.SelectRows(Trimmed, each
            [RawAliases] <> null and [RawAliases] <> ""),
Renamed = Table.RenameColumns(NoBlank, {{"RawAliases","RawSpelling"}})
```

**Fifteen dimension rows split into 24, and 23 survive.** The twenty-fourth is
the Unknown row's empty alias list. If you skip the filter you have a blank
spelling in your lookup, every blank city name in a future file will match it,
and those rows will silently become `CityKey = -1` *without ever being
counted* — which is the one failure this whole week is written against.

Check it against `data/alias_lookup.csv`: **23 rows, 14 distinct keys.**

### 6b · Merge, twice, and keep every row

**Home → Merge Queries** on `FactStaging[OriginRaw]` against
`AliasLookup[RawSpelling]`, **Join Kind: Left Outer**. Expand, take **only**
`CityKey`, rename it `OriginCityKey`. Then do the whole thing again for
`DestRaw` → `DestCityKey`.

```m
MergedOrg = Table.NestedJoin(NoDupes, {"OriginRaw"},
              AliasLookup, {"RawSpelling"}, "O", JoinKind.LeftOuter),
ExpandOrg = Table.ExpandTableColumn(MergedOrg, "O", {"CityKey"},
              {"OriginCityKey"}),
MergedDst = Table.NestedJoin(ExpandOrg, {"DestRaw"},
              AliasLookup, {"RawSpelling"}, "D", JoinKind.LeftOuter),
ExpandDst = Table.ExpandTableColumn(MergedDst, "D", {"CityKey"},
              {"DestCityKey"})
```

### 6c · Null becomes −1

**Right-click the key column → Replace Values → null → -1**, both columns:

```m
Filled = Table.ReplaceValue(ExpandDst, null, -1,
           Replacer.ReplaceValue, {"OriginCityKey","DestCityKey"})
```

**Three decisions in those three clicks, and all three are marked:**

- **Why Left Outer, not Inner.** An inner join drops unmatched rows. A shipment
  to a city you do not recognise is still a shipment that happened, and
  dropping it moves the 578,650. Left outer keeps every row and makes the
  problem visible.
- **Why −1, not blank.** A blank key joins to nothing, so the row vanishes from
  every breakdown while still counting in the grand total. −1 joins to a row
  that says **Unknown**, out loud.
- **And it still goes in the log.** Routing to Unknown is not forgiveness.
  Every row that took the −1 branch is counted, and the count is written down.
  On tonight's files that count is **0**. Check it anyway; see step 9.

> Forgetting to **expand** the merged column is the most common first-time
> mistake in this tool. A column of `Table` values is not a key.

---

## Step 7 — load, and prove it

### 7a · Staging queries to connection-only

**Right-click → Enable load, off** on `Marine`, `Rail`, `Road` and
`AliasLookup`.

They still run on refresh and still feed the queries below them — they just do
not appear as tables. **Six tables in the model, ten queries behind it.** Load
them and you ship your own working surface into the semantic layer for users
to find, which is the staging-tier violation from slide 18.

### 7b · Close & Apply, then the eight checks

| # | Check | Expected | How |
|---|---|---|---|
| 1 | Contract columns in each query | 7 | read the headers |
| 2 | Rail subtotal in kg | **295,250** | filter `ModeKey = 2`, `SUM(WeightKG)` |
| 3 | Distinct `StatusRaw` values | **3** | slicer, count the entries |
| 4 | Latest day in `ShipDate` | **13 Feb 2026** | slicer, read the range |
| 5 | Rows in FactShipment | **34** | card, `COUNTROWS` |
| 6 | Rows on a −1 city key | **0** | slice each key, find Unknown |
| 7 | `SUM(WeightKG)` | **578,650** | card, no filters |
| 8 | `SUM(FreightCostPKR)` | **4,808,000** | card, no filters |

**Checks 1 to 4 come first, and that is not an ordering accident.** Checks 7
and 8 are the famous ones and they are also the weakest — a locale bug and a
status casing bug both pass them perfectly. A pipeline that reconciles is not
the same as a pipeline that is right.

If a check fails, go to the troubleshooting table at the bottom. Do not adjust
the check.

---

## Step 8 — the refresh test, and it is the whole point

Take the **night-two** folder: `data/source/night2/`.

Same marine file, same rail file, and a road file you have never seen. It has
an extra consignment, a second copy of `RD-508` that differs from the first by
**one trailing space**, a status typed as `  DELAYED  `, and a shipment from
**Chaman Border** — a city no alias in `DimCity` resolves.

Point your three source queries at that folder and press **Refresh**.

**Nothing should need fixing.** What your model must then report:

| After refresh | Expected | What it proves |
|---|---|---|
| Rows in FactShipment | **35** | the dedup rule survived a duplicate that is not byte-identical |
| `SUM(WeightKG)` | **584,950** | every per-source step replayed on an unseen file |
| `SUM(FreightCostPKR)` | **4,860,000** | the same, for the second fact |
| Distinct `StatusRaw` | **3** | `  DELAYED  ` was trimmed and cased without you touching a step |
| Rows on a −1 key | **1** | the left outer join kept the row instead of dropping it |
| Rows with status `Delayed` | **5** | four last night, five tonight — the breakdown moved, correctly |

**If you get 36 rows and 591,550 kg,** you deduplicated before you trimmed and
the second `RD-508` survived on a trailing space. That is the constraint from
T3 arriving as a number, and nothing on the first night's file would ever have
told you.

**Which city went to −1, and what you do about it.** `Chaman Border` is not in
the alias map. Write it down with the row count beside it. You should add it to
`DimCity` **tomorrow, deliberately, with somebody who knows** whether Chaman
Border is its own city or a border post belonging to Quetta. But tonight's
report cannot wait for that conversation, and a pipeline that stops for every
new spelling is a pipeline nobody runs.

Take a screenshot of the before-and-after totals. It is part of the submission.

---

## Step 9 — if you finish early (homework, unmarked)

The sixteen steps get you a keyed table with city keys. Three keys are still
missing and `DimRoute` is still Week 4's file rather than yours:

1. **`DateKey`.** Add Column → Custom:
   `Date.Year([ShipDate]) * 10000 + Date.Month([ShipDate]) * 100 + Date.Day([ShipDate])`,
   typed as whole number. Gives `20260205`. **Merge Columns would also get you
   there** — year, month, day joined and typed — but merge is lossy in one
   direction, so prefer the arithmetic for a key and keep merge for
   presentation.
2. **`StatusKey`.** The same merge pattern as step 6, against `DimStatus`
   on `StatusName`, nulls to −1.
3. **`RouteKey`.** Merge against `DimRoute` on the origin/destination key pair.
4. **Build `DimRoute` yourself.** Group the keyed fact on `OriginCityKey` and
   `DestCityKey`, take the distinct pairs, merge the city names back in, and
   build `RouteName` as `Karachi -> Lahore` — a **Merge Columns** with `" -> "`
   as the separator. Twenty pairs, plus Unknown.

That last one is next week's warm-up, done today.

---

## Troubleshooting — read the total, name the cause

Every wrong total is arithmetic, not mystery. Each one is 578,650 plus or minus
something specific, and the something tells you which step failed.

| What you see | The arithmetic | The cause, and the fix |
|---|---|---|
| Headers read `Column1`, `Column2` … | — | rail: you promoted before skipping two title rows. Remove Top Rows 2, *then* promote |
| The appended table has 20 columns | 7 + 7 + 7, only `Status` shared | you appended before renaming. Rename into the contract first — step 3 before step 5 |
| `SUM(WeightKG)` = **283,695.25** | 206,500 + 76,900 + 295.25 | the rail tons were never multiplied by 1,000. Convert before the append |
| `SUM(WeightKG)` = **584,750** | 578,650 + 6,100 | duplicate `RD-505` survived. Remove Duplicates on `ShipmentID`, after the trim |
| `SUM(WeightKG)` = **661,650** | 578,650 + 83,000 | the road `TOTAL` footer loaded as a shipment. Filter it out in the road query |
| 35 rows but both totals exactly right | — | the blank road row loaded. It carries no weight and no cost, so it moves `COUNTROWS` and neither total — and it will appear as `(Blank)` in every slicer |
| Dates appear in January, March and May | 10 wrong, 1 lucky, 1 error | plain Change Type on a `dd/MM/yyyy` column. Delete the step and redo it **Using Locale, en-GB** |
| The status slicer offers 17 choices | 17 instead of 3 | trim, clean or Proper Case missing — or a conditional column written above them |
| A key column shows `Table` not a number | — | you merged and forgot to expand |
| Rows disappeared and the total dropped | — | you chose Inner instead of Left Outer on step 6 |
| `AliasLookup` has 24 rows, not 23 | 23 + the Unknown row's blank | filter out the empty spelling after the split |
| Refresh fails: "column not found" | — | you renamed a column but a later step still names the old one. Read the step it names — this is the one defect of the ten that fails **loudly**, and it is doing you a favour |

### The debugging order that saves the lab

**Shape, then text, then type, then keys — and debug in that same order.**

Click the **earliest** applied step and look at the table there. The first step
whose output is wrong is the step with the bug, and it is almost never the last
one you added. The pane exists so that you can look instead of guess.

Ask for help once you can state three things: the symptom, the step you
stopped at, and the number you expected. That sentence usually contains the
answer.

---

## Definition of done

- [ ] Three source queries — road 11 steps, marine 9, rail 13 — every name one
      you would defend in a review
- [ ] `FactStaging` with five more: append, dedup, merge, expand, replace nulls
- [ ] `Marine`, `Rail`, `Road`, `AliasLookup` all connection-only
- [ ] Six tables in the model; ten queries behind it
- [ ] All eight checks pass
- [ ] The −1 count written down — as a number, not as "none"
- [ ] The two written rules from slide 39: what makes two rows a duplicate and
      why that test cannot run before the trim; and what happens to a row whose
      city you cannot resolve, and why that is not "delete it"
- [ ] The refresh test run against `night2`, with the before-and-after
      screenshot

**Submit** `W5_<roll number>.pbix` plus the written rules, the −1 count and the
screenshot, on the LMS before Week 6.

---

# Appendix · The Same Pipeline, In Python

**Slides 33 to 37.** If you are doing the lab in pandas instead of Power Query,
this appendix is your version of steps 1 to 8. Everything else in this guide —
the contract, the order, the constraints, the eight checks, the refresh test —
applies unchanged, because those are facts about the data and not about the
tool.

**You are marked the same.** The four things we ask for instead of the
applied-steps pane are on slide 36 and repeated at the bottom of this appendix.

## Requirements

```bash
pip install pandas openpyxl
```

`openpyxl` is what lets pandas read the rail `.xlsx`.

## The whole pipeline

This runs as written, from the folder that contains `data/`. It produces 34
rows, 578,650 kg and PKR 4,808,000, and the fact table it builds is identical
to Week 4's `FactShipment.csv`.

```python
"""PakFreight Week 5 — the seventeen steps, in pandas."""
from pathlib import Path
import pandas as pd

SOURCE = Path("data/source")      # the only line you change for the refresh test
DIMS = SOURCE.parent / "dims"

CONTRACT = ["ShipmentID", "ShipDate", "OriginRaw", "DestRaw",
            "WeightKG", "FreightCostPKR", "StatusRaw"]

RENAME = {
    "marine": {"Shipment_ID": "ShipmentID", "Ship_Date": "ShipDate",
               "Origin_Port": "OriginRaw", "Dest_Port": "DestRaw",
               "Weight_KG": "WeightKG", "Cost_PKR": "FreightCostPKR",
               "Status": "StatusRaw"},
    "road":   {"trip_id": "ShipmentID", "trip_date": "ShipDate",
               "from_city": "OriginRaw", "to_city": "DestRaw",
               "weight_kg": "WeightKG", "cost_pkr": "FreightCostPKR",
               "status": "StatusRaw"},
    "rail":   {"Consignment No": "ShipmentID", "Dispatch Date": "ShipDate",
               "From Station": "OriginRaw", "To Station": "DestRaw",
               "Weight (Tons)": "WeightTons",
               "Freight Charges (PKR)": "FreightCostPKR", "Status": "StatusRaw"},
}
MODE = {"marine": 1, "rail": 2, "road": 3}


# ---------------------------------------------------------------- E1-E2 extract
def extract(src, name):
    if name == "rail":
        return pd.read_excel(src / "rail_shipments.xlsx",
                             sheet_name="Rail", skiprows=2)
    return pd.read_csv(src / f"{name}_shipments.csv")


# ----------------------------------------------------------- T1-T7 per source
def transform(df, name):
    df = df.rename(columns=RENAME[name])                      # T2
    ids = df.ShipmentID.astype("string").str.strip()          # T1
    df = df[ids.notna() & (ids != "") & (ids.str.upper() != "TOTAL")].copy()

    for c in ("OriginRaw", "DestRaw"):                        # T3
        df[c] = df[c].astype("string").str.strip()
    df["StatusRaw"] = (df.StatusRaw.astype("string")          # T3 + T4
                       .str.replace(r"\s+", " ", regex=True)
                       .str.strip().str.title())

    if name == "rail":                                        # slide 35
        df["ShipmentID"] = "RL-" + df.ShipmentID.astype(int).astype(str)
        df["WeightKG"] = df.WeightTons * 1000                 # T6
        df = df.drop(columns=["WeightTons"])
        df["ShipDate"] = pd.to_datetime(df.ShipDate)          # real date values
    else:
        df["ShipmentID"] = df.ShipmentID.astype("string").str.strip().str.upper()
        fmt = "%d/%m/%Y" if name == "marine" else "%Y-%m-%d"  # T5 — STATE IT
        df["ShipDate"] = pd.to_datetime(df.ShipDate, format=fmt)

    df["WeightKG"] = df.WeightKG.astype("int64")
    df["FreightCostPKR"] = df.FreightCostPKR.astype("int64")
    df["ModeKey"] = MODE[name]                                # T7
    return df[CONTRACT + ["ModeKey"]]


# ------------------------------------------------------- T10 the alias lookup
def alias_lookup():
    dim = pd.read_csv(DIMS / "DimCity.csv")
    out = (dim[["CityKey", "RawAliases"]]
           .assign(RawAliases=lambda d: d.RawAliases.str.split(" | ", regex=False))
           .explode("RawAliases"))
    out["RawAliases"] = out.RawAliases.str.strip()
    out = out[out.RawAliases.notna() & (out.RawAliases != "")]
    return out.rename(columns={"RawAliases": "RawSpelling"})


# ----------------------------------------------------- T8-T10 once, combined
def pipeline(src=SOURCE):
    parts = [transform(extract(src, n), n) for n in ("marine", "rail", "road")]
    fact = pd.concat(parts, ignore_index=True)                # T8
    appended = len(fact)
    fact = fact.drop_duplicates(subset=["ShipmentID"])        # T9
    alias = alias_lookup()                                    # T10
    for raw, key in (("OriginRaw", "OriginCityKey"),
                     ("DestRaw", "DestCityKey")):
        fact = fact.merge(alias.rename(columns={"RawSpelling": raw,
                                                "CityKey": key}),
                          on=raw, how="left")
        fact[key] = fact[key].fillna(-1).astype("int64")
    return fact.reset_index(drop=True), appended
```

## The eight checks, as assertions

A card visual tells you a number. An assertion refuses to let the run finish.

```python
fact, appended = pipeline()

assert list(fact.columns[:7]) == CONTRACT                       # 1  seven names
assert fact[fact.ModeKey == 2].WeightKG.sum() == 295_250        # 2  tons converted
assert fact.StatusRaw.nunique() == 3                            # 3  not 17
assert set(fact.ShipDate.dt.month) == {2}                       # 4  the locale
assert fact.ShipDate.dt.day.max() == 13                         # 4  the range
assert len(fact) == 34                                          # 5  rows
assert fact.WeightKG.sum() == 578_650                           # 7
assert fact.FreightCostPKR.sum() == 4_808_000                   # 8

# 6 is COUNTED and REPORTED, never asserted — see below
minus_one = ((fact.OriginCityKey == -1) | (fact.DestCityKey == -1)).sum()
print(f"rows routed to Unknown: {minus_one}")
```

Write `set(...) == {2}` and not `fact.ShipDate.dt.month.unique() == [2]`. The
second one looks equivalent and **raises `ValueError: The truth value of an
array with more than one element is ambiguous`** precisely when the locale bug
it is meant to catch is present — so it sends you debugging the assertion
instead of the dates.

### Why check 6 is a `print` and not an `assert`

Because the right answer is not a constant. On the three night-one files it is
**0**, but only because `DimCity`'s alias map happens to cover all 23 spellings
those files contain. An assertion would fail the whole run the first time a new
city spelling appears — and a pipeline that stops for every new spelling is a
pipeline nobody runs.

So the count is reported, and written on your submission. That is slide 43
arriving as a line of code: integrity is logging the rows you could not fix.

## The refresh test

One changed constant, nothing else:

```python
night2, _ = pipeline(SOURCE / "night2")

assert len(night2) == 35
assert night2.WeightKG.sum() == 584_950
assert night2.FreightCostPKR.sum() == 4_860_000
assert night2.StatusRaw.nunique() == 3
assert int((night2.StatusRaw == "Delayed").sum()) == 5

unresolved = sorted(set(night2.loc[night2.OriginCityKey == -1, "OriginRaw"])
                    | set(night2.loc[night2.DestCityKey == -1, "DestRaw"]))
print(f"rows to Unknown: {len(unresolved)}  {unresolved}")   # 1  ['Chaman Border']
```

If `len(night2)` comes out **36** and the weight **591,550**, you deduplicated
before you trimmed and the second `RD-508` survived on a trailing space.

## Your applied-steps pane, if you write one

Power Query gave you four things free: repeatable, inspectable, reviewable,
portable. A script is already repeatable, reviewable and portable. The one you
lose is **inspectable** — and twelve lines get it back:

```python
STEPS = [("Source",             read),
         ("RenamedToContract",  rename),
         ("RemovedBlankRows",   drop_blank),
         ("RemovedTotalRow",    drop_total),
         ("TrimmedTextColumns", trim),
         # ...
         ]

frames = {}
for name, fn in STEPS:
    df = fn(df)
    frames[name] = df.copy()      # now look at frames["TrimmedTextColumns"]
```

Named steps, in order, with every intermediate table still there to look at
when step 9 is wrong. **Debug by looking, not by guessing** — the same method
as clicking step 7 in the pane, and the same debugging order: shape, then text,
then type, then keys.

## What we ask for instead of the pane

| | Requirement | Marked the same as |
|---|---|---|
| 1 | A **named step list** as above | renaming applied steps |
| 2 | An **explicit date format** — `format="%d/%m/%Y"` | Change Type **Using Locale** |
| 3 | **`drop_duplicates(subset=["ShipmentID"])`** — never bare | dedup on the business key |
| 4 | **`how="left"` then `fillna(-1)`** — never `how="inner"` | left outer, then null → −1 |

Plus one that replaces "Enable load, off": say in a comment or a short note
**which frames are intermediate and which are published**. There is no setting
that marks the staging boundary for you, so you mark it yourself.

## Things that do not translate

- **Query folding** has no analogue. It is inert this week anyway — flat files
  have no engine to push work to — but it is the whole of Weeks 12 and 14, so
  read slide 23 even though you will not use it here.
- **`Text.Clean`** has no single equivalent. `.str.replace(r"\s+", " ",
  regex=True)` collapses runs of whitespace, which covers tabs and the double
  space inside `In  Transit`; for genuine control characters use
  `.str.replace(r"[\x00-\x1f]", "", regex=True)`.
- **`dayfirst=True`** is *not* the same as stating a format. It is a hint pandas
  may override on ambiguous input. State the format.

## One thing to weigh before you choose

The Week 8 midterm practical is an ingestion pipeline and a star, **under
time**, and Weeks 9 and 10 are Power BI visualization and DAX. A pipeline
written in pandas earns full marks here — and leaves you meeting Power Query
cold in the exam.

The workbook's 95 marks are tool-agnostic. The lab is not. If you are unsure,
do the workbook in either and the lab in Power Query.

---

## One sentence to leave with

Week 2 cleaned a file and Week 5 built the thing that cleans it, so the
deliverable was never the table: it is the sixteen steps, in order, with their
names on them — because those are what still work tomorrow night at two in the
morning when nobody is watching.
