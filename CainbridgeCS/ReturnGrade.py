Grade = "Fail"
Mark = 0
Reply = "y"

while Reply == "y":
    Mark = float(input("Enter your exam mark "))

    if Mark < 40:
        Grade = "Fail"
    elif Mark < 60:
        Grade = "Pass" 
    elif Mark < 80:
        Grade = "Merit"
    else:
        Grade = "Distiction"

    print("Your grade is: " + Grade)

    Reply = input("Enter another exam mark? y/n ")



