import streamlit as st
import numpy as np
import pandas as pd
from backend import run_workforce_planning  # Import your full scheduling logic here

st.set_page_config(page_title="AI Workforce Scheduler", layout="wide")

st.title("🧠 AI-Powered Workforce Scheduling System")

# Sidebar Inputs
with st.sidebar:
    st.header("📊 Configuration")
    num_employees = st.slider("Number of Employees", min_value=5, max_value=50, value=15)
    num_days = st.slider("Number of Days", min_value=1, max_value=14, value=7)
    num_shifts = st.selectbox("Shifts per Day", options=[1, 2, 3], index=2)
    run_button = st.button("Run Scheduler")

# Run backend and show results
if run_button:
    with st.spinner("Running AI model and scheduling logic..."):
        schedule, demand = run_workforce_planning(
            num_employees=num_employees,
            num_days=num_days,
            num_shifts_per_day=num_shifts
        )

    st.success("✅ Schedule generated successfully!")

    st.subheader("📅 Demand Forecast")
    demand_df = pd.DataFrame(demand, columns=[f"Shift {i+1}" for i in range(num_shifts)])
    demand_df.index = [f"Day {i+1}" for i in range(num_days)]
    st.dataframe(demand_df)

    st.subheader("🧾 Employee Schedule")
    shift_names = ['Morning', 'Afternoon', 'Night'][:num_shifts]
    schedule_df = pd.DataFrame(columns=['Employee', 'Day', 'Shift'])

    for e in range(num_employees):
        for d in range(num_days):
            for s in range(num_shifts):
                if schedule[e, d, s] == 1:
                    schedule_df = pd.concat([schedule_df, pd.DataFrame([{
                        "Employee": f"Employee {e+1}",
                        "Day": f"Day {d+1}",
                        "Shift": shift_names[s]
                    }])], ignore_index=True)

    st.dataframe(schedule_df)

    st.download_button("⬇️ Download Schedule as CSV", data=schedule_df.to_csv(index=False),
                       file_name="employee_schedule.csv", mime="text/csv")

else:
    st.info("Set configuration and click **Run Scheduler** to start.")
