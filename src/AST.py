# coding=utf-8
# 抽象语法树定义
# 非终结符: InternalNode 类型对象
# 终结符: ExternalNode 类型对象
import json
import yaml

# 抽象语法树 结点基类
class Node:
    def __init__(self, key):
        self.key = str(key)

    def to_dict(self):
        return {"type": self.key}
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)
    
    def to_yaml(self):
        return yaml.dump(self.to_dict(), default_flow_style=False)


# 抽象语法树 内部结点类
# self.key {String}  符号类型
# self.children {List of InternalNode or ExternalNode}  子结点列表
class InternalNode(Node):
    def __init__(self, key, children):
        Node.__init__(self, key)
        self.children = children
        for i in range(len(self.children)):
            if not isinstance(self.children[i], Node):
                self.children[i] = ExternalNode(str(self.children[i]), str(self.children[i]))

    def to_dict(self):
        return {"type": self.key, "children": [child.to_dict() for child in self.children]}
    
    def __str__(self):
        return ' '.join(map(str, self.children))


# 抽象语法树 外部结点类
# self.key {String}  符号类型
# self.value {String}  终结符-值
class ExternalNode(Node):
    def __init__(self, key, value):
        Node.__init__(self, key)
        self.value = str(value)

    def to_dict(self):
        return {"type": self.key, "value": self.value}
    
    def __str__(self):
        return self.value