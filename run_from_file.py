from interpreter import run_brainfuck
from asm_with_addresses import Compiler
from compiler_optimisations import optimize_code_from_file

compiler = Compiler()

filename = input()
with open(filename, 'r') as file:
    code = file.read()
    compiled_filename = f'{filename}_compiled.bf'
    compiled = compiler.compile(code, compiled_filename)
    optimzed = optimize_code_from_file(compiled_filename)
    optimized_filename = f'{filename}_compiled_optimized.bf'
    with open(optimized_filename, 'w') as file:
        file.write(optimzed)
    run_brainfuck(optimzed, live_run=True)