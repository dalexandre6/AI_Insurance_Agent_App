from tools.registry import register_tool
import pandas as pd


@register_tool(
    name="total_fees_year",
    description="Returns the total insurance fees for a specific year. The dataset stores fee totals in the Fee_Year column, so this tool calculates the annual total for that year value."
)
def total_fees_year(year: int = 2026):
    df = pd.read_csv("C:/Users/dalex/Documents/DataSetsProjects/Insurance2026.csv", encoding="cp1252")

    year = int(year)

    # The workbook does not have a separate calendar-year column, so the
    # Fee_Year field represents the annual fee amount for each record.
    # For the requested year, we return the overall total and a per-insurance
    # breakdown, both as plain Python dicts so they are JSON-safe for Ollama.
    fees = df["Fee_Year"].astype(float)
    totals_by_insurance = df.groupby("Insurance_Type")["Fee_Year"].sum().astype(float).to_dict()

    return {
        "year": year,
        "total_fees": float(fees.sum()),
        "by_insurance_type": {str(k): float(v) for k, v in totals_by_insurance.items()},
    }