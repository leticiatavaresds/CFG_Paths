def compute_gcd():

    x, y = input()
    if x > y:
        small = y
    else:
        small = x
    for i in range(1, small+1):
        if((x % i == 0) and (y % i == 0)):
            gcd = i

    return gcd
    
compute_gcd()





