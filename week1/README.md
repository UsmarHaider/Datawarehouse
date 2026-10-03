# Week 1 — Introduction to DW & BI

Datasets and assignments for Week 1.

← [Back to the course index](../README.md)

| Lecture | Topic | Outcome | CLO | 3C |
|---|---|---|---|---|
| **L1** | Module discussion & fundamentals | Explain the operational scope, importance and foundational concepts of DW & BI in organizational decision-making | CLO1 | Competence |
| **L2** | First hands-on connection | Establish a live connection between Power BI and an enterprise dataset to extract initial high-level summaries | CLO1 | Courage |

## Generate the data

```bash
cd week1/assignments
python3 generate_week1_data.py
```

Requires `pandas` and `openpyxl`. Both files are built from a fixed seed (`SEED = 42`), so every student gets identical data.

## Contents

| Path | What it is |
|---|---|
| `assignments/TASKS.md` | Five tasks and the marking guide |
| `assignments/generate_week1_data.py` | Builds both datasets |
| `assignments/data/DWBI_W1_Messy_Sales_Log.csv` | 38 rows, deliberately dirty — the Lecture 1 inquiry |
| `assignments/data/DWBI_W1_Regional_Sales.xlsx` | Sales / Products / Regions — the Lecture 2 hands-on |

## Assignments

| Task | Covers | Data |
|---|---|---|
| 1 | The messy sales log — six faults, who owns each, and the real Beverages total | `DWBI_W1_Messy_Sales_Log.csv` |
| 2 | OLTP vs OLAP — classify eight scenarios, then write your own | — |
| 3 | No history, no single truth — the two failures of a live database | — |
| 4 | Place eight items in the four-stage architecture, and draw it | — |
| 5 | **Hands-on:** first live Power BI connection, relationships, slicer, validation | `DWBI_W1_Regional_Sales.xlsx` |

Full briefs in [`assignments/TASKS.md`](assignments/TASKS.md).

## The messy log — what is planted in it

The file is dirty on purpose. Eight faults are deliberate, and the task asks students to find at least six:

| | Fault |
|---|---|
| 1 | One branch written four ways — `LHR-Gulberg`, `Lahore Gulberg`, `khi clifton`, `ISB F-7` |
| 2 | Five date formats in one column |
| 3 | A duplicated order row (`1004`) |
| 4 | One product under three names — `Cola 1.5L`, `CL-150`, `Cola 1.5 Ltr` |
| 5 | Category inconsistent and sometimes blank — `Beverages`, `Bev.`, `""` |
| 6 | Amounts stored as text — `Rs 180`, `2,450` |
| 7 | A return recorded as negative quantity and amount (`1007`) |
| 8 | A decimal-point error — `1008` charges 3600 for what `1001` sells at 360 |

Faults 1, 4 and 5 are why `GROUP BY` lies. Fault 6 is why `SUM` either fails or silently under-counts.

## The regional sales workbook

| Sheet | Rows | Role |
|---|---|---|
| `Sales` | 480 | Fact table — the numbers |
| `Products` | 15 | Dimension — `Category` lives here, not in `Sales` |
| `Regions` | 4 | Dimension — `RegionName` lives here, not in `Sales` |

Clean by design: `SalesAmount = Quantity × UnitPrice` holds on every row, every `ProductID` and `RegionID` resolves, and there are no nulls. The learning is in the *relationships*, not in cleaning.

The common failure is building **Total Sales by Region** before the relationship to `Regions` exists — every region then shows the same number.
