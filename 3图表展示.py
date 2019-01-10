#  城市岗位分布  饼状图 柱状图 直方图 折线图....
city_count = {
    '上海': 1500,
    '北京': 2000,
    '深圳': 1800,
    '武汉': 50,
}

# 导入饼图Pie
from pyecharts import Pie

# 设置行名
columns = city_count.keys()
# 设置数据
data1 = city_count.values()
# # 设置主标题与副标题，标题设置居中，设置宽度为900
pie = Pie("饼状图", "各城市工作数量", title_pos='center', width=900)
# 加入数据，设置坐标位置为【75，50】，上方的colums选项取消显示，显示label标签
pie.add("工作数量", columns, data1, center=[75, 50], is_legend_show=False, is_label_show=True)
# 保存图表
pie.render("饼状图.html")

from pyecharts import Line

columns = ["1月1日", "1月2日", "1月3日", "1月4日"]
data1 = [100, 50, 150, 200]
line = Line("折线图", "一年的降水量与蒸发量")
# is_label_show是设置上方数据是否显示
line.add("工作数量", columns, data1, is_label_show=True)
line.render("折线图.html")
