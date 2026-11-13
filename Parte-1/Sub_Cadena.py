def racha_mas_larga(gastos, limite):
    cola = 0          # donde empieza el gusano
    suma = 0          # lo que tiene el gusano en el cuerpo
    record = 0

    for cabeza in range(len(gastos)):       # la cabeza SIEMPRE avanza
        suma += gastos[cabeza]              # se come el dia nuevo

        while suma > limite:                # mientras el cuerpo no sea valido...
            suma -= gastos[cola]            # ...la cola suelta el dia de atras
            cola += 1                       # ...y avanza

        largo = cabeza - cola + 1           # tamano del gusano
        record = max(record, largo)

    return record

casos = ["abcabcbb", "pwwkew", ""]
print(racha_mas_larga(casos))