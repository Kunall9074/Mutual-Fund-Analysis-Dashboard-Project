# 📊 Mutual Fund Analysis Dashboard

### 🔍 Python + Interactive Web Dashboard | Top 30 Low-Risk, High-Return Schemes

> **2500+ Indian Mutual Fund Schemes ka data-driven analysis karke Top 30 best funds identify kiye gaye hain — Python (Pandas, Sklearn) se data clean, normalize, score kiya aur ek premium interactive web dashboard banaya for visualisation.**

---

## 🖼️ Dashboard Preview

> **Note:** Screenshots generate karne ke liye `take_screenshots.py` run karo (neeche instructions hain). Screenshots `screenshots/` folder mein save honge.

<!-- After running take_screenshots.py, uncomment these lines: -->
<!-- ![Dashboard Overview](screenshots/01_dashboard_overview.png) -->
<!-- ![Charts Section](screenshots/02_charts_section.png) -->
<!-- ![Insights & Table](screenshots/03_insights_table.png) -->
<!-- ![Full Dashboard](screenshots/04_full_dashboard.png) -->

### 📸 Screenshots Generate Kaise Kare

```bash
pip install selenium
python take_screenshots.py
```

Ye 4 screenshots automatically capture karega:
1. `01_dashboard_overview.png` — Header, Filters, KPI Cards
2. `02_charts_section.png` — All 6 Interactive Charts
3. `03_insights_table.png` — Insight Cards + Top 30 Table
4. `04_full_dashboard.png` — Full Page Screenshot

---

## 🧠 Project Goal (Project ka Uddeshya)

Is project ka main goal hai:

1. **2500+ mutual fund schemes** ka data collect karna
2. Data ko **clean, normalize aur score** karna Python se
3. **Top 30 best funds identify** karna jo **low risk + high return** dete hain
4. Ek **beautiful interactive dashboard** banana jisme sab kuch visually samajh aaye

> 💡 **Ye project un logon ke liye hai** jo mutual funds mein invest karna chahte hain lekin confused hain ki **konsa fund best hai**. Is dashboard se aap data ke basis par smart decisions le sakte ho.

---

## 🛠️ Tools & Technologies Used

| Tool | Kya Kaam Karta Hai |
|------|---------------------|
| **Python** | Data processing ka main engine — saara calculation Python karega |
| **Pandas** | CSV/Excel files padhna, data clean karna, tables banana |
| **Scikit-Learn (Sklearn)** | `MinMaxScaler` se data ko 0-1 scale pe normalize karna |
| **NumPy** | Random realistic data generate karna |
| **Chart.js** | Interactive charts banana (donut, bar, polar area) |
| **HTML/CSS/JS** | Web dashboard ka UI banana — dark theme, animations |
| **Excel (openpyxl)** | Top 30 funds ko `.xlsx` file mein export karna |

---

## 🚀 Quick Start — Kaise Run Kare?

### ✅ Option 1: One Click Run (Sabse Aasan)

```
run.bat
```

> Bas **double-click** karo `run.bat` pe — sab kuch automatically hoga aur dashboard browser mein khul jayega! 🎉

### ✅ Option 2: Manual Steps

```bash
# Step 1: Dependencies install karo
pip install -r requirements.txt

# Step 2: Dataset generate karo (2600 schemes banega)
python analysis/generate_data.py

# Step 3: Analysis run karo (clean → normalize → score → rank)
python analysis/analyze.py

# Step 4: Dashboard start karo
python run_dashboard.py
```

> 🌐 Dashboard yahan khulega: **http://localhost:8050/dashboard/index.html**

---

## 🐍 Python Analysis Pipeline — Step by Step Samjho

### 📌 Step 1: Data Generation (`generate_data.py`)

Is script se **2600 realistic Indian mutual fund schemes** generate hote hain.

**Kya kya data generate hota hai:**

| Field | Example | Description |
|-------|---------|-------------|
| Scheme Name | SBI Bluechip Large Cap Fund - Direct Plan - Growth | Fund ka poora naam |
| AMC Name | SBI Mutual Fund | Asset Management Company (30 real AMCs) |
| Fund Type | Equity, Debt, Hybrid, Solution Oriented, Other | Fund ka type |
| Category | Large Cap, Mid Cap, Small Cap, Liquid, etc. | 20 categories hain |
| Sub Category | Bluechip, Index, Growth, Banking, etc. | Category ke andar sub-type |
| Risk Level | Low → Low to Moderate → Moderate → Moderately High → High → Very High | Kitna risky hai |
| Fund Rating | 1 to 5 Stars ⭐ | Fund ki quality rating |
| Return 1Y (%) | 15.3% | Last 1 saal ka return |
| Return 3Y (%) | 22.5% | Last 3 saal ka return |
| Return 5Y (%) | 18.7% | Last 5 saal ka return |
| Expense Ratio (%) | 0.85% | Fund manage karne ka charge |
| NAV (₹) | ₹245.60 | Net Asset Value — ek unit ki kimat |
| AUM (Cr) | ₹5,400 Cr | Total paisa jo fund mein invested hai |
| Min SIP (₹) | ₹500 | Minimum monthly SIP amount |
| Min Lumpsum (₹) | ₹5,000 | One-time invest karne ka minimum |
| Fund Age (Years) | 12.5 years | Fund kitne saal purana hai |
| Fund Manager | Prashant Jain | Fund kaun manage karta hai (36 managers) |
| Investment Strategy | Growth, Value, Blend, Index, etc. | Fund ki investment strategy |

**Fund Type Distribution:**

```
Equity            — ~45% (sabse zyada)
Debt              — ~25%
Hybrid            — ~18%
Solution Oriented — ~7%
Other             — ~5%
```

---

### 📌 Step 2: Data Cleaning (`analyze.py` — Step 1)

Raw data mein problems hoti hain — unhe fix karna zaroori hai.

| Problem | Solution |
|---------|----------|
| Duplicate schemes | `drop_duplicates()` se remove (2600 → ~2405 bache) |
| Missing return values (NaN) | Same category ka **median** value se fill kiya |
| Negative expense ratios | Minimum 0.01% set kiya |
| Fund age 0 ya negative | Minimum 0.1 years rakha |

---

### 📌 Step 3: Data Description (`analyze.py` — Step 2)

Cleaned data ka statistical summary nikaala:

```
                Mean      Min      Max    Std Dev
Return 3Y (%)   14.26%    2.32%    44.52%   8.65%
Expense (%)      0.99%    0.10%     2.49%   0.52%
AUM (Cr)     ₹3,416 Cr   ₹3.5 Cr  ₹2.5L Cr  ₹9,172 Cr
Fund Age       15.3 yrs   0.5 yr    30 yrs   8.5 yrs
```

---

### 📌 Step 4: Data Normalization (`analyze.py` — Step 3)

**Problem:** Returns `2% se 44%` tak hain, Expense `0.1% se 2.5%` tak — inhe compare nahi kar sakte directly.

**Solution:** `MinMaxScaler` se sab values ko **0 se 1 scale** pe laaye.

```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
# Ab 0 = sabse kharab, 1 = sabse accha
```

| Original Value | Normalized (0–1) |
|----------------|-------------------|
| Return 3Y: 44.52% (max) | 1.00 |
| Return 3Y: 2.32% (min) | 0.00 |
| Return 3Y: 22.5% (middle) | ~0.48 |

---

### 📌 Step 5: Scoring Formula (`analyze.py` — Step 4)

Har fund ko ek **Score (0 to 100)** diya gaya based on multiple factors:

```
Score = 0.40 × Normalized 3Y Return          (sabse zyada weight — long-term return)
      + 0.25 × (1 - Normalized Expense Ratio) (kam expense = accha)
      + 0.20 × Normalized 1Y Return           (recent performance)
      + 0.10 × Normalized Fund Age             (experience matters)
      + 0.05 × Normalized AUM                  (zyada AUM = zyada trust)
      + Risk Bonus                             (Low risk = +0.05, High risk = -0.02)
      + Rating Bonus                           (5-star = +0.04, 1-star = -0.04)
```

**Samjho aise:**

| Factor | Weight | Kyun? |
|--------|--------|-------|
| 3-Year Return | 40% | Long-term growth sabse important hai |
| Low Expense Ratio | 25% | Kam charge = zyada paisa aapka |
| 1-Year Return | 20% | Recent performance bhi dekhna chahiye |
| Fund Age | 10% | Purane funds zyada trustworthy hote hain |
| AUM (Fund Size) | 5% | Bade funds mein zyada investors ka bharosa hai |
| Risk Bonus | Extra | Low risk funds ko bonus milta hai |
| Rating Bonus | Extra | High rated funds ko bonus milta hai |

---

### 📌 Step 6: Top 30 Extraction (`analyze.py` — Step 5)

Score ke basis par **Top 30 funds** extract kiye aur save kiye:

| Output File | Format | Description |
|-------------|--------|-------------|
| `top_30_mutual_funds.csv` | CSV | Top 30 funds ka data |
| `top_30_mutual_funds.xlsx` | Excel | Same data Excel format mein |
| `mutual_funds_processed.csv` | CSV | All 2405 funds with scores |
| `dashboard_data.json` | JSON | Dashboard ke liye aggregated data |

---

## 📈 Dashboard Features — Kya Kya Hai Dashboard Mein

### 🔽 Dynamic Filters (5 Filters)

Aap in filters se data ko real-time filter kar sakte ho — sab kuch (charts, KPIs, table) turant update hoga:

| Filter | Options | Kya Karta Hai |
|--------|---------|---------------|
| **Fund Type** | Equity, Debt, Hybrid, Solution Oriented, Other | Fund type se filter |
| **Category** | Large Cap, Small Cap, Mid Cap, Liquid, etc. (20 options) | Category wise dekhne ke liye |
| **Risk Level** | Low → Very High (6 levels) | Risk appetite ke hisab se |
| **AMC Name** | SBI, HDFC, ICICI, Axis, etc. (30 AMCs) | Kisi specific AMC ka data dekhne ke liye |
| **Fund Rating** | 1 ⭐ to 5 ⭐⭐⭐⭐⭐ | Quality rating se filter |

> 🔄 **Reset** button se sab filters ek click mein clear ho jaayenge!

---

### 📊 KPI Cards (5 Key Metrics)

Dashboard ke top pe 5 animated cards hain:

| KPI | Kya Dikhata Hai | Example Value |
|-----|-----------------|---------------|
| 💼 **Total Funds** | Kitne funds hain (filter ke baad) | 2,405 |
| 💰 **Total AUM** | Total paisa invested (in Crores) | ₹82.2 L Cr |
| 📈 **Avg 3Y Return** | Average 3-year return percentage | 14.3% |
| ⏱️ **Avg Expense Ratio** | Average charge percentage | 0.99% |
| 🎒 **Avg Min SIP** | Average minimum SIP amount | ₹1,467 |

---

### 📊 Interactive Charts (6 Charts)

| # | Chart Name | Type | Kya Dikhata Hai |
|---|------------|------|-----------------|
| 1 | **3-Year Returns by Category** | 🍩 Donut | Konsi category mein zyada return hai |
| 2 | **Top AMCs by Avg Return** | 📊 Bar | Konsi AMC sabse accha perform kar rahi hai |
| 3 | **Total AUM by Fund Type** | 🍩 Doughnut | Equity/Debt/Hybrid mein kitna paisa hai |
| 4 | **Expense Ratio by Strategy** | 📊 Bar | Konsi strategy mein zyada charge hai |
| 5 | **Fund Manager AUM Comparison** | 📊 Horizontal Bar | Konsa fund manager sabse zyada paisa manage karta hai |
| 6 | **Risk Level Distribution** | 🎯 Polar Area | Kitne funds Low/Moderate/High risk mein hain |

> 💡 Sab charts **hover** karne pe tooltip dikhate hain with exact values!

---

### 💡 Key Insights (6 Auto-Generated Cards)

Dashboard automatically 6 insights generate karta hai:

| Insight | Kya Batata Hai |
|---------|----------------|
| 📈 Average 3-Year Return | Overall average return kitna hai |
| 🏆 Top Performer | Sabse zyada return dene wala fund |
| 💰 Lowest Expense Ratio | Sabse kam charge lene wala fund |
| 🏦 Largest AUM | Sabse bada fund (size wise) |
| 📊 Dominant Fund Type | Konsa fund type sabse zyada hai |
| 🛡️ Low-Risk Options | Kitne funds low-risk hain |

---

### 📋 Top 30 Funds Table

Sabse neeche ek **sortable table** hai jo Top 30 funds dikhata hai:

- **Rank #** — Fund ka ranking (score ke basis par)
- **Scheme Name** — Fund ka poora naam
- **AMC** — Asset Management Company
- **Type** — Equity/Debt/Hybrid
- **Category** — Large Cap/Mid Cap etc.
- **Risk** — Color-coded badge (🟢 Low → 🔴 Very High)
- **Rating** — ⭐⭐⭐⭐⭐ Stars
- **3Y Return** — Color-coded (🟢 >20%, 🟡 10-20%, 🔴 <10%)
- **Expense %** — Fund ka charge
- **AUM** — Fund ka size
- **Score** — Final score (0-100)

> 🔃 Kisi bhi column pe click karke **sort** kar sakte ho (ascending/descending)!

---

## 📁 Project Structure

```
M/
│
├── 📂 analysis/                    ← Python Analysis Scripts
│   ├── generate_data.py            ← 2600 mutual fund schemes generate karta hai
│   └── analyze.py                  ← Data clean → normalize → score → rank
│
├── 📂 dashboard/                   ← Web Dashboard Files
│   ├── index.html                  ← Dashboard ka HTML structure
│   ├── style.css                   ← Premium dark theme CSS
│   └── app.js                      ← Chart.js + Filters + Interactivity
│
├── 📂 data/                        ← Generated Data Files
│   ├── mutual_funds_raw.csv        ← Raw generated data (2600 rows)
│   ├── mutual_funds_processed.csv  ← Cleaned + scored data (2405 rows)
│   ├── top_30_mutual_funds.csv     ← Top 30 best funds (CSV)
│   ├── top_30_mutual_funds.xlsx    ← Top 30 best funds (Excel)
│   └── dashboard_data.json         ← Aggregated data for dashboard
│
├── 📂 screenshots/                 ← Dashboard screenshots (auto-generated)
│
├── requirements.txt                ← Python dependencies
├── run.bat                         ← One-click run script
├── run_dashboard.py                ← HTTP server for dashboard
├── take_screenshots.py             ← Auto-screenshot capture script
└── README.md                       ← Ye file! 📖
```

---

## 🎨 Dashboard Design

- **Theme:** Premium Dark Mode (Navy + Charcoal)
- **Style:** Glassmorphism cards with blur effects
- **Colors:** Indigo → Cyan → Violet gradient accents
- **Font:** Inter (Google Fonts)
- **Animations:** Fade-in cards, animated KPI counters, smooth chart transitions
- **Responsive:** Desktop, Tablet, Mobile — sab pe kaam karega

---

## 🧪 Technical Details

### Scoring Formula Explained

```python
# Weights — returns ko sabse zyada importance di gayi hai
WEIGHTS = {
    "3Y Return":     0.40,   # Long-term growth
    "Expense Ratio": 0.25,   # Lower = better (inverted)
    "1Y Return":     0.20,   # Recent performance
    "Fund Age":      0.10,   # Experience
    "AUM":           0.05,   # Investor confidence
}

# Risk Bonus
# Low risk      → +0.05
# Moderate      → +0.01
# High risk     → -0.02
# Very High     → -0.05

# Rating Bonus
# 5 Star  → +0.04
# 3 Star  →  0.00
# 1 Star  → -0.04
```

### Data Normalization

```python
from sklearn.preprocessing import MinMaxScaler

# MinMaxScaler formula:
# normalized = (value - min) / (max - min)
# Output: 0.0 (worst) to 1.0 (best)
```

---

## 📝 Key Results

| Metric | Value |
|--------|-------|
| Total Schemes Analyzed | 2,405 (after cleaning) |
| Fund Types | 5 |
| Categories | 20 |
| AMCs | 30 |
| Fund Managers | 36 |
| Top Score | 100.0 |
| Best 3Y Return | 44.52% |
| Lowest Expense Ratio | 0.10% |
| Average 3Y Return | 14.26% |

---

## 🤝 Contributing

Feel free to fork, explore, and contribute! 

### Ideas for Improvement:
- Real mutual fund API se live data fetch karna
- More charts aur analysis add karna (Sharpe Ratio, Sortino Ratio)
- User portfolio tracking feature
- Export to PDF report

---

## 📜 License

Open Source — Free to use for learning and projects! 🎓

---

> **💡 Remember:** *"The best time to start investing was 20 years ago. The second best time is NOW."*
