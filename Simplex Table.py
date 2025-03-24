from tabulate import tabulate
from fractions import Fraction
import numpy as np

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

# Counter for simplex iterations
c = 0


def get_data(choice):
    """
    Function to collect user input for the coefficients of the constraints and objective function.
    """
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
            if cnt == 2 and i == 2:  # Skip input for Z's RHS (already initialized to 0)
                break
            while True:
                try:
                    # Input coefficient and convert to a fraction
                    augument[cnt][i] = Fraction(
                        float(input(f"{augument[cnt][i]} = "))
                    ).limit_denominator(10)
                    break
                except ValueError:
                    print("INVALID INPUT. ENTER A NUMBER.")
                    continue
        cnt += 1

    print("\nFOR x <= 0")
    print("FOR y <= 0")

    if choice == 2:
        print("\n\nThe Augmented Form:")
        print_arugument()
        print("AFTER TRANSPOSING:")
        transpose()

    # Negate the coefficients of the objective function for maximization or minimization
    augument[2][0] = (-1) * augument[2][0]
    augument[2][1] = (-1) * augument[2][1]

    store_data_in_table()  # Store the collected data into the simplex table
    print("CONSIDERING s, t >= 0 AS SLACK VARIABLES")
    print("\n\nSET OF EQUATIONS ARE:")

    for i in range(3):
        k = ["s", "t", "Z"]
        print(f"{augument[i][0]}x+{augument[i][1]}y+{k[i]}={augument[i][2]}")


def store_data_in_table():
    """
    Function to populate the simplex table with the collected data.
    """
    global array, augument
    for i in range(3):  # Loop through each row of the augmented matrix
        for k in range(3):  # Map augmented matrix values to the simplex table
            j = [1, 2, 6]  # Columns in the simplex table corresponding to C1, C2, and RHS
            array[i + 1][j[k]] = augument[i][k]


def transpose():
    """
    Function to transpose the augmented matrix.
    """
    global augument
    augument = np.array(augument)  # Convert to a NumPy array
    augument = augument.T  # Transpose the array
    print_arugument()


def print_arugument():
    """
    Function to display the augmented matrix in a formatted manner.
    """
    global augument
    print("-" * 18)
    for row in augument:
        print(f"|{float(row[0]):<5} {float(row[1]):<5} : {float(row[2]):<5}|")
    print("-" * 18)


def edit_data():
    """
    Function to allow the user to edit specific entries in the simplex table.
    """
    global array
    while True:
        try:
            # Prompt user for row, column, and new value
            array[int(input("ROW:"))][int(input("COLUMN:"))] = float(
                input("NEW INTEGER:")
            )
            break
        except ValueError:
            print("INVALID INPUT. ENTER A NUMBER.")
            continue


def solve_simplex_table():
    """
    Function to iteratively solve the simplex table until an optimal solution is found.
    """
    global array, c
    column = 0
    row = 0
    while array[3][1] < 0 or array[3][2] < 0:  # Continue until all Z-row values are non-negative
        # Determine the pivot column
        if array[3][1] < array[3][2]:
            column = 1
        else:
            column = 2
        ratio(column)  # Calculate ratios for the current pivot column
        c += 1
        print(f"\nSimplex Table {c}\n")
        print_array()
        print_ans(0)
        # Determine the pivot row based on the minimum ratio
        if array[1][7] < array[2][7]:
            row = 1
        else:
            row = 2
        print_data(row, column)  # Display pivot information
        solving(row, column)  # Perform row operations to update the simplex table
    for i in range(2):
        array[i + 1][7] = ""  # Clear the ratio column after optimization
    c += 1
    print(f"\nSimplex Table {c}\n")
    print_array()
    print_ans(1)  # Display the final solution


def solving(r, col):
    """
    Function to perform row operations for the simplex method.
    """
    global array
    if array[r][col] != 1:  # Normalize the pivot element to 1
        print(f"R{r}->R{r}*({Fraction(1 / array[r][col]).limit_denominator(10)})")
        divide = array[r][col]
        for i in range(6):
            array[r][i + 1] = Fraction(array[r][i + 1] / divide).limit_denominator(10)
    for i in range(3):  # Eliminate other rows in the pivot column
        if i + 1 != r:
            divide_by = array[i + 1][col] / array[r][col]
            print(f"R{i+1}->R{i+1}-R{r}*({Fraction(divide_by).limit_denominator(10)})")
            for j in range(6):
                array[i + 1][j + 1] = Fraction(
                    array[i + 1][j + 1] - (array[r][j + 1] * divide_by)
                ).limit_denominator(10)


def print_data(r, c):
    """
    Function to display pivot information.
    """
    global array
    print(
        f"\n\nPivot Column: C{c}\nDeparting Row: R{r}\nEntering Element: C{c} R{r} = {array[r][c]}\n"
    )


def ratio(col):
    """
    Function to calculate the ratio column for the current pivot column.
    """
    global array
    for i in range(2):  # Calculate ratios for rows 1 and 2
        array[i + 1][7] = Fraction(
            array[i + 1][6] / array[i + 1][col]
        ).limit_denominator(10)


ans = ["", "", "", "", ""]


def print_ans(command):
    """
    Function to extract and display the current solution from the simplex table.
    """
    global array, ans
    cnt = 0
    for i in range(5):  # Iterate through columns C1 to C5
        for j in range(3):  # Check rows R1, R2, and R3
            if array[j + 1][i + 1] == 1:  # Identify basic variables
                for k in [1, 2, 3]:
                    if array[k][i + 1] == 0:
                        cnt += 1
                if cnt == 2:
                    ans[i] = array[j + 1][6]  # Assign RHS value to the variable
                    cnt = 0
                    break
                ans[i] = 0
            else:
                ans[i] = 0
            cnt = 0

    print(f"\nx={ans[0]}\ny={ans[1]}\ns={ans[2]}\nt={ans[3]}\nZ Max={ans[4]}")
    if command == 0:
        print(
            f"\n-------IT IS NOT AN OPTIMAL SOLUTION AS IT CONTAINS NEGATIVE VALUES IN ROW 3-------"
        )
    else:
        print(f"\n--------IT IS AN OPTIMAL SOLUTION--------")


def print_array():
    """
    Function to display the simplex table in a formatted grid.
    """
    global array
    print(tabulate(array, tablefmt="fancy_grid"))


def main():
    """
    Main function to execute the simplex method.
    """
    while True:
        try:
            # Prompt user to choose between maximization and minimization
            choice = int(input("Solving For?\n1) MAXIMUM\n2) MINIMUM\n"))
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
            "\n\nEnter 'EDIT' or 'edit' To Edit Any Given Data, Else Enter Any Key: "
        ).lower()
        == "edit"
    ):
        edit_data()
    solve_simplex_table()
    global ans
    if choice == 2:
        print(
            f"\n\n__FINAL ANSWER__\n Z {'Min' if choice == 2 else 'Max'} = {ans[-1]} at {f'({ans[0]},{ans[1]})' if choice == 1 else f'({array[3][3]},{array[3][4]})'})"
        )


if __name__ == "__main__":
    main()
