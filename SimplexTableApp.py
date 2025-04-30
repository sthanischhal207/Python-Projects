import streamlit as st
from tabulate import tabulate
from fractions import Fraction
import numpy as np

# Initialize global variables
array = [
    ["Basis", "x(C1)", "y(C2)", "s(C3)", "t(C4)", "Z(C5)", "RHS(C6)", "Ratio"],
    ["s(R1)", "", "", 1, 0, 0, "", ""],
    ["t(R2)", "", "", 0, 1, 0, "", ""],
    ["Z(R3)", "", "", 0, 0, 1, "", ""],
]
augument = [["a", "b", "c"], ["d", "e", "f"], ["g", "h", 0]]
ans = ["", "", "", "", ""]
c = 0


def get_data(choice, inputs):
    global array, augument
    for i in range(3):
        for j in range(3):
            if i == 2 and j == 2:
                break
            augument[i][j] = Fraction(inputs[i][j]).limit_denominator(10)

    if choice == 2:
        transpose()

    augument[2][0] *= -1
    augument[2][1] *= -1
    store_data_in_table()


def store_data_in_table():
    global array, augument
    for i in range(3):
        for k in range(3):
            j = [1, 2, 6]
            array[i + 1][j[k]] = augument[i][k]


def transpose():
    global augument
    augument = np.array(augument).T


def solve_simplex_table():
    global array, c
    column = 0
    row = 0
    output = []
    while array[3][1] < 0 or array[3][2] < 0:
        column = 1 if array[3][1] < array[3][2] else 2
        ratio(column)
        c += 1
        output.append(f"Simplex Table {c}")
        output.append(tabulate(array, tablefmt="fancy_grid"))
        output.append(print_ans(0))
        row = 1 if array[1][7] < array[2][7] else 2
        output.append(print_data(row, column))
        output.append(solving(row, column))
    for i in range(2):
        array[i + 1][7] = ""
    c += 1
    output.append(f"Simplex Table {c}")
    output.append(tabulate(array, tablefmt="fancy_grid"))
    output.append(print_ans(1))
    return output


def solving(r, col):
    global array
    steps = ""
    if array[r][col] != 1:
        steps += f"R{r} -> R{r} * ({Fraction(1 / array[r][col]).limit_denominator(10)})\n"
        divide = array[r][col]
        for i in range(6):
            array[r][i + 1] = Fraction(array[r][i + 1] / divide).limit_denominator(10)
    for i in range(3):
        if i + 1 != r:
            divide_by = array[i + 1][col] / array[r][col]
            steps += f"R{i+1} -> R{i+1} - R{r} * ({Fraction(divide_by).limit_denominator(10)})\n"
            for j in range(6):
                array[i + 1][j + 1] = Fraction(
                    array[i + 1][j + 1] - (array[r][j + 1] * divide_by)
                ).limit_denominator(10)
    return steps


def print_data(r, c):
    global array
    return (
        f"Pivot Column: C{c}\n"
        f"Departing Row: R{r}\n"
        f"Entering Element: C{c} R{r} = {array[r][c]}\n"
    )


def ratio(col):
    global array
    for i in range(2):
        array[i + 1][7] = Fraction(
            array[i + 1][6] / array[i + 1][col]
        ).limit_denominator(10)


def print_ans(command):
    global array, ans
    cnt = 0
    for i in range(5):
        for j in range(3):
            if array[j + 1][i + 1] == 1:
                for k in [1, 2, 3]:
                    if array[k][i + 1] == 0:
                        cnt += 1
                if cnt == 2:
                    ans[i] = array[j + 1][6]
                    cnt = 0
                    break
                ans[i] = 0
            else:
                ans[i] = 0
            cnt = 0

    out = (
        f"x = {ans[0]}\ny = {ans[1]}\ns = {ans[2]}\nt = {ans[3]}\nZ = {ans[4]}\n"
    )
    if command == 0:
        out += "------- NOT OPTIMAL YET (Z-row has negatives) -------"
    else:
        out += "-------- OPTIMAL SOLUTION FOUND --------"
    return out


# Streamlit App
def main():
    st.title("Simplex Method Solver")

    choice = st.radio("Solving For:", ["Maximum", "Minimum"])
    is_max = 1 if choice == "Maximum" else 2

    st.subheader("Enter coefficients for the following:")
    col1, col2, col3 = st.columns(3)
    st.subheader("eqn1-> ax + by = c")
    with col1:
        a = st.number_input("a (x in eq1)", value=1.0)
        b = st.number_input("b (y in eq1)", value=1.0)
        c = st.number_input("c (RHS eq1)", value=1.0)
    st.subheader("eqn2-> dx + ey = f")
    with col2:
        d = st.number_input("d (x in eq2)", value=1.0)
        e = st.number_input("e (y in eq2)", value=1.0)
        f = st.number_input("f (RHS eq2)", value=1.0)
    st.subheader("Z = gx + hy")    
    with col3:
        g = st.number_input("g (x in Z)", value=1.0)
        h = st.number_input("h (y in Z)", value=1.0)
        

    if st.button("Solve"):
        user_inputs = [[a, b, c], [d, e, f], [g, h, 0]]
        get_data(is_max, user_inputs)
        steps = solve_simplex_table()
        for step in steps:
            st.text(step)


if __name__ == "__main__":
    main()