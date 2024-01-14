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
            statment_list = child.children[1]
            if statment_list.key == "statement_list":
                code.append(trans_statement_list(statment_list))
            else:
                code.append(['pass','\n'])
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

# statement_list
def trans_statement_list(node):
    code = []
    for child in node.children:
        if child.key == "statement_list":
            code += trans_statement_list(child)
        else:
            grandchild = child.children[0]
            if grandchild.key == "declaration_statement":
                code += trans_declaration(grandchild)
            elif grandchild.key == "expression_statement":
                code += trans_expression(grandchild)
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
def trans_declaration(node):
    # todo
    return []

# expression_statement
def trans_expression(node):
    # todo
    return []

# selection_statement
def trans_selection(node):
    # todo
    return []

# iteration_statement
def trans_iteration(node):
    # todo
    return []

# jump_statement
def trans_jump(node):
    # todo
    return []

# assignment_statement
def trans_assignment(node):
    # todo
    return []

# 规范风格和缩进，生成python代码
def format(code,tab=0):
    out = ""
    out += "\t" * tab
    for word in code:
        if isinstance(word, list):
            # 增加缩进
            out += format(word,tab+1)
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
