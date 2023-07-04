from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time,random
from threading import Thread
import csv,re
import os

# Get the directory of the Python script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Create the relative file path for the CSV file
csv_file_path = os.path.join(script_dir, "机房节能改造.csv")

# Open the CSV file
head = ["采购需求单位", "时间", "网址",  "标题", "内容", "投标截止时间", "地址", "项目预算"]
f = open(csv_file_path, "a", newline='')#, encoding="utf-8"

f_csv = csv.writer(f)
f_csv.writerow(head)

#启动Firefox浏览器并请求初始url
from selenium.webdriver.firefox.options import Options

# Set the path to the Firefox binary
firefox_binary_path = r"C:\Users\yiou.sun\AppData\Local\Mozilla Firefox\firefox.exe"  

# Configure Firefox options
firefox_options = Options()
firefox_options.binary_location = firefox_binary_path

# Create the Firefox driver with the specified binary path
driver = webdriver.Firefox(options=firefox_options)
data= driver.get("https://urldefense.com/v3/__https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=16__;!!C8PT2x6w!vRAbg1F-usd1TH9F4jQe-q5GOscbcqD1ylGJEOUJ2LqIDqmi8f4EqRg11l9UVGyYqIrtcEPeb2seaznEbvh54IyI$ ")
wait = WebDriverWait(driver, 10) #页面加载
driver.maximize_window()  #窗口最大化
time.sleep(2)

submit_1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="caigou"]')))
submit_1.click()  #点击
#搜索“数据中心”并点击

input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="title"]')))
input.send_keys('机房节能改造') #输入关键字
submit_2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search"]')))
submit_2.click()  #搜索
time.sleep(10)

#获取页面当中的页码信息

html = driver.page_source
doc = pq(html, parser='html')
data = doc('#pageid2 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6)')
page = data.find('span:nth-child(1)').text()

#正则化得到页码
pattern1 = re.compile(r'.*?数据(.*?)页', re.S)
page1 = re.findall(pattern1, page)
r = "[\\\[\]',/]"
page1 = re.sub(r, '', str(page1))
print(page1)
url_list = {}

# 获取公告内容
def get_text():
    for k, v in url_list.items():
        driver.get(v)
        driver.implicitly_wait(30)
        time.sleep(0.5)
        title = driver.find_element(By.XPATH, '//*[@id="title"]').text
        print(title)
        text1 = driver.find_element(By.XPATH, '//*[@id="contentInfo"]').text
        text1 = text1.replace("\u2003", "")
        text1 = text1.replace("\xa5", "")
        text1 = text1.replace("\u2022", "")
        text1 = text1.replace("\xb3", "")
        text1 = text1.replace("\u2611", "")
        text1 = text1.replace("\xb2", "")
        text1 = text1.replace("\uf06c", "")
        text1 = text1.replace("\xad", "")
        text1 = text1.replace("\uff61", "")
        text1 = text1.replace("\xd8", "")
        text1 = text1.replace("\uf0b2", "")
        text1 = text1.replace("\xf8", "")
        text1 = text1.replace("\u2002", "")
        text1 = text1.replace("\u200d", "")
        #print(text1)

#正则化需要的信息（"项目预算", "地址", "项目联系人", "投标截止时间", "招标文件获取时间"）

        # 提取投标截止时间
        pattern1 = re.compile(r'.截止时间为(.*?分).', re.S)
        project_survey = re.findall(pattern1, text1)
        r = "[\\\[\]'\",：（应答截止间，下同）为简称“”]"
        project_time = re.sub(r, '', str(project_survey))
        #限制字符串长度
        if len(project_time) > 20:
            project_time = "无"
        else:
            project_time = project_time
        if len(str(project_time)) <= 0:
            project_time = "无"
        else:
            project_time = project_time
        print(project_time)

        # 提取地址
        pattern2 = re.compile(r'.址：(.*?号).', re.S)
        project_address = re.findall(pattern2, text1)
        if project_address == []:
            project_address = []
        else:
            r = "[\\\[\]'\"：,]"
            project_address = re.sub(r, '', str(project_address[0]))

        if project_address == []:
            pattern9 = re.compile(r'.址：(.*?司).', re.S)
            project_address = re.findall(pattern9, text1)
        else:
            project_address = project_address
        #限制字符串长度
        if len(project_address) > 30:
            project_address = "无"
        else:
            project_address = project_address
        if len(str(project_address)) <= 0:
            project_address = "无"
        else:
            project_address = project_address
        r = "[\\\[\]'\",：]"
        project_address = re.sub(r, '', str(project_address))
        print(project_address)

        ## 提取金额
        pattern3 = re.compile(r'.金额(.*?元)', re.S)
        project_money = re.findall(pattern3, text1)

        if project_money == []:
            pattern4 = re.compile(r'.预算(.*?元)', re.S)
            project_money = re.findall(pattern4, text1)
        elif project_money == []:
            pattern5 = re.compile(r'.预估金额(.*?元)', re.S)
            project_money = re.findall(pattern5, text1)
        elif project_money == []:
            pattern6 = re.compile(r'.最高投标限价(.*?元)', re.S)
            project_money = re.findall(pattern6, text1)
        elif project_money == []:
            pattern7 = re.compile(r'.最高应答限价(.*?元)', re.S)
            project_money = re.findall(pattern7, text1)
        elif project_money == []:
            pattern8 = re.compile(r'.最高限价(.*?元)', re.S)
            project_money = re.findall(pattern8, text1)
        else:
            project_money = project_money
        r = "[\\\[\]'\"：]"
        project_money = re.sub(r, '', str(project_money))
        project_money = "号" + project_money + "号"

        #正则化金额数字
        pattern9 = re.compile(r'\D(\d.*?元).', re.S)
        project_money = re.findall(pattern9, project_money)
        if project_money == [] :
            project_money = project_money
        else:
            project_money = project_money[0]
        r = "[\\\[\]'\"：,（） 向下取整至,元最高限价本项目设置最高限价处汇聚机房预算金额为不低于采购包应答框架协议上年共计含税总保证人民币贰投资约】]"
        project_money = re.sub(r, '', str(project_money))

        #限制字符串长度
        if len(project_money) > 20:
            project_money = 0
        else:
            project_money = project_money
        if len(str(project_money)) <= 0:
            project_money = 0
        else:
            project_money = project_money
        #去除特殊情况
        if str(project_money).count(".") >= 2:        #查找"."字符的个数
            project_money = str(project_money)[2:]    #从第3位获取字符
        else:
            project_money = project_money
        if str(project_money).count("，") >= 1:
            project_money = 0
        else:
            project_money = project_money
        if str(project_money).count("。") >= 1:
            project_money = 0
        else:
            project_money = project_money
        if str(project_money).count("、") >= 1:
            project_money = 0
        else:
            project_money = project_money
        if str(project_money).count("n") >= 1:
            project_money = 0
        else:
            project_money = project_money
        #单位转化
        if str(project_money)[-1:] == "亿":
            project_money = float(project_money[:-1]) * 100000000
        elif str(project_money)[-1:] == "万":
            project_money = float(project_money[:-1]) * 10000
        else:
            project_money = project_money

        for i in str(project_money):
            if u'\u4e00' <= i <= u'\u9fff':
                project_money = 0
            else:
                project_money = project_money

        print(project_money)

        f_csv.writerow([title, text1, project_time, project_address, project_money])



class Gte:
    i = 0
    def get(self, datas):
        time.sleep(2)
        results = driver.find_elements(By.XPATH, '//table[@class="zb_result_table"]/tbody//tr')
        for result in results[2:]:
            ID = result.get_attribute('onclick')
            g_id = re.findall(r"selectResult.*?'(.*?)'.*?", str(ID))[0]    #正则化出链接的编号
            # text = result.find_element(By.XPATH, './td[3]/a').text
            title = result.find_element(By.XPATH, './td[1]').text          #采购单位
            url_list[g_id] = "https://urldefense.com/v3/__https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=__;!!C8PT2x6w!vRAbg1F-usd1TH9F4jQe-q5GOscbcqD1ylGJEOUJ2LqIDqmi8f4EqRg11l9UVGyYqIrtcEPeb2seaznEbqnyep1p$ " + g_id       #网址
            wz = url_list[g_id]
            g_time = result.find_element(By.XPATH, './td[4]').text          #时间
            heads = [(title, g_time, wz)]
            f_csv.writerows(heads)
            # 下一页
        #driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/table/tbody/tr/td[2]/div[2]/div/div/table/tbody/tr/td/table/tbody/tr/td[4]/a/span').click()
        # 等待
        driver.implicitly_wait(20)
        time.sleep(0.5)
        self.i += 1
        # 爬取156页
        if self.i < 6:
            self.get(driver)

# 线程
def main():
    thread_list = []
    app = Gte()
    t1 = Thread(app.get(data))
    t2 = Thread(get_text())
    thread_list.append(t1)
    thread_list.append(t2)
    for i in thread_list:
        i.start()


if __name__ == "__main__":
    main()
