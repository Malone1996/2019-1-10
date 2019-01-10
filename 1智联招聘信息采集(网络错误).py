import requests
from lxml import etree
import re

keywords = ['python', 'html', 'php', 'java']
for keyword in keywords:
    url = f"https://search.51job.com/list/000000,000000,0000,00,9,99,{keyword},2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
    content = requests.get(url)
    content.encoding = content.apparent_encoding
    content = content.text
    root = etree.HTML(content)
    all_page = root.xpath("//div[@class='p_in']/span[@class='td']/text()")[0]
    # 1
    # all_page = all_page.replace("共", "").replace("页，到第", "")
    pattern = re.compile(r"\d+")
    all_page = pattern.findall(all_page)[0]
    all_page = int(all_page)

    for page in range(1, all_page + 1):
        new_url = f"https://search.51job.com/list/000000,000000,0000,00,9,99,{keyword},2,{page}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        content = requests.get(new_url)
        content.encoding = 'gbk'  # 查看网页编码
        content = content.text
        root = etree.HTML(content)
        job_infos = root.xpath("//div[@class='dw_table']/div[@class='e1']")  # 按行找数据
        for job_info in job_infos:
            job_name = job_info.xpath("p[contains(@class,'t1 ')]/span/a/@title")  # p标签属性下包含...
            company = job_info.xpath("span[@class='t2']/a/@title")
            salary = job_info.xpath("span[@class='t4']/text()")
            place = job_info.xpath("span[@class='t3']/text()")
            publish = job_info.xpath("span[@class='t5']/text()")
            print(job_name, company, salary, place, publish)
