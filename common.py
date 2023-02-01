import os
import shutil


# 首先使用 shutil.rmtree 删除目标目录，然后使用 shutil.copytree 将源目录复制到目标目录
# src 是要复制的源目录，
# dst 是要被覆盖的目标目录。
def overwrite_dir(src, dst):
    shutil.rmtree(dst)
    shutil.copytree(src, dst)


# 定义了 get_file_info 函数，该函数接受一个文件路径，并返回其文件名、模块名和模块路径。
def get_file_info(file_path):
    file_name = os.path.basename(file_path)
    module_name, _ = os.path.splitext(file_name)
    module_path = os.path.dirname(file_path)
    return file_name, module_name, module_path
