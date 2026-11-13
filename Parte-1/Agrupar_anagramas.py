palabras = ["eat","tea","tan","ate","nat","bat"]
grupos = {}

for palabra in palabras:
    llave = "".join(sorted(palabra))    # las fichas ordenadas (lo que hiciste en la tabla)

    if llave not in grupos:
        grupos[llave] = []
    grupos[llave].append(palabra)

resultado = list(grupos.values())    # pista: solo te sirve la parte derecha del diccionario
print(resultado)