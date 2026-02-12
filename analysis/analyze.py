"""
Mutual Fund Analysis Script
- Data Cleaning
- Statistical Description
- Normalization (MinMaxScaler)
- Custom Scoring & Ranking
- Export Top 30 Funds + Dashboard JSON
"""

import pandas as pd
import numpy as np
import json
import os
from sklearn.preprocessing import MinMaxScaler

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_data():
    """Load the raw mutual fund dataset."""
    path = os.path.join(DATA_DIR, "mutual_funds_raw.csv")
    df = pd.read_csv(path)
    print(f"📂 Loaded {len(df)} records from mutual_funds_raw.csv")
    return df


def clean_data(df):
    """Step 1: Data Cleaning."""
    print("\n🧹 Step 1: Data Cleaning...")

    initial_count = len(df)

    # Drop duplicates
    df = df.drop_duplicates(subset=["Scheme Name"], keep="first")
    print(f"   Removed {initial_count - len(df)} duplicate schemes")

    # Fill missing returns with median of same category
    for col in ["Return 1Y (%)", "Return 3Y (%)", "Return 5Y (%)"]:
        median_by_cat = df.groupby("Category")[col].transform("median")
        df[col] = df[col].fillna(median_by_cat)
        # If still NaN (entire category missing), fill with overall median
        df[col] = df[col].fillna(df[col].median())

    # Ensure no negative expense ratios
    df["Expense Ratio (%)"] = df["Expense Ratio (%)"].clip(lower=0.01)

    # Ensure fund age is positive
    df["Fund Age (Years)"] = df["Fund Age (Years)"].clip(lower=0.1)

    # Ensure AUM is positive
    df["AUM (Cr)"] = df["AUM (Cr)"].clip(lower=1)

    print(f"   Remaining records: {len(df)}")
    print(f"   Missing values after cleaning: {df.isnull().sum().sum()}")

    return df


def describe_data(df):
    """Step 2: Data Description & Statistical Summary."""
    print("\n📊 Step 2: Data Description & Understanding...")

    numeric_cols = ["Return 1Y (%)", "Return 3Y (%)", "Return 5Y (%)",
                    "Expense Ratio (%)", "NAV (₹)", "AUM (Cr)", "Fund Age (Years)"]

    stats = df[numeric_cols].describe()
    print(stats.round(2).to_string())

    print(f"\n   Fund Types: {df['Fund Type'].nunique()}")
    print(f"   Categories: {df['Category'].nunique()}")
    print(f"   AMCs: {df['AMC Name'].nunique()}")
    print(f"   Fund Managers: {df['Fund Manager'].nunique()}")

    return stats


def normalize_data(df):
    """Step 3: Data Normalization using MinMaxScaler."""
    print("\n📏 Step 3: Data Normalization (MinMaxScaler)...")

    scaler = MinMaxScaler()
    cols_to_normalize = ["Return 1Y (%)", "Return 3Y (%)", "Return 5Y (%)",
                         "Expense Ratio (%)", "Fund Age (Years)", "AUM (Cr)"]

    df_normalized = df.copy()
    df_normalized[["Norm_Return_1Y", "Norm_Return_3Y", "Norm_Return_5Y",
                    "Norm_Expense_Ratio", "Norm_Fund_Age", "Norm_AUM"]] = \
        scaler.fit_transform(df[cols_to_normalize])

    print("   ✅ Normalized columns: Return 1Y, 3Y, 5Y, Expense Ratio, Fund Age, AUM")

    return df_normalized


def score_and_rank(df):
    """Step 4: Custom Scoring & Ranking."""
    print("\n🏆 Step 4: Fund Scoring & Ranking...")

    # Custom scoring formula:
    # Score = 0.40 × Norm_3Y_Return
    #       + 0.25 × (1 - Norm_Expense_Ratio)   [lower expense = better]
    #       + 0.20 × Norm_1Y_Return
    #       + 0.10 × Norm_Fund_Age               [moderate age preferred]
    #       + 0.05 × Norm_AUM                    [larger AUM = more stable]

    df["Score"] = (
        0.40 * df["Norm_Return_3Y"] +
        0.25 * (1 - df["Norm_Expense_Ratio"]) +
        0.20 * df["Norm_Return_1Y"] +
        0.10 * df["Norm_Fund_Age"] +
        0.05 * df["Norm_AUM"]
    )

    # Bonus for low-risk funds
    risk_bonus = df["Risk Level"].map({
        "Low": 0.05,
        "Low to Moderate": 0.03,
        "Moderate": 0.01,
        "Moderately High": 0.0,
        "High": -0.02,
        "Very High": -0.05
    }).fillna(0)

    df["Score"] = df["Score"] + risk_bonus

    # Bonus for higher fund rating
    df["Score"] = df["Score"] + (df["Fund Rating"] - 3) * 0.02

    # Normalize final score to 0-100
    df["Score"] = ((df["Score"] - df["Score"].min()) /
                   (df["Score"].max() - df["Score"].min()) * 100).round(2)

    df = df.sort_values("Score", ascending=False).reset_index(drop=True)
    df["Rank"] = range(1, len(df) + 1)

    print(f"   ✅ Scoring complete. Top score: {df['Score'].iloc[0]}, Bottom score: {df['Score'].iloc[-1]}")

    return df


def extract_top_30(df):
    """Step 5: Extract Top 30 Funds."""
    print("\n🥇 Step 5: Extracting Top 30 Funds...")

    top_30 = df.head(30)[[
        "Rank", "Scheme Name", "AMC Name", "Fund Type", "Category",
        "Sub Category", "Risk Level", "Fund Rating",
        "Return 1Y (%)", "Return 3Y (%)", "Return 5Y (%)",
        "Expense Ratio (%)", "NAV (₹)", "AUM (Cr)",
        "Fund Age (Years)", "Min SIP (₹)", "Min Lumpsum (₹)",
        "Fund Manager", "Investment Strategy", "Score"
    ]]

    print(f"   ✅ Top 30 funds extracted")
    print(f"\n   Top 5 Funds:")
    for _, row in top_30.head(5).iterrows():
        print(f"   #{int(row['Rank'])} | {row['Scheme Name'][:50]}... | Score: {row['Score']} | 3Y Return: {row['Return 3Y (%)']}%")

    return top_30


def generate_dashboard_data(df, top_30):
    """Generate JSON data for the web dashboard."""
    print("\n📈 Generating Dashboard Data (JSON)...")

    # ── KPI Summaries ──
    kpis = {
        "total_funds": int(len(df)),
        "total_aum": round(float(df["AUM (Cr)"].sum()), 2),
        "avg_return_3y": round(float(df["Return 3Y (%)"].mean()), 2),
        "avg_expense_ratio": round(float(df["Expense Ratio (%)"].mean()), 2),
        "avg_sip": round(float(df["Min SIP (₹)"].mean()), 2),
        "avg_lumpsum": round(float(df["Min Lumpsum (₹)"].mean()), 2),
    }

    # ── Returns by Category (for Donut Chart) ──
    returns_by_category = df.groupby("Category")["Return 3Y (%)"].mean().round(2).to_dict()

    # ── AUM by Fund Type ──
    aum_by_fund_type = df.groupby("Fund Type")["AUM (Cr)"].sum().round(2).to_dict()

    # ── Top AMCs by Average Return ──
    top_amcs = (df.groupby("AMC Name").agg({
        "Return 3Y (%)": "mean",
        "AUM (Cr)": "sum",
        "Scheme Name": "count"
    }).rename(columns={"Scheme Name": "Fund Count"})
      .sort_values("Return 3Y (%)", ascending=False)
      .head(15)
      .round(2))
    top_amcs_data = top_amcs.reset_index().to_dict(orient="records")

    # ── Fund Manager AUM Comparison ──
    fund_managers = (df.groupby("Fund Manager").agg({
        "AUM (Cr)": "sum",
        "Return 3Y (%)": "mean",
        "Scheme Name": "count"
    }).rename(columns={"Scheme Name": "Fund Count"})
      .sort_values("AUM (Cr)", ascending=False)
      .head(12)
      .round(2))
    fund_managers_data = fund_managers.reset_index().to_dict(orient="records")

    # ── Expense Ratio by Strategy ──
    expense_by_strategy = df.groupby("Investment Strategy")["Expense Ratio (%)"].mean().round(2).to_dict()

    # ── Risk Level Distribution ──
    risk_distribution = df["Risk Level"].value_counts().to_dict()

    # ── Fund Rating Distribution ──
    rating_distribution = df["Fund Rating"].value_counts().sort_index().to_dict()

    # ── SIP vs Lumpsum Summary ──
    sip_by_type = df.groupby("Fund Type")["Min SIP (₹)"].mean().round(0).to_dict()
    lumpsum_by_type = df.groupby("Fund Type")["Min Lumpsum (₹)"].mean().round(0).to_dict()

    # ── Category Distribution ──
    category_counts = df["Category"].value_counts().to_dict()

    # ── Top 30 Funds for Table ──
    top_30_records = top_30.to_dict(orient="records")

    # ── All funds summary for filtering ──
    all_funds = df[[
        "Scheme Name", "AMC Name", "Fund Type", "Category", "Sub Category",
        "Risk Level", "Fund Rating", "Return 1Y (%)", "Return 3Y (%)",
        "Return 5Y (%)", "Expense Ratio (%)", "NAV (₹)", "AUM (Cr)",
        "Fund Age (Years)", "Min SIP (₹)", "Min Lumpsum (₹)",
        "Fund Manager", "Investment Strategy", "Score", "Rank"
    ]].to_dict(orient="records")

    # ── Filter Options ──
    filters = {
        "fund_types": sorted(df["Fund Type"].unique().tolist()),
        "categories": sorted(df["Category"].unique().tolist()),
        "risk_levels": ["Low", "Low to Moderate", "Moderate", "Moderately High", "High", "Very High"],
        "amc_names": sorted(df["AMC Name"].unique().tolist()),
        "fund_ratings": sorted(df["Fund Rating"].unique().tolist()),
        "strategies": sorted(df["Investment Strategy"].unique().tolist()),
    }

    dashboard = {
        "kpis": kpis,
        "returns_by_category": returns_by_category,
        "aum_by_fund_type": aum_by_fund_type,
        "top_amcs": top_amcs_data,
        "fund_managers": fund_managers_data,
        "expense_by_strategy": expense_by_strategy,
        "risk_distribution": risk_distribution,
        "rating_distribution": rating_distribution,
        "sip_by_type": sip_by_type,
        "lumpsum_by_type": lumpsum_by_type,
        "category_counts": category_counts,
        "top_30": top_30_records,
        "all_funds": all_funds,
        "filters": filters,
    }

    return dashboard


def main():
    print("=" * 60)
    print("  📊 MUTUAL FUND ANALYSIS")
    print("=" * 60)

    # Load
    df = load_data()

    # Step 1: Clean
    df = clean_data(df)

    # Step 2: Describe
    describe_data(df)

    # Step 3: Normalize
    df = normalize_data(df)

    # Step 4: Score & Rank
    df = score_and_rank(df)

    # Step 5: Top 30
    top_30 = extract_top_30(df)

    # ── Save outputs ──
    print("\n💾 Saving outputs...")

    # Processed CSV
    processed_path = os.path.join(DATA_DIR, "mutual_funds_processed.csv")
    df.to_csv(processed_path, index=False)
    print(f"   ✅ Processed data: {processed_path}")

    # Top 30 CSV
    top30_path = os.path.join(DATA_DIR, "top_30_mutual_funds.csv")
    top_30.to_csv(top30_path, index=False)
    print(f"   ✅ Top 30 funds: {top30_path}")

    # Top 30 Excel
    top30_xlsx = os.path.join(DATA_DIR, "top_30_mutual_funds.xlsx")
    top_30.to_excel(top30_xlsx, index=False, sheet_name="Top 30 Funds")
    print(f"   ✅ Top 30 Excel: {top30_xlsx}")

    # Dashboard JSON
    dashboard_data = generate_dashboard_data(df, top_30)
    dashboard_path = os.path.join(DATA_DIR, "dashboard_data.json")
    with open(dashboard_path, "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, ensure_ascii=False, indent=2)
    print(f"   ✅ Dashboard JSON: {dashboard_path}")

    print("\n" + "=" * 60)
    print("  ✅ ANALYSIS COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
