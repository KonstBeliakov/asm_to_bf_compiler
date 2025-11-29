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
        set a 97
        out a
        add a 5
        out a
        out 39
    '''
    _test(code, [97, 102, 39])

def test2():
    code = '''
        set a 39
        set b 20
        out a
        out b
    '''
    _test(code, [39, 20])

def test3():
    code = '''
        set a 97
        set b a
        out a
        out b
    '''
    _test(code, [97, 97])

def test4():
    code = '''
        set a 97
        set b 5
        add a b
        out b
        out a
    '''
    _test(code, [5, 102])

def test5():
    code = '''
        set a 5
        set b 2
        while a
            out b
            out a
            add a -1
        end
    '''
    _test(code, [2, 5, 2, 4, 2, 3, 2, 2, 2, 1])

def test6():
    code = '''
        set a 5
        repeat 5
            out a
        end
    '''
    _test(code, [5, 5, 5, 5, 5])

def test7():
    code = '''
        set a 5
        repeat a
            out a
        end
    '''
    _test(code, [5, 5, 5, 5, 5])

if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
