import ply.lex as lex
import sys
# Define the tokens
tokens = (
    'ID',   # 标识符
    'NUMBER',    # 数字
    'STRING',   # 字符串
    'OP',   # 运算符
    'SEMICOLON',    # 分号
    # todo
)
reversed = {
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'void': 'VOID',
    'double': 'DOUBLE',
    'long': 'LONG',
    'const': 'CONST',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'do': 'DO',
    'return': 'RETURN',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'include': 'INCLUDE',
    'false': 'FALSE',
    'true': 'TRUE',
    # todo
}

tokens += tuple(reversed.values())

t_SEMICOLON = r';'

# Define the regular expressions for each token
def t_ID(token):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    token.type = reversed.get(token.value, 'ID')
    return token

def t_CONST(token):
    r'\d+'
    token.value = int(token.value)
    return token

def t_ANNOTATION(token):
    r'//[^\n]*'
    pass
# Add more token definitions here

# Define any ignored characters (whitespace, etc.)
t_ignore = ' \t\r\n'

# Define error handling rule
def t_error(token):
    print("Illegal character '%s'" % token.value[0])
    token.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
if __name__ == '__main__':
    file_path = "./huiwen.cpp"
    arguments = sys.argv[1:]
    if len(arguments) > 0:
        file_path = arguments[0]

        
    
    with open(file_path, "r") as file:
        data = file.read()

    lexer.input(data)
    with open("output.txt", "w") as file:
        while True:
            token = lexer.token()
            if not token:
                break
            print(token, file=file)

