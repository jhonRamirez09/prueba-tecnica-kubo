def parentesis_validos(cadena):
    pares = {")": "(", "]": "[", "}": "{"} 
    pila = []
    for simbolo in cadena:
        if simbolo not in pares:
            pila.append(simbolo)
        else:
         if len(pila) == 0:
            return False
         sacado = pila.pop()
         if sacado != pares[simbolo]:
            return False
    return len(pila) == 0


print(parentesis_validos("{[()]}"))
print(parentesis_validos("{[(])}")) 
print(parentesis_validos("(("))
