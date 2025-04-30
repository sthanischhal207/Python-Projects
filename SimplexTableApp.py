import streamlit as st
from tabulate import tabulate
from fractions import Fraction

st.set_page_config(page_title="Simplex Solver", layout="centered")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
if "tables" not in st.session_state:
    st.session_state.tables = []
if "final_output" not in st.session_state:
    st.session_state.final_output = ""
if "objective_type" not in st.session_state:
    st.session_state.objective_type = "Maximize"

st.title("2-Variable Simplex Method Solver")
st.markdown("---")

# Input form
with st.form("input_form"):
    st.subheader("Enter Objective Function Coefficients (Z = gx + hy)")
    col1, col2 = st.columns(2)
    with col1:
        g = st.number_input("g (coefficient of x)", value=1.0)
    with col2:
        h = st.number_input("h (coefficient of y)", value=1.0)

    objective = st.radio("Optimization Type", ["Maximize", "Minimize"])

    st.subheader("Enter Constraint Coefficients")
    st.markdown("### Constraint 1: ax + by ≤ c")
    a = st.number_input("a", value=1.0, key="a")
    b = st.number_input("b", value=1.0, key="b")
    c_val = st.number_input("c", value=1.0, key="c")

    st.markdown("### Constraint 2: dx + ey ≤ f")
    d = st.number_input("d", value=1.0, key="d")
    e = st.number_input("e", value=1.0, key="e")
    f_val = st.number_input("f", value=1.0, key="f")

    submitted = st.form_submit_button("Solve")

# When the form is submitted
if submitted:
    # Store for later
    st.session_state.objective_type = objective

    # Convert all to Fraction for exact math
    a, b, c_val = Fraction(a), Fraction(b), Fraction(c_val)
    d, e, f_val = Fraction(d), Fraction(e), Fraction(f_val)
    g, h = Fraction(g), Fraction(h)

    # Negate coefficients for maximization
    if objective == "Maximize":
        g *= -1
        h *= -1

    # Initialize the tableau
    tableau = [
        ["Basis", "x", "y", "s1", "s2", "Z", "RHS", "Ratio"],
        ["s1", a, b, 1, 0, 0, c_val, ""],
        ["s2", d, e, 0, 1, 0, f_val, ""],
        ["Z", g, h, 0, 0, 1, 0, ""]
    ]
    st.session_state.tables = [tableau]

    def calculate_ratios(tbl, pivot_col):
        for i in [1, 2]:
            try:
                val = tbl[i][pivot_col]
                if val > 0:
                    tbl[i][7] = Fraction(tbl[i][6] / val).limit_denominator(10)
                else:
                    tbl[i][7] = "-"
            except:
                tbl[i][7] = "-"

    def find_pivot_column(tbl):
        return min(range(1, 3), key=lambda i: tbl[3][i])

    def find_pivot_row(tbl, pivot_col):
        valid = [(i, tbl[i][7]) for i in [1, 2] if isinstance(tbl[i][7], Fraction)]
        return min(valid, key=lambda x: x[1])[0] if valid else None

    def pivot_operation(tbl, pivot_row, pivot_col):
        pivot_val = tbl[pivot_row][pivot_col]
        tbl[pivot_row][1:7] = [Fraction(x / pivot_val).limit_denominator(10) for x in tbl[pivot_row][1:7]]

        for i in [1, 2, 3]:
            if i != pivot_row:
                factor = tbl[i][pivot_col]
                tbl[i][1:7] = [
                    Fraction(tbl[i][j] - factor * tbl[pivot_row][j]).limit_denominator(10)
                    for j in range(1, 7)
                ]
        tbl[pivot_row][0] = tbl[0][pivot_col]

    # SIMPLEX LOOP
    while True:
        current = st.session_state.tables[-1]

        if all(current[3][i] >= 0 for i in range(1, 3)):
            break

        pivot_col = find_pivot_column(current)
        calculate_ratios(current, pivot_col)
        pivot_row = find_pivot_row(current, pivot_col)

        if pivot_row is None:
            st.error("Unbounded solution. No valid pivot row found.")
            break

        # Narrate pivot info
        st.markdown(f"""
        **Pivot Operation**
        - Pivot Column: `{current[0][pivot_col]}`
        - Pivot Row: `{pivot_row}`
        - Pivot Element: `{current[pivot_row][pivot_col]}`
        """)

        # Clone the table and perform pivot
        new_table = [row[:] for row in current]
        pivot_operation(new_table, pivot_row, pivot_col)

        new_table[pivot_row][7] = ""
        for i in [1, 2]:
            if i != pivot_row:
                new_table[i][7] = ""

        st.session_state.tables.append(new_table)

    # Final output
    final = st.session_state.tables[-1]
    variables = {"x": 0, "y": 0, "Z": 0}

    for row in final[1:4]:
        var = row[0]
        if var in variables:
            variables[var] = row[6]

    result_Z = variables["Z"]
    if objective == "Minimize":
        result_Z *= -1

    st.session_state.final_output = f"""
    ### __Final Optimal Solution__
    - x = `{variables['x']}`
    - y = `{variables['y']}`
    - Z {objective} = `{result_Z}`
    """

# Display tables
for idx, table in enumerate(st.session_state.tables):
    st.markdown(f"### Simplex Table {idx}")
    st.code(tabulate(table, tablefmt="fancy_grid"))

# Final result
if st.session_state.final_output:
    st.markdown("---")
    st.markdown(st.session_state.final_output)