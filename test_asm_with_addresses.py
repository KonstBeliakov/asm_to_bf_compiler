from asm_with_addresses import Compiler
from interpreter import run_brainfuck

test_number = 1


def _test(code, result):
    global test_number
    compiler = Compiler()
    compiled = compiler.compile(code)
    t = [ord(i) for i in run_brainfuck(compiled)]
    if t != result:
        print(f"Error: {t} != {result}")
        print(compiled)
        raise Exception("Test failed")
    else:
        print(f"Test passed {test_number}")
    test_number += 1


def test1():
    code = '''
        seti a 97
        out a
        addi a 5
        out a
    '''
    _test(code, [97, 102])

def test2():
    code = '''
        seti a 97
        seti b 5
        add a b
        out b
        out a
    '''
    _test(code, [5, 102])
