import streamlit as st
from fractions import Fraction
import numpy as np
import pandas as pd

def main():
    st.title("Simplex Method Solver")
    
    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.simplex_table = []
        st.session_state.augmented = []
        st.session_state.iteration = 0
        st.session_state.solution = []
        st.session_state.problem_type = 1

    # Problem type selection
    problem_type = st.selectbox("Select problem type:", ["Maximization", "Minimization"])
    st.session_state.problem_type = 1 if problem_type == "Maximization" else 2

    # Input constraints and objective function
    st.subheader("Enter Coefficients:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Constraint 1 (ax + by <= c)")
        a = st.number_input("a", key='a', value=2.0)
        b = st.number_input("b", key='b', value=1.0)
        c = st.number_input("c", key='c', value=10.0)
    
    with col2:
        st.write("Constraint 2 (dx + ey <= f)")
        d = st.number_input("d", key='d', value=1.0)
        e = st.number_input("e", key='e', value=2.0)
        f_val = st.number_input("f", key='f', value=12.0)
    
    with col3:
        st.write("Objective Function (Z = gx + hy)")
        g = st.number_input("g", key='g', value=5.0)
        h = st.number_input("h", key='h', value=4.0)

    if st.button("Initialize Simplex Table"):
        initialize_simplex(a, b, c, d, e, f_val, g, h)
        st.session_state.step = 1

    if st.session_state.step >= 1:
        display_current_state()
        
        if st.button("Next Iteration"):
            perform_iteration()
            st.session_state.iteration += 1
            st.experimental_rerun()

def initialize_simplex(a, b, c, d, e, f_val, g, h):
    augmented = [
        [Fraction(a).limit_denominator(), Fraction(b).limit_denominator(), Fraction(c).limit_denominator()],
        [Fraction(d).limit_denominator(), Fraction(e).limit_denominator(), Fraction(f_val).limit_denominator()],
        [Fraction(-g).limit_denominator(), Fraction(-h).limit_denominator(), Fraction(0).limit_denominator()]
    ]

    if st.session_state.problem_type == 2:
        augmented = np.array(augmented).T.tolist()

    # Initialize simplex table
    st.session_state.simplex_table = [
        ['Basis', 'x', 'y', 's', 't', 'Z', 'RHS'],
        ['s', Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0), augmented[0][2]],
        ['t', augmented[1][0], augmented[1][1], Fraction(0), Fraction(1), Fraction(0), augmented[1][2]],
        ['Z', augmented[2][0], augmented[2][1], Fraction(0), Fraction(0), Fraction(1), Fraction(0)]
    ]

    st.session_state.solution = [''] * 5

def display_current_state():
    st.subheader(f"Iteration {st.session_state.iteration}")
    
    # Convert table to DataFrame for better display
    df = pd.DataFrame(st.session_state.simplex_table[1:], columns=st.session_state.simplex_table[0])
    st.write("Current Simplex Table:")
    st.dataframe(df.style.format(formatter={col: "{:.2f}" for col in df.columns}))
    
    # Display current solution
    st.write("\nCurrent Solution:")
    st.write(f"x = {st.session_state.solution[0]}")
    st.write(f"y = {st.session_state.solution[1]}")
    st.write(f"Z = {st.session_state.solution[4]}")

def perform_iteration():
    table = st.session_state.simplex_table
    z_row = table[-1][1:-1]  # Exclude Basis and RHS
    
    # Check if optimal
    if all(x >= 0 for x in z_row if isinstance(x, Fraction)):
        st.session_state.step = 2
        return

    # Pivot column selection
    pivot_col = 1 if z_row[0] < z_row[1] else 2
    
    # Ratio calculation
    ratios = []
    for row in table[1:-1]:
        if row[pivot_col] > 0:
            ratios.append(row[-1] / row[pivot_col])
        else:
            ratios.append(Fraction(np.inf))
    
    # Pivot row selection
    pivot_row = ratios.index(min(ratios)) + 1
    
    # Perform pivoting
    pivot_element = table[pivot_row][pivot_col]
    
    # Normalize pivot row
    for i in range(1, len(table[pivot_row])):
        if i != pivot_col:
            table[pivot_row][i] /= pivot_element
    
    # Update other rows
    for i in range(1, len(table)):
        if i != pivot_row and table[i][pivot_col] != 0:
            factor = table[i][pivot_col]
            for j in range(1, len(table[i])):
                if j != pivot_col:
                    table[i][j] -= factor * table[pivot_row][j]
                else:
                    table[i][j] = Fraction(0)
    
    # Update basis
    table[pivot_row][0] = 'x' if pivot_col == 1 else 'y'
    
    # Update solution
    update_solution()

def update_solution():
    table = st.session_state.simplex_table
    basis = {'x': 0, 'y': 0, 's': 0, 't': 0, 'Z': 0}
    
    for row in table[1:-1]:
        var = row[0]
        basis[var] = row[-1]
    
    st.session_state.solution = [
        basis.get('x', 0),
        basis.get('y', 0),
        basis.get('s', 0),
        basis.get('t', 0),
        table[-1][-1]
    ]

if __name__ == "__main__":
    main()