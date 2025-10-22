import re

TOKEN_SPECIFICATIONS = [
    ('Keywords',
     r'\b(if|else|switch|case|default|while|for|do|break|continue|goto|int|short|long|float|double|void|bool|char|string|signed|unsigned|auto|const|static|new|delete|using|namespace|try|throw|catch|class|struct|union|public|private|protected|friend|this|virtual|return|true|false)\b'),
    ('Identifiers', r'[a-zA-Z_]\w*'),
    ('Numeric_constants', r'\b\d+(\.\d+)?([eE][+-]?\d+)?\b'),
    ('Operators',
     r'(\+\+|--|==|!=|<=|>=|<<=|>>=|\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<|>>|->|&&|\|\||::|[+\-*/%=&|^~<>!]=?|[<>]=?|[+\-*/%=&|^~<>!])'),
    ('Special_characters', r'[{}();]'),
    ('Character_constants', r"'.'"),
    ('Comments', r'//.*?$|/\*.*?\*/'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
]


class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"<{self.type}, {self.value}>"


def tokenize(code):
    tokens = []
    line_num = 1
    line_start = 0
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATIONS)
    get_token = re.compile(token_regex, re.MULTILINE | re.DOTALL).match

    pos = 0
    match = get_token(code)
    while match is not None:
        type = match.lastgroup
        value = match.group(type)
        if type == 'NewLine':
            line_start = match.end()
            line_num += 1
        elif type == 'Skip':
            pass
        elif type == 'Mismatch':
            print(f"Unexpected character {value!r} at line {line_num}")
        else:
            column = match.start() - line_start
            tokens.append(Token(type, value, line_num, column))
        pos = match.end()
        match = get_token(code, pos)
    return tokens


def main():
    while True:
        print("Enter your C++ code \n(press enter to compile):")
        Cpp_Code = ""
        while True:
            line = input()
            if line == "":
                break
            Cpp_Code += line + "\n"

        try:
            tokens = tokenize(Cpp_Code)

            print("\n--- Tokenized Output ---")
            for token in tokens:
                print(token)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
