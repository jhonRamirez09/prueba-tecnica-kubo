def subcadena_mas_larga(texto):
    cuerpo = set()    # letras que tiene el gusano (sin repetidos)
    cola = 0          # donde empieza el gusano
    record = 0

    for cabeza in range(len(texto)):            # la cabeza SIEMPRE avanza
        letra = texto[cabeza]

        while letra in cuerpo:                  # mientras la letra nueva ya este en el cuerpo...
            cuerpo.remove(texto[cola])          # ...la cola suelta la letra de atras
            cola += 1                           # ...y avanza

        cuerpo.add(letra)                       # ahora si, se come la letra nueva
        record = max(record, cabeza - cola + 1) # tamano del gusano

    return record


casos = ["abcabcbb", "pwwkew", ""]
for caso in casos:
    print(f'"{caso}" ->', subcadena_mas_larga(caso))   # 3, 3, 0
