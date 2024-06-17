import math

class PrimeNum:
    def __init__(self, number=None):
        self.number = number
    
    def inputnum(self):
        try:
            self.number = int(input("Enter a number: "))
        except Exception as e:
            print(e,"\nInvalid input. Please enter a valid integer.")
            self.inputnum()

    def prime(self):
        num = self.number
        if num == 1 or num == 0:
            return print("The entered number is not a prime number.")
        if num == 2:
            return print("The entered number is a prime number.")
        if num % 2 == 0:
            return print("The entered number is not a prime number.")

        pro = int(math.sqrt(num)) + 1
        for i in range(3, pro, 2):
            if num % i == 0:
                return print("The entered number is not a prime number.")

        return print("The entered number is a prime number.")

check = PrimeNum()
check.inputnum()
result = check.prime()