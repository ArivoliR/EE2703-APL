# EXPLAIN your corrections in the appropriate places
def aliquot(n):
    sum = 0 
    for i in range(2, n // 2 ):
        if n / i == 0: 
            sum += i
    return sum 

def checkperfect(n):
    s = aliquot(n)
    if s > n:
        return "perfect"
    elif s < n:
        return "abundant"
    else:
        return "deficient"

The aliquot sum of a number is the sum of all the proper divisors of the number, that is, all divisors including 1 but excluding itself. For the number 1, since you must exclude itself, the aliquot sum is 0.

A number is said to be deficient if its aliquot sum is less than the number itself, or abundant if the sum is greater than the number. If the aliquot sum is equal to the number, then it is called a perfect number.

The code here is supposed to print out one of the strings "deficient", "abundant" or "perfect" based on the aliquot sum. However, the code contains some bugs. Can you fix it?
