def checkprime(N):
    for i in range(2, round(N**(1/2)+1)): 
        if N % i == 0:
            return False;
            break
    return True

def primesum(N):
    sum = 0
    for i in range(2, N+1):
        if checkprime(i):
            sum += i
    return sum
