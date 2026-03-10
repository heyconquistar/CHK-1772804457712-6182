import streamlit as st
import pandas as pd


st.set_page_config(page_title="Protein Tracker Webpage", layout="centered")

st.title("🥗 Protein Intake & Goal Consultant")
st.write("Calculate your physiological needs and track your daily consumption.")


st.sidebar.header("User Metrics")
height = st.sidebar.number_input("Height (cm)", value=170)
weight = st.sidebar.number_input("Weight (kg)", value=70)
activity_level = st.sidebar.selectbox("Activity Level", ["Sedentary", "Moderate", "Active"])


bmi = weight / ((height / 100) ** 2)
multiplier = 1.2 if activity_level == "Sedentary" else 1.6 if activity_level == "Moderate" else 2.0
suggested_protein = round(weight * multiplier, 1)

st.sidebar.info(f"**Suggested Target:** {suggested_protein}g/day")
st.sidebar.caption(f"Based on a BMI of {round(bmi, 1)}")


food_data = {
    "Food Item": ["Chicken Breast (100g)", "Eggs (2 Large)", "Sattu (100g)", "Milk (250ml)", "Paneer (100g)", "Whey Protein (1 Scoop)"],
    "Protein (g)": [25, 12, 20, 8, 18, 24]
}
df_food = pd.DataFrame(food_data)


st.subheader("Add Today's Intake")
selected_food = st.selectbox("Select Food Consumed", df_food["Food Item"])
quantity = st.number_input("Quantity (Portions)", min_value=1.0, step=0.5)

if 'total_protein' not in st.session_state:
    st.session_state.total_protein = 0.0

if st.button("Add to Daily Vector"):
    # Get protein value from Pandas dataframe
    protein_per_unit = df_food[df_food["Food Item"] == selected_food]["Protein (g)"].values[0]
    st.session_state.total_protein += (protein_per_unit * quantity)
    st.success(f"Added {protein_per_unit * quantity}g of protein!")


st.divider()
progress = min(st.session_state.total_protein / suggested_protein, 1.0)

col1, col2 = st.columns(2)
col1.metric("Total Intake", f"{st.session_state.total_protein}g")
col2.metric("Target", f"{suggested_protein}g", delta=round(st.session_state.total_protein - suggested_protein, 1))

st.progress(progress)

if st.session_state.total_protein >= suggested_protein:
    st.balloons()
    st.success("🎯 Daily Physiological Target Achieved!")
else:
    remaining = round(suggested_protein - st.session_state.total_protein, 1)
    st.warning(f"You need {remaining}g more to hit your target.")

if st.button("Reset Day"):
    st.session_state.total_protein = 0.0
    st.rerun()