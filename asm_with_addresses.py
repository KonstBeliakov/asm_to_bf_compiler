import re

from interpreter import run_brainfuck


def count_leading_spaces(line: str) -> int:
    count = 0
    for i in line:
        if i == ' ':
            count += 1
        else:
            return count
    return count


class Compiler:
    def __init__(self):
        self.current_address = 0
        self.variables = {}
        self.used_ptr = 0  # first 10 memory cells are reserved as registers
        self.code = ''
        self.cycle_address_stack = []
        self.alloc_counter = 0

    def ensure_varname(self, varname: str):
        if varname not in self.variables:
            self.variables[varname] = self.used_ptr
            self.used_ptr += 1

    def allocate_memory(self, bytes: int):
        names = []
        for i in range(bytes):
            names.append(f'__t{self.alloc_counter}')
            self.alloc_counter += 1
            self.ensure_varname(names[-1])
        return names

    def free_vars(self, *args, zero=True):
        for varname in args:
            if varname in self.variables:
                if zero:
                    self.seti(varname, 0)
                del self.variables[varname]
            else:
                raise ValueError(f'Can\'t delete not existing variable {varname}')

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
        r0 = self.allocate_memory(1)[0]
        self.seti(r0, n)
        self.out(r0)
        self.free_vars(r0)
        #self.seti('r0', 0)

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
        r0 = self.allocate_memory(1)[0]

        self.goto(varname2)
        self.code += '['
        self.code += '-'

        self.goto(varname)
        self.code += '+'

        self.goto(r0)
        self.code += '+'

        self.goto(varname2)
        self.code += ']'

        self.goto(r0)
        self.code += '['
        self.code += '-'

        self.goto(varname2)
        self.code += '+'

        self.goto(r0)
        self.code += ']'

        self.free_vars(r0)

    def sub(self, varname: str, varname2: str):
        r0 = self.allocate_memory(1)[0]

        self.goto(varname2)
        self.code += '['
        self.code += '-'

        self.goto(varname)
        self.code += '-'

        self.goto(r0)
        self.code += '+'

        self.goto(varname2)
        self.code += ']'

        self.goto(r0)
        self.code += '['
        self.code += '-'

        self.goto(varname2)
        self.code += '+'

        self.goto(r0)
        self.code += ']'

        self.free_vars(r0)

    def set(self, varname: str, varname2: str):
        self.seti(varname, 0)
        self.add(varname, varname2)

    def while_begin(self, varname: str):
        self.goto(varname)
        self.code += '['
        self.cycle_address_stack.append(('while', varname))

    def end(self):
        if self.cycle_address_stack:
            op, arg = self.cycle_address_stack.pop()
            if op == 'while':
                self.goto(arg)
                self.code += ']'
            if op == 'if':
                self.if_end(arg)
        else:
            pass # lets just ignore it for now
            #raise RuntimeError("Unmatched end")

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
        r0 = self.allocate_memory(1)[0]
        self.set(r0, varname)
        self.goto(r0)
        self.code += '['
        self.cycle_address_stack.append(('if', r0))

    def if_end(self, r0):
        self.seti(r0, 0)
        self.goto(r0)
        self.code += ']'

    def not_op(self, varname: str, arg: str):
        #self.set('r3', arg)
        #self.seti('r2', 1)
        #self.goto('r3')
        #self.code += '[>->]>[>>]<< <' # not [>->] could be replaced with goto
        #self.set(varname, 'r2')
        #self.seti('r2', 0) # last two lines should be replaced with mov
        #self.seti('r3', 0)
        self.seti(varname, 1)
        self.if_begin(arg)
        self.seti(varname, 0)
        self.end()


    def noti_op(self, varname: str, arg: int):
        if arg:
            self.seti(varname, 0)
        else:
            self.seti(varname, 1)

    def eq(self, varname: str, arg1: str, arg2: str):
        r0 = self.allocate_memory(1)[0]
        self.set(r0, arg1)
        self.sub(r0, arg2)
        self.not_op(varname, r0)
        self.free_vars(r0)

    def eqi(self, varname: str, arg1: str, arg2: int):
        r0 = self.allocate_memory(1)[0]
        self.set(r0, arg1)
        self.subi(r0, arg2)
        self.not_op(varname, r0)
        self.free_vars(r0)

    def neq(self, varname: str, arg1: str, arg2: str):
        raise NotImplemented

    def lt(self, varname: str, arg1: str, arg2: str):
        r4, r5, r6 = self.allocate_memory(3)

        self.seti(varname, 0)
        self.set(r4, arg1)
        self.set(r5, arg2)
        self.while_begin(r5)
        self.not_op(r6, r4)
        self.if_begin(r6)
        self.seti(varname, 1)
        self.end()
        self.subi(r4, 1)
        self.subi(r5, 1)
        self.end()
        self.seti(r4, 0)
        self.seti(r5, 0)
        self.seti(r6, 0)

        self.free_vars(r4, r5, r6)

    def gt(self, varname: str, arg1: str, arg2: str):
        self.lt(varname, arg2, arg1)

    def leq(self, varname: str, arg1: str, arg2: str):
        raise NotImplemented

    def geq(self, varname: str, arg1: str, arg2: str):
        self.leq(varname, arg2, arg1)

    def or_op(self, varname: str, arg1: str, arg2: str):
        self.seti(varname, 0)
        self.if_begin(arg1)
        self.seti(varname, 1)
        self.end()
        self.if_begin(arg2)
        self.seti(varname, 1)
        self.end()

    def and_op(self, varname: str, arg1: str, arg2: str):
        self.seti(varname, 0)
        self.if_begin(arg1)
        self.if_begin(arg2)
        self.seti(varname, 1)
        self.end()
        self.end()

    def mul(self, varname: str, arg1: str, arg2: str):
        self.seti(varname, 0)
        self.repeat(arg1)
        self.add(varname, arg2)
        self.end()

    def muli(self, varname: str, arg1: str, arg2: int):
        self.seti(varname, 0)
        self.repeati_begin(arg2)
        self.add(varname, arg1)
        self.end()

    def compile(self, asm: str, output_file=None) -> str:
        self.code = ""
        asm += '\nend'
        indent_stack = []
        for line in asm.splitlines():
            if line.isspace():
                continue
            indent = count_leading_spaces(line)

            if not indent_stack or indent > indent_stack[-1]:
                indent_stack.append(indent)

            while indent_stack and indent < indent_stack[-1]:
                indent_stack.pop()
                self.end()

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
                case ('lt', varname, arg1, arg2):
                    self.lt(varname, arg1, arg2)
                case ('gt', varname, arg1, arg2):
                    self.gt(varname, arg1, arg2)
                case ('goto', varname):
                    self.goto(varname)
                case ('and', varname, arg1, arg2):
                    self.and_op(varname, arg1, arg2)
                case ('or', varname, arg1, arg2):
                    self.or_op(varname, arg1, arg2)
                case ('mul', varname, arg1, arg2):
                    if re.fullmatch(r'[+-]?\d+', arg2):
                        self.muli(varname, arg1, int(arg2))
                    else:
                        self.mul(varname, arg1, arg2)
                case _:
                    self.code += line + '\n'
        if output_file is not None:
            with open(output_file, "w") as f:
                f.write(self.code)
        return self.code
