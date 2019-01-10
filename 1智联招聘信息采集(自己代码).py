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
    for page in range(1, 1 + 1):
        new_url = f"https://search.51job.com/list/000000,000000,0000,00,9,99,{keyword},2,{page}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        content = requests.post(new_url)
        content.encoding = 'gbk'
        content = content.text
        root = etree.HTML(content)
        job_infos = root.xpath("//div[@class='dw_table']/div[@class='el']")
        for job_info in job_infos:
            job_name = job_info.xpath("p[contains(@class,'t1 ')]/span/a/@title")
            job_name = job_name[0]

            company = job_info.xpath("span[@class='t2']/a/@title")
            company = company[0]
            salary = job_info.xpath("span[@class='t4']/text()")
            salary = salary[0]
            place = job_info.xpath("span[@class='t3']/text()")
            place = place[0]
            place = place.split("-")[0]
            publish = job_info.xpath("span[@class='t5']/text()")
            publish = publish[0]
            if len(salary) == 0:
                salary.append("工资面议")
            salary = salary[0]
            # print(salary)

            # 薪资格式处理
            pattern = re.compile(r"\d+\.?\d*")  # 转义字符匹配.
            result = pattern.findall(salary)
            # if len(result)==2:
            # if '-' in salary:

            if len(result) == 2:
                min_salary = result[0]
                max_salary = result[1]
            elif len(result) == 0:
                min_salary = "工资面议"
                max_salary = "工资面议"
                # else:
                #     if len(result) == 0:
                #         min_salary = "工资面议"
                #         max_salary = ""

            else:
                min_salary = max_salary = result[0]

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

            # print(min_salary, max_salary)

            print(job_name, company, place, min_salary, max_salary, publish)

            f = open(f"{keyword}.csv", "a+", encoding="utf-8")
            info = [job_name, company, place, str(min_salary), str(max_salary), publish]  # 调用join方法列表中只能存放字符串
            f.write('"' + '","'.join(info) + '"' + "\n")

            # f = open(f"{keyword}.csv", "a+", encoding="utf-8")
            # f.write(f"{job_name},{company},{min_salary},{max_salary},{place},{publish}\n")
            # f.close()
