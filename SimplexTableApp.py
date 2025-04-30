import streamlit as st 
from fractions import Fraction 
from tabulate import tabulate

st.set_page_config(page_title="Simplex Solver", layout="centered")

st.title("2-Variable Simplex Method Solver") st.markdown("---")

User Inputs

with st.form("input_form"): st.subheader("Objective Function: Z = gx + hy") col1, col2 = st.columns(2) with col1: g = st.number_input("g (coefficient of x)", value=1.0) with col2: h = st.number_input("h (coefficient of y)", value=1.0)

objective = st.radio("Optimization Type:", ["Maximize", "Minimize"])

st.subheader("Constraints")
st.markdown("Each constraint is of the form: ax + by <= c")
col3, col4, col5 = st.columns(3)
with col3:
    a = st.number_input("a", value=1.0)
    d = st.number_input("d", value=1.0)
with col4:
    b = st.number_input("b", value=1.0)
    e = st.number_input("e", value=1.0)
with col5:
    c = st.number_input("RHS 1 (c)", value=1.0)
    f = st.number_input("RHS 2 (f)", value=1.0)

submit = st.form_submit_button("Solve")

if submit: # Convert to Fractions a, b, c = Fraction(a), Fraction(b), Fraction(c) d, e, f = Fraction(d), Fraction(e), Fraction(f) g, h = Fraction(g), Fraction(h)

if objective == "Maximize":
    g, h = -g, -h

# Initial Tableau
table = [
    ["Basis", "x", "y", "s1", "s2", "Z", "RHS", "Ratio"],
    ["s1", a, b, 1, 0, 0, c, ""],
    ["s2", d, e, 0, 1, 0, f, ""],
    ["Z", g, h, 0, 0, 1, 0, ""]
]

history = [table]
iteration = 0
final_answer = ""

def calculate_ratios(tab, col):
    for i in range(1, 3):
        val = tab[i][col]
        rhs = tab[i][6]
        tab[i][7] = rhs / val if val > 0 else "-"

def print_table(t):
    return tabulate(t, tablefmt="fancy_grid")

def find_pivot_column(t):
    z_row = t[3][1:6]
    min_val = min(z_row)
    if min_val >= 0:
        return -1
    return z_row.index(min_val) + 1

def find_pivot_row(t, pivot_col):
    options = [(i, t[i][6] / t[i][pivot_col]) for i in range(1, 3) if t[i][pivot_col] > 0]
    return min(options, key=lambda x: x[1])[0] if options else None

def pivot(t, pivot_row, pivot_col):
    pivot_element = t[pivot_row][pivot_col]
    st.markdown(f"**Pivot Element:** Row {pivot_row}, Col {pivot_col} = {pivot_element} ")
    t[pivot_row][1:7] = [x / pivot_element for x in t[pivot_row][1:7]]
    for i in range(1, 4):
        if i != pivot_row:
            factor = t[i][pivot_col]
            t[i][1:7] = [t[i][j] - factor * t[pivot_row][j] for j in range(1, 7)]
    t[pivot_row][0] = t[0][pivot_col]

st.markdown("### Initial Simplex Table")
st.code(print_table(table))

while True:
    iteration += 1
    st.markdown(f"---\n### Iteration {iteration}")

    pivot_col = find_pivot_column(table)
    if pivot_col == -1:
        st.success("**All Z-row entries are non-negative. Optimal solution reached.**")
        break

    st.markdown(f"- Not optimal. Most negative value in Z-row is in column {pivot_col} ({table[3][pivot_col]})")
    calculate_ratios(table, pivot_col)

    pivot_row = find_pivot_row(table, pivot_col)
    if pivot_row is None:
        st.error("Unbounded solution. Cannot proceed.")
        break

    st.markdown(f"- Pivot column: {pivot_col} ({table[0][pivot_col]})")
    st.markdown(f"- Pivot row: {pivot_row} (min ratio)")

    # Deep copy
    new_table = [row[:] for row in table]
    pivot(new_table, pivot_row, pivot_col)

    for i in range(1, 3):
        new_table[i][7] = ""

    table = new_table
    history.append(table)
    st.code(print_table(table))

# Extract answer
values = {"x": 0, "y": 0, "s1": 0, "s2": 0, "Z": 0}
for i in range(1, 4):
    var = table[i][0]
    if var in values:
        values[var] = table[i][6]
z_val = values["Z"] if objective == "Maximize" else -values["Z"]

st.markdown("---")
st.markdown(f"### __FINAL ANSWER__")
st.markdown(f"Z {'Max' if objective == 'Maximize' else 'Min'} = **{z_val}** at (x = {values['x']}, y = {values['y']})")
st.success("-------- IT IS AN OPTIMAL SOLUTION --------")

