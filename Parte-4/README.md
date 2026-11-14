# Parte 4 · JavaScript y frontend

## 4.1 ¿Qué imprime? Explica por qué

```js
console.log(1);
setTimeout(() => console.log(2), 0);
Promise.resolve().then(() => console.log(3));
(async () => { console.log(4); await null; console.log(5); })();
console.log(6);

for (var i = 0; i < 3; i++) setTimeout(() => console.log(i), 0);
console.log(typeof null, [] + {}, 0.1 + 0.2 === 0.3);
```

**Salida** (ejecutado como un solo script):

```
1
4
6
object [object Object] false
3
5
2
3
3
3
```

### Por qué: el event loop

JavaScript ejecuta primero todo el código **síncrono**. Después vacía la cola de **microtareas** (promesas y `await`) y, al final, toma las **macrotareas** (`setTimeout`), una por una.

| Paso | Qué pasa | Imprime |
|---|---|---|
| Síncrono | `console.log(1)` | `1` |
| Síncrono | `setTimeout(...2)` va a la cola de **macrotareas** | — |
| Síncrono | `.then(...3)` va a la cola de **microtareas** | — |
| Síncrono | La función `async` corre hasta el `await`: imprime 4. Lo que sigue (`log(5)`) queda como microtarea | `4` |
| Síncrono | `console.log(6)` | `6` |
| Síncrono | El `for` programa 3 `setTimeout` (macrotareas) | — |
| Síncrono | `typeof null`, `[] + {}` y `0.1 + 0.2 === 0.3` | `object [object Object] false` |
| Microtareas | Primero la promesa, luego lo que quedó después del `await` | `3`, `5` |
| Macrotareas | Los `setTimeout` en el orden en que se programaron | `2`, `3`, `3`, `3` |

### Los detalles de la última línea

- **`typeof null` → `"object"`**: es un error histórico de JavaScript que se mantuvo para no romper código viejo. `null` no es un objeto.
- **`[] + {}` → `"[object Object]"`**: el `+` convierte ambos lados a texto. `[]` se vuelve `""` y `{}` se vuelve `"[object Object]"`.
- **`0.1 + 0.2 === 0.3` → `false`**: los decimales se guardan en binario y no son exactos. `0.1 + 0.2` da `0.30000000000000004`. Para comparar decimales se usa un margen: `Math.abs(a - b) < Number.EPSILON`.

### ¿Por qué el `for` imprime `3, 3, 3` y no `0, 1, 2`?

`var` tiene alcance de **función**, no de bloque: las tres funciones del `setTimeout` comparten **la misma** variable `i`. Cuando por fin se ejecutan, el ciclo ya terminó e `i` vale 3.

Con `let`, cada vuelta del ciclo tiene su propia `i`, y sí imprime `0, 1, 2`:

```js
for (let i = 0; i < 3; i++) setTimeout(() => console.log(i), 0);
```

---

## 4.2 `debounce(fn, ms)`

Código en [`debounce.js`](debounce.js).

```js
function debounce(fn, ms) {
  let temporizador;
  return function (...args) {
    clearTimeout(temporizador);
    temporizador = setTimeout(() => fn.apply(this, args), ms);
  };
}
```

**Cómo funciona:** cada vez que llaman a la función, se cancela la ejecución que estaba esperando y el reloj vuelve a empezar. `fn` solo se ejecuta cuando pasan `ms` milisegundos **sin llamadas nuevas**.

**Situación real: un buscador.** Si el usuario escribe "tareas", sin debounce se harían 6 peticiones al servidor, una por cada letra. Con `debounce(buscar, 300)` se hace **una sola**, cuando deja de escribir durante 300 ms. También se usa al redimensionar la ventana, para recalcular el diseño solo cuando el usuario termina de arrastrar.

Prueba: `node debounce.js` imprime solo `c`, aunque la función se llamó con `a`, `b` y `c`.

---

## 4.3 Encuentra y corrige los 4 errores

Código corregido en [`cargarUsuarios.js`](cargarUsuarios.js).

**Original:**

```js
async function cargarUsuarios() {
    const res = fetch("/api/usuarios");
    const datos = res.json();
    const lista = document.getElementById("lista");
    datos.forEach(u => {
       lista.innerHTML += "<li>" + u.nombre + "</li>";
    });
}
cargarUsuarios();
```

| # | Error | Por qué falla | Corrección |
|---|---|---|---|
| 1 | **Falta `await`** en `fetch` y en `res.json()` | `fetch` devuelve una promesa, no la respuesta. `res.json` no existe en una promesa y explota. | `await fetch(...)` y `await res.json()` |
| 2 | **No revisa si la respuesta es OK** | `fetch` no lanza error con un 404 o un 500; el código seguiría con datos de error. | `if (!res.ok) throw new Error(...)` |
| 3 | **No hay manejo de errores** | Si se cae la red, la promesa se rechaza y el usuario no ve nada. | `try { ... } catch (error) { ... }` y mostrar un mensaje |
| 4 | **Riesgo de XSS con `innerHTML`** | Si un nombre fuera `<img src=x onerror="robarDatos()">`, el navegador ejecutaría ese código. | Crear el `<li>` con `createElement` y usar `textContent`, que trata todo como texto |

**Corregido:**

```js
async function cargarUsuarios() {
  const lista = document.getElementById("lista");

  try {
    const res = await fetch("/api/usuarios");
    if (!res.ok) {
      throw new Error(`Error HTTP ${res.status}`);
    }
    const datos = await res.json();

    lista.innerHTML = "";
    datos.forEach((u) => {
      const li = document.createElement("li");
      li.textContent = u.nombre;
      lista.appendChild(li);
    });
  } catch (error) {
    console.error("No se pudieron cargar los usuarios:", error);
    lista.textContent = "No se pudieron cargar los usuarios.";
  }
}

cargarUsuarios();
```

Además, construir el HTML con `innerHTML +=` dentro del ciclo vuelve a dibujar toda la lista en cada vuelta. Con `appendChild` solo se agrega el elemento nuevo.
