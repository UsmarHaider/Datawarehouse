"""
Build the two Week 1 datasets.

    python3 generate_week1_data.py

Creates, in data/:
  DWBI_W1_Messy_Sales_Log.csv   38 rows, one morning's orders from three
                                branches, exported raw. Used in Lecture 1
                                ("Inspect the Messy Sales Log").
  DWBI_W1_Regional_Sales.xlsx   Sales / Products / Regions, Jan-Jun 2026.
                                Used for the first Power BI connection.

Both are generated with a fixed seed so every student gets identical data
and answers can be compared. Do not change the seed.

The messy log is dirty ON PURPOSE. Every fault below is planted:
  1. branch name written four different ways      (LHR-Gulberg / Lahore Gulberg / khi clifton / ISB F-7)
  2. five different date formats in one column
  3. a duplicated order row                        (1004)
  4. the same product under three names            (Cola 1.5L / CL-150 / Cola 1.5 Ltr)
  5. category written inconsistently, and blank    (Beverages / Bev. / "")
  6. amounts stored as text                        ("Rs 180", "2,450")
  7. a return recorded as negative qty and amount  (1007)
  8. a decimal-point error: 3600 where 360 is right (1008)
"""
import csv, random
from pathlib import Path

DATA = Path(__file__).parent / "data"
SEED = 42

# ---------------------------------------------------------------- messy log
HEADER = ["OrderID", "Branch", "Date", "Product", "Category", "Qty", "Amount"]

# the ten rows shown on the lecture slide, exactly as printed
SEEDED = [
    ["1001", "LHR-Gulberg",     "12/09/2026", "Cola 1.5L",        "Beverages",  "2", "360"],
    ["1002", "Lahore Gulberg",  "2026-09-12", "CL-150",           "Bev.",       "1", "Rs 180"],
    ["1003", "KHI-Clifton",     "09-12-2026", "Cola 1.5 Ltr",     "Beverages",  "3", "540"],
    ["1004", "ISB-F7",          "12 Sep 26",  "Masala Chips 50g", "Snacks",     "4", "200"],
    ["1004", "ISB-F7",          "12 Sep 26",  "Masala Chips 50g", "Snacks",     "4", "200"],
    ["1005", "khi clifton",     "12/09/2026", "Fresh Milk 1L",    "",           "2", "440"],
    ["1006", "LHR-Gulberg",     "2026-09-12", "Basmati Rice 5kg", "Grocery",    "1", "2,450"],
    ["1007", "ISB-F7",          "12/09/2026", "LED Bulb 12W",     "Electrical", "-1", "-350"],
    ["1008", "Lahore Gulberg",  "12/09/2026", "Cola 1.5L",        "Beverages",  "2", "3600"],
    ["1009", "ISB F-7",         "2026/09/12", "Yogurt 500g",      "Dairy",      "3", "510"],
]

BRANCHES = ["LHR-Gulberg", "Lahore Gulberg", "KHI-Clifton", "khi clifton", "ISB-F7", "ISB F-7"]
DATES = ["12/09/2026", "2026-09-12", "09-12-2026", "12 Sep 26", "2026/09/12"]
CATALOGUE = [
    ("Cola 1.5L", ["Cola 1.5L", "CL-150", "Cola 1.5 Ltr"], "Beverages", ["Beverages", "Bev.", ""], 180),
    ("Orange Juice 1L", ["Orange Juice 1L", "OJ-1L"], "Beverages", ["Beverages", "Bev."], 320),
    ("Masala Chips 50g", ["Masala Chips 50g", "Chips Masala 50 g"], "Snacks", ["Snacks", "snacks"], 50),
    ("Salted Biscuits Pack", ["Salted Biscuits Pack"], "Snacks", ["Snacks"], 120),
    ("Fresh Milk 1L", ["Fresh Milk 1L", "Milk 1 Litre"], "Dairy", ["Dairy", ""], 220),
    ("Yogurt 500g", ["Yogurt 500g"], "Dairy", ["Dairy", "dairy"], 170),
    ("Basmati Rice 5kg", ["Basmati Rice 5kg"], "Grocery", ["Grocery"], 2450),
    ("Cooking Oil 5L", ["Cooking Oil 5L"], "Grocery", ["Grocery", "grocery"], 1890),
    ("LED Bulb 12W", ["LED Bulb 12W"], "Electronics", ["Electrical", "Electronics"], 350),
]


def messy_log(rng):
    rows = [r[:] for r in SEEDED]
    order = 1010
    while len(rows) < 38:
        canon, names, cat, cats, price = rng.choice(CATALOGUE)
        qty = rng.randint(1, 5)
        amount = qty * price
        txt = f"{amount:,}" if amount >= 1000 and rng.random() < 0.4 else str(amount)
        if rng.random() < 0.12:
            txt = "Rs " + txt
        rows.append([str(order), rng.choice(BRANCHES), rng.choice(DATES),
                     rng.choice(names), rng.choice(cats), str(qty), txt])
        order += 1
    return rows


# ------------------------------------------------------- regional sales xlsx
PRODUCTS = [
    ("P01", "Cola 1.5L",           "Beverages",   180),
    ("P02", "Orange Juice 1L",     "Beverages",   320),
    ("P03", "Mineral Water 1.5L",  "Beverages",    60),
    ("P04", "Masala Chips 50g",    "Snacks",       50),
    ("P05", "Salted Biscuits Pack","Snacks",      120),
    ("P06", "Chocolate Bar",       "Snacks",      150),
    ("P07", "Fresh Milk 1L",       "Dairy",       220),
    ("P08", "Yogurt 500g",         "Dairy",       170),
    ("P09", "Butter 250g",         "Dairy",       480),
    ("P10", "Basmati Rice 5kg",    "Grocery",    2450),
    ("P11", "Cooking Oil 5L",      "Grocery",    1890),
    ("P12", "Tea 950g",            "Grocery",    1250),
    ("P13", "LED Bulb 12W",        "Electronics", 350),
    ("P14", "Electric Kettle",     "Electronics",3200),
    ("P15", "Ceiling Fan",         "Electronics",8900),
]
REGIONS = [
    ("R1", "Central", "Lahore",      "Ayesha Siddiqui"),
    ("R2", "North",   "Islamabad",   "Bilal Ahmed"),
    ("R3", "South",   "Karachi",     "Hina Raza"),
    ("R4", "West",    "Peshawar",    "Kamran Khan"),
]
# the four sale rows printed on the slide, reproduced exactly
SEED_SALES = [
    ("S1001", "2026-01-01", "P05", "R1", 10, 120, 1200),
    ("S1002", "2026-01-01", "P11", "R3",  1, 1890, 1890),
    ("S1003", "2026-01-02", "P07", "R3", 10,  220, 2200),
    ("S1004", "2026-01-03", "P02", "R3",  7,  320, 2240),
]


def regional_sales(rng):
    from datetime import date, timedelta
    price = {p[0]: p[3] for p in PRODUCTS}
    start, end = date(2026, 1, 1), date(2026, 6, 30)
    span = (end - start).days
    rows = [list(r) for r in SEED_SALES]
    n = 1005
    while len(rows) < 480:
        d = start + timedelta(days=rng.randint(0, span))
        pid = rng.choice([p[0] for p in PRODUCTS])
        rid = rng.choices([r[0] for r in REGIONS], weights=[35, 20, 30, 15])[0]
        qty = rng.choices(range(1, 13), weights=[10,10,9,9,8,7,6,5,4,4,3,3])[0]
        up = price[pid]
        rows.append([f"S{n}", d.isoformat(), pid, rid, qty, up, qty * up])
        n += 1
    rows[4:] = sorted(rows[4:], key=lambda r: r[1])
    return rows


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)

    rows = messy_log(rng)
    p = DATA / "DWBI_W1_Messy_Sales_Log.csv"
    with p.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        w.writerows(rows)
    print(f"  {p.name:<32} {len(rows)} rows")

    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Sales"
    ws.append(["SaleID", "SaleDate", "ProductID", "RegionID",
               "Quantity", "UnitPrice", "SalesAmount"])
    sales = regional_sales(rng)
    for r in sales:
        ws.append(r)

    wp = wb.create_sheet("Products")
    wp.append(["ProductID", "ProductName", "Category", "UnitPrice"])
    for r in PRODUCTS:
        wp.append(list(r))

    wr = wb.create_sheet("Regions")
    wr.append(["RegionID", "RegionName", "HeadOffice", "RegionalManager"])
    for r in REGIONS:
        wr.append(list(r))

    for sheet in (ws, wp, wr):
        for col in sheet.columns:
            width = max(len(str(c.value or "")) for c in col) + 3
            sheet.column_dimensions[col[0].column_letter].width = width
        sheet.freeze_panes = "A2"

    x = DATA / "DWBI_W1_Regional_Sales.xlsx"
    wb.save(x)
    print(f"  {x.name:<32} Sales {len(sales)} · Products {len(PRODUCTS)} · Regions {len(REGIONS)}")
    print("\nDone. Open TASKS.md and start with Task 1.")


if __name__ == "__main__":
    main()
