import streamlit as st from tabulate import tabulate from fractions import Fraction import numpy as np

st.set_page_config(page_title="Simplex Solver", layout="centered")

st.title("Simplex Method Solver") st.markdown("This app solves linear programming problems using the Simplex Method.")

Global variables

array = [ ["Basis", "x(C1)", "y(C2)", "s(C3)", "t(C4)", "Z(C5)", "RHS(C6)", "Ratio"], ["s(R1)", "", "", 1, 0, 0, "", ""], ["t(R2)", "", "", 0, 1, 0, "", ""], ["Z(R3)", "", "", 0, 0, 1, "", ""] ] augument = [["a", "b", "c"], ["d", "e", "f"], ["g", "h", 0]] ans = ["", "", "", "", ""] c = 0

def transpose(): global augument augument = np.array(augument).T.tolist()

def store_data_in_table(): global array, augument for i in range(3): for k in range(3): j = [1, 2, 6] array[i + 1][j[k]] = augument[i][k]

def ratio(col): for i in range(2): try: array[i + 1][7] = Fraction(array[i + 1][6] / array[i + 1][col]).limit_denominator(10) except: array[i + 1][7] = "inf"

def solving(r, col): global array pivot = array[r][col] array[r][1:7] = [Fraction(val / pivot).limit_denominator(10) for val in array[r][1:7]] for i in range(1, 4): if i != r: factor = array[i][col] array[i][1:7] = [Fraction(array[i][j] - factor * array[r][j - 1]).limit_denominator(10) for j in range(1, 7)]

def solve_simplex(): global array, c, ans while array[3][1] < 0 or array[3][2] < 0: col = 1 if array[3][1] < array[3][2] else 2 ratio(col) c += 1 row = 1 if array[1][7] < array[2][7] else 2 solving(row, col) for i in range(2): array[i + 1][7] = "" for i in range(5): for j in range(1, 4): if array[j][i + 1] == 1 and all(array[k][i + 1] == 0 for k in [1, 2, 3] if k != j): ans[i] = array[j][6] break ans[i] = 0

def main(): global augument, array, ans choice = st.radio("Solving For", ["MAXIMUM", "MINIMUM"]) ch = 1 if choice == "MAXIMUM" else 2

with st.form("coeff_form"):
    st.subheader("Enter Coefficients")
    a = st.number_input("a (for ax + by ?= c)", value=1.0)
    b = st.number_input("b (for ax + by ?= c)", value=1.0)
    c1 = st.number_input("c (RHS)", value=4.0)

    d = st.number_input("d (for dx + ey ?= f)", value=1.0)
    e = st.number_input("e (for dx + ey ?= f)", value=1.0)
    f1 = st.number_input("f (RHS)", value=6.0)

    g = st.number_input("g (for Z = gx + hy)", value=3.0)
    h = st.number_input("h (for Z = gx + hy)", value=2.0)

    submitted = st.form_submit_button("Solve")

if submitted:
    augument = [
        [Fraction(a).limit_denominator(10), Fraction(b).limit_denominator(10), Fraction(c1).limit_denominator(10)],
        [Fraction(d).limit_denominator(10), Fraction(e).limit_denominator(10), Fraction(f1).limit_denominator(10)],
        [Fraction(-g).limit_denominator(10), Fraction(-h).limit_denominator(10), Fraction(0)]
    ]

    if ch == 2:
        transpose()
    store_data_in_table()
    solve_simplex()

    st.subheader("Final Simplex Table")
    st.text(tabulate(array, tablefmt="fancy_grid"))

    st.subheader("Optimal Solution")
    st.markdown(f"**x = {ans[0]}**")
    st.markdown(f"**y = {ans[1]}**")
    st.markdown(f"**Z {'Min' if ch == 2 else 'Max'} = {ans[4]}**")

if name == "main": main()

