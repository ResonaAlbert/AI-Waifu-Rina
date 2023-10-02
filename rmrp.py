import re
def remove_brackets_and_replace(string):
  
  """
  去掉字符串中括号里的文本，并替换“哥哥”成“欧尼酱”。

  Args:
    string: 待处理的字符串。

  Returns:
    处理后的字符串。
  """

  # 去掉括号里的文本
  string = re.sub(r"（.*?）", "", string)
  string = re.sub(r"\(.*?\)", "", string)
  string = re.sub(r'\n', "", string)
  string = re.sub(r'\\', "", string)
  string = re.sub(r"n", "", string)
  return string
