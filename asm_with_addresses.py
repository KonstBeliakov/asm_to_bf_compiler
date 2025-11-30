import re

from interpreter import run_brainfuck


class Compiler:
    def __init__(self):
        self.current_address = 0
        self.registers = 10
        self.variables = {f'r{i}': (self.registers - i - 1) for i in range(self.registers)}
        self.used_ptr = self.registers  # first 10 memory cells are reserved as registers
        self.code = ''
        self.cycle_address_stack = []

    def ensure_varname(self, varname: str):
        if varname not in self.variables:
            self.variables[varname] = self.used_ptr
            self.used_ptr += 1

    def goto(self, varname: str):
        self.ensure_varname(varname)
        new_addr = self.variables[varname]
        mov = new_addr - self.current_address
        if mov > 0:
            self.code += '>' * mov
        else:
            self.code += '<' * (-mov)
        self.current_address = new_addr

    def seti(self, varname: str, n: int):
        self.goto(varname)
        self.code += '[-]'
        self.addi(varname, n)

    def input(self, varname: str):
        self.goto(varname)
        self.code += ','

    def outi(self, n: int):
        self.seti('r0', n)
        self.out('r0')
        self.seti('r0', 0)

    def out(self, varname: str):
        self.goto(varname)
        self.code += '.'

    def addi(self, varname: str, n: int):
        self.goto(varname)
        if n > 0:
            self.code += '+' * n
        else:
            self.code += '-' * (-n)

    def subi(self, varname: str, n: int):
        self.addi(varname, -n)

    def add(self, varname: str, varname2: str):
        self.goto(varname2)
        self.code += '['
        self.code += '-'

        self.goto(varname)
        self.code += '+'

        self.goto('r0')
        self.code += '+'

        self.goto(varname2)
        self.code += ']'

        self.goto('r0')
        self.code += '['
        self.code += '-'

        self.goto(varname2)
        self.code += '+'

        self.goto('r0')
        self.code += ']'

    def sub(self, varname: str, varname2: str):
        self.goto(varname2)
        self.code += '['
        self.code += '-'

        self.goto(varname)
        self.code += '-'

        self.goto('r0')
        self.code += '+'

        self.goto(varname2)
        self.code += ']'

        self.goto('r0')
        self.code += '['
        self.code += '-'

        self.goto(varname2)
        self.code += '+'

        self.goto('r0')
        self.code += ']'

    def set(self, varname: str, varname2: str):
        self.seti(varname, 0)
        self.add(varname, varname2)

    def while_begin(self, varname: str):
        self.goto(varname)
        self.code += '['
        self.cycle_address_stack.append(('while', varname))

    def end(self):
        if self.cycle_address_stack:
            op, args = self.cycle_address_stack.pop()
            if op == 'while':
                self.goto(args)
                self.code += ']'
            if op == 'if':
                self.if_end()
        else:
            raise RuntimeError("Unmatched end")

    def repeati_begin(self, n):
        cc = f'cycle_counter{len(self.cycle_address_stack)}'
        self.seti(cc, n)
        self.while_begin(cc)
        self.subi(cc, 1)

    def repeat(self, varname: str):
        cc = f'cycle_counter{len(self.cycle_address_stack)}'
        self.set(cc, varname)
        self.while_begin(cc)
        self.subi(cc, 1)

    def if_begin(self, varname: str):
        self.goto(varname)
        self.code += '['
        self.cycle_address_stack.append(('if', varname))

    def if_end(self):
        self.seti('r0', 0)
        self.code += ']'

    def not_op(self, varname: str, arg: str):
        self.set('r3', arg) # r3 r2 r1 r0 - tree empty cells in a row
        self.seti('r2', 1)
        self.goto('r3')
        self.code += '[>->]>[>>]<< <' # not [>->] could be replaced with goto
        self.set(varname, 'r2')
        self.seti('r2', 0) # last two lines should be replaced with mov
        self.seti('r3', 0)

    def noti_op(self, varname: str, arg: int):
        if arg:
            self.seti(varname, 0)
        else:
            self.seti(varname, 1)

    def eq(self, varname: str, arg1: str, arg2: str):
        self.set(varname, arg1)
        self.sub(varname, arg2)
        self.not_op(varname, varname)

    def eqi(self, varname: str, arg1: str, arg2: int):
        self.set(varname, arg1)
        self.subi(varname, arg2)
        self.not_op(varname, varname)

    def compile(self, asm: str, output_file=None) -> str:
        self.code = ""
        for line in asm.splitlines():
            match line.strip().split():
                case ('add', varname, arg):
                    if re.fullmatch(r'[+-]?\d+', arg):
                        self.addi(varname, int(arg))
                    else:
                        self.add(varname, arg)
                case ('sub', varname, arg):
                    if re.fullmatch(r'[+-]?\d+', arg):
                        self.subi(varname, int(arg))
                    else:
                        self.sub(varname, arg)
                case ('set', varname, arg):
                    if re.fullmatch(r'[+-]?\d+', arg):
                        self.seti(varname, int(arg))
                    else:
                        self.set(varname, arg)
                case ('in', varname):
                    self.input(varname)
                case ('out', arg):
                    if re.fullmatch(r'[+-]?\d+', arg):
                        self.outi(int(arg))
                    else:
                        self.out(arg)
                case ('while', varname):
                    self.while_begin(varname)
                case ('end',):
                    self.end()
                case ('repeat', arg):
                    if re.fullmatch(r'[+-]?\d+', arg):
                        self.repeati_begin(int(arg))
                    else:
                        self.repeat(arg)
                case ('if', varname):
                    self.if_begin(varname)
                case ('not', varname, arg):
                    if re.fullmatch(r'[+-]?\d+', arg):
                        self.noti_op(varname, int(arg))
                    else:
                        self.not_op(varname, arg)
                case ('eq', varname, arg1, arg2):
                    if re.fullmatch(r'[+-]?\d+', arg2):
                        self.eqi(varname, arg1, int(arg2))
                    else:
                        self.eq(varname, arg1, arg2)
                case _:
                    self.code += line + '\n'
        if output_file is not None:
            with open(output_file, "w") as f:
                f.write(self.code)
        return self.code
