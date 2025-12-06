from test_asm_with_addresses import Compiler, run_brainfuck
from compiler_optimisations import optimize_code

filename = 'examples/guess_a_number'

with open(filename, 'r', encoding='utf-8') as file:
    code = file.read()

compiler = Compiler()
compiled = compiler.compile(code)
optimized = optimize_code(compiled)

run_brainfuck(compiled, live_run=True)