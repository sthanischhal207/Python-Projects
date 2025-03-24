num = {
    "add": {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
            "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
            "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
            "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
            "seventy": 70, "eighty": 80, "ninety": 90},
    "mult": {"hundred": 100, "thousand": 1000, "million": 1_000_000, "billion": 1_000_000_000,
             "trillion": 1_000_000_000_000}
}

def main():
    try:
        # Input: Get the number in words from the user, split into a list of words
        user_input = input("Enter the Number in string: ").lower().split()
        
        # Variables to track multiplier usage and group counts
        count = []  # Tracks how many multipliers are grouped together (e.g., "thousand million")
        previous_index = 0  # Tracks the index of the last multiplier in `mult_keys`
        cnt = 0  # Temporary counter for consecutive multipliers
        
        # List of multiplier keys, sorted by their magnitude
        mult_keys = list(num["mult"].keys())
        
        # First pass: Identify groups of multipliers
        for word in user_input:
            if word in num["mult"]:
                current_index = mult_keys.index(word)  # Find the index of the multiplier
                if previous_index > current_index:
                    # If the current multiplier is smaller than the previous one, finalize the group
                    count.append(cnt)
                    cnt = 0
                cnt += 1
                previous_index = current_index
        count.append(cnt)  # Append the last group count

        # Variables for calculating the final number
        x = 0  # Temporary sum for the current group
        total_sum = 0  # Final result
        c = 0  # Counter for consecutive multipliers in the current group
        co = 0  # Index for the `count` list
        
        # Second pass: Calculate the number based on the input words
        for word in user_input:
            if word in num["add"]:
                # Add the value of the word to the temporary sum
                x += num["add"][word]
            elif word in num["mult"]:
                # Multiply the temporary sum by the multiplier's value
                x *= num["mult"][word]
                c += 1
                # If the current group of multipliers is complete, add to the total sum
                if c == count[co]:
                    total_sum += x
                    c = 0  # Reset the multiplier counter
                    x = 0  # Reset the temporary sum
                    co += 1  # Move to the next group
        
        # Add any remaining value in `x` to the total sum
        total_sum += x
        
        # Output the final result formatted with commas
        print(f"{total_sum:,}")
    
    except ValueError as e:
        # Handle invalid input gracefully
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
