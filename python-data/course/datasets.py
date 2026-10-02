"""Generate the practice datasets used throughout the course (deterministic).

Run: python datasets.py   -> writes data/*.csv and data/*.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "data"

FIRST = ["Ava", "Liam", "Priya", "Noah", "Mei", "Omar", "Sofia", "Lucas", "Aisha", "Ethan", "Yuki", "Mateo",
         "Zara", "Arjun", "Chloe", "Diego", "Fatima", "Leo", "Grace", "Ravi", "Hana", "Samuel", "Isla", "Kofi",
         "Elena", "Jonas", "Nia", "Felix", "Amara", "Tom", "Lina", "Victor", "Maya", "Hugo", "Sara", "Ben"]
LAST = ["Smith", "Patel", "Garcia", "Chen", "Okafor", "Müller", "Kim", "Silva", "Khan", "Brown", "Rossi",
        "Nguyen", "Cohen", "Haddad", "Novak", "Tanaka", "Lopez", "Wilson", "Singh", "Larsen", "Mensah", "Ali"]

PRODUCTS = [  # product, category, unit_price, unit_cost, supplier
    ("Laptop", "Electronics", 899.0, 640.0, "TechSource"),
    ("Monitor", "Electronics", 249.0, 170.0, "TechSource"),
    ("Headphones", "Electronics", 79.0, 38.0, "SoundCo"),
    ("Desk Chair", "Office", 189.0, 110.0, "OfficeHub"),
    ("Notebook", "Office", 4.5, 1.2, "PaperWorks"),
    ("Pen Pack", "Office", 6.0, 2.1, "PaperWorks"),
    ("Coffee Maker", "Home", 59.0, 31.0, "HomeGoods"),
    ("Desk Lamp", "Home", 35.0, 16.0, "HomeGoods"),
]


def customers(rng):
    n = 120
    names = set()
    rows = []
    while len(rows) < n:
        name = f"{rng.choice(FIRST)} {rng.choice(LAST)}"
        if name in names:
            continue
        names.add(name)
        i = len(rows) + 1
        rows.append({
            "customer_id": f"C{i:03d}",
            "name": name,
            "city": rng.choice(["London", "Manchester", "Leeds", "Bristol", "Glasgow", "Cardiff"], p=[.3, .2, .15, .15, .1, .1]),
            "segment": rng.choice(["Consumer", "Business", "Student"], p=[.55, .3, .15]),
            "age": int(rng.integers(18, 70)),
            "signup_date": (pd.Timestamp("2023-01-01") + pd.Timedelta(days=int(rng.integers(0, 1000)))).strftime("%Y-%m-%d"),
        })
    return pd.DataFrame(rows)


def sales(rng, cust):
    n = 600
    dates = pd.Timestamp("2025-01-01") + pd.to_timedelta(np.sort(rng.integers(0, 365, n)), unit="D")
    weights = np.array([.08, .1, .18, .07, .2, .17, .1, .1])
    prod_idx = rng.choice(len(PRODUCTS), n, p=weights)
    rows = []
    for i in range(n):
        p = PRODUCTS[prod_idx[i]]
        cheap = p[2] < 20
        units = int(rng.integers(1, 13 if cheap else 5))
        rows.append({
            "order_id": 1001 + i,
            "order_date": dates[i].strftime("%Y-%m-%d"),
            "customer_id": cust["customer_id"].iloc[int(rng.integers(0, len(cust)))],
            "region": rng.choice(["North", "South", "East", "West"], p=[.3, .25, .25, .2]),
            "product": p[0],
            "category": p[1],
            "units": units,
            "unit_price": p[2],
        })
    return pd.DataFrame(rows)


def products():
    return pd.DataFrame(PRODUCTS, columns=["product", "category", "unit_price", "unit_cost", "supplier"])


def employees_messy(rng):
    depts = ["Sales", "sales", "SALES ", "Marketing", "marketing", "Engineering", " Engineering", "Finance", "HR"]
    rows = []
    for i in range(1, 38):
        first, last = rng.choice(FIRST), rng.choice(LAST)
        name = f"{first} {last}"
        style = i % 5
        if style == 1:
            name = name.upper()
        elif style == 2:
            name = "  " + name.lower()
        elif style == 3:
            name = name + "  "
        salary = int(rng.integers(32, 95)) * 1000
        sal_style = i % 4
        salary_txt = {0: f"${salary:,}", 1: str(salary), 2: f"{salary:,}", 3: f"${salary}"}[sal_style]
        if i in (7, 19, 30):
            salary_txt = ""
        age = int(rng.integers(21, 64))
        if i == 12:
            age = 230
        if i == 25:
            age = -1
        start = (pd.Timestamp("2015-01-01") + pd.Timedelta(days=int(rng.integers(0, 3800)))).strftime("%Y-%m-%d")
        if i in (4, 22):
            start = ""
        email = f"{first.lower()}.{last.lower()}@example.com"
        if i in (9, 16, 28, 33):
            email = ""
        rows.append({"emp_id": 100 + i, "name": name, "department": depts[int(rng.integers(0, len(depts)))],
                     "salary": salary_txt, "age": age if i not in (5, 18) else None,
                     "start_date": start, "email": email})
    df = pd.DataFrame(rows)
    df = pd.concat([df, df.iloc[[3, 10, 20]]], ignore_index=True)  # exact duplicate rows
    df["age"] = df["age"].astype("Int64")
    return df


def weather(rng):
    days = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    t = np.arange(len(days))
    rows = []
    cities = {"London": (11.5, 6.5, 1.8, 0.45), "Mumbai": (27.5, 2.5, 8.0, 0.30), "New York": (13.0, 11.0, 3.0, 0.35)}
    for city, (mean, amp, rain_scale, rain_p) in cities.items():
        phase = 0 if city != "Mumbai" else 60
        temps = mean - amp * np.cos(2 * np.pi * (t - 15 - phase) / 365) + rng.normal(0, 2.0, len(t))
        rain = np.where(rng.random(len(t)) < rain_p, rng.gamma(1.5, rain_scale, len(t)), 0.0)
        if city == "Mumbai":  # monsoon: June to September
            monsoon = (days.month >= 6) & (days.month <= 9)
            rain = np.where(monsoon & (rng.random(len(t)) < 0.8), rng.gamma(2.0, 12.0, len(t)), rain * 0.2)
        for d, tc, r in zip(days, temps, rain):
            rows.append({"date": d.strftime("%Y-%m-%d"), "city": city, "temp_c": round(float(tc), 1), "rain_mm": round(float(r), 1)})
    df = pd.DataFrame(rows)
    missing = rng.choice(len(df), 12, replace=False)
    df.loc[missing, "temp_c"] = np.nan
    return df


def students(rng):
    rows = []
    used = set()
    while len(rows) < 60:
        name = f"{rng.choice(FIRST)} {rng.choice(LAST)[0]}."
        if name in used:
            continue
        used.add(name)
        hours = round(float(np.clip(rng.normal(6, 2.5), 0.5, 14)), 1)
        attendance = int(np.clip(rng.normal(88, 8), 55, 100))
        base = 35 + hours * 3.6 + (attendance - 85) * 0.5
        rows.append({
            "student": name,
            "class": rng.choice(["A", "B", "C"]),
            "hours_studied": hours,
            "attendance_pct": attendance,
            "math": int(np.clip(base + rng.normal(0, 9), 12, 100)),
            "science": int(np.clip(base + rng.normal(2, 9), 15, 100)),
            "english": int(np.clip(base * 0.6 + 30 + rng.normal(0, 10), 20, 100)),
        })
    return pd.DataFrame(rows)


def movies(rng):
    words1 = ["Midnight", "Silent", "Golden", "Last", "Hidden", "Broken", "Electric", "Paper", "Crimson", "Northern",
              "Lost", "Velvet", "Iron", "Summer", "Glass", "Wild"]
    words2 = ["Harbor", "Orchard", "Signal", "Kingdom", "River", "Garden", "Engine", "Lanterns", "Tide", "Atlas",
              "Echo", "Frontier", "Station", "Comet", "Mirror", "Voyage"]
    genres = ["Drama", "Comedy", "Action", "Sci-Fi", "Animation", "Thriller", "Documentary"]
    titles, rows = set(), []
    while len(rows) < 40:
        t = f"The {rng.choice(words1)} {rng.choice(words2)}" if rng.random() < .4 else f"{rng.choice(words1)} {rng.choice(words2)}"
        if t in titles:
            continue
        titles.add(t)
        genre = str(rng.choice(genres))
        box = round(float(rng.gamma(2.0, 60.0)), 1) if genre != "Documentary" else round(float(rng.gamma(1.2, 6.0)), 1)
        rows.append({
            "title": t,
            "year": int(rng.integers(2005, 2026)),
            "genre": genre,
            "runtime_min": int(rng.integers(82, 170)) if genre != "Animation" else int(rng.integers(80, 110)),
            "rating": round(float(np.clip(rng.normal(6.8, 0.9), 3.5, 9.4)), 1),
            "box_office_musd": None if rng.random() < .12 else box,
        })
    return rows


def main():
    rng = np.random.default_rng(2026)
    OUT.mkdir(exist_ok=True)
    cust = customers(rng)
    cust.to_csv(OUT / "customers.csv", index=False)
    sales(rng, cust).to_csv(OUT / "sales.csv", index=False)
    products().to_csv(OUT / "products.csv", index=False)
    employees_messy(rng).to_csv(OUT / "employees_messy.csv", index=False)
    weather(rng).to_csv(OUT / "weather.csv", index=False)
    students(rng).to_csv(OUT / "students.csv", index=False)
    (OUT / "movies.json").write_text(json.dumps(movies(rng), indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
