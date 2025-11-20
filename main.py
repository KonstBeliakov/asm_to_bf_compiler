from interpreter import run_brainfuck

example1 = ',+.+.+.'

def ptr(offset: int):
    if offset > 0:
        return '>' * offset + f" # ptr {offset}\n"
    return '<' * (-offset) + f" # ptr _{-offset}\n"

def mov(offset: int):
    if offset > 0:
        return f'[-{">"*offset}+{"<"*offset}] # mov {offset}\n'
    return f'[-{"<"*(-offset)}+{">"*(-offset)}] # mov _{-offset}\n'

def asm_to_brainfuck(asm: str, output_file=None) -> str:
    code = ""
    for line in asm.splitlines():
        match line.split():
            case 'ptr', n:
                code += ptr(offset=int(n))
            case 'set', n:
                code += '[-]' + '+' * int(n) + f" # set {n}\n"
            case 'addi', n:
                code += '+' * int(n) + f"# addi {n}\n"
            case 'subi', n:
                code += '-' * int(n) + f"# subi {n}\n"
            case 'mov', offset:
                code += mov(int(offset))
            case 'swap', offset, empty_offset:
                offset, empty_offset = int(offset), int(empty_offset)
                code += (f'\nswap {offset} {empty_offset}\n' +
                         mov(empty_offset) +
                         ptr(offset) + mov(-offset) +
                         ptr(empty_offset - offset) + mov(offset - empty_offset) +
                         ptr(-empty_offset) + '\n')
            case 'add', b_off, e_off:
                b_off, e_off = int(b_off), int(e_off)
                code += (f'\n# add {b_off} {e_off}\n{mov(e_off)}{ptr(e_off)}'+
                    f'[\n\t-\n\t{ptr(b_off - e_off)}\t+\n\t{ptr(-b_off)}\t+\n\t{ptr(e_off)}]'+
                    f'\n{ptr(-e_off)}\n')
            case 'sub', b_off, e_off:
                b_off, e_off = int(b_off), int(e_off)
                code += (f'\n# sub {b_off} {e_off}\n{mov(e_off)}{ptr(e_off)}' +
                    f'[\n\t-\n\t{ptr(b_off - e_off)}\t-\n\t{ptr(-b_off)}\t+\n\t{ptr(e_off)}]' +
                    f'\n{ptr(-e_off)}\n')
            case _:
                code += line + '\n'
    if output_file is not None:
        with open(output_file, "w") as f:
            f.write(code)
    return code


test_number = 1
def test(code, result):
    global test_number
    compiled = asm_to_brainfuck(code)
    t = [ord(i) for i in run_brainfuck(compiled)]
    if t != result:
        print(f"Error: {t} != {result}")
        print(compiled)
        raise Exception("Test failed")
    else:
        print(f"Test passed {test_number}")
    test_number += 1

exaple1 = '''
+>++>+++>++++<<<
set 0
.
ptr 1
.
ptr -1
.
''' # [3, 0]
test(exaple1, [0, 2, 0])

example2 = '''
set 97
.
addi 4
.
subi 2
.
''' # a e c [97, 101, 99]
test(example2, [97, 101, 99])

example3 = '''
set 97
mov 3
ptr 3
addi 2
.
''' # c
test(example3, [99])

example4 = '''
set 98
>
set 100
<
swap 1 2
.>.
'''
test(example4, [100, 98])

example5 = '''
set 3
ptr 1
set 5
ptr -1
add 1 2
.>.>.
'''
test(example5, [3, 8, 0])


example6 = '''
set 3
ptr 1
set 5
ptr -1
sub 1 2
.>.>.
'''
test(example6, [3, 2, 0])


if __name__ == "__main__":
    code = asm_to_brainfuck(example6)
    print(code)
    result = run_brainfuck(code)
    print(result)
    print([ord(i) for i in result])
