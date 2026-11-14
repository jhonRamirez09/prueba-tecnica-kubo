# Prueba Técnica · Desarrollador Junior — Kubo

**Autor:** Jhon Ramírez

Solución de la prueba técnica, organizada en una carpeta por parte.

| Parte | Tema | Carpeta |
|---|---|---|
| 1 | Lógica y algoritmos (Python) | [`Parte-1`](Parte-1) |
| 2 | Bases de datos y SQL | [`Parte-2`](Parte-2) |
| 3 | API REST de Gestión de Tareas (FastAPI + SQLite) | [`Parte-3`](Parte-3) |
| 4 | JavaScript y frontend | [`Parte-4`](Parte-4) |
| 5 | Conceptos y Git | [`Parte-5`](Parte-5) |

## Uso de IA

Usé herramientas de IA como apoyo para aprender los conceptos, revisar errores y estructurar partes de la solución, sobre todo en la API, las pruebas y la documentación. Las decisiones están explicadas en cada README.

---

## Parte 1 · Lógica y algoritmos

| Ejercicio | Archivo | Idea | Tiempo | Espacio |
|---|---|---|---|---|
| 1.1 Two Sum | `Two_Sum.py` | Diccionario: por cada número busco si ya vi el que le falta para llegar al objetivo. | O(n) | O(n) |
| 1.2 Paréntesis válidos | `Parentesis.py` | Pila: abro → apilo; cierro → saco y comparo con su pareja. Al final la pila debe quedar vacía. | O(n) | O(n) |
| 1.3 Agrupar anagramas | `Agrupar_anagramas.py` | Diccionario cuya llave son las letras ordenadas de cada palabra. | O(n · k log k) | O(n · k) |
| 1.4 Subcadena sin repetidos | `Sub_Cadena.py` | Ventana deslizante: la cabeza avanza siempre; si la letra ya está en el set, la cola avanza soltando letras hasta quitar la repetida. | O(n) | O(k) |
| 1.5 Fusionar intervalos | `Intervalos.py` | Ordeno por inicio y comparo cada intervalo con el último guardado; si se solapa (`<=`), estiro el final con `max`. | O(n log n) | O(n) |
| 1.6 Caché LRU | `Cache_LRU.py` | Diccionario + lista doblemente enlazada con nodos centinela. | O(1) get / put | O(capacidad) |
| 1.7 Rotar matriz | `Matriz.py` | In-place: transponer y luego invertir cada fila. | O(n²) | O(1) |

*n = cantidad de elementos; k = largo de la palabra más larga (en 1.4, k = cantidad de caracteres distintos).*

## Parte 2 · SQL

Las 6 consultas, los supuestos y la teoría (índices, WHERE vs HAVING, transacciones y ACID) están en [`Parte-2/README.md`](Parte-2/README.md). Las consultas listas para ejecutar están en [`Parte-2/consultas.sql`](Parte-2/consultas.sql).

## Parte 3 · API REST

Instalación, ejecución, ejemplos curl, pruebas y decisiones en [`Parte-3/README.md`](Parte-3/README.md).

Resumen:

```bash
cd Parte-3
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload      # Swagger en http://127.0.0.1:8000/docs
pytest                             # 13 pruebas
```

## Parte 4 · JavaScript

Event loop, `debounce` y corrección del código con XSS en [`Parte-4/README.md`](Parte-4/README.md).

## Parte 5 · Conceptos

POO, SOLID, estructuras de datos, REST, JWT, inyección SQL, pruebas y Git en [`Parte-5/README.md`](Parte-5/README.md).
