import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Price Forecast", layout="wide")
st.title("Monthly Price Forecast Dashboard")



@st.cache_resource
def load_model():
    return joblib.load("models/best_model.pkl")


model = load_model()

df = pd.read_csv("data/price_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")
price = df["avg_monthly_price"]


st.sidebar.header("Settings")
months = st.sidebar.slider("Months to forecast", 1, 24, 12)
years = st.sidebar.slider("Years of history to show", 1, 10, 5)


result = model.get_forecast(months)
forecast = result.predicted_mean
ci = result.conf_int()
lower = ci.iloc[:, 0]
upper = ci.iloc[:, 1]


table = pd.DataFrame({
    "Month": forecast.index.strftime("%Y-%m"),
    "Forecast": forecast.values.round(0),
    "Lower 95%": lower.values.round(0),
    "Upper 95%": upper.values.round(0),
})


tab1, tab2, tab3, tab4 = st.tabs(
    ["Forecast", "Model comparison", "Budget planner", "Monitoring check"]
)

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Last actual price", int(price.iloc[-1]))
    col2.metric("Forecast (average)", int(forecast.mean()))
    col3.metric("Lowest (95%)", int(lower.min()))
    col4.metric("Highest (95%)", int(upper.max()))

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(price.tail(years * 12), label="History")
    ax.plot(forecast.index, forecast, color="red", label="Forecast")
    ax.fill_between(forecast.index, lower, upper, color="red", alpha=0.2,
                    label="95% confidence interval")
    ax.legend()
    st.pyplot(fig)

    st.dataframe(table, hide_index=True)
    st.download_button("Download forecast as CSV", table.to_csv(index=False),
                       file_name="price_forecast.csv")

with tab2:
    st.write("Test results from the notebook (last 12 months). Lower MAPE is better.")
    comparison = pd.DataFrame({
        "Model": ["Naive (last value)", "ARIMA (0,1,0)", "XGBoost", "SARIMA",
                  "Seasonal Naive", "Prophet"],
        "Test MAPE (%)": [9.12, 9.12, 9.45, 13.75, 17.35, 30.81],
    })
    st.bar_chart(comparison.set_index("Model"))
    st.write("Selected model: **ARIMA (0,1,0)**. It ties for the lowest error and is the simplest.")

with tab3:
    st.write("Estimate the purchase cost over the forecast period.")
    quantity = st.number_input("Quantity bought per month", value=100, step=10)

    col1, col2, col3 = st.columns(3)
    col1.metric("Expected cost", int(forecast.sum() * quantity))
    col2.metric("Best case (lower band)", int(lower.sum() * quantity))
    col3.metric("Worst case (upper band)", int(upper.sum() * quantity))
    st.write("Use the worst case for budgeting and consider fixing part of the price with a contract.")


with tab4:
    first_month = forecast.index[0].strftime("%Y-%m")
    st.write("When the real price arrives, compare it with the forecast for " + first_month + ".")
    actual = st.number_input("Actual price", value=15000)

    forecast_value = forecast.iloc[0]
    error = abs(actual - forecast_value) / actual * 100
    st.write("Forecast: " + str(int(forecast_value)) + " | Error: " + str(round(error, 2)) + "%")

    if error > 15:
        st.error("ALERT: error above 15%. Retrain the model.")
    elif actual < lower.iloc[0] or actual > upper.iloc[0]:
        st.warning("WARNING: actual price is outside the 95% range. Review the model.")
    else:
        st.success("Model is OK.")