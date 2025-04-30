import streamlit as st
from fractions import Fraction
from tabulate import tabulate

st.set_page_config(page_title="Simplex Solver", layout="centered")

# Session State
if "tables" not in st.session_state:
    st.session_state.tables = []
if "final_output" not in st.session_state:
    st.session_state.final_output = ""

st.title("2-Variable Simplex Method Solver")
st.markdown("---")

# Input Section
with st.form("input_form"):
    st.subheader("Objective Function: Z = gx + hy")

    col1, col2 = st.columns(2)
    g = col1.number_input("g (Coefficient of x)", value=1.0)
    h = col2.number_input("h (Coefficient of y)", value=1.0)

    objective = st.radio("Optimization Type:", ["Maximize", "Minimize"])

    st.markdown("---")
    st.subheader("Constraints (ax + by ≤ c, etc.)")

    st.markdown("**Constraint 1: ax + by ≤ c**")
    a = st.number_input("a", value=1.0)
    b = st.number_input("b", value=1.0)
    c_val = st.number_input("c", value=1.0)

    st.markdown("**Constraint 2: dx + ey ≤ f**")
    d = st.number_input("d", value=1.0)
    e = st.number_input("e", value=1.0)
    f_val = st.number_input("f", value=1.0)

    submitted = st.form_submit_button("Solve")

if submitted:
    # Convert to Fraction
    a, b, c_val = Fraction(a), Fraction(b), Fraction(c_val)
    d, e, f_val = Fraction(d), Fraction(e), Fraction(f_val)
    g, h = Fraction(g), Fraction(h)

    # Negate Z-row for maximization
    if objective == "Maximize":
        g, h = -g, -h

    # Initial Tableau
    tableau = [
        ["Basis", "x", "y", "s1", "s2", "Z", "RHS", "Ratio"],
        ["s1", a, b, 1, 0, 0, c_val, ""],
        ["s2", d, e, 0, 1, 0, f_val, ""],
        ["Z", g, h, 0, 0, 1, 0, ""]
    ]
    st.session_state.tables = [tableau]

    # Functions
    def calculate_ratios(table, pivot_col):
        for i in range(1, 3):
            try:
                val = table[i][pivot_col]
                rhs = table[i][6]
                table[i][7] = rhs / val if val > 0 else "-"
            except:
                table[i][7] = "-"

    def find_pivot_column(table, is_max):
        # Minimization => most negative value, Maximization => same
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

    # Simplex Loop
    while True:
        current = st.session_state.tables[-1]
        if all(val >= 0 for val in current[3][1:3]):
            break
        pivot_col = find_pivot_column(current, objective == "Maximize")
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

    # Final Result
    final = st.session_state.tables[-1]
    vars = {"x": 0, "y": 0, "Z": 0}
    for row in final[1:4]:
        if row[0] in vars:
            vars[row[0]] = row[6]

    Z_val = vars['Z'] if objective == "Maximize" else -vars['Z']
    st.session_state.final_output = f"""
**Optimal Solution:**  
- x = {vars['x']}  
- y = {vars['y']}  
- Z = {Z_val}  
**Type:** {objective}
"""

# Show Tables
for i, t in enumerate(st.session_state.tables):
    st.subheader(f"Simplex Table {i}")
    st.code(tabulate(t, tablefmt="fancy_grid"))

# Final Output
if st.session_state.final_output:
    st.markdown("---")
    st.markdown(st.session_state.final_output)