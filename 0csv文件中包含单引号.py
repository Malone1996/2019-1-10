f = open("1.csv", "a+")
# f.write("hello,world")#数据分割
f.write('"hello,world"')  # 数据未分割
f.close()
