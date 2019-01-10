import re

# salary = "工资面议"
# salary = "4-12千/月"
salary = "6.5千元以下/月"
# {0,1}=? 重复0次或1次
pattern = re.compile(r"\d+\.?\d*")  # 转义字符匹配.
result = pattern.findall(salary)
# if len(result)==2:
# if '-' in salary:

if len(result) == 2:
    min_salary = result[0]
    max_salary = result[1]
elif len(result) == 0:
    min_salary = "工资面议"
    max_salary = ""
    # else:
    #     if len(result) == 0:
    #         min_salary = "工资面议"
    #         max_salary = ""

else:
    min_salary = max_salary = result[0]

# if type(min_salary) and type(max_salary) == str:
#     min_salary = "工资面议"
#     max_salary = ""
if min_salary == '工资面议':
    pass
else:
    min_salary = float(min_salary)
    max_salary = float(max_salary)

if '千' in salary:
    min_salary = min_salary * 1000
    max_salary = max_salary * 1000

if '万' in salary:
    min_salary = min_salary * 10000
    max_salary = max_salary * 10000

if '年' in salary:
    # min_salary = int(min_salary / 12)  # int取整
    min_salary = min_salary // 12  # 两数双斜杠表示整除
    max_salary = max_salary // 12  # 两数双斜杠表示整除

print(min_salary, max_salary)
