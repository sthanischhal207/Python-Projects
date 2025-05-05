import streamlit as st
from fractions import Fraction
import numpy as np
import pandas as pd

st.set_page_config(page_title="Simplex Solver", layout="centered")
st.title("Simplex Method Solver (Max & Min)")

def main():
    with st.form("input_form"):
        st.subheader("Objective Function")
        st.latex("Z = gx + hy")

        col_obj1, col_obj2 = st.columns(2)
        with col_obj1:
            g = st.number_input("g (coefficient of x in Z)", value=5.0)
        with col_obj2:
            h = st.number_input("h (coefficient of y in Z)", value=4.0)

        objective = st.radio("Optimization Type", ["Maximization", "Minimization"])
        st.markdown("---")

        st.subheader("Constraints")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Equation 1: ax + by ≤ c**")
            a = st.number_input("a (coefficient of x)", value=1.0)
            b = st.number_input("b (coefficient of y)", value=1.0)
            c = st.number_input("RHS (c)", value=100.0)

        with col2:
            st.markdown("**Equation 2: dx + ey ≤ f**")
            d = st.number_input("d (coefficient of x)", value=1.0)
            e = st.number_input("e (coefficient of y)", value=1.0)
            f_val = st.number_input("RHS (f)", value=150.0)

        submitted = st.form_submit_button("Solve")

    if submitted:
        solve_problem(g, h, a, b, c, d, e, f_val, objective)

def solve_problem(g, h, a, b, c, d, e, f_val, objective):
    # Convert to fractions and handle minimization transpose
    augument = [
        [Fraction(a), Fraction(b), Fraction(c)],
        [Fraction(d), Fraction(e), Fraction(f_val)],
        [Fraction(-g), Fraction(-h), Fraction(0)] if objective == "Maximization" else 
        [Fraction(g), Fraction(h), Fraction(0)]
    ]

    if objective == "Minimization":
        augument = np.array(augument).T.tolist()
        st.success("Converted to Dual Problem via Transpose:")

    # Build initial simplex table
    array = [
        ["Basis", "x(C1)", "y(C2)", "s(C3)", "t(C4)", "Z(C5)", "RHS(C6)", "Ratio"],
        ["s(R1)", augument[0][0], augument[0][1], 1, 0, 0, augument[0][2], ""],
        ["t(R2)", augument[1][0], augument[1][1], 0, 1, 0, augument[1][2], ""],
        ["Z(R3)", augument[2][0], augument[2][1], 0, 0, 1, augument[2][2], ""],
    ]
    
    solution = ["", "", "", "", ""]
    iteration = 0

    while True:
        # Check for optimality
        z_row = array[3][1:3]
        if all(float(x) >= 0 for x in z_row if isinstance(x, (int, float, Fraction))):
            break

        iteration += 1
        st.subheader(f"Iteration {iteration}")
        print_table(array)
        print_solution(array, solution, objective, 0)

        # Pivot column selection
        pivot_col = 1 if float(z_row[0]) < float(z_row[1]) else 2

        # Ratio calculation
        for i in range(2):
            if array[i+1][pivot_col] != 0:
                array[i+1][7] = Fraction(array[i+1][6]/array[i+1][pivot_col]).limit_denominator()
            else:
                array[i+1][7] = np.inf

        # Pivot row selection
        pivot_row = 1 if float(array[1][7]) < float(array[2][7]) else 2

        st.markdown(f"**Pivot Column:** C{pivot_col}  \n"
                    f"**Departing Row:** R{pivot_row}  \n"
                    f"**Pivot Element:** {array[pivot_row][pivot_col]}")

        perform_pivot(array, pivot_row, pivot_col)

    # Final table
    for i in range(2):
        array[i+1][7] = ""
        
    st.subheader("Final Result")
    print_table(array)
    print_solution(array, solution, objective, 1)

def print_table(array):
    df = pd.DataFrame(array[1:], columns=array[0])
    
    # Convert fractions to floats for display
    formatted_data = []
    for row in array[1:]:
        formatted_row = [
            str(cell) if isinstance(cell, str) else 
            f"{float(cell):.2f}" if isinstance(cell, (int, float, Fraction)) else ""
            for cell in row
        ]
        formatted_data.append(formatted_row)
    
    df = pd.DataFrame(formatted_data, columns=array[0])
    st.dataframe(df, use_container_width=True)

def perform_pivot(array, pivot_row, pivot_col):
    pivot_val = array[pivot_row][pivot_col]
    
    # Normalize pivot row
    if pivot_val != 1:
        factor = Fraction(1/pivot_val).limit_denominator()
        st.code(f"R{pivot_row} → R{pivot_row} × ({factor})")
        for i in range(1, 7):
            array[pivot_row][i] = Fraction(array[pivot_row][i] * factor).limit_denominator()

    # Update other rows
    for i in range(1, 4):
        if i != pivot_row and array[i][pivot_col] != 0:
            factor = Fraction(array[i][pivot_col]).limit_denominator()
            st.code(f"R{i} → R{i} - R{pivot_row} × ({factor})")
            for j in range(1, 7):
                array[i][j] = Fraction(array[i][j] - factor * array[pivot_row][j]).limit_denominator()

    # Update basis
    array[pivot_row][0] = "x" if pivot_col == 1 else "y"

def print_solution(array, solution, objective, command):
    for col in range(5):
        for row in range(1, 4):
            if array[row][col+1] == 1:
                unique = True
                for check_row in range(1, 4):
                    if check_row != row and array[check_row][col+1] != 0:
                        unique = False
                        break
                if unique:
                    solution[col] = float(array[row][6])
                    break
            solution[col] = 0.0

    st.markdown(f"""
    **Current Solution:**
    - x = {solution[0]:.2f}
    - y = {solution[1]:.2f}
    - s = {solution[2]:.2f}
    - t = {solution[3]:.2f}
    - Z {objective} = {solution[4]:.2f}
    """)

    if command == 0:
        st.warning("Intermediate solution (not optimal)")
    else:
        st.success("Optimal solution reached!")

if __name__ == "__main__":
    main()