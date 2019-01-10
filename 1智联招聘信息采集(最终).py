import requests
from lxml import etree
import re
from bloomfilter import Bloomfilter
import os

repeat_count = 0
# 汉字编码  gbk gb18030 gb2312
keywords = ['python', 'html', 'php', 'java']

if os.path.exists("state.txt"):
    print("文件存在直接加载状态")
    bloom = Bloomfilter("state.txt")
else:
    print("文件不存在设置大小为1000000")
    bloom = Bloomfilter(1000000)

for keyword in keywords:
    f = open(f"{keyword}.csv", "w", encoding="gbk")
    url = f"https://search.51job.com/list/000000,000000,0000,00,9,99,{keyword},2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
    content = requests.get(url)
    content.encoding = content.apparent_encoding
    content = content.text
    root = etree.HTML(content)
    all_page = root.xpath("//div[@class='p_in']/span[@class='td']/text()")[0]
    pattern = re.compile(r"\d+")
    all_page = pattern.findall(all_page)[0]
    all_page = int(all_page)
    for page in range(1, all_page + 1):
        new_url = f"https://search.51job.com/list/000000,000000,0000,00,9,99,{keyword},2,{page}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        content = requests.get(new_url)
        content.encoding = "gbk"
        content = content.text
        root = etree.HTML(content)
        job_infos = root.xpath("//div[@class='dw_table']/div[@class='el']")

        if repeat_count >= 10:
            print("后面的数据都采集过了，不用再看了")
            break

        for job_info in job_infos:
            job_href = job_info.xpath("p[contains(@class,'t1')]/span/a/@href")[0]

            if bloom.test(job_href):
                print("数据存在", job_href)
                repeat_count += 1
                if repeat_count >= 10:
                    print("后面的数据都采集过了，不用再看了")
                    break
            else:
                print("数据不存在！", job_href)
                bloom.add(job_href)
                bloom.save("state.txt")

                job_name = job_info.xpath("p[contains(@class,'t1')]/span/a/@title")
                job_name = job_name[0]
                company = job_info.xpath("span[@class='t2']/a/@title")
                company = company[0]
                salary = job_info.xpath("span[@class='t4']/text()")
                if salary:
                    salary = salary[0]
                    pattern = re.compile(r"\d+\.?\d*")
                    result = pattern.findall(salary)
                    if len(result) == 2:
                        min_salary = result[0]
                        max_salary = result[1]
                    else:
                        min_salary = max_salary = result[0]
                    min_salary = float(min_salary)
                    max_salary = float(max_salary)
                    if '千' in salary:
                        min_salary = min_salary * 1000
                        max_salary = max_salary * 1000
                    elif '万' in salary:
                        min_salary = min_salary * 10000
                        max_salary = max_salary * 10000
                    if '年' in salary:
                        min_salary = int(min_salary / 12)
                        max_salary = max_salary // 12
                else:
                    salary = "薪资面议"
                    min_salary = max_salary = 0
                place = job_info.xpath("span[@class='t3']/text()")
                place = place[0]
                place = place.split("-")[0]
                publish = job_info.xpath("span[@class='t5']/text()")
                publish = publish[0]
                min_salary = str(min_salary)
                max_salary = str(max_salary)
                print(job_name)
                info = [job_name, company, place, salary, min_salary, max_salary, publish]
                f.write('"' + '","'.join(info) + '"' + "\n")
                f.flush()
    f.close()