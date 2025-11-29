from interpreter import run_brainfuck


class Compiler:
    def __init__(self):
        self.current_address = 0
        self.variables = {}
        self.used_ptr = 10  # first 10 memory cells are reserved as registers
        self.code = ''

    def ensure_varname(self, varname: str):
        if varname not in self.variables:
            self.variables[varname] = self.used_ptr
            self.used_ptr += 1

    def goto(self, varname: str):
        self.ensure_varname(varname)
        new_addr = self.variables[varname]
        mov = new_addr - self.current_address
        if mov > 0:
            self.code += '+' * mov
        else:
            self.code += '-' * mov
        self.current_address = new_addr

    def seti(self, varname: str, n: int):
        self.goto(varname)
        self.code += '[-]'
        self.addi(varname, n)

    def input(self, varname: str):
        self.goto(varname)
        self.code += ','

    def out(self, varname: str):
        self.goto(varname)
        self.code += '.'

    def addi(self, varname: str, n: int):
        self.goto(varname)
        if n > 0:
            self.code += '+' * n + '\n'
        else:
            self.code += '-' * n + '\n'

    def subi(self, varname: str, n: int):
        self.addi(varname, -n)

    def add(self, varname: str, varname2: str):
        raise NotImplementedError()

    def sub(self, varname: str, varname2: str):
        raise NotImplementedError()

    def cp(self, varname: str, varname2: str):
        raise NotImplementedError()

    def compile(self, asm: str, output_file=None) -> str:
        self.code = ""
        for line in asm.splitlines():
            match line.strip().split():
                case ('seti', varname, n):
                    self.seti(varname, int(n))
                case('addi', varname, n):
                    self.addi(varname, int(n))
                case ('subi', varname, n):
                    self.subi(varname, int(n))
                case ('add', varname, varname2):
                    self.add(varname, varname2)
                case ('sub', varname, varname2):
                    self.sub(varname, varname2)
                case ('cp', varname, varname2):
                    self.cp(varname, varname2)
                case ('in', varname):
                    self.input(varname)
                case ('out', varname):
                    self.out(varname)
                case _:
                    self.code += line + '\n'
        if output_file is not None:
            with open(output_file, "w") as f:
                f.write(self.code)
        return self.code
