import streamlit as st

def main():
    """
    Main function to create the Streamlit frontend page.
    """
    st.set_page_config(page_title="Data Entry Form", layout="centered")
    st.title("Insurance Premium Prediction Data Entry 📝")
    st.markdown("---")

    # --- Input Fields ---

    st.header("Personal and Health Information")

    # 1. Age (Numerical Input)
    # Range is generally 18 to 100 for insurance/health data
    age = st.slider(
        "**Age** (Years)",
        min_value=18,
        max_value=100,
        value=30,
        step=1,
        help="The primary beneficiary's age."
    )

    # 2. BMI (Numerical Input)
    # Typical BMI range is 10 to 60
    bmi = st.number_input(
        "**BMI** (Body Mass Index - $kg/m^2$)",
        min_value=10.0,
        max_value=60.0,
        value=25.0,
        step=0.1,
        format="%.1f",
        help="Body Mass Index, providing an idea of body weight relative to height."
    )

    # 3. Children (Integer Input)
    # Number of children/dependents covered by the insurance
    children = st.select_slider(
        "**Children** (Number of Dependents)",
        options=list(range(0, 6)), # 0 to 5 children
        value=0,
        help="Number of children/dependents covered by the insurance."
    )

    # 4. Sex_male (Categorical/Binary Input)
    # The original feature 'sex' is likely encoded. 'sex_male' suggests 1 for male, 0 for female.
    st.subheader("Demographics and Lifestyle")
    sex = st.radio(
        "**Gender**",
        options=["Female", "Male"],
        index=0, # Default to Female (encoded as 0)
        horizontal=True,
        help="Select the primary beneficiary's gender."
    )
    # Convert 'sex' label to the required 'sex_male' (1 or 0) value
    sex_male = 1 if sex == "Male" else 0

    # 5. Smoker_yes (Categorical/Binary Input)
    # The original feature 'smoker' is likely encoded. 'smoker_yes' suggests 1 for yes, 0 for no.
    smoker = st.radio(
        "**Smoker**",
        options=["No", "Yes"],
        index=0, # Default to No (encoded as 0)
        horizontal=True,
        help="Do you smoke? (Used for 'smoker_yes' feature)"
    )
    # Convert 'smoker' label to the required 'smoker_yes' (1 or 0) value
    smoker_yes = 1 if smoker == "Yes" else 0

    # 6. Region (Categorical Input)
    # Assuming standard regions for insurance data
    region = st.selectbox(
        "**Region**",
        options=["southeast", "southwest", "northeast", "northwest"],
        index=0,
        help="The residential area of the beneficiary."
    )

    st.markdown("---")

    # --- Display Submitted Values (Optional: for verification/debugging) ---

    st.header("Review & Submit")
    if st.button("Submit Data"):
        st.success("Data Submitted Successfully! ✅")

        # Create a dictionary of the final values for processing
        data = {
            "age": age,
            "bmi": bmi,
            "children": children,
            "sex_male": sex_male,
            "smoker_yes": smoker_yes,
            "region": region
        }

        # Display the collected data in a table
        st.write("### Input Values:")
        st.json(data)

        # Example of how you would display the final encoded features:
        st.write(f"**Encoded Feature Values:**")
        st.markdown(f"- `age`: **{age}**")
        st.markdown(f"- `bmi`: **{bmi}**")
        st.markdown(f"- `children`: **{children}**")
        st.markdown(f"- `sex_male` (Male=1): **{sex_male}**")
        st.markdown(f"- `smoker_yes` (Yes=1): **{smoker_yes}**")
        st.markdown(f"- `region`: **{region}**")
        # In a real model, 'region' would also be one-hot encoded (e.g., region_southeast, region_southwest, etc.)

if __name__ == "__main__":
    main()