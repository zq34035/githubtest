import urllib.request as req
from bs4 import BeautifulSoup

import requests
import os
import time
import threading


# from multiprocessing import Pool

class PPT():
    """
    整个的爬虫类
    """

    def __init__(self):
        self.baseUrl = "http://www.ypppt.com/moban/"
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        self.num = 0
        self.page_count = 0

    def getResponseContent(self, url):
        """
        获取页面请求信息
        """
        try:
            req_str = req.Request(url, headers=self.header)
            response = req.urlopen(req_str, timeout=10)
        except Exception as e:
            print(e)
            print("请求失败")
        else:
            return response.read().decode("utf-8")

    def getPageInfo(self, url):
        """
        获取页面数量
        """
        html = self.getResponseContent(url)
        soup = BeautifulSoup(html, "html.parser")

        page_info = soup.find("div", attrs={"class": "page-navi"})
        a_list = page_info.find_all("a")
        last_a = a_list[-1]
        href = last_a["href"]
        page_count = href.replace("list-", "").replace(".html", "")

        self.page_count = int(page_count)

    def spyder(self, url):
        """
        解析页面
        """
        html = self.getResponseContent(url)
        soup = BeautifulSoup(html, "html.parser")
        divs = soup.find_all("div", attrs={"class": "wrapper"})

        div = divs[1]

        ul = div.find_all("ul")[3]
        li_list = ul.find_all("li")
        ppt_link_list = []
        for li in li_list:
            aTag_href = li.find_all("a")[1]["href"]
            ppt_link = "http://www.ypppt.com" + aTag_href
            ppt_link_list.append(ppt_link)
            self.PPT_info(ppt_link)

            # self.PPT_info(ppt_link)
            threads = []
            if len(threads) < 5:
                threads.append(threading.Thread(target=self.PPT_info, args=(ppt_link,)))

            for thread in threads:
                thread.start()
                if not threads[0].isAlive():
                    thread.remove(thread)

        # pool = Pool(processes=1)
        # pool.map(self.PPT_info, ppt_link_list)
        # # 方法， 参数

    def PPT_info(self, url):
        """
        PPT 下载页面
        """
        html = self.getResponseContent(url)
        soup = BeautifulSoup(html, "html.parser")
        down_button = soup.find("a", attrs={"class": "down-button"})["href"]
        down_url = "http://www.ypppt.com" + down_button
        self.DL_PPT(down_url)
        time.sleep(1)

    def DL_PPT(self, url):
        """
        下载ppt页面
        """
        html = self.getResponseContent(url)
        soup = BeautifulSoup(html, "lxml")
        ul = soup.find("ul", attrs={"class": "down clear"})
        rar_link = ul.find_all("a")[0]["href"]

        # 个别的ppt下载页面不是绝对地址，需要手动添加
        if rar_link.find(".com") > 0:
            pass
        else:
            rar_link = "http://www.ypppt.com" + rar_link
        ppt_name = soup.find("h1").text
        if ppt_name.find("-") > 0:
            ppt_name = ppt_name.split("-")[0].strip()
        f = requests.get(rar_link, headers=self.header)
        with open(ppt_name + ".rar", "wb") as rar:
            self.num += 1
            print("正在下载第 {} 个PPT模板...".format(self.num))
            rar.write(f.content)
        print(ppt_name, "下载完成......")


if __name__ == "__main__":
    print("Downloadings begin...")
    ppt = PPT()
    start_time = time.time()
    ppt.getPageInfo(ppt.baseUrl)
    # 解析第一个页面，因为其url与之后的有所不同
    ppt.spyder(ppt.baseUrl)

    for page in range(2, ppt.page_count + 1):
        url = ppt.baseUrl + "list-{}.html".format(page)
        ppt.spyder(url)
        time.sleep(1)
        print(url, "下载完成")

    end_time = time.time()
    print("用时： ", end_time - start_time)


