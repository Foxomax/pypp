# Py++

## A strictly-typed language compiled to optimized bytecode, written in Python.

Py++ does not attempt to reinvent the wheel; instead, it aims to overcome the performance limitations of dynamic typing in modern Python.

By introducing a **strict static typing system**, Py++ eliminates runtime type inference overhead. In critical loops, this allows the virtual machine to completely bypass recurring dynamic type checks, resulting in a massive increase in execution speed.

### Compilation Roadmap
* **Phase 1 (Current):** Direct transpilation to Python source code, temporarily delegating bytecode generation to CPython and abstracting error handling via Source Mapping.
* **Phase 2 (Future):** Direct compilation to optimized bytecode (specialized `.pyc` for the Adaptive Interpreter or a proprietary binary format), bypassing the Python frontend to optimize native execution in the virtual machine.

---

## Syntax

Py++ utilizes a strongly-typed syntax with explicit delimiters and statement termination via semicolons (`;`).

```python
fn main() -> void {
    let hello: string = "HELLO";
    print(hello);
}