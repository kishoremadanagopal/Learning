"""Generate the extra practice datasets for Statistics with Python (deterministic).

The shared files (sales, customers, students, weather, movies) come from the Python for Data course.
Run: python datasets.py   -> writes data/ab_test.csv, data/housing.csv, data/training.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "data"


def ab_test(rng):
    n = 4000
    group = rng.choice(["A", "B"], n)
    device = rng.choice(["mobile", "desktop"], n, p=[0.6, 0.4])
    base = np.where(device == "mobile", 0.085, 0.12)
    lift = np.where(group == "B", 0.022, 0.0)
    converted = (rng.random(n) < base + lift).astype(int)
    revenue = np.where(converted == 1, np.round(rng.gamma(4.0, 12.0, n), 2), 0.0)
    return pd.DataFrame({"visitor_id": np.arange(1, n + 1), "group": group, "device": device,
                         "converted": converted, "revenue": revenue})


def housing(rng):
    n = 160
    hood = rng.choice(["Central", "Riverside", "Hillside"], n, p=[0.3, 0.4, 0.3])
    area = np.round(rng.normal(95, 28, n).clip(35, 220))
    bedrooms = np.clip(np.round(area / 32 + rng.normal(0, 0.6, n)), 1, 6).astype(int)
    age = rng.integers(0, 80, n)
    distance = np.round(rng.gamma(2.2, 3.0, n).clip(0.3, 30), 1)
    hood_bonus = np.select([hood == "Central", hood == "Riverside"], [90, 35], 0)
    price = 60 + 3.1 * area + 12 * bedrooms - 0.9 * age - 4.5 * distance + hood_bonus + rng.normal(0, 38, n)
    return pd.DataFrame({"home_id": np.arange(1, n + 1), "neighborhood": hood, "area_sqm": area.astype(int),
                         "bedrooms": bedrooms, "age_years": age, "distance_km": distance,
                         "price_k": np.round(price, 1)})


def training(rng):
    n = 30
    before = np.round(rng.normal(62, 9, n)).clip(30, 95)
    after = np.round(before + rng.normal(5.5, 6, n)).clip(30, 100)
    names = [f"E{i:02d}" for i in range(1, n + 1)]
    return pd.DataFrame({"employee": names, "before": before.astype(int), "after": after.astype(int)})


def main():
    rng = np.random.default_rng(1729)
    OUT.mkdir(exist_ok=True)
    ab_test(rng).to_csv(OUT / "ab_test.csv", index=False)
    housing(rng).to_csv(OUT / "housing.csv", index=False)
    training(rng).to_csv(OUT / "training.csv", index=False)


if __name__ == "__main__":
    main()
