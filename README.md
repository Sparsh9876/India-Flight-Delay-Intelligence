# ✈️ India Flight Delay Intelligence

![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

An industry-level end-to-end data analytics project analysing **India's domestic aviation network** using PostgreSQL, Python, and Power BI — built to mirror real workflows used at companies like **IndiGo, Air India, DGCA, Deloitte, and Deutsche Bank**.

---

## 📸 Dashboard Preview

| Page 1 — Executive Overview | Page 2 — Airline Analysis |
|---|---|
| ![Executive Overview](<img width="1543" height="870" alt="Page1" src="https://github.com/user-attachments/assets/249d8b1b-a0e5-41d6-8518-b280d25aac26" />) | ![Airline Analysis](<img width="1544" height="866" alt="Page2" src="https://github.com/user-attachments/assets/f69fdaaf-d061-4e16-b20e-cb53e2e94366" />)|

| Page 3 — Airport Analysis | Page 4 — Route Intelligence |
|---|---|
| ![Airport Analysis](<img width="1542" height="865" alt="Page3" src="https://github.com/user-attachments/assets/27e0720a-3aae-43cb-9da9-b12263879d61" />
) | ![Route Intelligence](<img width="1545" height="869" alt="Page4" src="https://github.com/user-attachments/assets/9a52e284-47f1-4da8-9454-56e8bc5eaff2" />
) |

| Page 5 — Insights & Recommendations |
|---|
| ![Insights](<img width="1547" height="870" alt="Page5" src="https://github.com/user-attachments/assets/0685cdcf-f15b-4f72-b178-43143b18969f" />
) |

---

## 📌 Project Overview

India's domestic aviation sector moved **167 million passengers** in 2025 — but growth is masking a deepening punctuality crisis. This project ingests 11 years of DGCA (Directorate General of Civil Aviation) data across four datasets, cleans and models it through a full **Python → PostgreSQL → Power BI** pipeline, and delivers a five-page interactive dashboard answering three core business questions:

- **Which airlines are on time — and which are in decline?**
- **How concentrated is traffic around a handful of hub airports?**
- **Which routes and months drive the most demand?**

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| PostgreSQL 15 + pgAdmin 4 | Database storage, table design, SQL aggregations, city-level rollups |
| Python 3.10+ | Data pipeline, cleaning, unpivoting, feature engineering |
| pandas | Data manipulation, wide-to-long transformation, aggregations |
| numpy | Numerical operations |
| matplotlib + seaborn + squarify | Publication-quality chart previews |
| SQLAlchemy + psycopg2 | Python ↔ PostgreSQL connection |
| Power BI Desktop | 5-page interactive dashboard, DAX measures, conditional formatting |
| PowerPoint | Custom dark-navy background theme applied across all pages |

---

## 🔄 Project Workflow

```
Raw DGCA CSV Files (4 tables)
    ↓
PostgreSQL Database
(pgAdmin 4 — table creation, import, SQL aggregations)
    ↓
Python Pipeline
(cleaning → unpivoting → feature engineering → dimension tables)
    ↓
Power BI Data Model
(star schema → DAX measures → relationships → 5-page dashboard)
    ↓
Business Insights & Recommendations
```

---

## 📁 Project Structure

```
india-flight-delay-intelligence/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── clean_carrier.csv          # Airline × month: passengers, aircraft, load factor
│   ├── clean_city.csv             # Route × month: origin, destination, passenger counts
│   ├── clean_otp.csv              # Airline × month: OTP % and status (2024)
│   ├── clean_daily.csv            # Daily OTP & PLF per airline (Jul 2021–Jun 2026)
│   ├── DailyLong.csv              # Unpivoted daily table (Python-generated)
│   ├── DimAirline.csv             # Airline dimension: key, full name, accent colour
│   ├── DimMonth.csv               # Month dimension: YearMonth key for relationships
│   └── airport_traffic.csv        # City-level traffic rollup (origin + destination)
│
├── notebooks/
│   └── data_cleaning.ipynb        # Full cleaning pipeline: raw → clean CSVs
│
├── sql/
│   └── flight_analysis.sql         # PostgreSQL: city-level traffic aggregation
│
├── powerbi/
│   └── India_Flight_Delay_Intelligence.pbix
│
├── screenshots/
│   ├── page1_executive_overview.png
│   ├── page2_airline_analysis.png
│   ├── page3_airport_analysis.png
│   ├── page4_route_intelligence.png
│   └── page5_insights.png
│
└── README.md
```

---

## 📊 Dataset

| Property | Value |
|---|---|
| Total raw tables | 4 CSV files |
| Total rows (combined) | 67,220 rows |
| Date range | January 2015 – June 2026 |
| Airlines tracked | 25 carriers |
| Routes tracked | 2,034 city-pairs |
| Cities served | 179 airports |
| Key tables | clean_carrier, clean_city, clean_otp, clean_daily |
| Target metrics | OTP %, Load Factor %, Market Share %, Passenger Count |
| Data source | DGCA (Directorate General of Civil Aviation), India |

---

## 📈 Key Results & Findings

| # | Finding | Value |
|---|---|---|
| 1 | Total passengers in 2025 | **167.1 million** |
| 2 | Total aircraft departures in 2025 | **1.14 million flights** |
| 3 | YoY passenger growth (2024 → 2025) | **+3.6%** |
| 4 | IndiGo market share — 2025 vs 2015 | **64.1%** (up from 36.8%) |
| 5 | Industry OTP (trailing 12 months) | **74.8%** — below the 80% benchmark hit in 2022 |
| 6 | Best punctuality airline — 2024 | **Akasa Air at 80.9%** |
| 7 | Worst punctuality airline — 2024 | **Alliance Air at 51.2%** |
| 8 | SpiceJet OTP trajectory (2021 → 2026) | **90.3% → 47%** (collapse) |
| 9 | Airline-months below DGCA minimum OTP | **25 of 35 (71%)** |
| 10 | Top 3 airports' share of all traffic | **Delhi + Mumbai + Bengaluru = 41%** |
| 11 | Top 6 airports' share of all traffic | **59%** |
| 12 | Busiest route (cumulative, 2015–2026) | **Bengaluru → Delhi — 42.6M passengers** |
| 13 | Peak travel month | **December — 128M passengers** |
| 14 | Quietest travel month | **May — 89M passengers** |

---

## 🧹 Data Cleaning Steps

| Step | Check | Result |
|---|---|---|
| 1 | Null value audit across all 4 tables | Handled via imputation and exclusion per column |
| 2 | Data type corrections | `date` column fixed from Date/Time → Date for Power BI join |
| 3 | Wide-to-long transformation | `clean_daily` unpivoted from 5 airline columns → `DailyLong` (AirlineKey, OTP_Pct, PLF_Pct) |
| 4 | Airline name standardisation | Short codes (`indigo`) mapped to full names (`IndiGo`) via `DimAirline` |
| 5 | Airport traffic rollup | `clean_city` UNION'd on origin + destination → `airport_traffic.csv` |
| 6 | YearMonth key engineering | `year * 100 + month` computed in both Python and DAX for relationship join |
| 7 | Duplicate route check | 2,034 unique city-pairs confirmed |
| 8 | PLF null handling | SpiceJet, Vistara, Akasa load factor data absent from DGCA — blanked intentionally, not dropped |

---

## ⚙️ Feature Engineering

| New Column / Table | Created From | Purpose |
|---|---|---|
| `DailyLong[AirlineKey]` | `clean_daily` wide columns | Enables single slicer to filter all 5 airlines |
| `DailyLong[OTP_Pct]` | `otp_indigo`, `otp_airindia` … | Unpivoted OTP for trend analysis |
| `DailyLong[PLF_Pct]` | `plf_indigo`, `plf_airindia` | Unpivoted load factor (IndiGo + Air India only) |
| `airport_traffic[airport_traffic]` | `clean_city` origin + dest | Total city footprint = inbound + outbound passengers |
| `DimMonth[YearMonth]` | `year * 100 + month` | Unique monthly key; solves duplicate-key error on DimDate |
| `DimAirline[AccentColor]` | Manual | Enforces consistent per-airline colour across all 5 pages |
| `OTP Status bucket` | `otp_pct` | Above 85% / Meets 75% / Below Min — used for conditional formatting |

---

## 📉 DAX Measures Built

| Measure | Formula Pattern | Used On |
|---|---|---|
| `Total Passengers` | `SUM(Carrier[passenger_count])` | All pages |
| `YoY Passenger Growth %` | `FILTER(ALL(DimMonth), Year = SELECTEDVALUE - 1)` | Page 1 KPI |
| `Market Share %` | `DIVIDE([Total Passengers], CALCULATE(..., ALL(airline)))` | Pages 1, 2, 5 |
| `Avg Load Factor %` | `AVERAGE(Carrier[load_factor_pct]) / 100` | Pages 2, 5 |
| `Avg OTP %` | `AVERAGE(DailyLong[OTP_Pct])` | Pages 1, 2 |
| `Avg OTP % (Scorecard)` | `LOOKUPVALUE` + `TREATAS` cross-table translation | Page 5 only |
| `Airport Cumulative Share %` | `RANKX` rolling sum / grand total | Page 3 Pareto |
| `Unique Routes Tracked` | `COUNTROWS(SUMMARIZE(...))` with `ALL()` | Page 3 card |
| `Route Rank` | `RANKX(ALL(origin, dest), [Total Route Passengers])` | Page 4 table |

---

## 📋 Power BI Dashboard

**5-page interactive report with 3 cross-page slicers (Year, Month, Airline Name)**

**Page 1 — Executive Overview**
- 5 KPI cards (Total Passengers, YoY Growth %, Avg Load Factor %, Avg Industry OTP %, Aircraft Departures)
- Area line chart — Total Passengers by Year (2015–2026) with 2026 partial annotation
- Donut chart — Market Share % by airline (2025)
- Combo chart — Avg OTP % (line) vs Avg Load Factor % (column) by year

**Page 2 — Airline Analysis**
- Horizontal bar chart — OTP % by airline (2024), colour-coded by status (Above 85% / Meets 75% / Below Min)
- Multi-line chart — Monthly OTP % trend per airline (Jul 2021 – Jun 2026) — shows SpiceJet collapse visually
- Line chart — Avg Load Factor % by year, one line per airline
- Heatmap matrix — Market Share % × Airline × Year (2020–2025)

**Page 3 — Airport Analysis**
- Horizontal bar chart — Top 15 cities by airport traffic (2025)
- Line and clustered column chart — Pareto concentration curve (individual share % + cumulative %)
- Bubble map — City as location, bubble size = airport traffic
- 2 KPI cards — Unique Cities Served (179) / Unique Routes Tracked (2,034)

**Page 4 — Route Intelligence**
- Table — Top 20 routes by cumulative passengers with data bars
- Column chart — Seasonality: Total Passengers by Month (all years summed), highlighting Dec peak and May trough
- Bubble map — Origin cities sized by outbound passenger volume

**Page 5 — Insights & Recommendations**
- 5 insight cards (headline stat + context body text)
- Scorecard matrix — Airline × {Market Share %, Avg Load Factor %, Avg OTP %} with OTP conditional formatting
- Recommendations text block grouped by audience (Airlines / Airport Operators / Route Planners)

---

## 💡 Business Recommendations

| # | Insight | Recommendation |
|---|---|---|
| 1 | SpiceJet OTP: 90% → 47% (2021–2026) | Immediate operational root-cause review — punctuality at sub-50% threatens route licences |
| 2 | Akasa Air leads at 80.9% OTP despite being newest entrant | Study Akasa's scheduling and turnaround discipline as an industry template |
| 3 | 3 airports carry 41% of all traffic | Prioritise infrastructure and slot investment at Delhi, Mumbai, Bengaluru first |
| 4 | Top 6 airports carry 59% of all traffic | Hub congestion drives cascading network delays — expand terminal capacity |
| 5 | 71% of airline-months below DGCA minimum OTP | DGCA should enforce stricter monthly compliance reviews with financial penalties |
| 6 | Ahmedabad–Delhi: 21.3M cumulative pax | Examine seat-to-demand ratio — potential under-served corridor |
| 7 | Delhi–Srinagar: 19.8M cumulative pax | Tourism-driven corridor worth capacity expansion |
| 8 | May is the quietest month (89M pax) | Airlines should schedule heavy maintenance in May to minimise revenue impact |

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/Sparsh9876/india-flight-delay-intelligence.git
cd india-flight-delay-intelligence
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up PostgreSQL
```
1. Open pgAdmin 4
2. Create a new database: india_flights_analytics
3. Run: sql/flight_analysis.sql
4. Import the 4 clean CSV files from the data/ folder
5. Update your credentials in the Python notebook
```

```python
# In notebooks/data_cleaning.ipynb, update:
DB_PASSWORD = "YourPassword"
DB_NAME = "india_flights_analytics"
```


### 4. Open Power BI
```
1. Open powerbi/India_Flight_Delay_Intelligence.pbix in Power BI Desktop
2. All CSV sources are pre-connected relative to the /data folder
3. Click Refresh to reload data
```

---

## 📦 Requirements

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
squarify>=0.4.3
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
jupyter>=1.0.0
```

---

## 🎯 Target Roles

This project demonstrates skills required for:

- **Data Analyst**
- **Business Intelligence Analyst**
- **Aviation / Transport Analytics Analyst**
- **Operations Analytics Analyst**

At companies like: **IndiGo · Air India · DGCA · Deutsche Bank · Google · Deloitte · PwC India · Morgan Stanley · Adobe · Amazon**

---

## 🙋 About Me

🎓 MCA Student — ML & AI Specialisation | Amity University, Noida
💼 Aspiring Data Analyst / Junior Data Scientist
🛠 Skills: Python · SQL · Power BI · Tableau · pandas · DAX · Data Visualisation · EDA
🔗 LinkedIn: [linkedin.com/in/sparshbhatnagar](https://linkedin.com/in/sparshbhatnagar)
📧 Email: sparsh.bhatnagar13@gmail.com
🐙 GitHub: [github.com/Sparsh9876](https://github.com/Sparsh9876)

---

## ⭐ If you found this project useful

Give it a star ⭐ on GitHub — it helps others find the project!

---

*Built with ❤️ as part of my Data Analytics portfolio — demonstrating end-to-end analytics from raw government data to executive-ready dashboards.*
