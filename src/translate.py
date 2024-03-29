from AST import *
from yacc import parser
import os

# 把C代码翻译成python字符串列表
def translate(tree):
    code =[]
    # 深度优先遍历
    for child in tree.children:
        if isinstance(child, InternalNode):
            if child.key == "include_statement" or child.key == "namespace_statement":
                # include和namespace语句不翻译
                continue
            elif child.key == "function_declaration":
                code += trans_function(child)
            else:
                code += translate(child)
        else:
            # 叶子节点
            code.append(child.value)
    return code
# function_declaration
def trans_function(node):
    # todo
    code = []
    for child in node.children:
        if child.key == "declaration_specifiers":
            # declaration_specifiers，不需要类型，换成def
            code.append("def")
        elif child.key == "func_declarator":
            # func_declarator
            direct_declarator = child.children[-1]
            if direct_declarator.children[0].value == "main":
                code.pop() # 去掉def
                code += ["if","__name__","==","'__main__'",":"]
                code.append("\n")
            else:
                code.append(direct_declarator.children[0].value)
                code.append("(")
                # parameter_list
                parameter_list = direct_declarator.children[2]
                if parameter_list.key == "parameter_list":
                    code += trans_parameter_list(parameter_list)
                code.append("):")
                code.append("\n")
        else:
            # compound_statement，缩进+1
            code.append(trans_compound(child))
    return code

# parameter_list
def trans_parameter_list(node):
    code = []
    for child in node.children:
        if isinstance(child, InternalNode):
            if child.key == "parameter_list":
                code += trans_parameter_list(child)
            elif child.key == "parameter_declaration":
                declarator = child.children[1]
                # python参数不需要类型，只保留id名即可
                code.append(declarator.children[0].value)   
        else:
            code.append(child.value)               
    return code

# compound_statement
def trans_compound(node):
    code = []
    statment_list = node.children[1]
    if statment_list.key == "statement_list":
        code += trans_statement_list(statment_list)
    else:
        code.append("pass")
        code.append("\n")
    return code

# statement_list
def trans_statement_list(node):
    code = []
    for child in node.children:
        if child.key == "statement_list":
            code += trans_statement_list(child)
        else:
            grandchild = child.children[0]
            if grandchild.key == "declaration_statement":
                code += trans_declaration_statement(grandchild)
            elif grandchild.key == "expression_statement":
                code += trans_expression_statement(grandchild)
            elif grandchild.key == "selection_statement":
                code += trans_selection(grandchild)
            elif grandchild.key == "iteration_statement":
                code += trans_iteration(grandchild)
            elif grandchild.key == "jump_statement":
                code += trans_jump(grandchild)
            elif grandchild.key == "assignment_statement":
                code += trans_assignment(grandchild)
    return code


# declaration_statement
def trans_declaration_statement(node):
    code = []
    child = node.children[0]
    code = trans_declaration(child)
    code.append("\n")
    return code

# declaration
def trans_declaration(node):
    code = []
    for child in node.children:
        if child.key == "declaration_specifiers":
            # declaration_specifiers，不需要类型
            pass
        elif child.key == "init_declarator_list":
            code += trans_init_declarator_list(child)
    return code

# init_declarator_list
def trans_init_declarator_list(node):
    code = []
    for child in node.children:
        if child.key=='init_declarator_list':
            code += trans_init_declarator_list(child)
        elif child.key=='init_declarator':
            code += trans_init_declarator(child)
        else:
            code.append(child.value)
    return code

# init_declarator
def trans_init_declarator(node):
    code = []
    if len(node.children)==4:
        size = trans_expression(node.children[2])
        return [node.children[0].value,"=","[0 for _ in range("]+size+[")]"]
    elif len(node.children)==1:
        # 变量初始化
        return [node.children[0].value,"=","None"]
    for child in node.children:
        if isinstance(child,ExternalNode):
            code.append(child.value)
        else:
            code += trans_expression(child)
    return code

# expression_statement
def trans_expression_statement(node):
    # todo
    # expression_statement : expression SEMICOLON
    child = node.children[0]
    code = trans_expression(child)
    code.append("\n")
    return code

# expression
def trans_expression(node):
    #todo
    code = []
    for child in node.children:
        if child.key=='unary_expression':
            code += trans_unary_expression(child)
        elif child.key=='logical_operator':
            code += trans_logical_operator(child)
        elif child.key=='BINARY_OP':
            code.append(child.value)
        elif child.key=='COMPARISON_OP':
            code.append(child.value)
        elif child.key=='multiplicative_operator':
            code += trans_multiplicative_operator(child)
        elif child.key=='additive_operator':
            code += trans_additive_operator(child)
        elif child.key=='bitwise_operator':
            code += trans_bitwise_operator(child)
        elif child.key=='expression':
            code += trans_expression(child)
    return code

# unary_expression
def trans_unary_expression(node):
    # todo
    code = []
    if(len(node.children)==1):
        code += trans_primary_expression(node.children[0])
    else:
        ## 前置
        if node.children[0].key=='prefix_unary_operator':
            code = trans_primary_expression(node.children[1])
            if node.children[0].children[0].value=='++':
                code = code + ["+=1"]
            elif node.children[0].children[0].value=='--':
                code = code + ["-=1"]
        ## 后置
        else:
            code = trans_primary_expression(node.children[0])
            if node.children[1].children[0].value=='++':
                code = code + ["+=1"]
            elif node.children[1].children[0].value=='--':
                code = code + ["-=1"]
    return code

# logical_operator
def trans_logical_operator(node):
    # todo
    code = []
    if node.children[0].value=='&&':
        code.append('and')
    elif node.children[0].value=='||':
        code.append('or')
    else:
        code.append(node.children[0].value)
    return code

# multiplicative_operator
def trans_multiplicative_operator(node):
    # todo
    code = []
    code.append(node.children[0].value)
    return code

# additive_operator
def trans_additive_operator(node):
    # todo
    code = []
    code.append(node.children[0].value)
    return code

# bitwise_operator
def trans_bitwise_operator(node):
    # todo
    code = []
    code.append(node.children[0].value)
    return code

# primary_expression
def trans_primary_expression(node):
    # todo
    code = []
    for child in node.children:
        if child.key=='expression':
            code += trans_expression(child)
        elif child.key=='function_call':
            code += trans_function_call(child)
        elif child.key=='array_index':
            code += trans_array_index(child)
        elif child.value=='true':
            code.append('True')
        elif child.value=='false':
            code.append('False')
        else:
            #print(child.key)
            code.append(child.value)
    return code

# constant_expression
def trans_constant_expression(node):
    # todo
    code = []
    code.append(node.children[0].value)
    return code

# function_call
def trans_function_call(node):
    # todo
    code = []
    if node.children[0].value=='scanf':
        # id = input()
        param = trans_call_parameter_list(node.children[2])
        code+=param[2:]
        code.append('=')
        if param[0]=='\"%d\"':
            code.append('int(input())')
        else:
            code.append('input()')
        return code
    if node.children[0].value=='printf':
        # print("format" %id)
        param = trans_call_parameter_list(node.children[2])
        code.append('print(')
        print(param)
        if ',' in param:
            code.append(param[0])
            code.append('%')
            code+=param[2:]
        else:
            code+=param
        code.append(')')
        print(code)
        return code
    if node.children[0].value=='strlen':
        # len(param)
        param = trans_call_parameter_list(node.children[2])
        code.append('len(')
        code+=param
        code.append(')')
        return code
    for child in node.children:
        if child.key=='call_parameter_list':
            code+=trans_call_parameter_list(child)
        else:
            code.append(child.value)
    return code

# array_index
def trans_array_index(node):
    # todo
    code = []
    for child in node.children:
        if child.key=='array_index':
            code += trans_array_index(child)
        elif child.key=='expression':
            code += trans_expression(child)
        else:
            code.append(child.value)
    return code

# call_parameter_list
def trans_call_parameter_list(node):
    # todo
    code = []
    for child in node.children:
        if child.key=='call_parameter_list':
            code +=trans_call_parameter_list(child)
        elif child.key=='call_parameter':
            code +=trans_call_parameter(child)
        else:
            code.append(child.value)
    return code

# call_parameter
def trans_call_parameter(node):
    # todo
    code = []
    code += trans_expression(node.children[0])
    return code

# selection_statement
def trans_selection(node):
    code = []
    if node.children[0].value == "if":
        code.append("if")
        code += trans_expression(node.children[2])
        code.append(":")
        code.append("\n")
        code.append(trans_compound(node.children[4]))
        if len(node.children) >= 7 and node.children[5].value=="else":
            # If there is an else statement
            code.append("else:")
            code.append("\n")
            code.append(trans_compound(node.children[6]))
    return code
        
        
# iteration_statement
def trans_iteration(node):
    code = []
    if node.children[0].value == "for":
        '''
        初始化表达式
        while 条件表达式:
            循环体
            更新表达式
        '''
        code += trans_declaration_statement(node.children[2]) 
        code.append("\n")
        code.append("while")
        code += trans_expression(node.children[3])
        code.append(":")
        code.append("\n")
        inner = []
        inner += trans_compound(node.children[-1])
        print(node.children[4].key)
        if node.children[4].key == "expression":
            inner += trans_expression(node.children[4])
            inner.append("\n")
        code.append(inner)
    elif node.children[0].value == "while":
        '''
        while 表达式:
            循环体
        '''
        code.append("while")
        code += trans_expression(node.children[2])
        code.append(":")
        code.append("\n")
        code.append(trans_compound(node.children[-1]))
    return code

# jump_statement
def trans_jump(node):
    return [node.children[0].value]+trans_expression(node.children[1])+["\n"]

# assignment_statement
def trans_assignment(node):
    code = []
    for child in node.children:
        if isinstance(child,ExternalNode):
            if child.value == ";":
                code.append("\n")
            else:
                code.append(child.value)
        elif child.key == "assignment_operator":
            code.append(child.children[0].value)
        elif child.key == "expression":
            code += trans_expression(child)
        elif child.key == "array_index":
            code += trans_array(child)    
    return code

# array_index
def trans_array(node):
    code = []
    for child in node.children:
        if isinstance(child,ExternalNode):
            code.append(child.value)
        elif child.key == "array_index":
            code += trans_array(child)
        elif child.key == "expression":
            code += trans_expression(child)
    return code

# 规范风格和缩进，生成python代码
def format(code,tab=0):
    out = ""
    out += "\t" * tab
    for word in code:
        if isinstance(word, list):
            # 增加缩进
            out = out.rstrip(" \t")
            out += format(word,tab+1)
            out += "\t" * tab
        else:
            out += word
            # 换行后缩进
            if word == "\n":
                out += "\t" * tab
            else:
                out += " "
    # 去掉末尾多余的空格和tab
    out = out.rstrip(" \t")
    return out

if __name__ == '__main__':
    try:
        filename = input("Enter the filename: ")
        with open(filename, 'r', encoding='utf-8') as file:
            code = file.read()
        # 得到语法分析树
        tree = parser.parse(code)
        output_filename = "output.json"
        with open(output_filename, 'w') as output_file:
            output_file.write(tree.to_json())
        # 翻译
        code = translate(tree)
        print(code)
        # 规范风格和缩进
        out = format(code)
        with open("result.py", 'w') as result_file:
            result_file.write(out)
        
    except EOFError:
        print("EOFError")
