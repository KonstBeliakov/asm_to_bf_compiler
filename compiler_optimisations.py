
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
        text = f.read()
        print(len(text))
        text2 = remove_unnecessary_chars(text)
        print(f'Remove unnecessary chars: {len(text)} -> {len(text2)} (-{100 - len(text2) / len(text) * 100:.2f}%)')
        text3 = optimisation1(text2)
        print(f'Optimisation1: {len(text2)} -> {len(text3)} (-{100 - len(text3) / len(text2) * 100:.2f}%)')
        return optimisation1(remove_unnecessary_chars(f.read()))


if __name__ == '__main__':
    assert optimisation1("++>++>+++>++++<<<") == "++>++>+++>++++<<<"
    assert optimisation1("[][][]++----[><][-+][]++[[[]]][>><<+-]>>>[]<<+") == '>+'
    assert optimisation1("[][][]++----[><][-+][]++[[[]]][>><<+-]>>>[][]<<+") == '>+'

    optimize_code_from_file('ne_operator_example')