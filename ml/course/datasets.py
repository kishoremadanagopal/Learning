"""Generate the practice datasets for Machine Learning with scikit-learn (deterministic).

housing.csv and students.csv come from the Statistics with Python course.
Run: python datasets.py   -> writes data/churn.csv, data/fruit.csv, data/shoppers.csv, data/messages.csv, data/energy.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "data"


def churn(rng):
    """1,000 phone/internet customers; about a quarter leave (churn). Some ages are missing."""
    n = 1000
    contract = rng.choice(["month-to-month", "one-year", "two-year"], n, p=[0.5, 0.28, 0.22])
    plan = rng.choice(["basic", "standard", "premium"], n, p=[0.4, 0.4, 0.2])
    max_tenure = np.select([contract == "two-year", contract == "one-year"], [72, 60], 48)
    tenure = np.ceil(rng.random(n) * max_tenure).astype(int)
    base = np.select([plan == "premium", plan == "standard"], [75, 52], 30)
    monthly = np.round(base + rng.normal(0, 7, n), 2).clip(18, 110)
    calls = rng.poisson(1.4, n).clip(0, 9)
    age = rng.integers(18, 80, n).astype(float)
    data_gb = np.round(rng.gamma(3, 6, n), 1)
    logit = (-1.35
             + np.select([contract == "month-to-month", contract == "one-year"], [1.35, 0.0], -1.2)
             - 0.035 * tenure
             + 0.48 * calls
             + 0.022 * (monthly - 50)
             - 0.012 * (age - 45)
             + 1.1 * (tenure <= 6)                                   # brand-new customers leave more
             + 1.4 * ((plan == "basic") & (data_gb > 24)))          # heavy users squeezed on the basic plan
    churned = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    age[rng.random(n) < 0.05] = np.nan
    return pd.DataFrame({"customer_id": np.arange(1001, 1001 + n), "contract": contract, "plan": plan,
                         "tenure_months": tenure, "monthly_charge": monthly, "support_calls": calls,
                         "age": age, "data_gb": data_gb, "churned": churned})


def fruit(rng):
    """150 pieces of fruit, 50 of each kind, measured by width, height and weight."""
    rows = []
    specs = {"apple": (7.4, 7.0, 0.45, 0.45, 165), "orange": (7.8, 7.7, 0.55, 0.55, 190), "lemon": (5.9, 8.4, 0.35, 0.55, 110)}
    for name, (w, h, sw, sh, g) in specs.items():
        width = rng.normal(w, sw, 50)
        height = rng.normal(h, sh, 50)
        weight = g * (width * height) / (w * h) + rng.normal(0, 9, 50)
        for a, b, c in zip(width, height, weight):
            rows.append((name, round(a, 1), round(b, 1), int(round(c))))
    df = pd.DataFrame(rows, columns=["fruit", "width_cm", "height_cm", "weight_g"])
    df = df.sample(frac=1, random_state=7).reset_index(drop=True)
    df.insert(0, "fruit_id", np.arange(1, len(df) + 1))
    return df[["fruit_id", "width_cm", "height_cm", "weight_g", "fruit"]]


def shoppers(rng):
    """200 shop customers in five natural groups by income and spending score (no labels)."""
    centres = [(25, 78, 24, 9), (27, 22, 45, 3), (55, 50, 40, 5), (88, 82, 32, 8), (90, 18, 46, 2)]
    sizes = [36, 34, 64, 36, 30]
    rows = []
    for (inc, spend, age, visits), k in zip(centres, sizes):
        rows.append(pd.DataFrame({
            "annual_income_k": np.round(rng.normal(inc, 6.5, k)).clip(12, 140).astype(int),
            "spending_score": np.round(rng.normal(spend, 7.5, k)).clip(1, 99).astype(int),
            "age": np.round(rng.normal(age, 6, k)).clip(18, 75).astype(int),
            "visits_per_month": np.round(rng.normal(visits, 1.5, k)).clip(0, 20).astype(int),
        }))
    df = pd.concat(rows).sample(frac=1, random_state=3).reset_index(drop=True)
    df.insert(0, "customer_id", np.arange(1, len(df) + 1))
    return df


SPAM = [
    "WINNER! You have won a {prize}. Call {num} now to claim",
    "Congratulations, you've been selected for a FREE {prize}. Reply YES",
    "URGENT: your account will be closed. Click {link} to verify",
    "Get cheap {thing} today only, {pct}% off! Visit {link}",
    "You are owed a refund of ${money}. Claim now at {link}",
    "Final notice: claim your {prize} before midnight. Text WIN to {num}",
    "Hot deal!!! {thing} at {pct}% discount, limited offer, buy now",
    "Earn ${money} a week from home, no experience needed. Call {num}",
    "Your parcel is waiting, pay the ${money} fee at {link}",
    "Exclusive offer: free {prize} for the first 100 customers, click {link}",
    "Hi, it's your bank. We noticed a problem, please confirm your details at {link}",
    "Hey {name}, I found a way to make ${money} fast, message me at {num}",
    "Last chance to get {thing} for {pct}% less, offer ends {day}",
    "Hi {name}, sorry I missed you, call me back on {num}",
    "Is this still your number? Message me on {num}, it's {name}",
]
HAM = [
    "Are we still meeting for {meal} at {time}?",
    "Can you send me the {doc} before the meeting tomorrow?",
    "Running {mins} minutes late, sorry!",
    "Thanks for the {doc}, I'll read it tonight",
    "Happy birthday! Hope you have a great day",
    "Don't forget to buy {food} on the way home",
    "The {doc} looks good, just one small change on page {page}",
    "Shall we watch a film on {day}?",
    "I'm at the station, see you in {mins} minutes",
    "Mum says {meal} is ready at {time}",
    "Did you finish the {doc} for {day}?",
    "Call me when you're free, it's about {day}",
    "Great game last night! Same time on {day}?",
    "Your appointment is confirmed for {day} at {time}",
    "Are you free for {meal} on {day}?",
    "We won the quiz on {day}! {name} knew every answer",
    "Call me now, I can't find the {doc}",
    "I sent you the link to the {doc}, click it when you can",
    "Hi {name}, can you call me back after {time}?",
    "Free tickets from work for {day}, want to come?",
    "{name} is bringing {food}, can you bring drinks?",
    "Got the {doc}, thanks {name}!",
    "Your order has shipped, track it at {link}",
    "Reminder: your {pct}% discount voucher from the gym ends {day}",
    "Congratulations on the new job {name}!",
]
FILL = {
    "prize": ["iPhone", "holiday", "gift card", "cash prize", "laptop", "cruise"],
    "num": ["0800 123 456", "09061 111 222", "87121", "80082"],
    "link": ["bit.ly/claim-now", "www.free-prize.biz", "secure-verify.info", "tinyurl.com/x9win"],
    "thing": ["watches", "meds", "sunglasses", "loans", "followers"],
    "pct": ["50", "70", "80", "90"],
    "money": ["250", "500", "1,000", "2.99", "1.99"],
    "meal": ["lunch", "dinner", "breakfast", "coffee"],
    "time": ["1pm", "7:30", "noon", "6pm", "8"],
    "doc": ["report", "slides", "notes", "spreadsheet", "draft", "photos"],
    "mins": ["5", "10", "15", "20"],
    "food": ["milk", "bread", "eggs", "rice", "apples"],
    "page": ["2", "3", "5", "7"],
    "day": ["Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"],
    "name": ["Sam", "Priya", "Leo", "Ana", "Tom", "Mei", "Omar", "Zoe", "Raj", "Ella"],
}


def messages(rng):
    """400 short text messages labelled spam or ham (not spam); about 30% spam."""
    def fill(t):
        out = t
        for key, options in FILL.items():
            while "{" + key + "}" in out:
                out = out.replace("{" + key + "}", options[rng.integers(len(options))], 1)
        return out
    rows, seen = [], set()
    while len(rows) < 400:
        if rng.random() < 0.3:
            row = (fill(SPAM[rng.integers(len(SPAM))]), "spam")
        else:
            row = (fill(HAM[rng.integers(len(HAM))]), "ham")
        if row[0] not in seen:
            seen.add(row[0])
            rows.append(row)
    df = pd.DataFrame(rows, columns=["text", "label"])
    df.insert(0, "message_id", np.arange(1, len(df) + 1))
    return df


def energy(rng):
    """40 days: outdoor temperature and an office building's energy use (heating when cold, cooling when hot)."""
    n = 40
    temp = np.round(rng.uniform(-4, 34, n), 1)
    kwh = 210 + 0.55 * (temp - 17) ** 2 + rng.normal(0, 22, n)
    df = pd.DataFrame({"day": np.arange(1, n + 1), "temperature_c": temp, "energy_kwh": np.round(kwh, 1)})
    return df


def main():
    rng = np.random.default_rng(2026)
    OUT.mkdir(exist_ok=True)
    churn(rng).to_csv(OUT / "churn.csv", index=False)
    fruit(rng).to_csv(OUT / "fruit.csv", index=False)
    shoppers(rng).to_csv(OUT / "shoppers.csv", index=False)
    messages(rng).to_csv(OUT / "messages.csv", index=False)
    energy(rng).to_csv(OUT / "energy.csv", index=False)


if __name__ == "__main__":
    main()
