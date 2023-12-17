import ply.lex as lex
import sys
# Define the tokens
tokens = (
    'ID',              # 标识符
    'NUMBER',          # 数字
    'STRING',          # 字符串
    'ASSIGN',          # 赋值
    'UNARY_OP',        # 单目运算
    'BINARY_OP',       # 双目运算
    'COMPARISON_OP',   # 比较运算
    'AND_OP',          # 且
    'OR_OP',           # 或
    'NO_OP',           # 非
    'SEMICOLON',       # 分号
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
ASSIGN = r'>>=|<<=|\+=|-=|\*=|/=|%=|&=|\^=|\|='
t_UNARY_OP = r'--|\+\+'
t_BINARY_OP = r'<<|>>'
t_COMPARISON_OP = r'<=|>=|==|!=|<|>'
t_AND_OP = r'&&'
t_OR_OP = r'\|\|'
t_NO_OP = r'!'


# 变量名、函数名等标识符，除去保留字
def t_ID(token):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    token.type = reversed.get(token.value, 'ID')
    return token

# 整数，十六进制证书，浮点数
def t_NUMBER(token):
    r'0[xX][0-9a-fA-F]+|\d+\.\d+|\d+'
    if token.value.startswith('0x'):
        token.value = int(token.value, 16)
    elif '.' in token.value:
        token.value = float(token.value)
    else:
        token.value = int(token.value)
    return token

def t_STRING(token):
    r'\"[^"\n]*\"'
    token.value = token.value[1:-1]  # 去除双引号，保留字符串内容
    return token

def t_ANNOTATION(token):
    r'//[^\n]*'
    pass
# Add more token definitions here

# 过滤空格换行
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

