🇻🇪 Venezuela Economic Indicators Analysis (1990–2024)
Exploratory Data Analysis + Interactive Dashboard
Author: Vilma Windevoxchel · GitHub
---
Overview
Comprehensive EDA of Venezuela's macroeconomic trajectory using public data from World Bank WDI, IMF WEO 2025, OPEC/EIA, and CEPAL. Venezuela offers one of the richest analytical case studies in Latin American history: oil boom, catastrophic collapse, hyperinflation, and partial recovery.
---
Key Findings
Finding	Value	Context
GDP per capita decline	−77% (2013→2020)	$6,369 → $1,451
Peak inflation	65,374% (2018)	Top 5 globally since WWII
Oil production decline	−82% (peak → 2020)	~3,240 kbd → 570 kbd
Oil-GDP correlation	r = 0.574	Resource curse confirmed
2024 GDP growth	+5.3%	Partial recovery underway
2024 inflation	254.9%	Still critically elevated
---
Run the Project
```bash
git clone https://github.com/VWinde/venezuela-economic-indicators-analysis.git
cd venezuela-economic-indicators-analysis
pip install -r requirements.txt

# Generate all 6 charts
python notebooks/01_exploratory_analysis.py

# Launch interactive dashboard
streamlit run app.py
```
---
Project Structure
```
├── notebooks/01_exploratory_analysis.py   # EDA — 6 publication charts
├── src/                                   # Reusable modules
├── data/raw/venezuela_complete_data.csv   # Dataset 1990–2024
├── outputs/figures/                       # 6 PNG charts
├── venezuela-economic-indicators.py                                 # Streamlit dashboard
└── requirements.txt
```
---
Data Sources
World Bank WDI — GDP, inflation, oil rents, unemployment (1990–2024)
IMF WEO Oct 2025 — National accounts estimates post-2018
OPEC / EIA — Oil production series
CEPAL — Latin American regional benchmarks
---
Author
Vilma Windevoxchel · Data Analyst & BI Specialist · BS Economics · MSc PM (in progress)
LinkedIn · GitHub
