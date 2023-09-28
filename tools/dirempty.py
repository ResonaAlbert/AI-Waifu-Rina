import os
def check_dir_empty(path):
    """
    判断指定文件夹是否为空

    Args:
        path: 指定文件夹的路径

    Returns:
        True 表示文件夹为空，False 表示文件夹不为空
    """

    if os.path.isdir(path) and os.listdir(path) == []:
        return True
    else:
        return False