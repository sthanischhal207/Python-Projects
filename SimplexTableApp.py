import streamlit as st 
from tabulate import tabulate 
from fractions import Fraction

Configure page

st.set_page_config(page_title="Simplex Solver", layout="centered")

Initialize session state

if "tables" not in st.session_state: st.session_state.tables = [] if "logs" not in st.session_state: st.session_state.logs = [] if "final_vars" not in st.session_state: st.session_state.final_vars = {}

Title

st.title("🧮 2-Variable Simplex Method Solver") st.markdown("---")

Input form

with st.form("input_form"): st.subheader("Enter Objective Function Coefficients") g = st.number_input("g (coeff of x in Z)", value=1.0) h = st.number_input("h (coeff of y in Z)", value=1.0) objective = st.radio("Optimization Type:", ["Maximize", "Minimize"])

st.markdown("---")
st.subheader("Enter Constraint Coefficients")
a = st.number_input("a (coeff of x in eq1)", value=1.0)
b = st.number_input("b (coeff of y in eq1)", value=1.0)
c = st.number_input("c (RHS of eq1)", value=1.0)
d = st.number_input("d (coeff of x in eq2)", value=1.0)
e = st.number_input("e (coeff of y in eq2)", value=1.0)
f = st.number_input("f (RHS of eq2)", value=1.0)

submitted = st.form_submit_button("Solve")

Helper functions

def to_fraction_matrix(a, b, c, d, e, f, g, h, objective): # Convert inputs to Fraction A, B, C = Fraction(a), Fraction(b), Fraction(c) D, E, F = Fraction(d), Fraction(e), Fraction(f) G, H = Fraction(g), Fraction(h) # Negate for maximization if objective == "Maximize": G, H = -G, -H

# Build initial tableau
return [
    ["Basis", "x", "y", "s1", "s2", "Z", "RHS", "Ratio"],
    ["s1", A,   B,    1,    0,    0,   C,     ""],
    ["s2", D,   E,    0,    1,    0,   F,     ""],
    ["Z",  G,   H,    0,    0,    1,   0,     ""],
]

def calculate_ratios(table, pivot_col): logs = [] for i in [1, 2]: coeff = table[i][pivot_col] if coeff > 0: table[i][7] = table[i][6] / coeff logs.append( f"Row {i}: ratio = {table[i][6]} / {coeff} = {table[i][7]}" ) else: table[i][7] = None logs.append( f"Row {i}: pivot column value <= 0, ratio skipped." ) return logs

def find_pivot_column(table): # Most negative entry in Z-row among x and y return min(range(1, 3), key=lambda j: table[3][j])

def find_pivot_row(table, pivot_col): candidates = [(i, table[i][7]) for i in [1, 2] if table[i][7] is not None] if not candidates: return None return min(candidates, key=lambda x: x[1])[0]

def pivot_operation(table, pivot_row, pivot_col): logs = [] # Normalize pivot row pivot_val = table[pivot_row][pivot_col] logs.append(f"Normalizing pivot at (Row {pivot_row}, Col {pivot_col}) = {pivot_val}") table[pivot_row][1:7] = [val / pivot_val for val in table[pivot_row][1:7]] logs.append(f"Row {pivot_row} after normalization: {table[pivot_row][1:7]}")

# Eliminate other rows
for r in [1, 2, 3]:
    if r != pivot_row:
        factor = table[r][pivot_col]
        logs.append(f"Eliminating row {r}, factor = {factor}")
        new_vals = []
        for j in range(1, 7):
            new_vals.append(
                table[r][j] - factor * table[pivot_row][j]
            )
        table[r][1:7] = new_vals
        logs.append(f"Row {r} after elimination: {new_vals}")

# Update basis label
table[pivot_row][0] = table[0][pivot_col]
return logs

def is_optimal(table): return all(val >= 0 for val in table[3][1:3])

def extract_solution(table, objective): sol = {"x": 0, "y": 0} for row in table[1:3]: var = row[0] if var in sol: sol[var] = row[6] Z_val = table[3][6] if objective == "Minimize": Z_val = -Z_val sol['Z'] = Z_val return sol

Main execution

if submitted: # Reset state st.session_state.tables = [] st.session_state.logs = [] st.session_state.final_vars = {}

# Create initial tableau
table = to_fraction_matrix(a, b, c, d, e, f, g, h, objective)
st.session_state.tables.append([row[:] for row in table])
st.session_state.logs.append("**Initial Tableau**")

# Iterations
iteration = 0
while not is_optimal(table):
    iteration += 1
    st.session_state.logs.append(f"--- Iteration {iteration} ---")

    pivot_col = find_pivot_column(table)
    st.session_state.logs.append(
        f"Pivot column: {pivot_col} ({table[0][pivot_col]})"
    )

    ratio_logs = calculate_ratios(table, pivot_col)
    st.session_state.logs.extend(ratio_logs)

    pivot_row = find_pivot_row(table, pivot_col)
    if pivot_row is None:
        st.session_state.logs.append(
            "Solution unbounded: no valid pivot row found."
        )
        break
    st.session_state.logs.append(f"Pivot row: {pivot_row}")

    op_logs = pivot_operation(table, pivot_row, pivot_col)
    st.session_state.logs.extend(op_logs)
    st.session_state.tables.append([row[:] for row in table])

# Final solution
sol = extract_solution(table, objective)
st.session_state.final_vars = sol
st.session_state.logs.append("**Optimal Solution Found**")
for k, v in sol.items():
    st.session_state.logs.append(f"{k} = {v}")

Display trace

if st.session_state.logs: st.markdown("## Solver Trace") for entry in st.session_state.logs: st.write(entry)

Display tableaus

if st.session_state.tables: st.markdown("---") for idx, tbl in enumerate(st.session_state.tables): st.subheader(f"Tableau {idx}") st.code(tabulate(tbl, tablefmt="fancy_grid"))

Display final result

if st.session_state.final_vars: st.markdown("---") st.subheader("🎉 Final Result") st.write(f"x = {st.session_state.final_vars['x']}") st.write(f"y = {st.session_state.final_vars['y']}") st.write(f"Z = {st.session_state.final_vars['Z']}")

