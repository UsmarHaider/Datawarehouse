# Week 2 — DW Lifecycle & Architecture

Datasets and assignments for Week 2.

← [Back to the course index](../README.md)

| Lecture | Topic | Outcome | CLO | 3C |
|---|---|---|---|---|
| **L3** | Architectural foundations | Describe the standard tiers of a data warehouse architecture and its lifecycle development phases | CLO1 | Competence |
| **L4** | Data ingestion | Perform structured file imports from heterogeneous sources into a BI tool environment | CLO1 | Courage |

## The case

**PakFreight** moves cargo three ways, and each mode keeps its own file in its own format. Three teams, three totals, zero trust. The week ends with one trusted table.

No setup needed — the data is already in `assignments/data/`.

## Contents

| Path | What it is |
|---|---|
| `assignments/TASKS.md` | Five tasks and the marking guide |
| `assignments/data/marine_shipments.csv` | 12 rows · `dd/mm/yyyy` · **KG** · UPPERCASE status |
| `assignments/data/rail_shipments.xlsx` | 10 rows · 2 title rows above the header · **TONS** · numeric IDs |
| `assignments/data/road_shipments.csv` | 15 rows · 12 trips + duplicate + blank + TOTAL row |
| `assignments/data/PakFreight_Activity_STUDENT.xlsx` | The Data Detective workbook — yellow cells to fill |

> The teacher key is **not** in this repository, and `.gitignore` blocks `*_KEY*`, `*TEACHER*` and `*ANSWER*` from ever being committed here.

## Assignments

| Task | Covers |
|---|---|
| 1 | The three tiers, Inmon's four properties, EDW vs ODS, independent vs dependent marts |
| 2 | Inmon vs Kimball, both architectures drawn, ten scenarios, the lifecycle, SDLC vs CLDS |
| 3 | **Data Detective** — profile the raw files, reproduce the four totals, trace the lineage |
| 4 | **Hands-on:** build staging → storage → presentation in Power BI |
| 5 | Latency, schema drift, lineage, BI roles, and the responsibility map |

Full briefs in [`assignments/TASKS.md`](assignments/TASKS.md).

## The contract

Task 4 bends all three sources into one schema:

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

## Expected results

Every figure below was verified against the three source files before this brief was written.

| Source | Raw records | Removed | Loaded | Weight (kg) |
|---|---|---|---|---|
| Marine | 12 | 0 | 12 | 206,500 |
| Rail | 10 | 0 | 10 | 295,250 |
| Road | 15 | 3 | 12 | 76,900 |
| **Total** | **37** | **3** | **34** | **578,650** |

By mode: Marine **206.5 t** · Rail **295.25 t** · Road **76.9 t**
By status: Delivered **22** · In Transit **8** · Delayed **4**

The three rows removed from Road are three *different* kinds of problem — one duplicate, one blank row, one TOTAL row that was never a shipment. The task requires naming each.

## The four totals

The Stovepipe Game in Task 3. One question, four answers:

| Who | Answer | What they did |
|---|---|---|
| Operations | 661.65 t | kept the TOTAL row |
| Finance | 283.70 t | read the rail tons as kilograms |
| Sales | 584.75 t | kept the duplicate |
| **One staging area** | **578.65 t** | **the true number** |

Students must reproduce each wrong figure arithmetically. Nobody in this story is lying or bad at arithmetic — that is the point.

## Traps worth knowing about

| Trap | What happens |
|---|---|
| Rail weight is in **tons** | 32.5 means 32,500 kg. Miss it and you get Finance's 283.70 t |
| Marine dates are `dd/mm/yyyy` | Without the UK locale, `MR-1003` reads as 2 March and `MR-1012` errors |
| Rail has 2 title rows | Power BI's automatic *Promoted Headers* guesses wrong and must be deleted |
| Append matches by **name** | Columns renamed inconsistently across queries silently produce extra columns |
