import streamlit as st
from fractions import Fraction
import pandas as pd

st.set_page_config(page_title="Simplex Solver ", layout="centered")
st.title("Simplex Method Solver     
[Note: Only Max Case is working for Now]")

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
        st.markdown("**Equation 1: ax + by = c**")
        a = st.number_input("a (coefficient of x)", value=1.0)
        b = st.number_input("b (coefficient of y)", value=1.0)
        c = st.number_input("RHS (c)", value=100.0)

    with col2:
        st.markdown("**Equation 2: dx + ey = f**")
        d = st.number_input("d (coefficient of x)", value=1.0)
        e = st.number_input("e (coefficient of y)", value=1.0)
        f = st.number_input("RHS (f)", value=150.0)

    submitted = st.form_submit_button("Solve")

if submitted:
    augument = [
        [Fraction(a), Fraction(b), Fraction(c)],
        [Fraction(d), Fraction(e), Fraction(f)],
        [Fraction(-g if objective == "Maximization" else g),
         Fraction(-h if objective == "Maximization" else h), 0],
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
        st.markdown(f"**Pivot Column:** C{c}  \n**Departing Row:** R{r}  \n**Entering Element:** C{c} R{r} = {array[r][c]}")

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
            f"**x = {ans[0]}**  \n"
            f"**y = {ans[1]}**  \n"
            f"**s = {ans[2]}**  \n"
            f"**t = {ans[3]}**  \n"
            f"**Z {'Min' if objective == 'Minimization' else 'Max'} = {ans[4]}**"
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