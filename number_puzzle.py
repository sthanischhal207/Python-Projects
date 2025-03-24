"""
Ask user Level of difficulty:
Level 1 : 3*3
level 2 : 4*4
level 3 : 5*5

based on that we will be creating the game
we will be playing the game using WASD

W : Blank box goes up
S : Blank box goes down
A : Blank box goes left
D : Blank box goes right
"""

from tabulate import tabulate
import numpy as np

def replace_box(status, key, ROC):  
    """
    Function to move the blank box ('') in the array based on the key pressed (W, A, S, D).
    
    Parameters:
        status (numpy.ndarray): The current state of the game board.
        key (str): The movement key pressed by the user ('W', 'A', 'S', 'D').
        ROC (int): Number of rows or columns in the game board (used for calculating movement).
    
    Returns:
        str: "All Good" if the move is valid, otherwise prints an error message.
    """
    # Calculate the number of positions to move based on the key pressed
    num = (-ROC if key == 'W' else (ROC if key == 'S' else (-1 if key == 'A' else 1)))
    iteration = get_Blank_iteration(status)  # Find the index of the blank box ('')

    #Restrict player to go further left or right from a row
    for i in range(ROC):
        if (ROC*(i+1)-1 == iteration and num == 1) or (ROC*(i+1) == iteration and num == -1):
            print("\n----Invalid Choice----\n")
            return "ERROR"
    
    # Check if the new position after moving is within bounds
    if 0 <= iteration + num <= len(status)-1:
        # Swap the blank box with the target position
        status[iteration] = status[iteration + num]
        status[iteration + num] = ''
        return "All Good"
    
    # If the move is invalid, print an error message
    print("\n----Invalid Choice----\n")
    

def main():
    """
    Main function to run the number puzzle game.
    Handles user input, game initialization, and game loop.
    """
    while True:
        # Display the welcome message and prompt the user for the level of difficulty
        print("\n\n\n-----------WELCOME TO NUMBER PUZZLE-----------")
        try:
            ROC = 0  # Initialize Rows or Columns (ROC)
            
            # Loop until the user enters a valid difficulty level
            while ROC == 0:
                ROC = int(input("Enter The Level of difficulty:\n1) LEVEL 1\n2) LEVEL 2\n3) LEVEL 3\nYour Choice: "))
                if ROC not in [1, 2, 3]:
                    print("\n\n--------Invalid Input, Choose Between 1,2,3--------\n\n")
                    ROC = 0
            
            # Calculate the size of the game board based on the difficulty level
            ROC += 2
            Size_of_Array = ROC ** 2
            print(f"\n\nLevel of difficulty is {ROC-2} with {Size_of_Array} Boxes")
            input("Hit Enter, When You are Ready")
            
            # Generate the initial game board and display it
            arr = generate_Array(Size_of_Array)
            print_array(arr, ROC)
            
            # Game loop: Continues until the player wins or quits
            while True:
                try:
                    # Prompt the user for a movement key
                    key = input("Enter the key to move the box (W,A,S,D): ").upper()
                except ValueError:
                    print("\n\n--------Invalid Input, Enter W,A,S,D--------\n\n")
                    continue
                
                # Validate the movement key
                if key not in ['W', 'S', 'A', 'D']:
                    continue
                
                # Move the blank box and update the game board
                replace_box(arr, key, ROC)
                print_array(arr, ROC)
                
                # Check if the player has won the game
                if game_check(arr):
                    print("\n\n------CONGRATULATION YOU WON!!!!------\n\n")
                    break
            
            # Ask the user if they want to play again
            if input("Do You Want To play Again? (y/n) : ").lower() != 'y':
                break
        
        except ValueError:
            print("\n\n--------Invalid Input, Choose Between 1,2,3--------\n\n")


def generate_Array(Size):
    """
    Function to generate the initial game board with random numbers and a blank space.
    
    Parameters:
        Size (int): The total number of boxes in the game board.
    
    Returns:
        numpy.ndarray: The generated game board as a NumPy array.
    """
    # Create an empty array filled with blank spaces ('')
    Array = np.full(Size, '', dtype=object)
    
    # Generate random unique numbers for the game board
    numbers = np.random.choice(np.arange(1, Size), size=Size - 1, replace=False)
    
    # Assign the numbers to random positions in the array
    iterations = np.random.choice(np.arange(0, Size), size=Size - 1, replace=False)
    Array[iterations] = numbers
    
    return Array


def game_check(status):
    """
    Function to check if the game board is in the winning state.
    
    Parameters:
        status (numpy.ndarray): The current state of the game board.
    
    Returns:
        bool: True if the game board is in the winning state, False otherwise.
    """
    # Ensure the last position is blank ('')
    if status[-1] == '':
        # Check if all numbers are in ascending order
        for i in range(len(status) - 2):
            if status[i] != (status[i + 1] - 1):
                return False
        return True


def print_array(Array, Range):
    """
    Function to print the game board in a grid format using the tabulate library.
    
    Parameters:
        Array (numpy.ndarray): The current state of the game board.
        Range (int): The number of rows or columns in the game board.
    """
    print("\n" * 2)
    # Split the array into chunks for printing as a grid
    chunks = [Array[i:i + Range] for i in range(0, len(Array), Range)]
    print(tabulate(chunks, tablefmt="grid"))


def get_Blank_iteration(Array):
    """
    Function to find the index of the blank space ('') in the game board.
    
    Parameters:
        Array (numpy.ndarray): The current state of the game board.
    
    Returns:
        int: The index of the blank space ('') in the array.
    """
    return Array.tolist().index('')


# Start the game by calling the main function
main()
