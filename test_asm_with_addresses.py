from asm_with_addresses import Compiler
from interpreter import run_brainfuck

test_number = 1


def _test(code, result, print_info=False):
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
        if print_info:
            print(compiled)
            print(t)
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

def test_while_1():
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

def test_while_2():
    code = '''
        set a 2
        while a
            set b 3
            while b
                set c a
                add c b
                out c
                sub b 1
            end
            sub a 1
        end
    '''
    _test(code, [5, 4, 3, 4, 3, 2])

def test_repeat_1():
    code = '''
        set a 5
        repeat 5
            out a
        end
    '''
    _test(code, [5, 5, 5, 5, 5])

def test_repeat_2():
    code = '''
        set a 5
        repeat a
            out a
        end
    '''
    _test(code, [5, 5, 5, 5, 5])

def test_if_1():
    code = '''
        set a 5
        if a
            out a
        end
        set a 0
        if a
            out a
        end
    '''
    _test(code, [5])

def test_if_2():
    code = '''
        set a 0
        set b 1
        if b
            set a 1
        end
        out a
    '''
    _test(code, [1])

def test_if_3():
    code = '''
        set a 1
        if a
            if a
                if a
                    out a
                end
                out a
            end
            out a
        end
        out a
    '''
    _test(code, [1, 1, 1, 1])

def test_not_1():
    code = '''
        set a 0
        not b a
        out a
        out b
        
        out r0
        out r1
        out r2
        out r3
    '''
    _test(code, [0, 1, 0, 0, 0, 0])

def test_not_2():
    code = '''    
        set a 39
        not b a
        out b
        out a
        
        out r0
        out r1
        out r2
        out r3
    '''
    _test(code, [0, 39, 0, 0, 0, 0])

def test_not_3():
    code = '''    
        not b 1
        out b
        
        not b 0
        out b
    '''
    _test(code, [0, 1])

def test_eq_1():
    code = '''
        set a 39
        set b 5
        set c 39
        
        eq d a b
        out d
        
        eq d a c
        out d
    '''
    _test(code, [0, 1])

def test_eq_2():
    code = '''
        set a 39

        eq d a 39
        out d

        eq d a 100
        out d
    '''
    _test(code, [1, 0])

def test_lt_1():
    code = '''
        set a 10
        set b 15
        lt c a b
        out c
        out a
        out b
        
        out r0
        out r1
        out r2
        out r3
        out r4
        out r5
        out r6
    '''
    _test(code, [1, 10, 15, 0, 0, 0, 0, 0, 0])

if __name__ == "__main__":
    # set, add, sub, out
    test1()
    test2()
    test3()
    test4()

    # while
    test_while_1()
    test_while_2()

    # repeat
    test_repeat_1()
    test_repeat_2()

    # if
    test_if_1()
    test_if_2()
    test_if_3()

    # not
    test_not_1()
    test_not_2()
    test_not_3()

    # eq
    test_eq_1()
    test_eq_2()

    # lt
    test_lt_1()
