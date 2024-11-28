import pyfiglet

text = input("Please enter some text: ")

ascii_art = pyfiglet.figlet_format(text, font = "banner3-D" )

print(ascii_art)