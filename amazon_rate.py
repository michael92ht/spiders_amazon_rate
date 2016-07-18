# -*- coding: utf-8 -*-
# coding=gbk

import requests
from BeautifulSoup import BeautifulSoup
import re


# 根据亚马逊商品的全部评价页面url,找到其单个评论页url模式
# 亚马逊商品评价页面的url：https://www.amazon.cn/XX/product-reviews/XX/ + ?pageNumber= X
def get_rate_url(url):
    return url[:(url.find("ref"))] + r"?pageNumber="


# 查询所有page数量
def get_total_page(rate_url):
    rate_url += "1"
    req = requests.get(rate_url)
    data = req.text
    context = re.findall(r'totalReviewCount">[0-9]+', data)[0]
    totalReviewCount = context.split('>')[1]
    return int(totalReviewCount) / 10 + 1


# 查询指定页面的评论
def get_rate_from_index(rate_url, page_number):
    rate_url += str(page_number)
    req = requests.get(rate_url)
    content = req.text
    soup = BeautifulSoup(content)
    index = 0
    for tag in soup.findAll('span'):
        if tag.has_key('class'):
            if tag['class'] == 'a-size-base review-text':
                rate = str(tag)
                left = rate.find(">")
                right = rate.find("</", left)
                rate = rate[left+1:right].replace("<br />", "\n")
                print ("comment number: " + str(index + (page_number-1) * 10 + 1))
                print (rate)
                index += 1


# 根据商品的评价页面和页面数量，对商品的所有评论进行爬虫
def get_rate(rate_url, total_page):
    error_page = []  # 由于会随机出现错误，导致部分页面无法获取，用来记录出现错误的页面
    for index in range(1, total_page+1):  # 所有的页面的评论内容进行提取
        try:
            get_rate_from_index(rate_url, index)
        except Exception,ex:               # 若此页面无法提取，记录到 error_page中
            error_page.append(index)

    while len(error_page) != 0:             # 如果有未提取的页面，就一直提取该页面，直至 error_page为0
        pages = [i for i in error_page]
        error_page = []
        for page in pages:
            try:
                get_rate_from_index(rate_url, page)
            except Exception,ex:
                error_page.append(index)
    print "------------------------finshed!-------------------------------"



if __name__ == "__main__":
    url = r"https://www.amazon.cn/Canon-%E4%BD%B3%E8%83%BD-EOS-700D-%E6%95%B0%E7%A0%81%E5%8D%95%E5%8F%8D%E5%A5%97%E6%9C%BA/product-reviews/B00C93NJCM/ref=dpx_acr_txt?showViewpoints=1"
    rate_url = get_rate_url(url)
    total_page = get_total_page(rate_url)
    get_rate(rate_url, total_page)