import langid

def detect_language(text):
  """
  检测输入文本的语种。

  Args:
    text: 输入文本。

  Returns:
    文本的语种，如果无法识别，返回 None。
  """

  # 使用 langid 库进行语言检测。
  result = langid.classify(text)

  # 如果无法识别，返回 None。
  if result is None:
    return None

  # 返回识别到的语言。
  return result[0]


# 测试
print(detect_language("Hello, world!"))
# 输出：en

print(detect_language("你好，世界！"))
# 输出：zh-cn
