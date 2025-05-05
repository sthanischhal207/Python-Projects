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

    # Input section - Objective function first
    st.subheader("Enter Objective Function:")
    col_obj = st.columns(2)
    with col_obj[0]:
        g = st.number_input("Coefficient for x (g)", key='g', value=5.0)
    with col_obj[1]:
        h = st.number_input("Coefficient for y (h)", key='h', value=4.0)

    # Constraints input
    st.subheader("Enter Constraints:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Constraint 1 (ax + by ≤ c)")
        a = st.number_input("a", key='a', value=2.0)
        b = st.number_input("b", key='b', value=1.0)
        c = st.number_input("c", key='c', value=10.0)
    
    with col2:
        st.write("Constraint 2 (dx + ey ≤ f)")
        d = st.number_input("d", key='d', value=1.0)
        e = st.number_input("e", key='e', value=2.0)
        f_val = st.number_input("f", key='f', value=12.0)

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
    try:
        # Convert inputs to fractions and then to floats for display
        augmented = [
            [float(Fraction(a).limit_denominator()), float(Fraction(b).limit_denominator()), float(Fraction(c).limit_denominator())],
            [float(Fraction(d).limit_denominator()), float(Fraction(e).limit_denominator()), float(Fraction(f_val).limit_denominator())],
            [float(Fraction(-g).limit_denominator()), float(Fraction(-h).limit_denominator()), 0.0]
        ]

        if st.session_state.problem_type == 2:
            augmented = np.array(augmented).T.tolist()

        # Initialize simplex table with float values
        st.session_state.simplex_table = [
            ['Basis', 'x', 'y', 's', 't', 'Z', 'RHS'],
            ['s', 1.0, 0.0, 1.0, 0.0, 0.0, augmented[0][2]],
            ['t', augmented[1][0], augmented[1][1], 0.0, 1.0, 0.0, augmented[1][2]],
            ['Z', augmented[2][0], augmented[2][1], 0.0, 0.0, 1.0, 0.0]
        ]

        st.session_state.solution = [0.0] * 5
        
    except Exception as e:
        st.error(f"Initialization error: {str(e)}")
        st.stop()

def display_current_state():
    try:
        st.subheader(f"Iteration {st.session_state.iteration}")
        
        # Process and display simplex table
        processed_data = []
        for row in st.session_state.simplex_table[1:]:
            processed_row = [
                str(cell) if isinstance(cell, str) else f"{float(cell):.2f}" 
                for cell in row
            ]
            processed_data.append(processed_row)
        
        df = pd.DataFrame(
            processed_data,
            columns=st.session_state.simplex_table[0]
        )
        
        st.write("Current Simplex Table:")
        st.table(df)
        
        # Display current solution
        current_sol = [
            float(val) if val != '' else 0.0 
            for val in st.session_state.solution
        ]
        
        st.subheader("Current Solution:")
        st.write(f"x = {current_sol[0]:.2f}")
        st.write(f"y = {current_sol[1]:.2f}")
        st.write(f"s = {current_sol[2]:.2f}")
        st.write(f"t = {current_sol[3]:.2f}")
        st.write(f"Z = {current_sol[4]:.2f}")
        
    except Exception as e:
        st.error(f"Display error: {str(e)}")
        st.stop()

def perform_iteration():
    try:
        table = st.session_state.simplex_table
        z_row = [float(x) for x in table[-1][1:-1]]  # Convert to floats for comparison
        
        # Check optimality
        if all(x >= 0 for x in z_row):
            st.session_state.step = 2
            st.success("Optimal Solution Reached!")
            return

        # Pivot column selection
        pivot_col = 1 if z_row[0] < z_row[1] else 2
        
        # Ratio calculation
        ratios = []
        for row in table[1:-1]:
            val = float(row[pivot_col])
            rhs = float(row[-1])
            ratios.append(rhs/val if val > 0 else np.inf)
        
        # Pivot row selection
        pivot_row = np.argmin(ratios) + 1
        
        # Perform pivoting
        pivot_element = float(table[pivot_row][pivot_col])
        
        # Normalize pivot row
        for i in range(1, len(table[pivot_row])):
            table[pivot_row][i] = float(table[pivot_row][i]) / pivot_element
        
        # Update other rows
        for i in range(1, len(table)):
            if i != pivot_row:
                factor = float(table[i][pivot_col])
                for j in range(1, len(table[i])):
                    table[i][j] = float(table[i][j]) - factor * float(table[pivot_row][j])
        
        # Update basis
        table[pivot_row][0] = 'x' if pivot_col == 1 else 'y'
        
        # Update solution
        update_solution()
        
    except Exception as e:
        st.error(f"Iteration error: {str(e)}")
        st.stop()

def update_solution():
    try:
        table = st.session_state.simplex_table
        solution = [0.0] * 5
        
        # Find basic variables
        for row in table[1:-1]:
            var = row[0]
            if var == 'x':
                solution[0] = float(row[-1])
            elif var == 'y':
                solution[1] = float(row[-1])
            elif var == 's':
                solution[2] = float(row[-1])
            elif var == 't':
                solution[3] = float(row[-1])
        
        # Z value
        solution[4] = float(table[-1][-1])
        
        st.session_state.solution = solution
        
    except Exception as e:
        st.error(f"Solution update error: {str(e)}")
        st.stop()

if __name__ == "__main__":
    main()