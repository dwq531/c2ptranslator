import ply.yacc as yacc
from lex import tokens
# 程序由不同的声明组成，声明可以是变量声明或函数声明
def p_program(p):
    '''program : external_declaration program
               | external_declaration'''
    print("program->")

# 声明可以是函数声明和变量等声明
def p_external_declaration(p):
    '''external_declaration : function_declaration
                            | declaration_statement'''   
    print("external_declaration->")

# 函数声明：返回类型 声明 函数体 
def p_function_declaration(p):
    '''function_declaration : declaration_specifiers func_declarator compound_statement'''
    print("function_declaration->")

# 返回类型：（const） 类型
def p_declaration_specifiers(p):
    '''declaration_specifiers : CONST type_specifier
                              | type_specifier'''
    print("declaration_specifiers->",p[1])

# 类型
def p_type_specifier(p):
    '''type_specifier : VOID
                      | INT
                      | CHAR
                      | FLOAT
                      | DOUBLE
                      | LONG
                      | BOOL'''
    print("type_specifier->",p[1])

# 函数声明 : 指针 函数声明体
def p_func_declarator(p):
    '''func_declarator : ASTERISK direct_declarator 
                        | direct_declarator'''
    print("func_declarator->")

# 函数声明体 : 标识符(空或参数)
def p_direct_declarator(p):
    '''direct_declarator ::= ID PARENTHESES_LEFT parameter_list PARENTHESES_RIGHT
	                    | ID PARENTHESES_LEFT PARENTHESES_RIGHT
                        '''
    print("direct_declarator->",p[1])

# 参数列表 : 参数列表,参数声明 | 参数声明
def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter_declaration
                      | parameter_declaration'''
    print("parameter_list->")

# 参数声明 : 类型 参数声明体
def p_parameter_declaration(p):
    '''parameter_declaration : declaration_specifiers declarator'''
    print("parameter_declaration->")

# 参数声明体 : 指针 标识符 | 标识符[] | 标识符
def p_declarator(p):
    '''declarator : ID
                | ID SQUARE_BRACKETS_LEFT SQUARE_BRACKETS_RIGHT
                | ID SQUARE_BRACKETS_LEFT expression SQUARE_BRACKETS_RIGHT
                | ASTERISK ID'''
    print("declarator->",p[1])

# 函数体 : { (语句列表) }
def p_compound_statement(p):
    '''compound_statement : CURLY_BRACES_LEFT CURLY_BRACES_RIGHT
                          | CURLY_BRACES_LEFT statement_list CURLY_BRACES_RIGHT'''
    print("compound_statement->")

# 语句列表 : 语句列表 语句 | 语句
def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    print("statement_list->")

# 语句 : 声明 ｜ 函数 ｜ 表达式 ｜ 选择语句 ｜ 迭代语句 ｜ 跳转语句 | 赋值语句
def p_statement(p):
    '''statement : declaration_statement
                 | expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement
                 | assignment_statement'''

# 声明语句 : 声明 ;
def p_declaration_statement(p):
    '''declaration_statement : declaration SEMICOLON'''
    print("declaration_statement->")

# 声明 : 类型 标识符
def p_declaration(p):
    '''declaration : declaration_specifiers init_declarator_list'''
    print("declaration->")

# 初始化声明列表 : 初始化声明列表 , 初始化声明 | 初始化声明
def p_init_declarator_list(p):
    '''init_declarator_list : init_declarator_list COMMA init_declarator
                            | init_declarator'''
    print("init_declarator_list->")



# 初始化声明 : 标识符([数]) | 标识符 = 初始值 
def p_init_declarator(p):
    '''init_declarator : ID
                       | ID EQUAL expression
                       | ID SQUARE_BRACKETS_LEFT expression SQUARE_BRACKETS_RIGHT'''
    print("init_declarator->")

# 表达式语句 : 表达式 ｜ 赋值表达式;
def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON'''
    print("expression_statement->")
    
# 赋值语句 : 标识符([表达式]) 赋值运算符 表达式
def p_assignment_statement(p):
    '''assignment_statement : ID assignment_operator expression SEMICOLON
                            | ID array_index assignment_operator expression SEMICOLON'''
    print("assignment_statement->")

# 赋值运算符 : = | += | -= | *= | /= | %= | &= | ^= | |= | <<= | >>=
def p_assignment_operator(p):
    '''assignment_operator : EQUAL
                           | ASSIGN'''
    print("assignment_operator->")

# 表达式 ： 运算单元 | 运算单元 运算符 表达式
def p_expression(p):
    '''expression : unary_expression
                  | unary_expression BINARY_OP expression
                  | unary_expression COMPARISON_OP expression
                  | unary_expression mutiplicative_operator expression
                  | unary_expression additive_operator expression
                  | unary_expression bitwise_operator expression'''
    print("expression->")   

# 乘法运算符 : * | / | %
def p_mutiplicative_operator(p):
    '''mutiplicative_operator : ASTERISK
                              | SLASH
                              | PERCENT'''
    print("mutiplicative_operator->")

# 加法运算符 : + | -
def p_additive_operator(p):
    '''additive_operator : PLUS
                         | MINUS'''
    print("additive_operator->")

# 位运算符 :  & | ^ | |
def p_bitwise_operator(p):
    '''bitwise_operator : AMPERSAND
                        | CARET
                        | PIPE'''
    print("bitwise_operator->")

# 运算单元 : 单元表达式 ｜ 单目运算符 单元表达式
def p_unary_expression(p):
    '''unary_expression : primary_expression postfix_unary_operator
                        | prefix_unary_operator primary_expression
                        | primary_expression'''
    print("unary_expression->")

# 前置单目运算符 : ++ | -- | * | ~ | ! | &
def p_prefix_unary_operator(p):
    '''prefix_unary_operator : UNARY_OP
                             | ASTERISK
                             | TILDE
                             | EXCLAMATION
                             | AMPERSAND'''
    print("prefix_unary_operator->")

# 后置单目运算符 : ++ | -- 
def p_postfix_unary_operator(p):
    '''postfix_unary_operator : UNARY_OP'''
    print("postfix_unary_operator->")

# 单元表达式 : 标识符 | 数字 | 字符串 | (表达式) ｜ 函数调用 | 数组访问 
def p_primary_expression(p):
    '''primary_expression : ID
                          | NUMBER
                          | STRING
                          | PARENTHESES_LEFT expression PARENTHESES_RIGHT
                          | function_call
                          | ID array_index
                          '''
    print("primary_expression->")

# 函数调用 : 标识符(参数列表)
def p_function_call(p):
    '''function_call : ID PARENTHESES_LEFT call_parameter_list PARENTHESES_RIGHT
                     | ID PARENTHESES_LEFT PARENTHESES_RIGHT'''
    print("function_call->")

# 调用参数列表 : 调用参数列表,调用参数 | 调用参数
def p_call_parameter_list(p):
    '''call_parameter_list : call_parameter_list COMMA call_parameter
                           | call_parameter'''
    print("call_parameter_list->")

# 调用参数 : 表达式
def p_call_parameter(p):
    '''call_parameter : expression'''
    print("call_parameter->")

# 数组访问 : 标识符[表达式]([表达式])
def p_array_index(p):
    '''array_index :  array_index SQUARE_BRACKETS_LEFT expression SQUARE_BRACKETS_RIGHT
                    | SQUARE_BRACKETS_LEFT expression SQUARE_BRACKETS_RIGHT'''

    print("array_index->")

# todo
def p_selection_statement(p):
    '''selection_statement : IF'''
    print("selection_statement->")

# todo
def p_iteration_statement(p):
    '''iteration_statement : WHILE'''
    print("iteration_statement->")

# todo
def p_jump_statement(p):
    '''jump_statement : RETURN'''
    print("jump_statement->")


# 错误处理
def p_error(p):
    print("Syntax error in input!type: %s, value: %s" % (p.type, p.value))

# Build the parser
parser = yacc.yacc()

if __name__ == '__main__':
    # Test the parser
    while True:
        try:
            filename = input("Enter the filename: ")
            with open(filename, 'r') as file:
                code = file.read()
            result = parser.parse(code)
            print(result)
        except EOFError:
            break
    
