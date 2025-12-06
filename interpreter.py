#!/usr/bin/env python3
"""
Простой интерпретатор Brainfuck.

Функции:
- run_brainfuck(code, inp="", cells=30000) -> output_str

CLI:
python bf_interpreter.py path/to/program.bf [--input "text"]
"""
from typing import Dict

def build_bracket_map(code: str) -> Dict[int, int]:
    """Возвращает соответствия между индексами '[' и ']' для быстрого перехода."""
    stack = []
    bm = {}
    for i, c in enumerate(code):
        if c == '[':
            stack.append(i)
        elif c == ']':
            if not stack:
                raise SyntaxError(f"Unmatched ']' at position {i}")
            j = stack.pop()
            bm[i] = j
            bm[j] = i
    if stack:
        raise SyntaxError(f"Unmatched '[' at position {stack[-1]}")
    return bm

def run_brainfuck(code: str, inp: str = "", cells: int = 30000, live_run=False) -> str:
    """
    Запустить Brainfuck-программу.
    - code: строка с кодом (все символы, не являющиеся командами, игнорируются).
    - inp: строка, используемая для команд ',' (последовательность символов).
    - cells: начальная длина ленты (при необходимости лента расширяется вправо).
    Возвращает собранный вывод как строку.
    """
    valid = set("<>+-.,[]")
    prog = [c for c in code if c in valid]

    bracket_map = build_bracket_map("".join(prog))

    tape = [0] * cells
    ptr = 0
    pc = 0  # program counter (индекс в prog)
    inp_pos = 0
    output_chars = []
    input_chars = ''

    while pc < len(prog):
        cmd = prog[pc]

        if cmd == '>':
            ptr += 1
            if ptr >= len(tape):
                tape.extend([0] * max(1024, len(tape)//2))  # динамическое расширение
        elif cmd == '<':
            if ptr == 0:
                raise IndexError("Pointer moved to negative index (underflow).")
            ptr -= 1
        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) & 0xFF  # 0-255 wrap
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) & 0xFF
        elif cmd == '.':
            if input_chars:
                print(chr(tape[ptr]), end='')
            output_chars.append(chr(tape[ptr]))
        elif cmd == ',':
            if live_run:
                print('AAAA')
                if not input_chars:
                    input_chars  += input() + '\n'
                c = input_chars[0]
                input_chars = input_chars[1:]
                tape[ptr] = ord(c) & 0xFF
            else:
                if inp_pos < len(inp):
                    tape[ptr] = ord(inp[inp_pos]) & 0xFF
                    inp_pos += 1
                else:
                    tape[ptr] = 0
        elif cmd == '[':
            if tape[ptr] == 0:
                pc = bracket_map[pc]
        elif cmd == ']':
            if tape[ptr] != 0:
                pc = bracket_map[pc]
        pc += 1

    return "".join(output_chars)


if __name__ == "__main__":
    import argparse, sys, pathlib

    parser = argparse.ArgumentParser(description="Brainfuck interpreter in Python")
    parser.add_argument("file", nargs="?", help="path to .bf file (if omitted, reads code from stdin)")
    parser.add_argument("--input", "-i", default="", help="input string to provide to ',' commands")
    parser.add_argument("--cells", "-c", type=int, default=30000, help="initial tape size (default 30000)")
    args = parser.parse_args()

    if args.file:
        p = pathlib.Path(args.file)
        if not p.exists():
            print(f"File not found: {args.file}", file=sys.stderr)
            sys.exit(2)
        code_text = p.read_text()
    else:
        print("Enter Brainfuck code (Ctrl-D to finish):")
        code_text = sys.stdin.read()

    try:
        out = run_brainfuck(code_text, inp=args.input, cells=args.cells)
    except (SyntaxError, IndexError) as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

    sys.stdout.write(out)
