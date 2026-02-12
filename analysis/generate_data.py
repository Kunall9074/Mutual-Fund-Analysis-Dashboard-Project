"""
Mutual Fund Dataset Generator
Generates a realistic synthetic dataset of 2500+ Indian mutual fund schemes.
"""

import pandas as pd
import numpy as np
import os
import random

np.random.seed(42)
random.seed(42)

# ── AMC Names ──────────────────────────────────────────────
AMC_NAMES = [
    "SBI Mutual Fund", "HDFC Mutual Fund", "ICICI Prudential Mutual Fund",
    "Axis Mutual Fund", "Kotak Mahindra Mutual Fund", "Aditya Birla Sun Life Mutual Fund",
    "Nippon India Mutual Fund", "UTI Mutual Fund", "DSP Mutual Fund",
    "Tata Mutual Fund", "Mirae Asset Mutual Fund", "Franklin Templeton Mutual Fund",
    "Canara Robeco Mutual Fund", "IDFC Mutual Fund", "L&T Mutual Fund",
    "Sundaram Mutual Fund", "HSBC Mutual Fund", "Invesco Mutual Fund",
    "Motilal Oswal Mutual Fund", "Parag Parikh Mutual Fund",
    "Edelweiss Mutual Fund", "PGIM India Mutual Fund", "Bandhan Mutual Fund",
    "Baroda BNP Paribas Mutual Fund", "Quant Mutual Fund",
    "Mahindra Manulife Mutual Fund", "JM Financial Mutual Fund",
    "Bank of India Mutual Fund", "Union Mutual Fund", "Quantum Mutual Fund"
]

# ── Fund Managers ──────────────────────────────────────────
FUND_MANAGERS = [
    "R. Srinivasan", "Prashant Jain", "Sankaran Naren", "Jinesh Gopani",
    "Harsha Upadhyaya", "Mahesh Patil", "Manish Gunwani", "Vetri Subramaniam",
    "Kalpen Parekh", "Rahul Baijal", "Swarup Mohanty", "Neelesh Surana",
    "Anish Tawakley", "Shreyash Devalkar", "Atul Kumar", "Gopal Agrawal",
    "Vinay Sharma", "Amit Ganatra", "Rajeev Thakkar", "Sailesh Raj Bhan",
    "Chirag Setalvad", "Roshi Jain", "S. Nagnath", "Ajay Tyagi",
    "Taher Badshah", "Nimesh Chandan", "Sohini Andani", "Chandraprakash Padiyar",
    "Divam Sharma", "Ashish Kela", "Niket Shah", "Varun Goel",
    "Ankit Agarwal", "Pranav Gokhale", "Rohit Singhania", "Dhaval Gada"
]

# ── Fund Configuration ─────────────────────────────────────
FUND_TYPES = {
    "Equity": {
        "weight": 0.45,
        "categories": {
            "Large Cap": {"sub": ["Bluechip", "Index", "Focused"], "risk": ["Moderate", "Moderately High"], "ret_3y": (8, 28), "expense": (0.3, 1.8)},
            "Mid Cap": {"sub": ["Growth", "Opportunities", "Discovery"], "risk": ["Moderately High", "High"], "ret_3y": (10, 35), "expense": (0.4, 2.0)},
            "Small Cap": {"sub": ["Emerging", "Micro Cap", "Discovery"], "risk": ["High", "Very High"], "ret_3y": (5, 45), "expense": (0.5, 2.2)},
            "Multi Cap": {"sub": ["Diversified", "Flexi Cap", "Dynamic"], "risk": ["Moderate", "Moderately High", "High"], "ret_3y": (8, 30), "expense": (0.4, 2.0)},
            "ELSS": {"sub": ["Tax Saver", "Tax Advantage"], "risk": ["Moderately High", "High"], "ret_3y": (8, 30), "expense": (0.5, 2.0)},
            "Sectoral": {"sub": ["Banking", "IT", "Pharma", "Infrastructure", "Energy", "Consumption"], "risk": ["High", "Very High"], "ret_3y": (2, 40), "expense": (0.5, 2.5)},
            "Thematic": {"sub": ["ESG", "MNC", "Dividend Yield", "Value", "Contra"], "risk": ["Moderately High", "High"], "ret_3y": (5, 32), "expense": (0.4, 2.2)},
        }
    },
    "Debt": {
        "weight": 0.25,
        "categories": {
            "Liquid": {"sub": ["Overnight", "Ultra Short"], "risk": ["Low"], "ret_3y": (3, 7), "expense": (0.1, 0.5)},
            "Short Duration": {"sub": ["Low Duration", "Money Market"], "risk": ["Low", "Low to Moderate"], "ret_3y": (4, 8), "expense": (0.2, 0.8)},
            "Medium Duration": {"sub": ["Corporate Bond", "Banking & PSU"], "risk": ["Low to Moderate", "Moderate"], "ret_3y": (5, 9), "expense": (0.3, 1.0)},
            "Long Duration": {"sub": ["Gilt", "Dynamic Bond", "10Y Gilt"], "risk": ["Moderate", "Moderately High"], "ret_3y": (4, 10), "expense": (0.3, 1.2)},
            "Credit Risk": {"sub": ["High Yield", "Corporate"], "risk": ["Moderate", "Moderately High"], "ret_3y": (5, 11), "expense": (0.5, 1.5)},
        }
    },
    "Hybrid": {
        "weight": 0.18,
        "categories": {
            "Aggressive Hybrid": {"sub": ["Balanced Advantage", "Equity Savings"], "risk": ["Moderately High", "High"], "ret_3y": (7, 22), "expense": (0.4, 1.8)},
            "Conservative Hybrid": {"sub": ["Regular Savings", "Income"], "risk": ["Low to Moderate", "Moderate"], "ret_3y": (5, 12), "expense": (0.3, 1.5)},
            "Dynamic Asset Allocation": {"sub": ["Multi Asset", "Balanced"], "risk": ["Moderate", "Moderately High"], "ret_3y": (6, 18), "expense": (0.4, 1.8)},
            "Arbitrage": {"sub": ["Equity Arbitrage"], "risk": ["Low"], "ret_3y": (4, 8), "expense": (0.2, 1.0)},
        }
    },
    "Solution Oriented": {
        "weight": 0.07,
        "categories": {
            "Retirement": {"sub": ["Pension", "Senior Citizen"], "risk": ["Moderate", "Moderately High"], "ret_3y": (6, 16), "expense": (0.4, 1.5)},
            "Children's Fund": {"sub": ["Education", "Gift"], "risk": ["Moderate", "Moderately High"], "ret_3y": (7, 18), "expense": (0.4, 1.5)},
        }
    },
    "Other": {
        "weight": 0.05,
        "categories": {
            "Index Fund": {"sub": ["Nifty 50", "Sensex", "Nifty Next 50", "Nifty 100"], "risk": ["Moderate", "Moderately High"], "ret_3y": (8, 22), "expense": (0.1, 0.5)},
            "Fund of Funds": {"sub": ["International", "Gold", "Domestic"], "risk": ["Moderate", "Moderately High", "High"], "ret_3y": (3, 20), "expense": (0.3, 1.5)},
        }
    }
}

INVESTMENT_STRATEGIES = ["Growth", "Value", "Blend", "Income", "Index", "Passive", "Active", "GARP"]

def generate_scheme_name(amc, category, sub_category, fund_type):
    """Generate a realistic mutual fund scheme name."""
    amc_short = amc.replace(" Mutual Fund", "")
    suffixes = ["Fund", "Plan", "Scheme"]
    plan_types = ["Direct Plan", "Regular Plan"]
    growth_div = ["Growth", "IDCW"]

    name = f"{amc_short} {sub_category} {category} {random.choice(suffixes)} - {random.choice(plan_types)} - {random.choice(growth_div)}"
    return name


def generate_dataset(n_schemes=2600):
    """Generate a synthetic mutual fund dataset."""
    records = []

    for i in range(n_schemes):
        # Pick fund type based on weights
        fund_type = np.random.choice(
            list(FUND_TYPES.keys()),
            p=[v["weight"] for v in FUND_TYPES.values()]
        )
        config = FUND_TYPES[fund_type]

        # Pick category
        category = random.choice(list(config["categories"].keys()))
        cat_config = config["categories"][category]

        # Pick sub-category
        sub_category = random.choice(cat_config["sub"])

        # Pick AMC and Fund Manager
        amc = random.choice(AMC_NAMES)
        fund_manager = random.choice(FUND_MANAGERS)

        # Risk level
        risk_level = random.choice(cat_config["risk"])

        # Returns
        ret_3y_low, ret_3y_high = cat_config["ret_3y"]
        return_3y = round(np.random.uniform(ret_3y_low, ret_3y_high), 2)
        return_1y = round(return_3y + np.random.uniform(-8, 8), 2)
        return_5y = round(return_3y + np.random.uniform(-5, 5), 2)

        # Expense ratio
        exp_low, exp_high = cat_config["expense"]
        expense_ratio = round(np.random.uniform(exp_low, exp_high), 2)

        # NAV
        nav = round(np.random.uniform(8, 800), 2)

        # AUM (in Crores)
        aum = round(np.random.lognormal(mean=7, sigma=1.5), 2)
        aum = min(aum, 250000)  # cap at 2.5 lakh crores

        # Fund age (years)
        fund_age = round(np.random.uniform(0.5, 30), 1)

        # SIP and Lumpsum
        min_sip = random.choice([100, 500, 500, 500, 1000, 1000, 1500, 2000, 2500, 5000])
        min_lumpsum = random.choice([500, 1000, 1000, 5000, 5000, 5000, 10000, 10000, 25000])

        # Fund rating (1-5 stars)
        if return_3y > 20 and expense_ratio < 1.0:
            rating = random.choices([4, 5], weights=[0.4, 0.6])[0]
        elif return_3y > 12:
            rating = random.choices([3, 4, 5], weights=[0.3, 0.5, 0.2])[0]
        elif return_3y > 6:
            rating = random.choices([2, 3, 4], weights=[0.3, 0.5, 0.2])[0]
        else:
            rating = random.choices([1, 2, 3], weights=[0.4, 0.4, 0.2])[0]

        # Investment strategy
        strategy = random.choice(INVESTMENT_STRATEGIES)

        # Scheme name
        scheme_name = generate_scheme_name(amc, category, sub_category, fund_type)

        records.append({
            "Scheme Name": scheme_name,
            "AMC Name": amc,
            "Fund Type": fund_type,
            "Category": category,
            "Sub Category": sub_category,
            "Risk Level": risk_level,
            "Fund Rating": rating,
            "Return 1Y (%)": return_1y,
            "Return 3Y (%)": return_3y,
            "Return 5Y (%)": return_5y,
            "Expense Ratio (%)": expense_ratio,
            "NAV (₹)": nav,
            "AUM (Cr)": aum,
            "Fund Age (Years)": fund_age,
            "Min SIP (₹)": min_sip,
            "Min Lumpsum (₹)": min_lumpsum,
            "Fund Manager": fund_manager,
            "Investment Strategy": strategy,
        })

    df = pd.DataFrame(records)

    # Add some missing values realistically (~2% missing in returns, ~1% in others)
    for col in ["Return 5Y (%)", "Return 1Y (%)"]:
        mask = np.random.random(len(df)) < 0.02
        df.loc[mask, col] = np.nan

    # Some funds with 0 fund age have no 3y/5y returns
    young_mask = df["Fund Age (Years)"] < 3
    df.loc[young_mask & (np.random.random(len(df)) < 0.3), "Return 3Y (%)"] = np.nan
    df.loc[young_mask & (np.random.random(len(df)) < 0.5), "Return 5Y (%)"] = np.nan

    return df


def main():
    # Create data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)

    print("📊 Generating Mutual Fund Dataset...")
    df = generate_dataset(2600)

    output_path = os.path.join(data_dir, "mutual_funds_raw.csv")
    df.to_csv(output_path, index=False)

    print(f"✅ Dataset generated: {len(df)} schemes")
    print(f"   Saved to: {output_path}")
    print(f"\n📋 Fund Type Distribution:")
    print(df["Fund Type"].value_counts().to_string())
    print(f"\n📋 Risk Level Distribution:")
    print(df["Risk Level"].value_counts().to_string())
    print(f"\n📋 Missing values:")
    print(df.isnull().sum()[df.isnull().sum() > 0].to_string())


if __name__ == "__main__":
    main()
