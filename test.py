import streamlit as st
from fractions import Fraction
import pandas as pd

st.set_page_config(page_title="Simplex Solver", layout="centered")

st.title("Simplex Method Solver")

# Input section
st.subheader("Step 1: Enter the coefficients")

choice = st.radio("Problem Type", ["Maximization", "Minimization"])

col1, col2 = st.columns(2)

with col1:
    a = st.number_input("a (in ax + by ≤ c)", value=1.0, key="a")
    b = st.number_input("b (in ax + by ≤ c)", value=1.0, key="b")
    c = st.number_input("c (RHS of 1st constraint)", value=100.0, key="c")

with col2:
    d = st.number_input("d (in dx + ey ≤ f)", value=1.0, key="d")
    e = st.number_input("e (in dx + ey ≤ f)", value=1.0, key="e")
    f = st.number_input("f (RHS of 2nd constraint)", value=150.0, key="f")

g = st.number_input("g (coefficient of x in objective)", value=5.0, key="g")
h = st.number_input("h (coefficient of y in objective)", value=4.0, key="h")

if st.button("Solve"):
    # Step 1: Initialize simplex table
    augument = [
        [Fraction(a), Fraction(b), Fraction(c)],
        [Fraction(d), Fraction(e), Fraction(f)],
        [Fraction(-g if choice == "Maximization" else g), Fraction(-h if choice == "Maximization" else h), 0],
    ]

    array = [
        ["Basis", "x(C1)", "y(C2)", "s(C3)", "t(C4)", "Z(C5)", "RHS(C6)", "Ratio"],
        ["s(R1)", augument[0][0], augument[0][1], 1, 0, 0, augument[0][2], ""],
        ["t(R2)", augument[1][0], augument[1][1], 0, 1, 0, augument[1][2], ""],
        ["Z(R3)", augument[2][0], augument[2][1], 0, 0, 1, augument[2][2], ""],
    ]
    ans = ["", "", "", "", ""]

    def print_array():
        df = pd.DataFrame(array[1:], columns=array[0])
        st.dataframe(df, use_container_width=True)

    def print_data(r, c):
        st.markdown(
            f"""
            **Pivot Column:** C{c}  
            **Departing Row:** R{r}  
            **Entering Element:** C{c} R{r} = {array[r][c]}
            """
        )

    def solving(r, col):
        if array[r][col] != 1:
            factor = Fraction(1 / array[r][col]).limit_denominator(10)
            st.code(f"R{r} → R{r} × ({factor})")
            divide = array[r][col]
            for i in range(6):
                array[r][i + 1] = Fraction(array[r][i + 1] / divide).limit_denominator(10)

        for i in range(3):
            if i + 1 != r:
                divide_by = array[i + 1][col] / array[r][col]
                factor = Fraction(divide_by).limit_denominator(10)
                st.code(f"R{i+1} → R{i+1} - R{r} × ({factor})")
                for j in range(6):
                    array[i + 1][j + 1] = Fraction(
                        array[i + 1][j + 1] - (array[r][j + 1] * divide_by)
                    ).limit_denominator(10)

    def ratio(col):
        for i in range(2):
            array[i + 1][7] = Fraction(array[i + 1][6] / array[i + 1][col]).limit_denominator(10)

    def print_ans(command):
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
        st.markdown(
            f"""
            **x = {ans[0]}**  
            **y = {ans[1]}**  
            **s = {ans[2]}**  
            **t = {ans[3]}**  
            **Z {'Min' if choice == 'Minimization' else 'Max'} = {ans[4]}**
            """
        )
        if command == 0:
            st.warning("It is not an optimal solution as it contains negative values in row 3.")
        else:
            st.success("It is an optimal solution.")

    def solve_simplex_table():
        column = 0
        row = 0
        iteration = 0
        while array[3][1] < 0 or array[3][2] < 0:
            column = 1 if array[3][1] < array[3][2] else 2
            ratio(column)
            iteration += 1
            st.subheader(f"Simplex Table {iteration}")
            print_array()
            print_ans(0)
            row = 1 if array[1][7] < array[2][7] else 2
            print_data(row, column)
            solving(row, column)
        for i in range(2):
            array[i + 1][7] = ""
        st.subheader("Final Table")
        print_array()
        print_ans(1)

    solve_simplex_table()