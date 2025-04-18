import streamlit as st

def main():
    # Title
    st.title("Gastrocarcinoma Treatment Decision Support (Demo)")

    # 1) Check if profile is complete; if not, go to profile page
    if "profile_complete" not in st.session_state:
        st.session_state.profile_complete = False

    if not st.session_state.profile_complete:
        profile_page()
        return  # Stop here until the user clicks "次へ"

    # 2) TREATMENT OPTIONS
    st.subheader("Select or Define Treatment Options")

    # Initialize or retrieve the list of treatment options
    if "treatment_options" not in st.session_state:
        # Example default options
        st.session_state.treatment_options = ["Surgery", "Chemotherapy A", "Chemotherapy B"]

    # Display existing options with Remove buttons
    st.write("**Current Treatment Options:**")
    for i, opt in enumerate(st.session_state.treatment_options):
        col1, col2 = st.columns([6,1])
        with col1:
            st.write(f"{i+1}. {opt}")
        with col2:
            if st.button("Remove", key=f"remove_option_{i}"):
                # SAFE removal via list comprehension
                st.session_state.treatment_options = [
                    item for idx, item in enumerate(st.session_state.treatment_options)
                    if idx != i
                ]
                # No st.experimental_rerun(): changes show on next interaction

    # Let user add a new option
    new_option = st.text_input("Add a new treatment option:")
    if st.button("Add Option"):
        if new_option.strip():
            st.session_state.treatment_options.append(new_option.strip())
            # No st.experimental_rerun()

    st.write("---")

    # 3) OUTCOMES
    st.subheader("Outcomes to Evaluate in OOVL")

    if "outcomes" not in st.session_state:
        st.session_state.outcomes = ["Prolonged survival", "Severe nausea", "Hospital stay length"]

    st.write("**Current Outcomes:**")
    for i, out in enumerate(st.session_state.outcomes):
        col1, col2 = st.columns([6,1])
        with col1:
            st.write(f"{i+1}. {out}")
        with col2:
            if st.button("Remove", key=f"remove_outcome_{i}"):
                st.session_state.outcomes = [
                    item for idx, item in enumerate(st.session_state.outcomes)
                    if idx != i
                ]

    new_outcome = st.text_input("Add a new outcome:")
    if st.button("Add Outcome"):
        if new_outcome.strip():
            st.session_state.outcomes.append(new_outcome.strip())

    st.write("---")

    # 4) OOVL DATA ENTRY
    if "oovl_data" not in st.session_state:
        st.session_state.oovl_data = {}

    # Ensure each option–outcome pair has "value" and "likelihood"
    for opt in st.session_state.treatment_options:
        if opt not in st.session_state.oovl_data:
            st.session_state.oovl_data[opt] = {}
        for out in st.session_state.outcomes:
            if out not in st.session_state.oovl_data[opt]:
                st.session_state.oovl_data[opt][out] = {
                    "value": 50,
                    "likelihood": 50
                }

    # Show sliders
    for opt in st.session_state.treatment_options:
        st.write(f"### OOVL Sliders for {opt}")
        for out in st.session_state.outcomes:
            col1, col2 = st.columns(2)
            with col1:
                val_label = f"{out} - Value (Importance) for {opt}"
                st.session_state.oovl_data[opt][out]["value"] = st.slider(
                    val_label, 0, 100,
                    st.session_state.oovl_data[opt][out]["value"],
                    key=f"slider_value_{opt}_{out}"
                )
            with col2:
                lik_label = f"{out} - Likelihood (Probability) for {opt}"
                st.session_state.oovl_data[opt][out]["likelihood"] = st.slider(
                    lik_label, 0, 100,
                    st.session_state.oovl_data[opt][out]["likelihood"],
                    key=f"slider_likelihood_{opt}_{out}"
                )

    st.write("---")

    # 5) CONSTRAINTS
    st.subheader("Constraints / Concerns (Free-Text)")

    if "constraints_list" not in st.session_state:
        st.session_state.constraints_list = []

    for i, c in enumerate(st.session_state.constraints_list):
        col1, col2 = st.columns([6,1])
        with col1:
            st.write(f"**{i+1}. {c['description']}**")
            c['importance'] = st.slider(
                f"Importance of constraint {i+1}:",
                0, 100, c['importance'],
                key=f"constraint_importance_{i}"
            )
        with col2:
            if st.button("Remove", key=f"remove_constraint_{i}"):
                st.session_state.constraints_list = [
                    item for idx, item in enumerate(st.session_state.constraints_list)
                    if idx != i
                ]

    new_constraint = st.text_input("Enter a new concern or constraint:")
    if st.button("Add Constraint"):
        if new_constraint.strip():
            st.session_state.constraints_list.append({
                "description": new_constraint.strip(),
                "importance": 50
            })

    st.write("---")

    # 6) CALCULATE / COMPARE
    if st.button("Compare Treatment Options"):
        compare_treatments()

def profile_page():
    """Profile page that collects prefecture and age instead of name."""
    st.title("ユーザープロファイル")

    # Example prefecture list
    prefectures = [
        "北海道", "青森県", "岩手県", "宮城県", "秋田県",
        "山形県", "福島県", "茨城県", "栃木県", "群馬県",
        "埼玉県", "千葉県", "東京都", "神奈川県",
        "新潟県", "富山県", "石川県", "福井県"
    ]

    selected_prefecture = st.selectbox("都道府県を選択してください:", prefectures)
    age = st.number_input("年齢を入力してください:", min_value=0, max_value=120, value=40)

    if st.button("次へ"):
        st.session_state.prefecture = selected_prefecture
        st.session_state.user_age = age
        st.session_state.profile_complete = True

def compare_treatments():
    """Naive example: sum (value * likelihood) for each option."""
    st.write("## Comparison Results:")

    oovl_data = st.session_state.oovl_data

    for opt, outcomes_dict in oovl_data.items():
        total_score = 0.0
        for out, vals in outcomes_dict.items():
            v = vals["value"] / 100.0
            l = vals["likelihood"] / 100.0
            total_score += (v * l)
        st.write(f"- **{opt}** raw OOVL score: {total_score:.2f}")

    # Sum constraints
    total_constraints = 0.0
    for c in st.session_state.constraints_list:
        total_constraints += c["importance"] / 100.0

    st.write(f"Aggregate Constraints score: {total_constraints:.2f}")
    st.info("You can incorporate constraints into final scoring, e.g., net = OOVL - constraints, etc.")

if __name__ == "__main__":
    main()
