number = float(input("Enter a number: "))

if number > 25:
    print("Error")
else:
    for i in range(int(number), 26):
        print(i)
