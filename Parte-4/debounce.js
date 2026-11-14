function debounce(fn, ms) {
  let temporizador; // guarda el setTimeout pendiente

  return function (...args) {
    clearTimeout(temporizador);              // cancelo la llamada que estaba esperando
    temporizador = setTimeout(() => {
      fn.apply(this, args);                  // ejecuto fn con los ultimos argumentos
    }, ms);
  };
}

// Prueba rapida en Node: solo debe imprimir "c"
const log = debounce((x) => console.log(x), 100);
log("a");
log("b");
log("c");

module.exports = { debounce };
