# Py++

## A strictly-typed language compiled to optimized bytecode, written in Python.

Py++ no intenta reinventar la rueda, sino resolver las limitaciones de rendimiento del tipado dinámico en Python moderno.

Al introducir un sistema de **tipado estático estricto**, Py++ elimina el overhead de la inferencia de tipos en tiempo de ejecución. En bucles críticos, esto permite omitir por completo las comprobaciones dinámicas recurrentes, logrando un incremento masivo en la velocidad de ejecución.

### Roadmap de Compilación
* **Fase 1 (Actual):** Transpilación directa a código fuente de Python, delegando temporalmente la generación de bytecode a CPython y abstrayendo el manejo de errores mediante Source Mapping.
* **Fase 2 (Futuro):** Compilación directa a Bytecode optimizado (`.pyc` especializado para el *Adaptive Interpreter* o un formato binario propietario), puenteando el frontend de Python para optimizar la ejecución nativa en la máquina virtual.

---

## Sintaxis

Py++ utiliza una sintaxis fuertemente tipada con delimitadores explícitos y finalización de sentencias mediante punto y coma (`;`).

```python
def main() -> void {
    let hello: string = "HELLO";
    print(hello);
}