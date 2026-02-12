

# 📊 Mutual Fund Analysis Dashboard

### Python + Interactive Dashboard | Top 30 Low-Risk, High-Return Funds

A simple, interactive dashboard to help investors pick the **best mutual funds** from 2,500+ Indian schemes. Built with Python for analysis and a web dashboard for visualization.

---

## 🔹 Features

* **Filters:** Fund Type, Category, Risk, AMC, Rating
* **KPI Cards:** Total Funds, Total AUM, Avg 3Y Return, Expense, Min SIP
* **Charts:** Returns by Category, Top AMCs, AUM by Fund Type, Expense by Strategy, Manager AUM, Risk Distribution
* **Top 30 Funds Table:** Rank, Fund Name, AMC, Type, Risk, Rating, 3Y Return, Expense, AUM, Score

---

## 🔹 How It Works

1. **Generate Data:** 2,600 realistic fund records (returns, risk, AUM, etc.)
2. **Clean & Normalize:** Remove duplicates, fill missing values, scale numbers 0–1
3. **Score Funds:** Weighted score based on returns, expense, fund age, AUM, risk, and rating
4. **Top 30 Extraction:** Exported to CSV, Excel, and JSON for the dashboard

---

## 🔹 Tech Stack

Python, Pandas, NumPy, Scikit-Learn, HTML/CSS/JS, Chart.js, Excel (openpyxl)

---

## 🔹 Quick Start

```bash
# One-click run
run.bat

# Or manually
pip install -r requirements.txt
python analysis/generate_data.py
python analysis/analyze.py
python run_dashboard.py
# Open http://localhost:8050/dashboard/index.html
```

---

## 🔹 Results

* Schemes analyzed: 2,405
* Fund Types: 5 | Categories: 20 | AMCs: 30 | Managers: 36
* Best 3Y Return: 44.52% | Lowest Expense: 0.10%
* Average 3Y Return: 14.26% | Top Score: 100

---

## 🔹 Project Structure

```
analysis/        # Data scripts
dashboard/       # Web UI
data/            # Generated datasets
screenshots/     # Dashboard previews
run.bat          # One-click run
run_dashboard.py # Start dashboard
```

---



Do you want me to do that?
