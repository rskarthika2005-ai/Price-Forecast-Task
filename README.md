# Monthly Price Forecasting — 12-Month Price Forecast

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=220&text=PRICE%20FORECAST&fontSize=48&fontAlignY=38&desc=TIME%20SERIES%20%7C%20ARIMA%20%7C%2012-MONTH%20FORECAST&descAlignY=60&animation=fadeIn&fontColor=ffffff&color=0:0F766E,50:0D9488,100:2563EB" alt="Price Forecast"/>

### Time Series Forecasting • Model Comparison • Business Recommendations

Reads 20 years of monthly prices, compares several models fairly, and forecasts the next 12 months with a 95% confidence band.

<img src="https://img.shields.io/badge/Time%20Series-0F766E?style=for-the-badge"/>
<img src="https://img.shields.io/badge/ARIMA-0D9488?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>

<br/>

### Developed by Karthika S

📧 [rskarthika08@gmail.com](mailto:rskarthika08@gmail.com)

<br/>

<a href="https://price-forecast-task-yl4dwyfy4ggws3jnlvajn9.streamlit.app/">
<img src="https://img.shields.io/badge/Live%20Dashboard-Open-0D9488?style=for-the-badge&logo=streamlit&logoColor=white" alt="Open Live Dashboard"/>
</a>

<a href="PASTE-GITHUB-REPO-LINK-HERE">
<img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Repository"/>
</a>

</div>

---

## ✦ ABOUT THE PROJECT

The task was to use historical monthly average prices to forecast the next 12 months, compare several models fairly, and turn the forecast into business advice.

The project gives three things:

- **Forecasting:** a 16-section notebook that cleans the data, tests stationarity, compares models and forecasts 12 months ahead.
- **Business Advice:** recommendations that manage price risk, plus a way to measure whether they worked.
- **Service:** a Streamlit dashboard and a FastAPI endpoint, with a monitoring plan for production.

### End-to-End Workflow

```text
Monthly Price CSV
        ↓
Cleaning (missing values, duplicates, outliers, anomalies)
        ↓
Stationarity Check (ADF test, differencing)
        ↓
Time-Based Split (last 12 months as test)
        ↓
Baselines + SARIMA, ARIMA, Prophet, XGBoost
        ↓
Evaluation (MAE, RMSE, MAPE, train vs test)
        ↓
Final 12-Month Forecast + Business Recommendations
        ↓
Dashboard • API • Monitoring Plan
```

### Quick Navigation

[Objective](#-project-objective) • [Overview](#-project-overview) • [Findings in the Data](#-findings-in-the-data) • [How I Solved It](#-how-i-solved-it) • [Results](#-results) • [Tools Used](#-tools-used) • [Skills](#-skills-demonstrated) • [Structure](#-project-structure) • [How to Run](#-how-to-run) • [Limitations](#-limitations) • [Recommendation](#-final-recommendation)

---

## ✦ PROJECT OBJECTIVE

A forecast is only useful if it is tested honestly. Time series data must never be split randomly, because that lets the model see the future. So every model was trained on the past only and tested on the **last 12 months**.

Every model also had to beat a simple baseline. If a fancy model cannot beat "tomorrow equals today", the model adds no value.

---

## ✦ PROJECT OVERVIEW

<table align="center">
<tr>
<td align="center" width="25%">

### 249

Monthly Prices

</td>
<td align="center" width="25%">

### 237

Training Months

</td>
<td align="center" width="25%">

### 12

Test Months

</td>
<td align="center" width="25%">

### 7

Models Compared

</td>
</tr>
<tr>
<td align="center">

### 9.12%

Best Test MAPE

</td>
<td align="center">

### 15,750

Forecast Price

</td>
<td align="center">

### 7

High-Price Outliers Kept

</td>
<td align="center">

### 16

Notebook Sections

</td>
</tr>
</table>

---

## ✦ FINDINGS IN THE DATA

- **Complete data.** 249 monthly prices from Jan 2005 to Sep 2025, with no missing months and no duplicates.
- **Multi-year cycles.** Prices peak around 2011, 2014-15, 2020 and 2024 instead of following one straight trend.
- **Weak seasonality.** The seasonal part is only about ±250 on prices ranging from 3,500 to 16,000.
- **A level shift in 2024.** Prices jumped and stayed between 11,000 and 16,000. Seven months were flagged as IQR outliers (Dec 2023, Apr-Jul 2024, Jul 2025). They sit in consecutive months, so they look like a real market event and were **kept, not deleted**.
- **Non-stationary prices.** The ADF test gave p = 0.4669 on the original prices and p = 0.0 after one difference, so the models use d = 1.

---

## ✦ HOW I SOLVED IT

### Stage 1: Understand and Clean

1. Converted dates, sorted by time and set the date as the index.
2. Checked missing months, duplicates, IQR outliers and rolling-mean anomalies.
3. Decided each outlier by asking: is it an error or a real event?

### Stage 2: Test Stationarity

1. Ran the ADF test on prices and on first differences.
2. Used ACF and PACF plots to keep model orders small.

### Stage 3: Build and Compare Models

| Model | Idea |
|---|---|
| Seasonal Naive | Same month last year |
| Naive (last value) | Every month equals the last known price |
| SARIMA | Statistical model with trend and seasonal parts |
| ARIMA | Order chosen by the lowest AIC (grid over p, q) |
| Prophet | Smooth trend plus yearly seasonality |
| XGBoost | Lag features, month and rolling mean, tuned with `TimeSeriesSplit` |

### Stage 4: Forecast and Advise

The best model was retrained on all the data, forecast 12 months ahead, and turned into business recommendations.

---

## ✦ RESULTS

All models were tested on the last 12 months.

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Naive (last value) | 1160.33 | 1565.74 | 9.12% |
| **ARIMA (0,1,0)** | 1160.33 | 1565.74 | **9.12%** |
| XGBoost (tuned) | 1185.02 | 1577.89 | 9.18% |
| XGBoost | 1231.44 | 1596.41 | 9.45% |
| SARIMA (1,1,1)(1,1,1,12) | 1740.08 | 2167.36 | 13.75% |
| Seasonal Naive | 2296.42 | 2921.06 | 17.35% |
| Prophet | 4373.92 | 4626.53 | 30.81% |

### Model selection

- **Selected:** ARIMA (0,1,0). It ties for the lowest test error, is the simplest model and gives confidence intervals.
- **Challenger:** tuned XGBoost stays for monitoring.
- **Why the others lost:** Prophet under-predicted because it missed the 2024 jump, and SARIMA's seasonal terms added noise because seasonality is weak.
- **Overfitting check:** tuned XGBoost has train MAPE 3.64% against test MAPE 9.18%, a sign of mild overfitting.

### Final forecast (Oct 2025 to Sep 2026)

- Point forecast: about **15,750** for every month (the last known price).
- 95% range: widens from **14,107 to 17,393** (Oct 2025) to **10,060 to 21,440** (Sep 2026).
- The current level is far above the long-term average of about 7,900, so downside risk is real.

---

## ✦ TOOLS USED

| Tool | Purpose |
|---|---|
| Python, Pandas, NumPy | Data handling and analysis |
| Statsmodels | ADF test, decomposition, SARIMA and ARIMA |
| Prophet | Trend and seasonality model |
| XGBoost, Scikit-learn | Lag-feature model, tuning and metrics |
| Matplotlib | Charts |
| FastAPI | `/predict` endpoint |
| Streamlit | Interactive dashboard |
| Claude | Planning, coding, debugging and checking |

---

## ✦ SKILLS DEMONSTRATED

<div align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Git%20%26%20GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>

</div>

| Skill Area | What I Did in This Project |
|---|---|
| 📈 **Time series analysis** | Checked trend, seasonality and level shifts, and tested stationarity with the ADF test and differencing |
| 🧹 **Data cleaning** | Checked missing months, duplicates, outliers and anomalies, and kept real events instead of deleting them blindly |
| 🤖 **Model building** | Built SARIMA, ARIMA, Prophet and XGBoost with lag features |
| 📏 **Honest evaluation** | Used a time-based split, baselines, MAE, RMSE and MAPE, and compared train and test error |
| 🎯 **Model selection** | Chose the simplest model that tied for the lowest error and kept a challenger |
| 💼 **Business thinking** | Turned a flat forecast with a wide band into a risk-management plan and a way to measure its effect |
| 🚀 **Deployment** | Built a FastAPI endpoint and a Streamlit dashboard, and planned Django and frontend integration |
| 🔍 **Monitoring plan** | Planned drift checks, a 15% MAPE alert, monthly retraining and champion/challenger updates |
| 🗂️ **Clean project structure** | Split the project into notebook, dashboard, API, model and data folders |

---

## ✦ PROJECT STRUCTURE

```text
Price-Forecast/
│
├── price_forecast.ipynb     # Full notebook (16 sections)
├── requirements.txt         # Python libraries needed
├── README.md                # Project overview, results, how to run
│
├── dashboard/
│   └── app.py               # Streamlit dashboard
│
├── fastapi_app/
│   └── main.py              # /predict endpoint with dates and 95% bounds
│
├── django_app/              # Django integration code
│
├── models/
│   └── best_model.pkl       # Saved ARIMA (0,1,0) model
│
└── data/
    ├── price_data.csv       # Monthly prices (date, avg_monthly_price)
    └── price_data.txt       # Column descriptions
```

---

## ✦ HOW TO RUN

### Clean-machine setup

```bash
git clone PASTE-GITHUB-REPO-LINK-HERE
cd Price-Forecast
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Run the notebook

```bash
jupyter notebook price_forecast.ipynb
```

Choose **Restart and Run All**.

### Start the dashboard

```bash
streamlit run dashboard/app.py
```

### Start the API

```bash
uvicorn fastapi_app.main:app --reload
```

Then open `http://127.0.0.1:8000/predict?months=12`.

---

## ✦ THREE WAYS TO VIEW THE OUTPUT

### 1. Streamlit Dashboard (`dashboard/app.py`)

- **Forecast:** history, 12-month forecast and the 95% confidence band
- **Table:** monthly forecast with lower and upper bounds
- **Model comparison:** test error of every model
- **Budget planner:** plan purchases using the forecast range
- **Monitoring check:** compare an actual price with the forecast

### 2. API Endpoint (`fastapi_app/main.py`)

Returns the forecast as JSON, with the date, forecast, lower 95% and upper 95% for each month. Other applications can use it without the dashboard.

### 3. Notebook (`price_forecast.ipynb`)

All 16 sections with the code, charts and explanations, from the data check to the conclusion.

---

## ✦ LIMITATIONS

- **No clear winner over the baseline.** No model clearly beat the naive baseline, so month-to-month changes are hard to predict from past prices alone.
- **Small test set.** The test period is only 12 months and includes a sharp dip that no model predicted.
- **Flat forecast, wide band.** The forecast says prices are likely to stay high but could move by about ±5,700 within a year, so it supports risk planning, not exact price calls.
- **No external factors.** Weather, demand and input costs are not used yet.
- **Overfitting risk.** Tuned XGBoost fits the training data much better than the test data.

---

## ✦ FINAL RECOMMENDATION

The forecast shows no clear direction but a wide range, so the company should **manage price risk instead of betting on one price**.

If prices rise (upper band around 21,000):

- Buy in phases instead of one large purchase
- Sign fixed or forward contracts for part of the volume
- Add a price-adjustment clause in customer contracts

If prices fall (lower band around 10,000):

- Avoid long fixed contracts at today's high price
- Keep inventory low and buy as needed
- Negotiate flexible or index-linked supplier pricing

In both cases, cover about half the expected demand with contracts, use the upper band as the worst-case budget, and re-run the forecast every month.

### Next Steps

1. **Add external factors** such as weather, demand and input costs, and test them as features.
2. **Retrain monthly** and alert if MAPE goes above 15%.
3. **Keep tuned XGBoost as the challenger** and replace ARIMA only if it does better on recent data.

---

<div align="center">

### Karthika S

📧 [rskarthika08@gmail.com](mailto:rskarthika08@gmail.com)

*Monthly Price Forecasting • 12-Month Price Forecast*

</div>
