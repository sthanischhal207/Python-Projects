from tabulate import tabulate
from fractions import Fraction

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
c = 0
c = 0


def get_data(choice):
    global array, augument
    cnt = 0
    print(f"\n----------------------\n")
    for j in [
        f"FOR ax + by{'<' if choice == 1 else '>'}= c",
        f"FOR dx + ey {'<' if choice == 1 else '>'}=  f",
        "FOR Z= gx+hy",
    ]:
        print(f"\n{j}")
        for i in range(3):
            if cnt == 2 and i == 2:
                break
            while 1:
                try:
                    augument[cnt][i] = Fraction(
                        float(input(f"{augument[cnt][i]} = "))
                    ).limit_denominator(10)
                    break
                except ValueError:
                    print("INVALD INPUT ENTER A INTEGER")
                    continue

        cnt += 1

    print("\nFOR x <= 0")
    print("FOR y <= 0")

    if choice == 2:
        print("\n\nThe Augumented Form:")
        print_arugument()
        print("AFTER TRANSPOSING:")
        transpose()

    augument[2][0] = (-1) * augument[2][0]
    augument[2][1] = (-1) * augument[2][1]

    store_data_in_table()
    print("CONSIDERING s, t >= 0 AS SLACK VARIABLES")
    print("\n\nSET OF EQUATIONS ARE:")

    for i in range(3):
        k = ["s", "t", "Z"]
        print(f"{augument[i][0]}x+{augument[i][1]}y+{k[i]}={augument[i][2]}")


def store_data_in_table():
    global array, augument
    for i in range(3):
        for k in range(3):
            j = [1, 2, 6]
            array[i + 1][j[k]] = augument[i][k]


import numpy as np


def transpose():
    global augument
    augument = np.array(augument)  # Convert to a NumPy array
    augument = augument.T  # Transpose the array
    print_arugument()


def print_arugument():
    global augument
    print("-" * 18)
    for row in augument:
        print(f"|{float(row[0]):<5} {float(row[1]):<5} : {float(row[2]):<5}|")
    print("-" * 18)


def edit_data():
    global array
    while 1:
        try:
            array[int(input("ROW:"))][int(input("COLUMN:"))] = float(
                input("NEW INTEGER:")
            )
            break
        except ValueError:
            print("INVALD INPUT ENTER A INTEGER: ")
            continue


def solve_simplex_table():
    global array, c
    column = 0
    row = 0
    while array[3][1] < 0 or array[3][2] < 0:
        if array[3][1] < array[3][2]:
            column = 1
        else:
            column = 2
        ratio(column)
        c += 1
        print(f"\nSimplex Table {c}\n")
        print_array()
        print_ans(0)
        if array[1][7] < array[2][7]:
            row = 1
        else:
            row = 2
        print_data(row, column)
        solving(row, column)
    for i in range(2):
        array[i + 1][7] = ""
    c += 1
    print(f"\nSimplex Table {c}\n")
    print_array()
    print_ans(1)


def solving(r, col):
    global array
    if array[r][col] != 1:
        print(f"R{r}->R{r}*({Fraction(1/array[r][col]).limit_denominator(10)})")
        divide = array[r][col]
        for i in range(6):
            array[r][i + 1] = Fraction(array[r][i + 1] / divide).limit_denominator(10)
    for i in range(3):
        if i + 1 != r:
            divide_by = array[i + 1][col] / array[r][col]
            print(f"R{i+1}->R{i+1}-R{r}*({Fraction(divide_by).limit_denominator(10)})")
            for j in range(6):
                array[i + 1][j + 1] = Fraction(
                    array[i + 1][j + 1] - (array[r][j + 1] * divide_by)
                ).limit_denominator(10)


def print_data(r, c):
    global array
    print(
        f"\n\nPivot Column: C{c}\nDeparting Row:R{r}\nEntering Element: C{c} R{r} = {array[r][c]}\n"
    )


def ratio(col):
    global array
    for i in range(2):
        array[i + 1][7] = Fraction(
            array[i + 1][6] / array[i + 1][col]
        ).limit_denominator(10)
        array[i + 1][7] = Fraction(
            array[i + 1][6] / array[i + 1][col]
        ).limit_denominator(10)


ans = ["", "", "", "", ""]


def print_ans(command):
    global array, ans
    check = [1, 2, 3]
    cnt = 0
    for i in range(5):
        for j in range(3):
            if array[j + 1][i + 1] == 1:
                for k in check:
                    if array[k][i + 1] == 0:
                        cnt += 1
                if cnt == 2:
                    ans[i] = array[j + 1][6]
                    break
                ans[i] = 0
            else:
                ans[i] = 0
            cnt = 0

    print(f"\nx={ans[0]}\ny={ans[1]}\ns={ans[2]}\nt={ans[3]}\nZ Max={ans[4]}")
    if command == 0:
        print(
            f"\n-------IT IS NOT AN OPTIMAL SOLUTION AS IT CONTAIN NEG INTEGER IN ROW 3-------"
        )
    else:
        print(f"\n--------IT IS AN OPTIMAL SOLUTION--------")


def print_array():
    global array
    print(tabulate(array, tablefmt="fancy_grid"))


def main():
    while 1:
        try:
            choice = int(input("Solving For?\n1)MAXIMUM\n2)MINIMUM\n"))
            if choice in [1, 2]:
                get_data(choice)
                break
            else:
                print("CHOOSE 1 OR 2")
                continue

        except ValueError:
            print("CHOOSE EITHER 1 OR 2")
            continue
    print("\n\n-----STORED DATA-----")
    print_array()
    while (
        input(
            "\n\nEnter 'EDIT' or 'edit' To edit out any Given data, Else enter any key: "
        ).lower()
        == "edit"
    ):
        edit_data()
    solve_simplex_table()
    global ans
    if choice == 2:
        print(
            f"\n\n__FINAL ANSWER__\n Z {'Min' if choice == 2 else ' Max'} = {ans[-1]} at {f'({ans[0]},{ans[1]})' if choice == 1 else f'({array[3][3]},{array[3][4]})'})"
        )


if __name__ == "__main__":
    main()
