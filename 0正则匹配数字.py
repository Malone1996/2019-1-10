import re

pattern = re.compile(r"\d{1,}")  # {1,}等价于+
result = pattern.findall("共10页,当前是第2页")
print(result)
