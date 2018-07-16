from random import randint


def true_random(how_many):
    minimum = 0
    maximum = 9
    numZero =0
    numOne = 0
    numTwo = 0
    numThree = 0
    numFour = 0
    numFive = 0
    numSix = 0
    numSeven = 0
    numEight = 0
    numNine = 0

    for n in range(how_many):
        num = randint(minimum, maximum)
        if num == 0:
            numZero = numZero + 1
        elif num == 1:
            numOne = numOne + 1

        elif num == 2:
            numTwo = numTwo + 1
        elif num == 3:
            numThree = numThree + 1
        elif num == 4:
            numFour = numFour + 1   
        elif num == 5:
            numFive = numFive + 1
        elif num == 6:
            numSix = numSix + 1
        elif num == 7:
            numSeven = numSeven + 1
        elif num == 8:
            numEight = numEight + 1
        elif num == 9:
            numNine = numNine + 1

    return num
