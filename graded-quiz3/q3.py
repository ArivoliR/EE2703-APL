def isbn10_validator(isbn2):
    isbn = ""
    for i in isbn2:
        if i!="-":
            isbn+=i
    if len(isbn) not in [9, 10] or not all(i.isdigit() or i == 'X' for i in isbn):
        return None
    for i in isbn[:len(isbn)-1]:
        if i == 'X':
            return None

    if len(isbn) == 9:
        #total = sum((i + 1) * int(isbn[i]) for i in range(9))
        total = 0 
        for i in range(9):
            total += (i+1)*int(isbn[i])
        check_digit = total % 11
        return 'X' if check_digit == 10 else str(check_digit)
    
    if len(isbn) == 10:
        #total = sum((i + 1) * (10 if isbn[i] == 'X' else int(isbn[i])) for i in range(10))
        total = 0 
        for i in range(10):
            if isbn[i]=='X':
                total += (i+1)*10 
            else:
                total += (i+1)*int(isbn[i])
        return total % 11 == 0
    
    return None

# Test cases
print(isbn10_validator("007462542"))  # → "X"
print(isbn10_validator("0-7475-3269-9"))  # → True
print(isbn10_validator("0-7475-3269-X"))  # → False
print(isbn10_validator("abc123456"))  # → None
