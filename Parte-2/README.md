# Parte 2 · Bases de datos y SQL

## Esquema

```
clientes(id, nombre, ciudad, creado_en)
productos(id, nombre, categoria, precio)
pedidos(id, cliente_id, fecha, estado)   -- 'PAGADO', 'PENDIENTE', 'CANCELADO'
detalle_pedido(pedido_id, producto_id, cantidad, precio_unitario)
```

## Supuestos

- Las ventas y el gasto se calculan solo con pedidos **PAGADOS**, porque un pedido pendiente o cancelado no es dinero real.
- El monto de cada línea se calcula con `detalle_pedido.precio_unitario` (el precio al momento de la venta) y no con `productos.precio`, que puede haber cambiado después.
- Las consultas usan SQL estándar. La única diferencia con SQLite está en la consulta 6 (`EXTRACT`), y está indicada ahí.

Todas las consultas están también en [`consultas.sql`](consultas.sql), listas para ejecutar.

---

## Consultas

### 1. Clientes de Bogotá registrados en 2025, ordenados por nombre

```sql
SELECT id, nombre, ciudad, creado_en
FROM clientes
WHERE ciudad = 'Bogotá'
  AND creado_en >= '2025-01-01'
  AND creado_en <  '2026-01-01'
ORDER BY nombre;
```

Uso un rango de fechas en vez de `YEAR(creado_en) = 2025`. Así funciona en cualquier motor y permite usar un índice sobre `creado_en`. El límite `< '2026-01-01'` incluye todo el 31 de diciembre, aunque la fecha tenga hora.

### 2. Total vendido por categoría, solo pedidos PAGADOS, de mayor a menor

```sql
SELECT p.categoria,
       SUM(d.cantidad * d.precio_unitario) AS total_vendido
FROM detalle_pedido d
JOIN pedidos   pe ON pe.id = d.pedido_id
JOIN productos p  ON p.id  = d.producto_id
WHERE pe.estado = 'PAGADO'
GROUP BY p.categoria
ORDER BY total_vendido DESC;
```

Une cada línea vendida con su pedido (para saber el estado) y con su producto (para saber la categoría). Después agrupa por categoría y suma.

### 3. Los 5 clientes con más gasto acumulado

```sql
SELECT c.id, c.nombre,
       SUM(d.cantidad * d.precio_unitario) AS gasto_total
FROM clientes c
JOIN pedidos pe       ON pe.cliente_id = c.id
JOIN detalle_pedido d ON d.pedido_id   = pe.id
WHERE pe.estado = 'PAGADO'
GROUP BY c.id, c.nombre
ORDER BY gasto_total DESC
LIMIT 5;
```

Agrupo por `id` y `nombre`, y no solo por `nombre`, porque dos clientes pueden llamarse igual.

### 4. Clientes que nunca han hecho un pedido

```sql
SELECT c.id, c.nombre
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
WHERE p.id IS NULL;
```

**¿Por qué LEFT JOIN y no INNER JOIN?**
`LEFT JOIN` conserva **todos** los clientes. A los que no tienen pedidos les quedan en `NULL` las columnas de `pedidos`, y el `WHERE p.id IS NULL` se queda justo con esos.
Con `INNER JOIN` solo quedan las filas que tienen pareja en las dos tablas. Los clientes sin pedidos desaparecerían, que es lo contrario de lo que se busca.

Se usa `IS NULL` y no `= NULL`, porque cualquier comparación con `NULL` usando `=` nunca da verdadero.

### 5. Productos vendidos más de 100 unidades en total

```sql
SELECT pr.id, pr.nombre, SUM(d.cantidad) AS unidades_vendidas
FROM productos pr
JOIN detalle_pedido d ON d.producto_id = pr.id
JOIN pedidos pe       ON pe.id = d.pedido_id
WHERE pe.estado = 'PAGADO'
GROUP BY pr.id, pr.nombre
HAVING SUM(d.cantidad) > 100;
```

El `WHERE` filtra filas **antes** de agrupar (solo pedidos pagados). El `HAVING` filtra grupos **después** de agrupar, cuando la suma ya existe. Por eso la condición `> 100` no puede ir en el `WHERE`.

### 6. Ticket promedio por mes de 2025 y cambio porcentual frente al mes anterior

```sql
WITH total_por_pedido AS (
    SELECT pe.id, pe.fecha,
           SUM(d.cantidad * d.precio_unitario) AS total
    FROM pedidos pe
    JOIN detalle_pedido d ON d.pedido_id = pe.id
    WHERE pe.estado = 'PAGADO'
      AND pe.fecha >= '2025-01-01'
      AND pe.fecha <  '2026-01-01'
    GROUP BY pe.id, pe.fecha
),
por_mes AS (
    SELECT EXTRACT(MONTH FROM fecha) AS mes,
           AVG(total) AS ticket_promedio
    FROM total_por_pedido
    GROUP BY EXTRACT(MONTH FROM fecha)
)
SELECT mes,
       ROUND(ticket_promedio, 2) AS ticket_promedio,
       ROUND(LAG(ticket_promedio) OVER (ORDER BY mes), 2) AS mes_anterior,
       ROUND(100.0 * (ticket_promedio - LAG(ticket_promedio) OVER (ORDER BY mes))
             / NULLIF(LAG(ticket_promedio) OVER (ORDER BY mes), 0), 2) AS cambio_pct
FROM por_mes
ORDER BY mes;
```

Se resuelve en tres pasos:

1. **`total_por_pedido`**: calcula el total de cada pedido. El ticket promedio es el promedio **por pedido**, no por línea; si se promediaran las líneas, los pedidos con más productos pesarían más.
2. **`por_mes`**: promedia esos totales por mes.
3. **`LAG(...) OVER (ORDER BY mes)`**: trae el valor del mes anterior para calcular el cambio: `(mes actual − mes anterior) / mes anterior × 100`.

`NULLIF(..., 0)` evita dividir entre cero. El primer mes queda en `NULL` porque no tiene mes anterior.

> En SQLite no existe `EXTRACT`; se reemplaza por `strftime('%m', fecha)`.

---

## Teoría

### ¿Qué es un índice y cuándo puede perjudicar?

Un índice es como el índice de un libro: en vez de leer todas las páginas para encontrar un tema, vas directo a la página correcta. La base de datos lo usa para encontrar filas rápido en `WHERE`, `JOIN` y `ORDER BY` sin recorrer toda la tabla.

Puede perjudicar cuando:

- Cada `INSERT`, `UPDATE` o `DELETE` también tiene que actualizar el índice, así que la escritura se vuelve más lenta.
- Ocupa espacio en disco.
- En tablas pequeñas, o en columnas con pocos valores distintos (por ejemplo, `estado`, con solo 3 opciones), casi no ayuda.
- Si se aplica una función a la columna, como `YEAR(fecha)`, muchos motores no pueden usarlo. Por eso la consulta 1 usa un rango de fechas.

### Diferencia entre WHERE y HAVING

|                                  | WHERE                     | HAVING                       |
| -------------------------------- | ------------------------- | ---------------------------- |
| Qué filtra                       | Filas                     | Grupos                       |
| Cuándo                           | Antes de agrupar          | Después de agrupar           |
| Puede usar `SUM`, `COUNT`, `AVG` | No                        | Sí                           |
| Ejemplo                          | `WHERE estado = 'PAGADO'` | `HAVING SUM(cantidad) > 100` |

### ¿Qué es una transacción?

Es un grupo de operaciones que se ejecutan **todas o ninguna**.
Ejemplo: una transferencia resta dinero de una cuenta y lo suma a otra. Si la segunda operación falla, se deshace la primera (`ROLLBACK`). Si todo sale bien, se confirma (`COMMIT`).

### ¿Qué significa ACID?

- **A – Atomicidad:** todo o nada. Si una parte falla, no queda nada a medias.
- **C – Consistencia:** la base pasa de un estado válido a otro válido, respetando sus reglas (llaves foráneas, campos únicos, etc.).
- **I – Aislamiento:** dos transacciones al mismo tiempo no se pisan; cada una trabaja como si estuviera sola.
- **D – Durabilidad:** lo confirmado con `COMMIT` no se pierde, aunque se vaya la luz justo después.
