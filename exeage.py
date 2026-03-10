import streamlit as st
import pandas as pd
import altair as alt  # MAJOR NEW COMPONENT

# --- PAGE SETUP ---
st.set_page_config(page_title="Protein Tracker Webpage", layout="wide")  # Use wide for layout matching

# --- CUSTOM CSS FOR DESIGN MATCHING ---
st.markdown("""
<style>
/* Overall card styling for a sleek look */
.card-container {
    background-color: white;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    margin-bottom: 25px;
}

/* User metrics suggested target info box */
.metrics-target-box {
    background-color: #e0f2fe; /* Light blue */
    border-radius: 8px;
    padding: 15px;
    margin-top: 20px;
}
.metrics-target-box p {
    margin: 0; /* Remove default padding for compact look */
}
.target-label {
    font-size: 1.1em;
    font-weight: bold;
    color: #333;
}
.target-value {
    font-size: 2.2em;
    font-weight: bold;
    color: #0c4a6e; /* Darker blue */
}
.target-subtext {
    font-size: 0.9em;
    color: #555;
    margin-top: 5px !important;
}

/* Progress bar color (image uses green) */
.stProgress > div > div > div > div {
    background-color: #6fb271; /* Green color for progress bar */
}

/* Progress metric styling to match image columns */
.progress-metrics p {
    margin: 0;
}
.metric-label-progress {
    font-size: 1em;
    color: #666;
}
.metric-value-progress {
    font-size: 2.5em;
    font-weight: bold;
}
.progress-bold-value {
    font-size: 1.2em;
    font-weight: bold;
    margin-top: 5px !important;
}

/* Full width Reset button styling */
.full-width-reset button {
    background-color: #f1f5f9; /* very light gray */
    color: #334155;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("<h1 style='text-align: center; color: black; font-weight: bold;'>💪 Smart Protein Intake Tracker</h1>",
            unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: gray;'>Track your daily protein intake based on your body metrics and exercise.</p>",
    unsafe_allow_html=True)
# High-quality hero image placeholder of healthy protein foods
st.image("https://images.unsplash.com/photo-1599058917212-d750089bc07e?q=80&w=2669&auto=format&fit=crop",
         use_container_width=True)

# --- MAIN LAYOUT ---
# Adjust columns to match narrow metrics column and wide data column from image.
col1, col2 = st.columns([1, 2.5])

# --- LOGIC INITIALIZATION ---
if "total_protein" not in st.session_state:
    st.session_state.total_protein = 0.0

if "extra_protein" not in st.session_state:
    st.session_state.extra_protein = 0.0

# --- USER METRICS SECTION (Col 1 - as a custom styled card) ---
with col1:
    with st.container():
        st.markdown("<div class='card-container'>", unsafe_allow_html=True)  # wrap in card style
        st.header("User Metrics")
        age = st.number_input("Age", min_value=10, max_value=100, value=20)
        height = st.number_input("Height (cm)", value=170)
        weight = st.number_input("Weight (kg)", value=70)

        activity_level = st.selectbox(
            "Activity Level",
            ["Sedentary", "Moderate", "Active"]
        )

        # BMI Calculation
        bmi = weight / ((height / 100) ** 2)

        # Protein multiplier based on activity
        multiplier = 1.2 if activity_level == "Sedentary" else 1.6 if activity_level == "Moderate" else 2.0

        # Base protein requirement
        base_protein = weight * multiplier

        # Suggested Target Info Box (custom styled)
        suggested_protein = round(base_protein + st.session_state.extra_protein, 1)
        st.markdown(f"""
        <div class='metrics-target-box'>
            <p class='target-label'>Suggested Target:</p>
            <p class='target-value'>{suggested_protein}g/day</p>
            <p class='target-subtext'>BMI: {round(bmi, 1)} | Age: {age}</p>
        </div>
        """, unsafe_allow_html=True)

        # "Divider" button (odd icon/label from image, adding as a button at bottom of metrics card)
        if st.button("⟳ Divider", key="divider_button_col1"):
            pass  # Placeholder for any action
        st.markdown("</div>", unsafe_allow_html=True)  # close card div

# --- MAIN PAGE SECTION (Col 2) ---
with col2:
    # Food & Exercise (Two side-by-side card-like columns)
    sub_col1, sub_col2 = st.columns(2)

    # ---------------- FOOD DATA ---------------- #
    food_data = {
        "Food Item": [
            "Chicken Breast (100g)",
            "Eggs (2 Large)",
            "Sattu (100g)",
            "Milk (250ml)",
            "Paneer (100g)",
            "Whey Protein (1 Scoop)"
        ],
        "Protein (g)": [25, 12, 20, 8, 18, 24]
    }
    df_food = pd.DataFrame(food_data)

    with sub_col1:
        with st.container():
            st.markdown("<div class='card-container'>", unsafe_allow_html=True)
            st.header("🍕 Food Intake")
            selected_food = st.selectbox("Select Food Consumed", df_food["Food Item"], key="food_selectbox_col2")
            quantity = st.number_input("Quantity (Portions)", min_value=1.0, step=0.5, key="food_quantity_col2")
            if st.button("Add Food", key="add_food_button_col2"):
                protein_per_unit = df_food[df_food["Food Item"] == selected_food]["Protein (g)"].values[0]
                added = protein_per_unit * quantity
                st.session_state.total_protein += added
                st.success(f"Added {added}g of protein!")
            st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- EXERCISE DATA ---------------- #
    exercise_data = {
        "Exercise": [
            "Walking (30 min)",
            "Running (30 min)",
            "Cycling (30 min)",
            "Gym Workout",
            "Yoga"
        ],
        "Extra Protein Needed (g)": [5, 10, 8, 15, 4]
    }
    df_exercise = pd.DataFrame(exercise_data)

    with sub_col2:
        with st.container():
            st.markdown("<div class='card-container'>", unsafe_allow_html=True)
            st.header("🏃 Exercise")
            selected_exercise = st.selectbox("Select Exercise", df_exercise["Exercise"], key="exercise_selectbox_col2")
            exercise_count = st.number_input("Times Performed", min_value=1, step=1, key="exercise_count_col2")
            if st.button("Add Exercise", key="add_exercise_button_col2"):
                extra = df_exercise[df_exercise["Exercise"] == selected_exercise]["Extra Protein Needed (g)"].values[0]
                added_extra = extra * exercise_count
                st.session_state.extra_protein += added_extra
                st.success(f"Exercise added! Protein requirement increased by {added_extra}g")
            st.markdown("</div>", unsafe_allow_html=True)

    # Protein Progress Card (Full width in Col 2)
    # recalculate suggested protein after potential updates
    suggested_protein = round(base_protein + st.session_state.extra_protein, 1)

    with st.container():
        st.markdown("<div class='card-container'>", unsafe_allow_html=True)
        st.header("🏃 Protein Progress")

        # Metrics in specific columns for layout matching
        met_col1, met_col2 = st.columns(2)

        # Protein Consumed with Tick and bold value below
        met_col1.markdown(
            f"<div class='progress-metrics'><p class='metric-label-progress'>Protein Consumed</p><p class='metric-value-progress'>{st.session_state.total_protein}g <span style='color: green; font-size: 0.8em; font-weight: normal;'>✓</span></p></div>",
            unsafe_allow_html=True)
        # bold value below
        met_col1.markdown(f"<p class='progress-bold-value'>{st.session_state.total_protein}g</p>",
                          unsafe_allow_html=True)

        # Target Protein and Delta below
        met_col2.markdown(
            f"<div class='progress-metrics'><p class='metric-label-progress'>Target Protein</p><p class='metric-value-progress'>{suggested_protein}g</p></div>",
            unsafe_allow_html=True)
        # delta value below (styled red/green)
        delta_val = round(st.session_state.total_protein - suggested_protein, 1)
        if delta_val >= 0:
            met_col2.markdown(f"<p class='progress-bold-value' style='color: green;'>+{delta_val}</p>",
                              unsafe_allow_html=True)
        else:
            met_col2.markdown(f"<p class='progress-bold-value' style='color: red;'>{delta_val}</p>",
                              unsafe_allow_html=True)

        # Progress bar (styled green)
        progress = min(st.session_state.total_protein / suggested_protein, 1.0)
        st.progress(progress)

        # Warning/Info Box
        remaining = round(suggested_protein - st.session_state.total_protein, 1)
        if remaining > 0:
            st.warning(f"⚠️ You need {remaining}g more protein today.")
        else:
            st.success("🎯 Daily Physiological Target Achieved!")

        st.markdown("</div>", unsafe_allow_html=True)

    # Protein Intake Visualization Card (Full width in Col 2)
    with st.container():
        st.markdown("<div class='card-container'>", unsafe_allow_html=True)
        st.header("📊 Protein Intake Visualization")

        # Chart Data
        chart_data = pd.DataFrame({
            'Category': ['Protein Consumed', 'Protein Target'],
            'Protein (g)': [st.session_state.total_protein, suggested_protein]
        })

        # Create Altair chart to perfectly match image colors and layout
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Category', sort=['Protein Consumed', 'Protein Target']),  # custom sorting
            y='Protein (g)',
            color=alt.condition(
                alt.datum.Category == 'Protein Consumed',
                alt.value('#6fb271'),  # green for consumed
                alt.value('#3c8dbc')  # blue for target (Streamlit default blue-ish)
            ),
            tooltip=['Category', 'Protein (g)']  # add interactive tooltips
        ).properties(
            title='',  # titles are already on the card container
            height=300  # set chart height
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        )

        st.altair_chart(chart, use_container_width=True)  # use full container width
        st.markdown("</div>", unsafe_allow_html=True)

    # Full Width Reset Button at the bottom (outside cards but still in col2)
    st.markdown("<div class='full-width-reset'>", unsafe_allow_html=True)
    if st.button("Reset Day", key="final_reset_button_bottom"):
        st.session_state.total_protein = 0.0
        st.session_state.extra_protein = 0.0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)