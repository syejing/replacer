import ast
import importlib.util
from common import get_file_info
'''
将给定源代码文件中的 import 语句进行转换。

定义了一个类 ImportFromReplacer，该类继承自 ast.NodeTransformer，用于替换导入模块中的 import 语句。

类的构造函数 __init__ 接收两个参数：module_prex 和 files。

该类实现了 visit 和两个方法：visit_Import 和 visit_ImportFrom。

visit_Import 方法用于替换语句 
"import config" 为 "from codes import config"。

visit_ImportFrom 方法用于替换语句 
"from handles import tick" 为 "from codes.handles import tick" 
"from calc import add" 为 "from codes.calc import add"。

方法 replacer_Subtree 用于替换导入模块中的 import 语句。
'''


class ImportFromReplacer(ast.NodeTransformer):
    def __init__(self, module_prex, files):
        self.module_prex = module_prex
        self.files = files

    # 用于替换导入模块中的 import 语句
    def replacer_Subtree(self, module, name):
        # 使用 find_spec() 获取子模块的文件地址
        if module is not None:
            module_path = f"{self.module_prex}.{module}.{name}"
        else:
            module_path = f"{self.module_prex}.{name}"
        spec = importlib.util.find_spec(module_path)
        if spec is not None:
            # 使用 ast.parse() 解析子模块的代码
            tree = ast.parse(spec.loader.get_source(spec.name))
            tree = self.visit(tree)
            with open(spec.origin, 'w') as f:
                f.write(ast.unparse(tree))

    def visit(self, node):
        if isinstance(node, ast.ImportFrom):
            node = self.visit_ImportFrom(node)
        elif isinstance(node, ast.Import):
            node = self.visit_Import(node)
        elif isinstance(node, ast.Module):
            for index, child in enumerate(node.body):
                child = self.visit(child)
                if child:
                    node.body[index] = child
        return node

    # import config => from codes import config，config是Module
    def visit_Import(self, node):
        for file_path in self.files:
            _, module_name, _ = get_file_info(file_path)
            for alias in node.names:
                if alias.name == module_name:
                    self.replacer_Subtree(None, alias.name)
                    new_node = ast.ImportFrom(module=self.module_prex,
                                              names=[ast.alias(name=alias.name, asname=None)], level=0)
                    return new_node
        return None

    # from handles import tick => from codes.handles import tick，tick是Module
    # from calc import add => from codes.calc import，add是Function
    def visit_ImportFrom(self, node):
        for file_path in self.files:
            _, module_name, module_path = get_file_info(file_path)
            if node.module == module_path:
                for alias in node.names:
                    if alias.name == module_name:
                        self.replacer_Subtree(node.module, alias.name)
                        node.module = f"{self.module_prex}.{node.module}"
                        return node
                break
            elif node.module == module_name:
                self.replacer_Subtree(None, node.module)
                node.module = f"{self.module_prex}.{node.module}"
                return node
        return None


def modify_code(code, module_prex, subfiles):
    """
    修改代码中的导入语句
    :param code: 代码字符串
    :param module_prex: 模块前缀
    :param subfiles: 子文件列表
    :return: 修改后的代码字符串
    """
    try:
        # 使用 ast.parse() 解析代码
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"Error parsing code: {e}")
        return code

    if len(tree.body) <= 0:
        print("Error: Code body is empty")
        return code
    else:
        # 使用 ImportFromReplacer 类来替换代码中的导入语句
        replacer = ImportFromReplacer(module_prex, subfiles)
        replacer.visit(tree)
        # 使用 ast.fix_missing_locations() 补充代码中缺少的位置信息
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)
