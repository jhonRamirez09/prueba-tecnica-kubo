def fusionar_intervalos(intervalos):
    intervalos = sorted(intervalos, key=lambda x: x[0])   # ordenar por inicio
    resultado = []
    for inicio, fin in intervalos:
        if resultado and inicio <= resultado[-1][1]:     # ¿se solapa con el ultimo?
            resultado[-1][1] = max(resultado[-1][1],fin)              # estiro el final
        else:
            resultado.append([inicio, fin])                  # intervalo nuevo
    return resultado

print(fusionar_intervalos([[1,3],[8,10],[2,6],[15,18],[17,20]]))  # [[1,6],[8,10],[15,20]]
print(fusionar_intervalos([[1,4],[4,5]]))                         # [[1,5]]
print(fusionar_intervalos([[1,10],[2,3]]))                        # [[1,10]]