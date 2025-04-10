import streamlit as st

def main():
    # 1) Title and Explanation
    st.title("Gastrocarcinoma Treatment Decision Support (Demo)")
    st.write("""
        This is a simplified demonstration of using an OOVL (Options, Outcomes, Value, Likelihood)
        approach for decision-making in gastrocarcinoma treatments.
    """)

    # 2) (Optional) User Profile
    # If you want the user to input their age/gender, or if you want to replicate the approach 
    # from your original app, you can do so here or in a separate function. 
    # For simplicity, let's just add a quick text input:
    if "profile_complete" not in st.session_state:
        st.session_state.profile_complete = False

    if not st.session_state.profile_complete:
        profile_page()
        return

    # 3) Gather possible treatment options
    st.subheader("Select or Define Treatment Options")
    # Maybe you define some defaults
    default_options = ["Surgery", "Chemotherapy A", "Chemotherapy B"]
    if "treatment_options" not in st.session_state:
        st.session_state.treatment_options = default_options.copy()

    # Let the user see current options
    st.write("**Current Treatment Options:**")
    for i, opt in enumerate(st.session_state.treatment_options):
        st.write(f"{i+1}. {opt}")

    # Let user add new option
    new_option = st.text_input("Add a new treatment option (leave blank if none).")
    if st.button("Add Option"):
        if new_option.strip():
            st.session_state.treatment_options.append(new_option.strip())

    st.write("---")

    # 4) OOVL for each option
    st.subheader("Rate Each Option by Outcomes, Value, and Likelihood")
    # Let user define outcomes or you can provide a standard list
    # For demonstration, let's let the user define them:

    if "outcomes" not in st.session_state:
        st.session_state.outcomes = ["Prolonged survival", "Severe nausea", "Hospital stay length"]

    # Show existing outcomes
    st.write("**Current Outcomes to Evaluate:**")
    for i, out in enumerate(st.session_state.outcomes):
        st.write(f"{i+1}. {out}")

    # Let user add a new outcome
    new_outcome = st.text_input("Add a new outcome to evaluate (leave blank if none).")
    if st.button("Add Outcome"):
        if new_outcome.strip():
            st.session_state.outcomes.append(new_outcome.strip())

    # Now, create a data structure for Value and Likelihood per option/outcome
    if "oovl_data" not in st.session_state:
        # Initialize as a nested dict:
        #   st.session_state.oovl_data[option][outcome] = {"value": ..., "likelihood": ...}
        st.session_state.oovl_data = {}

    # Ensure every option and outcome is represented in oovl_data
    for opt in st.session_state.treatment_options:
        if opt not in st.session_state.oovl_data:
            st.session_state.oovl_data[opt] = {}
        for out in st.session_state.outcomes:
            if out not in st.session_state.oovl_data[opt]:
                st.session_state.oovl_data[opt][out] = {
                    "value": 50,       # default midpoint
                    "likelihood": 50   # default midpoint
                }

    # Display sliders for each option-outcome pair
    for opt in st.session_state.treatment_options:
        st.write(f"### {opt}")
        for out in st.session_state.outcomes:
            col1, col2 = st.columns(2)
            with col1:
                val_label = f"{out} - Value (Importance) for {opt}"
                st.session_state.oovl_data[opt][out]["value"] = st.slider(
                    val_label, 0, 100, st.session_state.oovl_data[opt][out]["value"]
                )
            with col2:
                lik_label = f"{out} - Likelihood (Probability) for {opt}"
                st.session_state.oovl_data[opt][out]["likelihood"] = st.slider(
                    lik_label, 0, 100, st.session_state.oovl_data[opt][out]["likelihood"]
                )

    st.write("---")

    # 5) Free-text constraints (similar to OOVL but more open?)
    st.subheader("Constraints / Concerns (Free-Text)")
    if "constraints_list" not in st.session_state:
        st.session_state.constraints_list = []

    new_constraint = st.text_input("Enter a new concern or constraint:")
    if st.button("Add Constraint"):
        if new_constraint.strip():
            st.session_state.constraints_list.append({
                "description": new_constraint.strip(),
                "importance": 50  # default
            })

    # Display existing constraints
    for i, c in enumerate(st.session_state.constraints_list):
        st.write(f"Constraint {i+1}: **{c['description']}**")
        c['importance'] = st.slider(
            f"Importance of constraint {i+1}:", 0, 100, c['importance']
        )

    st.write("---")

    # 6) Perform a sample "net benefit" or "score" calculation
    if st.button("Compare Treatment Options"):
        compare_treatments()


def profile_page():
    """Very minimal profile page as an example."""
    st.title("User Profile for Gastrocarcinoma App")
    st.write("Enter your information:")
    name = st.text_input("Your Name:")
    age = st.number_input("Your Age:", min_value=0, max_value=120, value=40)
    if st.button("Next"):
        # Store
        st.session_state.user_name = name
        st.session_state.user_age = age
        st.session_state.profile_complete = True


def compare_treatments():
    """Computes a simple score for each treatment based on OOVL data."""
    oovl_data = st.session_state.oovl_data
    # We'll do a naive calculation:
    # "score" = sum( (value/100) * (likelihood/100) ) across all outcomes
    # Lower score could mean "less overall negative weight" if the outcome is negative.
    # But the user might also have some positive outcomes. 
    # In real usage, you'd clarify which outcomes are 'positive' or 'negative' 
    # or let user specify the direction. 
    # For demonstration, let's assume a bigger score means "more net effect" 
    # (but interpret carefully).

    st.write("## Comparison Results:")
    for opt, outcomes_dict in oovl_data.items():
        total_score = 0.0
        for out, vals in outcomes_dict.items():
            v = vals["value"] / 100.0
            l = vals["likelihood"] / 100.0
            total_score += (v * l)
        # Subtract constraints? Possibly. 
        # For simplicity, let's just show the raw total first:
        st.write(f"- **{opt}** score: {total_score:.2f}")

    # Optionally factor in constraints
    total_constraints = 0.0
    for c in st.session_state.constraints_list:
        importance_scaled = c["importance"] / 100.0
        total_constraints += importance_scaled
    st.write(f"Aggregate Constraints score = {total_constraints:.2f}")

    st.info("Interpretation step goes here: depending on how you define your scoring, a higher or lower score might be preferable. You’d also consider how constraints reduce or offset the benefit of each option.")


if __name__ == "__main__":
    main()
