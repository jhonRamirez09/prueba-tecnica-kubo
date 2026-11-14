// 4.3 - Version corregida de cargarUsuarios()

async function cargarUsuarios() {
  const lista = document.getElementById("lista");

  try {
    const res = await fetch("/api/usuarios");          // 1. faltaba await

    if (!res.ok) {                                      // 2. respuesta no OK (404, 500...)
      throw new Error(`Error HTTP ${res.status}`);
    }

    const datos = await res.json();                     // 1. tambien faltaba await

    lista.innerHTML = "";                               // limpio la lista antes de llenarla
    datos.forEach((u) => {
      const li = document.createElement("li");
      li.textContent = u.nombre;                        // 4. textContent en vez de innerHTML (evita XSS)
      lista.appendChild(li);
    });
  } catch (error) {                                     // 3. manejo de errores
    console.error("No se pudieron cargar los usuarios:", error);
    lista.textContent = "No se pudieron cargar los usuarios.";
  }
}

cargarUsuarios();
