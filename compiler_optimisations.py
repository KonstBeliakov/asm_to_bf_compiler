import re

def remove_unnecessary_chars(code: str) -> str:
    new_code = ""
    for i in code:
        if i in ".,+-<>[]":
            new_code += i
    return new_code

def optimisation1(code: str) -> str:
    inv = {'+': '-', '-': '+', '>': '<', '<': '>', '[': ']', ']': '['}
    stack = []
    for ch in code:
        if stack and ch in inv and stack[-1] == inv[ch]:
            stack.pop()
        else:
            stack.append(ch)
    return ''.join(stack)

def optimisation2(code: str) -> str:
    result = []
    last = '#'
    count = 0

    for c in code + '#':
        if c == last:
            count += 1
        else:
            if last in '+-':
                count %= 256
                if count > 128:
                    count = 256 - count
                    last = '+' if last == '-' else '-'
            result.append(last * count)
            last = c
            count = 1

    return ''.join(result)


def optimize_code_from_file(filename: str) -> str:
    with open(filename, 'r') as f:
        optimize_code(f.read())


def optimize_code(code: str) -> str:
    print(len(code))
    code2 = remove_unnecessary_chars(code)
    print(f'Remove unnecessary chars: {len(code)} -> {len(code2)} (-{100 - len(code2) / len(code) * 100:.2f}%)')
    code3 = optimisation1(code2)
    print(f'Removing meaningless pairs of operations: {len(code2)} -> {len(code3)} (-{100 - len(code3) / len(code2) * 100:.2f}%)')
    code4 = optimisation2(code3)
    print(f'Replacing >128 consecutive "+" and >128 consecutive "-" {len(code3)} -> {len(code4)} (-{100 - len(code4) / len(code3) * 100:.2f}%)')
    return code4


if __name__ == '__main__':
    assert optimisation1("++>++>+++>++++<<<") == "++>++>+++>++++<<<"
    assert optimisation1("[][][]++----[><][-+][]++[[[]]][>><<+-]>>>[]<<+") == '>+'
    assert optimisation1("[][][]++----[><][-+][]++[[[]]][>><<+-]>>>[][]<<+") == '>+'
    assert optimisation2('+' * 258) == '++'
    assert optimisation2('-' * 255) == '+'

    optimize_code_from_file('ne_operator_example')