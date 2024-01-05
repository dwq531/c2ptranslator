import ply.yacc as yacc
from lex import tokens
from AST import InternalNode,ExternalNode


# 程序由不同的声明组成，声明可以是变量声明或函数声明
def p_program(p):
    '''program : external_declaration program
               | external_declaration'''
    print("program->")
    p[0]=InternalNode('program',p[1:])

# 声明可以是函数声明和变量等声明
def p_external_declaration(p):
    '''external_declaration : function_declaration
                            | declaration_statement
                            | include_statement
                            | namespace_statement'''   
    print("external_declaration->")
    p[0]=InternalNode('external_declaration',p[1:])

# include语句
def p_include_statement(p):
    '''include_statement : HASH INCLUDE LESS_THAN ID GREATER_THAN'''
    print("include_statement->")

# using namespace语句
def p_namespace_statement(p):
    '''namespace_statement : ID ID ID SEMICOLON'''
    print("namespace_statement->")

# 函数声明：返回类型 声明 函数体 
def p_function_declaration(p):
    '''function_declaration : declaration_specifiers func_declarator compound_statement'''
    print("function_declaration->")
    p[0]=InternalNode('function_declaration',p[1:])

# 返回类型：（const） 类型
def p_declaration_specifiers(p):
    '''declaration_specifiers : CONST type_specifier
                              | type_specifier'''
    print("declaration_specifiers->",p[1])
    p[0]=InternalNode('declaration_specifiers',p[1:])

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
    p[0]=InternalNode('type_specifier',p[1:])

# 函数声明 : 指针 函数声明体
def p_func_declarator(p):
    '''func_declarator : ASTERISK direct_declarator 
                        | direct_declarator'''
    print("func_declarator->")
    p[0]=InternalNode('func_declarator',p[1:])

# 函数声明体 : 标识符(空或参数)
def p_direct_declarator(p):
    '''direct_declarator ::= ID PARENTHESES_LEFT parameter_list PARENTHESES_RIGHT
	                    | ID PARENTHESES_LEFT PARENTHESES_RIGHT
                        '''
    print("direct_declarator->",p[1])
    p[0]=InternalNode('direct_declarator',p[1:])

# 参数列表 : 参数列表,参数声明 | 参数声明
def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter_declaration
                      | parameter_declaration'''
    print("parameter_list->")
    p[0]=InternalNode('parameter_list',p[1:])


# 参数声明 : 类型 参数声明体
def p_parameter_declaration(p):
    '''parameter_declaration : declaration_specifiers declarator'''
    print("parameter_declaration->")
    p[0]=InternalNode('parameter_declaration',p[1:])


# 参数声明体 : 指针 标识符 | 标识符[] | 标识符
def p_declarator(p):
    '''declarator : ID
                | ID SQUARE_BRACKETS_LEFT SQUARE_BRACKETS_RIGHT
                | ID SQUARE_BRACKETS_LEFT expression SQUARE_BRACKETS_RIGHT
                | ASTERISK ID'''
    print("declarator->",p[1])
    p[0]=InternalNode('declarator',p[1:])


# 函数体 : { (语句列表) }
def p_compound_statement(p):
    '''compound_statement : CURLY_BRACES_LEFT CURLY_BRACES_RIGHT
                          | CURLY_BRACES_LEFT statement_list CURLY_BRACES_RIGHT'''
    print("compound_statement->")
    p[0]=InternalNode('compound_statement',p[1:])


# 语句列表 : 语句列表 语句 | 语句
def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    print("statement_list->")
    p[0]=InternalNode('statement_list',p[1:])


# 语句 : 声明 ｜ 函数 ｜ 表达式 ｜ 选择语句 ｜ 迭代语句 ｜ 跳转语句 | 赋值语句
def p_statement(p):
    '''statement : declaration_statement
                 | expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement
                 | assignment_statement'''
    print("statement->")
    p[0]=InternalNode('statement',p[1:])
    

# 声明语句 : 声明 ;
def p_declaration_statement(p):
    '''declaration_statement : declaration SEMICOLON'''
    print("declaration_statement->")
    p[0]=InternalNode('declaration_statement',p[1:])


# 声明 : 类型 标识符
def p_declaration(p):
    '''declaration : declaration_specifiers init_declarator_list'''
    print("declaration->")
    p[0]=InternalNode('declaration',p[1:])


# 初始化声明列表 : 初始化声明列表 , 初始化声明 | 初始化声明
def p_init_declarator_list(p):
    '''init_declarator_list : init_declarator_list COMMA init_declarator
                            | init_declarator'''
    print("init_declarator_list->")
    p[0]=InternalNode('init_declarator_list',p[1:])



# 初始化声明 : 标识符([数]) | 标识符 = 初始值 
def p_init_declarator(p):
    '''init_declarator : ID
                       | ID EQUAL expression
                       | ID SQUARE_BRACKETS_LEFT expression SQUARE_BRACKETS_RIGHT'''
    print("init_declarator->")
    p[0]=InternalNode('init_declarator',p[1:])


# 表达式语句 : 表达式 ｜ 赋值表达式;
def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON'''
    print("expression_statement->")
    p[0]=InternalNode('expression_statement',p[1:])

    
# 赋值语句 : 标识符([表达式]) 赋值运算符 表达式
def p_assignment_statement(p):
    '''assignment_statement : ID assignment_operator expression SEMICOLON
                            | ID array_index assignment_operator expression SEMICOLON'''
    print("assignment_statement->")
    p[0]=InternalNode('assignment_statement',p[1:])


# 赋值运算符 : = | += | -= | *= | /= | %= | &= | ^= | |= | <<= | >>=
def p_assignment_operator(p):
    '''assignment_operator : EQUAL
                           | ASSIGN'''
    print("assignment_operator->")
    p[0]=InternalNode('assignment_operator',p[1:])


# 表达式 ： 运算单元 | 运算单元 运算符 表达式
def p_expression(p):
    '''expression : unary_expression
                  | unary_expression BINARY_OP expression
                  | unary_expression COMPARISON_OP expression
                  | unary_expression mutiplicative_operator expression
                  | unary_expression additive_operator expression
                  | unary_expression bitwise_operator expression'''
    print("expression->") 
    p[0]=InternalNode('expression',p[1:])
    

# 乘法运算符 : * | / | %
def p_mutiplicative_operator(p):
    '''mutiplicative_operator : ASTERISK
                              | SLASH
                              | PERCENT'''
    print("mutiplicative_operator->")
    p[0]=InternalNode('mutiplicative_operator',p[1:])

# 加法运算符 : + | -
def p_additive_operator(p):
    '''additive_operator : PLUS
                         | MINUS'''
    print("additive_operator->")
    p[0]=InternalNode('additive_operator',p[1:])

# 位运算符 :  & | ^ | |
def p_bitwise_operator(p):
    '''bitwise_operator : AMPERSAND
                        | CARET
                        | PIPE'''
    print("bitwise_operator->")
    p[0]=InternalNode('bitwise_operator',p[1:])

# 运算单元 : 单元表达式 ｜ 单目运算符 单元表达式
def p_unary_expression(p):
    '''unary_expression : primary_expression postfix_unary_operator
                        | prefix_unary_operator primary_expression
                        | primary_expression'''
    print("unary_expression->")
    p[0]=InternalNode('unary_expression',p[1:])

# 前置单目运算符 : ++ | -- | * | ~ | ! | &
def p_prefix_unary_operator(p):
    '''prefix_unary_operator : UNARY_OP
                             | ASTERISK
                             | TILDE
                             | EXCLAMATION
                             | AMPERSAND'''
    print("prefix_unary_operator->")
    p[0]=InternalNode('prefix_unary_operator',p[1:])

# 后置单目运算符 : ++ | -- 
def p_postfix_unary_operator(p):
    '''postfix_unary_operator : UNARY_OP'''
    print("postfix_unary_operator->")
    p[0]=InternalNode('postfix_unary_operator',p[1:])

# 单元表达式 : 标识符 | 数字 | 字符串 | (表达式) ｜ 函数调用 | 数组访问 
def p_primary_expression(p):
    '''primary_expression : ID
                          | NUMBER
                          | STRING
                          | PARENTHESES_LEFT expression PARENTHESES_RIGHT
                          | function_call
                          | ID array_index
                          | TRUE
                          | FALSE
                          '''
    print("primary_expression->")
    p[0]=InternalNode('primary_expression',p[1:])


# 函数调用 : 标识符(参数列表)
def p_function_call(p):
    '''function_call : ID PARENTHESES_LEFT call_parameter_list PARENTHESES_RIGHT
                     | ID PARENTHESES_LEFT PARENTHESES_RIGHT'''
    print("function_call->")
    p[0]=InternalNode('function_call',p[1:])

# 调用参数列表 : 调用参数列表,调用参数 | 调用参数
def p_call_parameter_list(p):
    '''call_parameter_list : call_parameter_list COMMA call_parameter
                           | call_parameter'''
    print("call_parameter_list->")
    p[0]=InternalNode('call_parameter_list',p[1:])

# 调用参数 : 表达式
def p_call_parameter(p):
    '''call_parameter : expression'''
    print("call_parameter->")
    p[0]=InternalNode('call_parameter',p[1:])

# 数组访问 : 标识符[表达式]([表达式])
def p_array_index(p):
    '''array_index :  array_index SQUARE_BRACKETS_LEFT expression SQUARE_BRACKETS_RIGHT
                    | SQUARE_BRACKETS_LEFT expression SQUARE_BRACKETS_RIGHT'''

    print("array_index->")
    p[0]=InternalNode('array_index',p[1:])

# 条件：IF (表达式) 语句 | IF (表达式) 语句 ELSE 语句 | SWITCH (表达式) 语句
def p_selection_statement(p):
    '''selection_statement : IF PARENTHESES_LEFT logical_expression PARENTHESES_RIGHT compound_statement
                           | IF PARENTHESES_LEFT logical_expression PARENTHESES_RIGHT compound_statement ELSE compound_statement
                           | SWITCH PARENTHESES_LEFT logical_expression PARENTHESES_RIGHT CURLY_BRACES_LEFT case_list CURLY_BRACES_LEFT'''
    print("selection_statement->")
    p[0]=InternalNode('selection_statement',p[1:])

def p_case_list(p):
    '''case_list : case_list case
                 | case'''

def p_case(p):
    '''case : CASE constant_expression COLON statement_list
            | DEFAULT COLON statement_list'''

def p_constant_expression(p):
    '''constant_expression : NUMBER'''


# 迭代：WHILE (表达式) 语句 | DO 语句 WHILE (表达式) | FOR (表达式;表达式;) 语句 | FOR (表达式;表达式;表达式) 语句
def p_iteration_statement(p):
    '''iteration_statement : WHILE PARENTHESES_LEFT expression PARENTHESES_RIGHT compound_statement
                           | DO compound_statement WHILE PARENTHESES_LEFT expression PARENTHESES_RIGHT
                           | FOR PARENTHESES_LEFT expression_statement expression_statement PARENTHESES_RIGHT compound_statement
                           | FOR PARENTHESES_LEFT expression_statement expression_statement expression PARENTHESES_RIGHT compound_statement'''
    print("iteration_statement->")
    p[0]=InternalNode('iteration_statement',p[1:])
    
# 跳转：RETURN 表达式 ; | BREAK ; | CONTINUE ;
def p_jump_statement(p):
    '''jump_statement : RETURN expression SEMICOLON
                      | BREAK SEMICOLON
                      | CONTINUE SEMICOLON'''
    print("jump_statement->")
    p[0]=InternalNode('jump_statement',p[1:])

# 判断语句：与或非
def p_logical_expression(p):
    '''logical_expression : logical_expression AND_OP logical_expression
                          | logical_expression OR_OP logical_expression
                          | NO_OP logical_expression
                          | expression'''
    print("logical_expression->")
    p[0]=InternalNode('logical_expression',p[1:])
    

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
            with open(filename, 'r', encoding='utf-8') as file:
                code = file.read()
            result = parser.parse(code)
            output_filename = "output.json"
            with open(output_filename, 'w') as output_file:
                output_file.write(result.to_json())
            #print(result.to_yaml())
            #print(result)
        except EOFError:
            break
    
