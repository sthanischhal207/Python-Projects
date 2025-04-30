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

st.title("2-Variable Simplex Method Solver")
st.markdown("---")

# Input section
with st.form("input_form"):
    st.subheader("Enter Objective Function Coefficients \n **For Z = gx + hy**")

    col_obj1, col_obj2 = st.columns(2)
    with col_obj1:
        g = st.number_input("g (x in Z)", value=1.0)
    with col_obj2:
        h = st.number_input("h (y in Z)", value=1.0)

    objective = st.radio("Optimization Type:", ["Maximize", "Minimize"])

    st.markdown("---")
    st.subheader("Enter Constraints Coefficients")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Equation 1: ax + by = c**")
        a = st.number_input("a", value=1.0)
        b = st.number_input("b", value=1.0)
        c = st.number_input("RHS (c)", value=1.0)
    with col2:
        st.markdown("**Equation 2: dx + ey = f**")
        d = st.number_input("d", value=1.0)
        e = st.number_input("e", value=1.0)
        f = st.number_input("RHS (f)", value=1.0)

    submitted = st.form_submit_button("Solve")


# Logic after submitting
if submitted:
    # Convert to fractions for accuracy
    a, b, c = Fraction(a), Fraction(b), Fraction(c)
    d, e, f = Fraction(d), Fraction(e), Fraction(f)
    g, h = Fraction(g), Fraction(h)

    # Negate for maximization
    if objective == "Maximize":
        g, h = -g, -h

    # Initial simplex tableau
    tableau = [
        ["Basis", "x", "y", "s1", "s2", "Z", "RHS", "Ratio"],
        ["s1", a, b, 1, 0, 0, c, ""],
        ["s2", d, e, 0, 1, 0, f, ""],
        ["Z", g, h, 0, 0, 1, 0, ""]
    ]
    st.session_state.tables = [tableau]

    # --- SIMPLEX METHOD LOOP ---
    def calculate_ratios(table, pivot_col):
        for i in range(1, 3):
            try:
                rhs = table[i][6]
                val = table[i][pivot_col]
                table[i][7] = rhs / val if val > 0 else "-"
            except:
                table[i][7] = "-"

    def find_pivot_column(table):
        return min(range(1, 3), key=lambda i: table[3][i])

    def find_pivot_row(table, pivot_col):
        ratios = [(i, table[i][7]) for i in range(1, 3) if isinstance(table[i][7], Fraction)]
        return min(ratios, key=lambda x: x[1])[0] if ratios else None

    def pivot_operation(table, pivot_row, pivot_col):
        pivot_val = table[pivot_row][pivot_col]
        table[pivot_row][1:7] = [x / pivot_val for x in table[pivot_row][1:7]]
        for i in range(1, 4):
            if i != pivot_row:
                factor = table[i][pivot_col]
                table[i][1:7] = [
                    table[i][j] - factor * table[pivot_row][j] for j in range(1, 7)
                ]
        table[pivot_row][0] = table[0][pivot_col]

    while True:
        current = st.session_state.tables[-1]
        if all(val >= 0 for val in current[3][1:3]):
            break
        pivot_col = find_pivot_column(current)
        calculate_ratios(current, pivot_col)
        pivot_row = find_pivot_row(current, pivot_col)
        if pivot_row is None:
            st.error("Unbounded solution.")
            break
        new_table = [row[:] for row in current]
        pivot_operation(new_table, pivot_row, pivot_col)
        new_table[pivot_row][7] = ""
        for i in [1, 2]:
            if i != pivot_row:
                new_table[i][7] = ""
        st.session_state.tables.append(new_table)

    # --- FINAL OUTPUT ---
    final = st.session_state.tables[-1]
    variables = {"x": 0, "y": 0, "Z": 0}
    for row in final[1:4]:
        if row[0] in variables:
            variables[row[0]] = row[6]

    st.session_state.final_output = f"""
**Optimal Solution:**  
- x = {variables['x']}  
- y = {variables['y']}  
- Z = {variables['Z'] if objective == "Maximize" else -variables['Z']}  
**Type:** {objective}
"""


# Display all simplex tables
for idx, table in enumerate(st.session_state.tables):
    st.subheader(f"Simplex Table {idx}")
    st.code(tabulate(table, tablefmt="fancy_grid"))

# Final result
if st.session_state.final_output:
    st.markdown("---")
    st.markdown(st.session_state.final_output)