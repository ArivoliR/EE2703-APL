def calculate_growth_years(principal, rate, target, annual_deposit=0):
    years = 0
    cb = principal
    rate = rate / 100  
    while cb < target:
        if years > 1000:
            return -1
        cb += annual_deposit
        cb *= (1 + rate)
        years += 1

    return years


