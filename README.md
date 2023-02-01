# replacer
将给定源代码文件中的 import 语句进行转换


app.py

从codes目录中读取代码，并使用modify_code函数进行修改，然后将修改后的代码写入到同一个文件中。最后，执行该文件中的代码。

代码中用到了三个函数：modify_code、write_to_file、execute_code：

modify_code：通过修改代码中的import语句，使得代码可以引入额外的模块

write_to_file：将修改后的代码写入到指定的文件中

execute_code：执行代码中的代码，并输出执行结果

最后，主函数main()调用这三个函数，实现了整个流程。

reset.py

会执行 overwrite_dir 函数，该函数将 "temp" 目录中的内容覆盖到 "codes" 目录中

replacer.py

实现了对 Python 源代码中 import 语句的替换。

它定义了一个名为 ImportFromReplacer 的类，该类继承自 ast.NodeTransformer，用于替换导入模块中的 import 语句。
该类的构造函数 init 接收两个参数：module_prex 和 files。其中 module_prex 表示需要在 import 语句的前面加的字符串，而 files 则是包含需要修改的文件的路径的列表。

该类实现了 visit 和两个方法：visit_Import 和 visit_ImportFrom。

visit_Import 方法用于替换语句 “import config” 为 “from codes import config”。

visit_ImportFrom 方法用于替换语句 “from handles import tick” 为 “from codes.handles import tick” 和 “from calc import add” 为 “from codes.calc import add”。

方法 replacer_Subtree 用于替换导入模块中的 import 语句。

最后，modify_code 函数用于对代码进行修改，它接收三个参数：需要修改的代码，module_prex 和 subfiles。

还需要考虑以下方面：

代码安全：确保对输入文件的操作是安全的，避免破坏或损害原始文件。

错误处理：处理可能发生的异常，例如文件不存在、语法错误等。

性能：在大型代码库中，代码的性能可能是一个问题，因为它可能需要在大量的代码文件上运行。

测试：编写单元测试来验证代码的正确性，以确保修改不会对代码造成意外的影响。
