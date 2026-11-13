# Parte 5 · Conceptos y Git

## 1. ¿Cuáles son los 4 pilares de la POO?

| Pilar | Qué es | Ejemplo |
|---|---|---|
| **Encapsulamiento** | Protege los datos de una clase. | Atributos privados. |
| **Herencia** | Permite que una clase herede propiedades y métodos de otra. | `Perro` hereda de `Animal`. |
| **Polimorfismo** | Permite que un mismo método tenga diferentes comportamientos. | `Perro` hace "guau" y `Gato` hace "miau". |
| **Abstracción** | Oculta los detalles internos y muestra solo las funcionalidades esenciales. | Usar un cajero sin conocer su funcionamiento interno. |

---

## 2. Diferencia entre clase abstracta e interfaz

- **Clase abstracta:** permite compartir atributos y métodos entre clases.
- **Interfaz:** establece un contrato de métodos que las clases deben implementar.

Una clase puede implementar **varias interfaces**, pero normalmente solo puede heredar de **una clase**.

---

## 3. ¿Qué es SOLID? La S y la D con ejemplos

SOLID es un conjunto de cinco principios para desarrollar software organizado y fácil de mantener.

- **S – Responsabilidad única:** una clase debe tener una sola responsabilidad.
  *Ejemplo:* separar el registro de usuarios del envío de correos.
- **D – Inversión de dependencias:** las clases deben depender de abstracciones y no de implementaciones específicas.
  *Ejemplo:* usar una interfaz de notificaciones en lugar de depender directamente de una clase de correo.

---

## 4. Pila, cola y mapa hash

| Estructura | Cómo funciona | Búsqueda |
|---|---|---|
| **Pila (Stack)** | LIFO: el último en entrar es el primero en salir. | O(n) |
| **Cola (Queue)** | FIFO: el primero en entrar es el primero en salir. | O(n) |
| **Mapa hash (HashMap)** | Guarda la información en pares clave–valor. | O(1) promedio, O(n) en el peor caso |

---

## 5. REST: idempotencia, métodos y PUT vs PATCH

**Idempotente** significa que ejecutar una operación varias veces produce el mismo efecto final que ejecutarla una sola vez.

- Métodos idempotentes: `GET`, `PUT`, `DELETE`, `HEAD` y `OPTIONS`.
- `POST` **no** es idempotente: cada llamada puede crear un recurso nuevo.

| PUT | PATCH |
|---|---|
| Reemplaza el recurso completo. | Modifica el recurso parcialmente. |
| Idempotente. | Puede ser idempotente o no, según cómo se implemente. |

---

## 6. Autenticación vs autorización y JWT

- **Autenticación:** verifica **quién eres**.
- **Autorización:** determina **qué permisos tienes**.

**JWT:** es un token firmado que permite transmitir información entre aplicaciones y verificar que no fue alterada.

**Qué NO debe ir dentro:** contraseñas, claves privadas ni información sensible. Su contenido está codificado, pero **no cifrado** por defecto, así que cualquiera que tenga el token puede leerlo.

---

## 7. ¿Qué es la inyección SQL y cómo se previene?

Es un ataque en el que se introducen instrucciones SQL maliciosas para manipular una base de datos.

Se previene así:

- Usando **consultas parametrizadas**.
- Validando las entradas.
- Evitando concatenar directamente los datos del usuario en las consultas.

---

## 8. Pruebas unitarias vs de integración. ¿Qué es un mock?

- **Pruebas unitarias:** verifican una función o un componente individual.
- **Pruebas de integración:** comprueban que varios componentes funcionen correctamente juntos.
- **Mock:** objeto simulado que reemplaza una dependencia real durante una prueba.

---

## 9. Git

**Merge vs rebase**

- **Merge:** combina ramas conservando su historial.
- **Rebase:** reorganiza los commits para mantener un historial más lineal.

**¿Cómo deshacer el último commit ya subido?**

```bash
git revert HEAD
git push
```

`revert` crea un commit nuevo que deshace el anterior, sin reescribir el historial que otros ya descargaron.

**¿Cómo resolver un conflicto?**

1. Identificar los archivos afectados (`git status`).
2. Revisar los cambios de ambos lados.
3. Decidir qué código conservar.
4. Eliminar las marcas del conflicto (`<<<<<<<`, `=======`, `>>>>>>>`).
5. Finalizar la operación (`git add` y `git commit`).

---

## 10. Un bug difícil que resolví y cómo lo depuré

En un proyecto tuve un problema de conectividad entre dispositivos. Hice un diagnóstico revisando las direcciones IP, las conexiones físicas y la configuración de red. Usé herramientas como `ping` e `ipconfig` para identificar el origen del problema. Finalmente, corregí la configuración e hice pruebas para verificar que el servicio funcionara correctamente.