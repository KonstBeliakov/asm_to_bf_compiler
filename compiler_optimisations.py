
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


def optimize_code_from_file(filename: str) -> str:
    with open(filename, 'r') as f:
        optimize_code(f.read())


def optimize_code(code: str) -> str:
    print(len(code))
    code2 = remove_unnecessary_chars(code)
    print(f'Remove unnecessary chars: {len(code)} -> {len(code2)} (-{100 - len(code2) / len(code) * 100:.2f}%)')
    code3 = optimisation1(code2)
    print(f'Removing meaningless pairs of operations: {len(code2)} -> {len(code3)} (-{100 - len(code3) / len(code2) * 100:.2f}%)')
    return code3


if __name__ == '__main__':
    assert optimisation1("++>++>+++>++++<<<") == "++>++>+++>++++<<<"
    assert optimisation1("[][][]++----[><][-+][]++[[[]]][>><<+-]>>>[]<<+") == '>+'
    assert optimisation1("[][][]++----[><][-+][]++[[[]]][>><<+-]>>>[][]<<+") == '>+'

    optimize_code_from_file('ne_operator_example')