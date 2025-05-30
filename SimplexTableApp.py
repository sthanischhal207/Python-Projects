import streamlit as st
from fractions import Fraction
import numpy as np
import pandas as pd

st.set_page_config(page_title="Simplex Solver", layout="centered")
st.title("Simplex Method Solver")
st.markdown("Solves both Maximization and Minimization Linear Programming Problems")

# Global variables
array = [
    ["Basis", "x(C1)", "y(C2)", "s(C3)", "t(C4)", "Z(C5)", "RHS(C6)", "Ratio"],
    ["s(R1)", "", "", 1, 0, 0, "", ""],
    ["t(R2)", "", "", 0, 1, 0, "", ""],
    ["Z(R3)", "", "", 0, 0, 1, "", ""],
]
augument = [
    ["a", "b", "c"],
    ["d", "e", "f"],
    ["g", "h", 0],
]
ans = [0, 0, 0, 0, 0]  # [x, y, s, t, Z]

def print_array():
    """Function to display the simplex table in a formatted dataframe."""
    df = pd.DataFrame(array[1:], columns=array[0])
    return df

def print_augment():
    """Function to display the augmented matrix."""
    temp_augment = [[float(val) for val in row] for row in augument]
    return pd.DataFrame(temp_augment, 
                       index=["Constraint 1", "Constraint 2", "Objective Z"],
                       columns=["x", "y", "RHS"])

def print_data(r, c):
    """Function to display pivot information."""
    st.markdown(f"""
    **Pivot Column:** C{c}  
    **Departing Row:** R{r}  
    **Entering Element:** C{c} R{r} = {array[r][c]}
    """)

def solving(r, col):
    """Function to perform row operations for the simplex method."""
    operations = []

    if array[r][col] != 1:  # Normalize the pivot element to 1
        factor = Fraction(1 / array[r][col]).limit_denominator(10)
        operations.append(f"R{r} → R{r} × ({factor})")
        divide = array[r][col]
        for i in range(6):
            array[r][i + 1] = Fraction(array[r][i + 1] / divide).limit_denominator(10)

    for i in range(3):  # Eliminate other rows in the pivot column
        if i + 1 != r:
            divide_by = array[i + 1][col] / array[r][col]
            factor = Fraction(divide_by).limit_denominator(10)
            operations.append(f"R{i+1} → R{i+1} - R{r} × ({factor})")
            for j in range(6):
                array[i + 1][j + 1] = Fraction(
                    array[i + 1][j + 1] - (array[r][j + 1] * divide_by)
                ).limit_denominator(10)

    return operations

def ratio(col):
    """Function to calculate the ratio column for the current pivot column."""
    for i in range(2):  # Calculate ratios for rows 1 and 2
        if array[i + 1][col] > 0:  # Only calculate ratio if coefficient is positive
            array[i + 1][7] = Fraction(
                array[i + 1][6] / array[i + 1][col]
            ).limit_denominator(10)
        else:
            array[i + 1][7] = float('inf')  # Set to infinity if coefficient is negative or zero

def find_basic_variables():
    """Function to identify basic variables in the current tableau."""
    # Initialize solution vector
    solution = [0, 0, 0, 0, 0]  # [x, y, s, t, Z]

    # Each row corresponds to a basic variable
    # We need to find which column has exactly one 1 and zeros elsewhere
    for col in range(1, 6):  # Columns 1-5 (x, y, s, t, Z)
        for row in range(1, 4):  # Rows 1-3
            # Check if this column has exactly one 1 at this row and 0s elsewhere
            is_unit_column = True

            # First verify this position has a 1
            if array[row][col] != 1:
                continue

            # Then check all other positions in this column are 0
            for other_row in range(1, 4):
                if other_row != row and array[other_row][col] != 0:
                    is_unit_column = False
                    break

            if is_unit_column:
                # We found a basic variable
                # The value is the RHS of that row
                solution[col-1] = array[row][6]
                break

    return solution

def print_ans(command, choice):
    """Function to extract and display the current solution from the simplex table."""
    global ans

    # Find basic variables and their values
    solution = find_basic_variables()
    ans = solution

    # For minimization case, y value is in the second row RHS column (index 6)
    # and we need to check the correct column identification
    if choice == 2 and command == 1:  # Final minimization solution
        # For the minimization final solution, get y value specifically from row 2
        # Get value where y is a basic variable
        y_value = 0
        for row in range(1, 4):
            if array[row][2] == 1:  # Check if y column (C2) has a 1 in this row
                is_unit_column = True
                for other_row in range(1, 4):
                    if other_row != row and array[other_row][2] != 0:
                        is_unit_column = False
                        break
                if is_unit_column:
                    y_value = array[row][6]
                    break

        # Display solution
        solution_text = f"""
        **x = {ans[0]}**  
        **y = {y_value}**  
        **s = {ans[2]}**  
        **t = {ans[3]}**  
        **Z Min = {ans[4]}**
        """
        st.markdown(solution_text)
        st.success("It is an optimal solution.")
        final_text = f"**FINAL ANSWER:**  \nZ Min = {ans[4]} at ({ans[0]}, {y_value})"
        st.markdown(final_text)
    else:
        # Format for display for maximization or intermediate solution
        z_label = "Max" if choice == 1 else "Min"
        solution_text = f"""
        **x = {ans[0]}**  
        **y = {ans[1]}**  
        **s = {ans[2]}**  
        **t = {ans[3]}**  
        **Z {z_label} = {ans[4]}**
        """

        if command == 0:
            st.markdown(solution_text)
            st.warning("It is not an optimal solution as it contains negative values in row 3.")
        else:
            st.markdown(solution_text)
            st.success("It is an optimal solution.")

            # Final answer display
            if choice == 1:  # Maximization case
                final_text = f"**FINAL ANSWER:**  \nZ Max = {ans[4]} at ({ans[0]}, {ans[1]})"
                st.markdown(final_text)

def transpose_augument():
    """Function to transpose the augmented matrix."""
    global augument
    augument = np.array([[float(cell) for cell in row] for row in augument])  # Convert to a NumPy array
    augument = augument.T  # Transpose the array
    # Convert back to list of lists with Fractions
    augument = [[Fraction(cell).limit_denominator(10) for cell in row] for row in augument]
    return print_augment()

def store_data_in_table():
    """Function to populate the simplex table with the collected data."""
    global array, augument
    for i in range(3):  # Loop through each row of the augmented matrix
        for k in range(3):  # Map augmented matrix values to the simplex table
            j = [1, 2, 6]  # Columns in the simplex table corresponding to C1, C2, and RHS
            array[i + 1][j[k]] = augument[i][k]

def solve_simplex_table(choice):
    """Function to iteratively solve the simplex table until an optimal solution is found."""
    column = 0
    row = 0
    iteration = 0

    while array[3][1] < 0 or array[3][2] < 0:  # Continue until all Z-row values are non-negative
        iteration += 1
        st.subheader(f"Simplex Table {iteration}")

        # Determine the pivot column (most negative value in Z-row)
        if array[3][1] <= array[3][2]:
            column = 1
        else:
            column = 2

        ratio(column)  # Calculate ratios for the current pivot column

        # Display the current table
        st.dataframe(print_array(), use_container_width=True)
        print_ans(0, choice)

        # Find minimum positive ratio to determine pivot row
        valid_ratios = []
        for i in range(1, 3):
            if array[i][column] > 0:
                valid_ratios.append((i, array[i][7]))

        if not valid_ratios:
            st.error("No valid pivot found. The problem is unbounded.")
            break

        # Sort by ratio value and take the minimum
        row = min(valid_ratios, key=lambda x: x[1])[0]

        # Display pivot information
        print_data(row, column)

        # Perform row operations
        operations = solving(row, column)
        for op in operations:
            st.code(op)

    # Clear ratio column after optimization
    for i in range(2):
        array[i + 1][7] = ""

    # Display final table
    st.subheader("Final Simplex Table")
    st.dataframe(print_array(), use_container_width=True)

    # For final solution
    print_ans(1, choice)

# Main form for user input
with st.form("input_form"):
    st.subheader("Choose Optimization Type")
    choice = st.radio("", ["1. Maximization", "2. Minimization"], horizontal=True)
    choice = 1 if choice == "1. Maximization" else 2

    st.subheader("Enter Constraint Coefficients")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("**Constraint 1:**")
        st.latex(f"ax + by {'\\leq' if choice == 1 else '\\geq'} c")
        a = st.number_input("a = ", value=1.0, key="a")
        b = st.number_input("b = ", value=1.0, key="b")
        c = st.number_input("c = ", value=100.0, key="c")

    with col2:
        st.markdown("**Constraint 2:**")
        st.latex(f"dx + ey {'\\leq' if choice == 1 else '\\geq'} f")
        d = st.number_input("d = ", value=1.0, key="d")
        e = st.number_input("e = ", value=1.0, key="e")
        f = st.number_input("f = ", value=150.0, key="f")

    with col3:
        st.markdown("**Objective Function:**")
        st.latex("Z = gx + hy")
        g = st.number_input("g = ", value=5.0, key="g")
        h = st.number_input("h = ", value=4.0, key="h")

    submitted = st.form_submit_button("Solve")

if submitted:
    st.info(f"Solving {'Maximization' if choice == 1 else 'Minimization'} Problem")

    # Reset global variables
    array = [
        ["Basis", "x(C1)", "y(C2)", "s(C3)", "t(C4)", "Z(C5)", "RHS(C6)", "Ratio"],
        ["s(R1)", "", "", 1, 0, 0, "", ""],
        ["t(R2)", "", "", 0, 1, 0, "", ""],
        ["Z(R3)", "", "", 0, 0, 1, "", ""],
    ]
    ans = [0, 0, 0, 0, 0]

    # Set up augmented matrix
    augument = [
        [Fraction(a).limit_denominator(10), Fraction(b).limit_denominator(10), Fraction(c).limit_denominator(10)],
        [Fraction(d).limit_denominator(10), Fraction(e).limit_denominator(10), Fraction(f).limit_denominator(10)],
        [Fraction(g).limit_denominator(10), Fraction(h).limit_denominator(10), Fraction(0)],
    ]

    st.subheader("Input Data")
    st.dataframe(print_augment(), use_container_width=True)

    if choice == 2:  # For minimization
        st.subheader("For Minimization - Transpose the Augmented Form")
        st.dataframe(transpose_augument(), use_container_width=True)
        st.info("After transposing, we proceed with solving using the Simplex method")

    # Negate the coefficients of the objective function
    augument[2][0] = (-1) * augument[2][0]
    augument[2][1] = (-1) * augument[2][1]

    # Store the data in the simplex table
    store_data_in_table()

    st.subheader("System of Equations")
    for i in range(3):
        k = ["s", "t", "Z"]
        st.latex(f"{augument[i][0]}x + {augument[i][1]}y + {k[i]} = {augument[i][2]}")

    st.markdown("---")

    # Solve the problem
    solve_simplex_table(choice)