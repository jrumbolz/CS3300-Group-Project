# Module for all finance logic functions
import json
from pathlib import Path

# --- CONFIG ---
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage" / "MonthlySpending"
DATA_DIR1 = BASE_DIR / "BackEnd" / "Data Storage" / "YearlySpending"


def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return None


def get_month_files(year):
    return sorted(DATA_DIR.glob(f"{year}_*.json"))


def build_year_summary(year):
    yearly_data = {
        "year": year,
        "total_income": 0.0,
        "total_expense": 0.0,
        "net_total": 0.0,
        "months": {}
    }

    files = get_month_files(year)

    for file in files:
        data = load_json(file)
        if not data:
            continue

        summary = data.get("summary", {})

        # extract month name from filename: 2026_January.json
        month_name = file.stem.split("_")[1]

        income = float(summary.get("total_income", 0))
        expense = float(summary.get("total_expense", 0))
        net = float(summary.get("net_total", income - expense))

        yearly_data["months"][month_name] = {
            "income": income,
            "expense": expense,
            "net": net
        }

        yearly_data["total_income"] += income
        yearly_data["total_expense"] += expense
        yearly_data["net_total"] += net

    return yearly_data


def save_year_file(year, data):
    file_path = DATA_DIR1 / f"{year}.json"

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved yearly summary → {file_path}")


if __name__ == "__main__":
    year = 2026  # change this
    summary = build_year_summary(year)
    save_year_file(year, summary)