import ply.yacc as yacc
from lex import tokens
from AST import InternalNode,ExternalNode


# 程序由不同的声明组成，声明可以是变量声明或函数声明
def p_program(p):
    '''program : external_declaration program
               | external_declaration'''
    p[0]=InternalNode('program',p[1:])

# 声明可以是函数声明和变量等声明
def p_external_declaration(p):
    '''external_declaration : function_declaration
                            | declaration_statement
                            | include_statement
                            | namespace_statement'''   
    p[0]=InternalNode('external_declaration',p[1:])

# include语句
def p_include_statement(p):
    '''include_statement : HASH INCLUDE LESS_THAN ID GREATER_THAN'''
    p[0]=InternalNode('include_statement',p[1:])
    p[0].children[0]=ExternalNode('HASH',p[1])
    p[0].children[1]=ExternalNode('INCLUDE',p[2])
    p[0].children[2]=ExternalNode('LESS_THAN',p[3])
    p[0].children[3]=ExternalNode('ID',p[4])
    p[0].children[4]=ExternalNode('GREATER_THAN',p[5])
    

# using namespace语句
def p_namespace_statement(p):
    '''namespace_statement : ID ID ID SEMICOLON'''
    p[0]=InternalNode('namespace_statement',p[1:])
    p[0].children[0]=ExternalNode('ID',p[1])
    p[0].children[1]=ExternalNode('ID',p[2])
    p[0].children[2]=ExternalNode('ID',p[3])
    p[0].children[3]=ExternalNode('SEMICOLON',p[4])

# 函数声明：返回类型 声明 函数体 
def p_function_declaration(p):
    '''function_declaration : declaration_specifiers func_declarator compound_statement'''
    p[0]=InternalNode('function_declaration',p[1:])

# 返回类型：（const） 类型
def p_declaration_specifiers(p):
    '''declaration_specifiers : CONST type_specifier
                              | type_specifier'''
    p[0]=InternalNode('declaration_specifiers',p[1:])
    if(p.slice[1].type=='CONST'):
        p[0].children[0]=ExternalNode('CONST',p[1])

# 类型
def p_type_specifier(p):
    '''type_specifier : VOID
                      | INT
                      | CHAR
                      | FLOAT
                      | DOUBLE
                      | LONG
                      | BOOL'''
    p[0]=InternalNode('type_specifier',p[1:])
    type_mapping = {'void': 'VOID', 'int': 'INT', 'char': 'CHAR', 'float': 'FLOAT',
                     'double': 'DOUBLE', 'long': 'LONG', 'bool': 'BOOL'}
    type_value = type_mapping.get(p[1])
    if type_value:
        p[0].children[0] = ExternalNode(type_value, p[1])


# 函数声明 : 指针 函数声明体
def p_func_declarator(p):
    '''func_declarator : ASTERISK direct_declarator 
                        | direct_declarator'''
    p[0]=InternalNode('func_declarator',p[1:])
    if(len(p)==3):
        p[0].children[0]=ExternalNode('ASTERISK',p[1])


# 函数声明体 : 标识符(空或参数)
def p_direct_declarator(p):
    '''direct_declarator ::= ID PARENTHESES_LEFT parameter_list PARENTHESES_RIGHT
	                    | ID PARENTHESES_LEFT PARENTHESES_RIGHT
                        '''
    p[0]=InternalNode('direct_declarator',p[1:])
    p[0].children[0]=ExternalNode('ID',p[1])
    p[0].children[1]=ExternalNode('PARENTHESES_LEFT',p[2])
    if(len(p)==5):
        p[0].children[3]=ExternalNode('PARENTHESES_RIGHT',p[4])
    else:
        p[0].children[2]=ExternalNode('PARENTHESES_RIGHT',p[3])

    
# 参数列表 : 参数列表,参数声明 | 参数声明
def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter_declaration
                      | parameter_declaration'''
    p[0]=InternalNode('parameter_list',p[1:])
    if len(p) == 4:
        if p.slice[2].type == 'COMMA':
            p[0].children[1]=ExternalNode('COMMA',p[2])


# 参数声明 : 类型 参数声明体
def p_parameter_declaration(p):
    '''parameter_declaration : declaration_specifiers declarator'''
    p[0]=InternalNode('parameter_declaration',p[1:])


# 参数声明体 : 指针 标识符 | 标识符[] | 标识符
def p_declarator(p):
    '''declarator : ID
                | ID SQUARE_BRACKETS_LEFT SQUARE_BRACKETS_RIGHT
                | ID SQUARE_BRACKETS_LEFT expression SQUARE_BRACKETS_RIGHT
                | ASTERISK ID'''
    p[0]=InternalNode('declarator',p[1:])
    if (len(p) == 2):
        p[0].children[0] = ExternalNode('ID', p[1])
    elif (len(p) == 4):
        p[0].children[0] = ExternalNode('ID', p[1])
        p[0].children[1] = ExternalNode('SQUARE_BRACKETS_LEFT', p[2])
        p[0].children[2] = ExternalNode('SQUARE_BRACKETS_RIGHT', p[3])
    elif (len(p) == 5):
        p[0].children[0] = ExternalNode('ID', p[1])
        p[0].children[1] = ExternalNode('SQUARE_BRACKETS_LEFT', p[2])
        #p[0].children[2] = p[3]  # Assuming expression produces an AST
        p[0].children[3] = ExternalNode('SQUARE_BRACKETS_RIGHT', p[4])
    elif (len(p) == 3):
        p[0].children[0] = ExternalNode('ASTERISK', p[1])
        p[0].children[1] = ExternalNode('ID', p[2])


# 函数体 : { (语句列表) }
def p_compound_statement(p):
    '''compound_statement : CURLY_BRACES_LEFT CURLY_BRACES_RIGHT
                          | CURLY_BRACES_LEFT statement_list CURLY_BRACES_RIGHT'''
    p[0]=InternalNode('compound_statement',p[1:])
    p[0].children[0]=ExternalNode('CURLY_BRACES_LEFT',p[1])
    if(p.slice[2].type =="statement_list"):
        #p[0].children[1]=p[2]
        p[0].children[2]=ExternalNode('CURLY_BRACES_RIGHT',p[3])
    else:
        p[0].children[1]=ExternalNode('CURLY_BRACES_RIGHT',p[2])


# 语句列表 : 语句列表 语句 | 语句
def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    p[0]=InternalNode('statement_list',p[1:])


# 语句 : 声明 ｜ 函数 ｜ 表达式 ｜ 选择语句 ｜ 迭代语句 ｜ 跳转语句 | 赋值语句
def p_statement(p):
    '''statement : declaration_statement
                 | expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement
                 | assignment_statement'''
    p[0]=InternalNode('statement',p[1:])
    

# 声明语句 : 声明 ;
def p_declaration_statement(p):
    '''declaration_statement : declaration SEMICOLON'''
    p[0]=InternalNode('declaration_statement',p[1:])


# 声明 : 类型 标识符
def p_declaration(p):
    '''declaration : declaration_specifiers init_declarator_list'''
    p[0]=InternalNode('declaration',p[1:])


# 初始化声明列表 : 初始化声明列表 , 初始化声明 | 初始化声明
def p_init_declarator_list(p):
    '''init_declarator_list : init_declarator_list COMMA init_declarator
                            | init_declarator'''
    p[0]=InternalNode('init_declarator_list',p[1:])
    if (len(p) == 4):
        if p.slice[2].type == 'COMMA':
            p[0].children[1] = ExternalNode('COMMA', p[2])



# 初始化声明 : 标识符([数]) | 标识符 = 初始值 
def p_init_declarator(p):
    '''init_declarator : ID
                       | ID EQUAL expression
                       | ID SQUARE_BRACKETS_LEFT expression SQUARE_BRACKETS_RIGHT'''
    p[0]=InternalNode('init_declarator',p[1:])
    p[0].children[0] = ExternalNode('ID', p[1])
    if len(p) == 4 and p.slice[2].type == 'EQUAL':
        p[0].children[1] = ExternalNode('EQUAL', p[2])
        #p[0].children[2] = p[3]
    elif len(p) == 5 and p.slice[2].type == 'SQUARE_BRACKETS_LEFT':
        p[0].children[1] = ExternalNode('SQUARE_BRACKETS_LEFT', p[2])
        #p[0].children[2] = p[3]
        p[0].children[3] = ExternalNode('SQUARE_BRACKETS_RIGHT', p[4])


# 表达式语句 : 表达式 ｜ 赋值表达式;
def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON'''
    p[0]=InternalNode('expression_statement',p[1:])
    p[0].children[1] = ExternalNode('SEMICOLON', p[2])

    
# 赋值语句 : 标识符([表达式]) 赋值运算符 表达式
def p_assignment_statement(p):
    '''assignment_statement : ID assignment_operator expression SEMICOLON
                            | ID array_index assignment_operator expression SEMICOLON'''
    p[0]=InternalNode('assignment_statement',p[1:])
    p[0].children[0]=ExternalNode('ID',p[1])
    #p[0].children[1]=p[2]
    #p[0].children[2]=p[3]
    if len(p)==5:
        p[0].children[3]=ExternalNode('SEMICOLON',p[4])
    else:
        #p[0].children[3]=p[4]
        p[0].children[4]=ExternalNode('SEMICOLON',p[5])



# 赋值运算符 : = | += | -= | *= | /= | %= | &= | ^= | |= | <<= | >>=
def p_assignment_operator(p):
    '''assignment_operator : EQUAL
                           | ASSIGN'''
    p[0]=InternalNode('assignment_operator',p[1:])
    if p.slice[1].type == 'EQUAL':
        p[0].children[0] = ExternalNode('EQUAL', p[1])
    elif p.slice[1].type == 'ASSIGN':
        p[0].children[0] = ExternalNode('ASSIGN', p[1])


# 表达式 ： 运算单元 | 运算单元 运算符 表达式
def p_expression(p):
    '''expression : unary_expression
                  | unary_expression logical_operator expression
                  | unary_expression BINARY_OP expression
                  | unary_expression COMPARISON_OP expression
                  | unary_expression multiplicative_operator expression
                  | unary_expression additive_operator expression
                  | unary_expression bitwise_operator expression'''
    p[0]=InternalNode('expression',p[1:])
    if len(p) == 4:
        if(p.slice[2].type =='BINARY_OP'):
            p[0].children[1]=ExternalNode('BINARY_OP',p[2])
        elif(p.slice[2].type =='COMPARISON_OP'):
            p[0].children[1]=ExternalNode('COMPARISON_OP',p[2])

    

# 逻辑运算符 : && | ||
def p_logical_operator(p):
    '''logical_operator : AND_OP
                        | OR_OP
                        | GREATER_THAN
                        | LESS_THAN'''
    p[0]=InternalNode('logical_operator',p[1:])
    if(p.slice[1].type =='AND_OP'):
        p[0].children[0]=ExternalNode('AND_OP',p[1])
    elif(p.slice[1].type =='OR_OP'):
        p[0].children[0]=ExternalNode('OR_OP',p[1])
    elif(p.slice[1].type =='GREATER_THAN'):
        p[0].children[0]=ExternalNode('GREATER_THAN',p[1])
    elif(p.slice[1].type =='LESS_THAN'):
        p[0].children[0]=ExternalNode('LESS_THAN',p[1])

# 乘法运算符 : * | / | %
def p_multiplicative_operator(p):
    '''multiplicative_operator : ASTERISK
                              | SLASH
                              | PERCENT'''
    p[0]=InternalNode('multiplicative_operator',p[1:])
    if(p.slice[1].type=='ASTERISK'):
        p[0].children[0]=ExternalNode('ASTERISK',p[1])
    elif(p.slice[1].type =='SLASH'):
        p[0].children[0]=ExternalNode('SLASH',p[1])
    elif(p.slice[1].type =='PERCENT'):
        p[0].children[0]=ExternalNode('PERCENT',p[1])

# 加法运算符 : + | -
def p_additive_operator(p):
    '''additive_operator : PLUS
                         | MINUS'''
    p[0]=InternalNode('additive_operator',p[1:])
    if(p.slice[1].type =='PLUS'):
        p[0].children[0]=ExternalNode('PLUS',p[1])
    elif(p.slice[1].type =='MINUS'):
        p[0].children[0]=ExternalNode('MINUS',p[1])

# 位运算符 :  & | ^ | |
def p_bitwise_operator(p):
    '''bitwise_operator : AMPERSAND
                        | CARET
                        | PIPE'''
    p[0]=InternalNode('bitwise_operator',p[1:])
    if(p.slice[1].type =='AMPERSAND'):
        p[0].children[0]=ExternalNode('AMPERSAND',p[1])
    elif(p.slice[1].type =='CARET'):
        p[0].children[0]=ExternalNode('CARET',p[1])
    elif(p.slice[1].type =='PIPE'):
        p[0].children[0]=ExternalNode('PIPE',p[1])

# 运算单元 : 单元表达式 ｜ 单目运算符 单元表达式
def p_unary_expression(p):
    '''unary_expression : primary_expression postfix_unary_operator
                        | prefix_unary_operator primary_expression
                        | primary_expression'''
    p[0]=InternalNode('unary_expression',p[1:])

# 前置单目运算符 : ++ | -- | * | ~ | ! | &
def p_prefix_unary_operator(p):
    '''prefix_unary_operator : UNARY_OP
                             | ASTERISK
                             | TILDE
                             | EXCLAMATION
                             | AMPERSAND'''
    p[0]=InternalNode('prefix_unary_operator',p[1:])
    if(p.slice[1].type =='UNARY_OP'):
        p[0].children[0]=ExternalNode('UNARY_OP',p[1])
    elif(p.slice[1].type =='ASTERISK'):
        p[0].children[0]=ExternalNode('ASTERISK',p[1])
    elif(p.slice[1].type =='TILDE'):
        p[0].children[0]=ExternalNode('TILDE',p[1])
    elif(p.slice[1].type =='EXCLAMATION'):
        p[0].children[0]=ExternalNode('EXCLAMATION',p[1])
    elif(p.slice[1].type =='AMPERSAND'):
        p[0].children[0]=ExternalNode('AMPERSAND',p[1])


# 后置单目运算符 : ++ | -- 
def p_postfix_unary_operator(p):
    '''postfix_unary_operator : UNARY_OP'''
    p[0]=InternalNode('postfix_unary_operator',p[1:])
    p[0].children[0]=ExternalNode('UNARY_OP',p[1])

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
    p[0]=InternalNode('primary_expression',p[1:])
    if(p.slice[1].type =='ID'):
        p[0].children[0]=ExternalNode('ID',p[1])
    elif(p.slice[1].type =='NUMBER'):
        p[0].children[0]=ExternalNode('NUMBER',p[1])
    elif(p.slice[1].type =='STRING'):
        p[0].children[0]=ExternalNode('STRING',p[1])
    elif(p.slice[1].type =='PARENTHESES_LEFT'):
        p[0].children[0]=ExternalNode('PARENTHESES_LEFT',p[1])
        #p[0].children[1]=p[2]
        p[0].children[2]=ExternalNode('PARENTHESES_RIGHT',p[3])
    elif(p.slice[1].type =='TRUE'):
        p[0].children[0]=ExternalNode('TRUE',p[1])
    elif(p.slice[1].type =='FALSE'):
        p[0].children[0]=ExternalNode('FALSE',p[1])


# 函数调用 : 标识符(参数列表)
def p_function_call(p):
    '''function_call : ID PARENTHESES_LEFT call_parameter_list PARENTHESES_RIGHT
                     | ID PARENTHESES_LEFT PARENTHESES_RIGHT'''
    p[0]=InternalNode('function_call',p[1:])
    p[0].children[0]=ExternalNode('ID',p[1])
    p[0].children[1]=ExternalNode('PARENTHESES_LEFT',p[2])
    if(len(p)==5):
        p[0].children[3]=ExternalNode('PARENTHESES_RIGHT',p[4])
    else:
        p[0].children[2]=ExternalNode('PARENTHESES_RIGHT',p[3])

# 调用参数列表 : 调用参数列表,调用参数 | 调用参数
def p_call_parameter_list(p):
    '''call_parameter_list : call_parameter_list COMMA call_parameter
                           | call_parameter'''
    p[0]=InternalNode('call_parameter_list',p[1:])
    if len(p) == 4:
        if p.slice[2].type == 'COMMA':
            p[0].children[1] = ExternalNode('COMMA', p[2])

# 调用参数 : 表达式
def p_call_parameter(p):
    '''call_parameter : expression'''
    p[0]=InternalNode('call_parameter',p[1:])

# 数组访问 : 标识符[表达式]([表达式])
def p_array_index(p):
    '''array_index :  array_index SQUARE_BRACKETS_LEFT expression SQUARE_BRACKETS_RIGHT
                    | SQUARE_BRACKETS_LEFT expression SQUARE_BRACKETS_RIGHT'''

    p[0]=InternalNode('array_index',p[1:])
    if(len(p)==5):
        #p[0].children[0]=p[1]
        p[0].children[1]=ExternalNode('SQUARE_BRACKETS_LEFT',p[2])
        #p[0].children[2]=p[3]
        p[0].children[3]=ExternalNode('SQUARE_BRACKETS_RIGHT',p[4])
    else:
        p[0].children[0]=ExternalNode('SQUARE_BRACKETS_LEFT',p[1])
        #p[0].children[1]=p[2]
        p[0].children[2]=ExternalNode('SQUARE_BRACKETS_RIGHT',p[3])

# 条件：IF (表达式) 语句 | IF (表达式) 语句 ELSE 语句 | SWITCH (表达式) 语句
def p_selection_statement(p):
    '''selection_statement : IF PARENTHESES_LEFT expression PARENTHESES_RIGHT compound_statement
                           | IF PARENTHESES_LEFT expression PARENTHESES_RIGHT compound_statement ELSE compound_statement
                           | SWITCH PARENTHESES_LEFT expression PARENTHESES_RIGHT CURLY_BRACES_LEFT case_list CURLY_BRACES_LEFT'''
    p[0]=InternalNode('selection_statement',p[1:])
    if(p.slice[1].type =='IF'):
        p[0].children[0]=ExternalNode('IF',p[1])
        p[0].children[1]=ExternalNode('PARENTHESES_LEFT',p[2])
        #p[0].children[2]=p[3]
        p[0].children[3]=ExternalNode('PARENTHESES_RIGHT',p[4])
        #p[0].children[4]=p[5]
        if(len(p)==8):
            p[0].children[5]=ExternalNode('ELSE',p[6])
            #p[0].children[6]=p[7]
    elif(p.slice[1].type =='SWITCH'):
        p[0].children[0]=ExternalNode('SWITCH',p[1])
        p[0].children[1]=ExternalNode('PARENTHESES_LEFT',p[2])
        #p[0].children[2]=p[3]
        p[0].children[3]=ExternalNode('PARENTHESES_RIGHT',p[4])
        #p[0].children[4]=p[5]

def p_case_list(p):
    '''case_list : case_list case
                 | case'''
    p[0]=InternalNode('case_list',p[1:])

def p_case(p):
    '''case : CASE constant_expression COLON statement_list
            | DEFAULT COLON statement_list'''
    p[0]=InternalNode('case',p[1:])
    if(p.slice[1].type =='CASE'):
        p[0].children[0]=ExternalNode('CASE',p[1])
        #p[0].children[1]=p[2]
        p[0].children[2]=ExternalNode('COLON',p[3])
        #p[0].children[3]=p[4]
    elif(p.slice[1].type =='DEFAULT'):
        p[0].children[0]=ExternalNode('DEFAULT',p[1])
        p[0].children[1]=ExternalNode('COLON',p[2])
        #p[0].children[2]=p[3]

def p_constant_expression(p):
    '''constant_expression : NUMBER'''
    p[0]=InternalNode('constant_expression',p[1:])
    p[0].children[0]=ExternalNode('NUMBER',p[1])


# 迭代：WHILE (表达式) 语句 | DO 语句 WHILE (表达式) | FOR (表达式;表达式;) 语句 | FOR (表达式;表达式;表达式) 语句
def p_iteration_statement(p):
    '''iteration_statement : WHILE PARENTHESES_LEFT expression PARENTHESES_RIGHT compound_statement
                           | DO compound_statement WHILE PARENTHESES_LEFT expression PARENTHESES_RIGHT
                           | FOR PARENTHESES_LEFT declaration_statement expression_statement PARENTHESES_RIGHT compound_statement
                           | FOR PARENTHESES_LEFT declaration_statement expression_statement expression PARENTHESES_RIGHT compound_statement'''
    p[0]=InternalNode('iteration_statement',p[1:])
    if(p.slice[1].type =='WHILE'):
        p[0].children[0]=ExternalNode('WHILE',p[1])
        p[0].children[1]=ExternalNode('PARENTHESES_LEFT',p[2])
        #p[0].children[2]=p[3]
        p[0].children[3]=ExternalNode('PARENTHESES_RIGHT',p[4])
        #p[0].children[4]=p[5]
    elif(p.slice[1].type =='DO'):
        p[0].children[0]=ExternalNode('DO',p[1])
        #p[0].children[1]=p[2]
        p[0].children[2]=ExternalNode('WHILE',p[3])
        p[0].children[3]=ExternalNode('PARENTHESES_LEFT',p[4])
        #p[0].children[4]=p[5]
        p[0].children[5]=ExternalNode('PARENTHESES_RIGHT',p[6])
    elif(p.slice[1].type =='FOR'):
        p[0].children[0]=ExternalNode('FOR',p[1])
        p[0].children[1]=ExternalNode('PARENTHESES_LEFT',p[2])
        #p[0].children[2]=p[3]
        #p[0].children[3]=p[4]
        if(len(p)==6):
            p[0].children[4]=ExternalNode('PARENTHESES_RIGHT',p[5])
            #p[0].children[5]=p[6]
        else:
            #p[0].children[4]=p[5]
            p[0].children[5]=ExternalNode('PARENTHESES_RIGHT',p[6])
            #p[0].children[6]=p[7]      


    
# 跳转：RETURN 表达式 ; | BREAK ; | CONTINUE ;
def p_jump_statement(p):
    '''jump_statement : RETURN expression SEMICOLON
                      | BREAK SEMICOLON
                      | CONTINUE SEMICOLON'''
    p[0]=InternalNode('jump_statement',p[1:])
    if(p.slice[1].type =='RETURN'):
        p[0].children[0]=ExternalNode('RETURN',p[1])
        #p[0].children[1]=p[2]
        p[0].children[2]=ExternalNode('SEMICOLON',p[3])
    elif(p.slice[1].type =='BREAK'):
        p[0].children[0]=ExternalNode('BREAK',p[1])
        p[0].children[1]=ExternalNode('SEMICOLON',p[2])
    elif(p.slice[1].type =='CONTINUE'):
        p[0].children[0]=ExternalNode('CONTINUE',p[1])
        p[0].children[1]=ExternalNode('SEMICOLON',p[2])



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
    
