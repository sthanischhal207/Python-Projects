from tabulate import tabulate
from fractions import Fraction

array = [
    ["Basis", "x(C1)", "y(C2)", "s(C3)", "t(C4)", "Z(C5)", "RHS(C6)", "Ratio"],
    ["s(R1)", "", "", "", "", "", "", ""],
    ["t(R2)", "", "", "", "", "", "", ""],
    ["Z(R3)", "", "", "", "", "", "", ""],
]
c = 0


def get_data():
    global array
    print("\n\n----------FOR GIVEN TABLE----------\n")
    print_array()
    for i in range(3):
        print(f"\nEnter value for Row {i+1}:")
        for j in range(6):
            while 1:
                try:
                    array[i + 1][j + 1] = float(input(f"R{i+1} C{j+1}: "))
                    break
                except ValueError:
                    print("INVALD INPUT ENTER A NUMBER OR DECIMAL")
                    continue


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


def print_ans(command):
    global array
    ans = ["", "", "", "", ""]
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
                else:
                    ans[i] = 0
                cnt = 0
            else:
                if ans[i] == "":
                    ans[i] = 0
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
    get_data()
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


if __name__ == "__main__":
    main()
