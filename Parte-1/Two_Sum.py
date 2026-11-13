def two_sum(numeros,objetivo):
    libreta = {}
    for i, num in enumerate(numeros):
        falta = objetivo - num
        if falta in libreta:
            return[libreta[falta],i]
        libreta[num] = i
    return None



print(two_sum([2,7,11,15], 9))
print(two_sum([5,10,20,15], 30))