import streamlit as st from tabulate import tabulate from fractions import Fraction

Configure page

st.set_page_config(page_title="Simplex Solver", layout="centered")

Session state for tables and logs

if "tables" not in st.session_state: st.session_state.tables = [] if "logs" not in st.session_state: st.session_state.logs = [] if "final_output" not in st.session_state: st.session_state.final_output = ""

st.title("2-Variable Simplex Method Solver") st.markdown("---")

Input section

with st.form("input_form"): st.subheader("Enter Objective Function Coefficients") col_obj1, col_obj2 = st.columns(2) with col_obj1: g = st.number_input("g (coefficient of x)", value=1.0) with col_obj2: h = st.number_input("h (coefficient of y)", value=1.0) objective = st.radio("Optimization Type:", ["Maximize", "Minimize"]) st.markdown("---") st.subheader("Enter Constraints Coefficients") col1, col2 = st.columns(2) with col1: a = st.number_input("a (x in Eq1)", value=1.0) b = st.number_input("b (y in Eq1)", value=1.0) c = st.number_input("c (RHS Eq1)", value=1.0) with col2: d = st.number_input("d (x in Eq2)", value=1.0) e = st.number_input("e (y in Eq2)", value=1.0) f = st.number_input("f (RHS Eq2)", value=1.0) submitted = st.form_submit_button("Solve")

if submitted: # Convert to fractions a, b, c = Fraction(a), Fraction(b), Fraction(c) d, e, f = Fraction(d), Fraction(e), Fraction(f) g, h = Fraction(g), Fraction(h)

# For maximization, we negate coefficients
if objective == "Maximize":
    g, h = -g, -h
    st.write("**Maximization chosen, objective row coefficients negated for tableau.**")
else:
    st.write("**Minimization chosen, objective row unchanged.**")

# Build initial tableau
headers = ["Basis", "x", "y", "s1", "s2", "Z", "RHS", "Ratio"]
initial = [headers,
           ["s1", a, b, 1, 0, 0, c, ""],
           ["s2", d, e, 0, 1, 0, f, ""],
           ["Z", g, h, 0, 0, 1, 0, ""]]
st.session_state.tables = [initial]
st.session_state.logs = ["**Initial Tableau:**"]

# Helper functions
def print_table(table, idx):
    st.subheader(f"Simplex Table {idx}")
    st.code(tabulate(table, tablefmt="fancy_grid"))

def calculate_ratios(table, pivot_col):
    for i in (1, 2):
        val = table[i][pivot_col]
        rhs = table[i][6]
        if val > 0:
            table[i][7] = rhs / val
        else:
            table[i][7] = "-"

def find_pivot_column(table):
    row = table[3]
    candidates = row[1:3]
    if objective == "Maximize":
        # most negative
        pivot_val = min(candidates)
    else:
        # most positive
        pivot_val = max(candidates)
    return row.index(pivot_val)

def find_pivot_row(table, pivot_col):
    ratios = [(i, table[i][7]) for i in (1, 2) if isinstance(table[i][7], Fraction)]
    if not ratios:
        return None
    return min(ratios, key=lambda x: x[1])[0]

def pivot_operation(table, pivot_row, pivot_col):
    pivot_val = table[pivot_row][pivot_col]
    # Normalize pivot row
    table[pivot_row][1:7] = [x / pivot_val for x in table[pivot_row][1:7]]
    table[pivot_row][0] = table[0][pivot_col]
    # Eliminate other rows
    for i in (1, 2, 3):
        if i != pivot_row:
            factor = table[i][pivot_col]
            table[i][1:7] = [table[i][j] - factor * table[pivot_row][j] for j in range(1,7)]

# Iteration loop
iteration = 0
while True:
    current = st.session_state.tables[-1]
    iteration += 1
    print_table(current, iteration-1)
    # Check optimality
    test_vals = current[3][1:3]
    if objective == "Maximize" and all(v >= 0 for v in test_vals):
        st.success("Optimal solution reached for maximization!")
        break
    if objective == "Minimize" and all(v <= 0 for v in test_vals):
        st.success("Optimal solution reached for minimization!")
        break
    # Pivot selection
    p_col = find_pivot_column(current)
    calculate_ratios(current, p_col)
    p_row = find_pivot_row(current, p_col)
    if p_row is None:
        st.error("Unbounded solution detected.")
        break
    # Log pivot info
    st.write(f":arrow_right: Pivot Column: C{p_col}  |  Pivot Row: R{p_row}  |  Element= {current[p_row][p_col]} ")
    # Perform pivot
    new_tab = [row.copy() for row in current]
    pivot_operation(new_tab, p_row, p_col)
    new_tab[p_row][7] = ""
    for i in (1,2):
        if i != p_row:
            new_tab[i][7] = ""
    st.session_state.tables.append(new_tab)

# Final display and solution
final = st.session_state.tables[-1]
print_table(final, iteration)
# Extract solution
sol = {"x": 0, "y": 0, "Z": 0}
for row in final[1:4]:
    var = row[0]
    if var in sol:
        sol[var] = row[6]
z_val = sol['Z']
if objective == "Minimize":
    z_val = -z_val
st.markdown("---")
st.markdown(f"**Optimal Solution:**  \n- x = {sol['x']}  \n- y = {sol['y']}  \n- Z = {z_val}  \n**Type:** {objective}")

