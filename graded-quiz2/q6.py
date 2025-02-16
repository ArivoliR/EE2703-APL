def checkprime(N):
    for i in range(2, round(N**(1/2)+1)): 
        if N % i == 0:
            return False;
            break
    return True

def primesum(n):
    sum = 0
    sieve = set(range(2,n+1))
    while sieve:
        prime = min(sieve)
        sum += prime
        sieve -= set(range(prime, n+1, prime))
    return sum

print(primesum(1000))
