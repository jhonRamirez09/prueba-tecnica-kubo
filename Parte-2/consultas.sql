-- =====================================================================
-- Prueba tecnica Kubo - Parte 2: Bases de datos y SQL
-- Esquema:
--   clientes(id, nombre, ciudad, creado_en)
--   productos(id, nombre, categoria, precio)
--   pedidos(id, cliente_id, fecha, estado)  -- 'PAGADO','PENDIENTE','CANCELADO'
--   detalle_pedido(pedido_id, producto_id, cantidad, precio_unitario)
--
-- Supuestos generales:
--   - Las ventas y el gasto se calculan solo con pedidos PAGADOS
--     (un pedido pendiente o cancelado no es dinero real).
--   - El monto de una linea se calcula con detalle_pedido.precio_unitario
--     (precio al momento de la venta), no con productos.precio, que puede
--     haber cambiado despues.
-- =====================================================================


-- ---------------------------------------------------------------------
-- 1. Clientes de Bogota registrados en 2025, ordenados por nombre
-- Uso un rango de fechas en vez de YEAR(creado_en) = 2025: funciona en
-- cualquier motor y permite usar un indice sobre creado_en.
-- ---------------------------------------------------------------------
SELECT id, nombre, ciudad, creado_en
FROM clientes
WHERE ciudad = 'Bogotá'
  AND creado_en >= '2025-01-01'
  AND creado_en <  '2026-01-01'
ORDER BY nombre;


-- ---------------------------------------------------------------------
-- 2. Total vendido por categoria, solo pedidos PAGADOS, de mayor a menor
-- ---------------------------------------------------------------------
SELECT p.categoria,
       SUM(d.cantidad * d.precio_unitario) AS total_vendido
FROM detalle_pedido d
JOIN pedidos   pe ON pe.id = d.pedido_id
JOIN productos p  ON p.id  = d.producto_id
WHERE pe.estado = 'PAGADO'
GROUP BY p.categoria
ORDER BY total_vendido DESC;


-- ---------------------------------------------------------------------
-- 3. Los 5 clientes con mas gasto acumulado
-- Agrupo por id y nombre (no solo nombre) porque dos clientes pueden
-- llamarse igual.
-- ---------------------------------------------------------------------
SELECT c.id, c.nombre,
       SUM(d.cantidad * d.precio_unitario) AS gasto_total
FROM clientes c
JOIN pedidos pe       ON pe.cliente_id = c.id
JOIN detalle_pedido d ON d.pedido_id   = pe.id
WHERE pe.estado = 'PAGADO'
GROUP BY c.id, c.nombre
ORDER BY gasto_total DESC
LIMIT 5;


-- ---------------------------------------------------------------------
-- 4. Clientes que nunca han hecho un pedido
-- LEFT JOIN conserva TODOS los clientes; a los que no tienen pedido les
-- quedan en NULL las columnas de pedidos, y el WHERE se queda con esos.
-- Con INNER JOIN solo quedan filas con pareja en ambas tablas, asi que
-- los clientes sin pedidos desaparecerian: justo lo contrario de lo
-- que se busca.
-- ---------------------------------------------------------------------
SELECT c.id, c.nombre
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
WHERE p.id IS NULL;


-- ---------------------------------------------------------------------
-- 5. Productos vendidos mas de 100 unidades en total
-- WHERE filtra filas antes de agrupar; HAVING filtra grupos despues,
-- cuando la suma ya existe.
-- ---------------------------------------------------------------------
SELECT pr.id, pr.nombre, SUM(d.cantidad) AS unidades_vendidas
FROM productos pr
JOIN detalle_pedido d ON d.producto_id = pr.id
JOIN pedidos pe       ON pe.id = d.pedido_id
WHERE pe.estado = 'PAGADO'
GROUP BY pr.id, pr.nombre
HAVING SUM(d.cantidad) > 100;


-- ---------------------------------------------------------------------
-- 6. Ticket promedio por pedido en cada mes de 2025 y cambio porcentual
--    frente al mes anterior (LAG)
-- Paso 1: total de cada pedido (el ticket es por pedido, no por linea;
--         promediar lineas haria pesar mas a los pedidos con mas productos).
-- Paso 2: promedio de esos totales por mes.
-- Paso 3: LAG trae el valor del mes anterior para calcular el cambio.
-- NULLIF evita dividir entre cero; el primer mes queda en NULL porque no
-- tiene mes anterior.
-- Nota: EXTRACT es SQL estandar (PostgreSQL/MySQL). En SQLite se usa
-- strftime('%m', fecha).
-- ---------------------------------------------------------------------
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
