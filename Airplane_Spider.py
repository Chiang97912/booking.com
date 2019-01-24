# -*- coding: utf-8 -*-
import os
import csv
import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ua import chrome_ua_list


def spider(ap_date, depart_city, arrive_city):
    """

    The airplane spider of booking.com

    Arguments:
        ap_date {str} -- 出发日期
        depart_city {str} -- 出发城市
        arrive_city {str} -- 到达城市

    Returns:
        dict -- 航班信息
    """
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=%s" % random.choice(chrome_ua_list))
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(chrome_options=options)
    browser = webdriver.Firefox(firefox_options=options)
    data = []
    for yd_date in range(len(ap_date)):
        print('正在抓取%s->%s航班数据' % (code2city[depart_city], code2city[arrive_city]))
        url = "https://booking.kayak.com/flights/%s-%s/%s?sort=price_a" % (depart_city, arrive_city, ap_date[yd_date])
        try:
            browser.get(url)
        except Exception as e:
            print('time out after 30 seconds when loading page')
            browser.execute_script('window.stop()')
        WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'Base-Results-HorizonResult'))
        )
        element = browser.find_element_by_class_name("Base-Results-HorizonResult")

        for i in range(len(element)):
            att_id = element[i].get_attribute('id')  # 获取元素ID
            airline = element[i].find_element_by_xpath('//*[@id="%s-info-leg-0"]/div/div[1]/div[2]' % att_id).text  # 航空公司
            depart_time = element[i].find_element_by_xpath('//*[@id="%s-info-leg-0"]/div/div[2]/div[1]' % att_id).text  # 出发时间
            arrive_time = element[i].find_element_by_xpath('//*[@id="%s-info-leg-0"]/div/div[4]/div[1]' % att_id).text  # 到达时间
            price = element[i].find_element_by_xpath('//*[@id="%s-price-mb-above-button"]/div[1]/a[1]/span[1]' % att_id).text  # 价格
            json_data = {
                'airline': airline,
                'depart': code2city[depart_city],
                'dest': code2city[arrive_city],
                'depart_time': depart_time,
                'arrive_time': arrive_time,
                'price': price,
            }
            data.append(json_data)
        time.sleep(3)
    browser.quit()
    return data


if __name__ == '__main__':
    history_file = 'history.csv'  # 已经抓取城市列表
    if not os.path.exists(history_file):
        wh = open(history_file, 'w')
    else:
        wh = open(history_file, 'a')
    rh = open(history_file, 'r')
    reader = csv.reader(rh)
    history = [row for row in reader]
    rh.close()
    city2code = json.load(open('city2code.json'))
    code2city = {value: key for key, value in city2code.items()}
    citys = ['Beijing', 'Tokyo', 'Bangkok', 'Ottawa', 'Los Angeles', 'Alaska', 'Sydney', 'Suva', 'Oakland', 'Moscow', 'Stockholm', 'Geneva', 'Cape Town', 'Khartoum', 'Lima', 'Rio de Janeiro', 'Santiago']
    n = len(citys)
    """

    两两城市抓取航班信息
    """
    k = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                if [citys[i], citys[j]] not in history:
                    # 在此设置需要查取得日期
                    ap_date = ["2019-02-22"]
                    # 在此设置出发、到达城市 需要从携程查看相应城市代码
                    depart_city = city2code[citys[i]]
                    arrive_city = city2code[citys[j]]
                    data = spider(ap_date, depart_city, arrive_city)
                    result = dict()
                    result['%s->%s' % (citys[i], citys[j])] = data
                    with open('data/%s.json' % k, 'w') as f:
                        f.write(json.dumps(result))
                    wh.write('%s,%s\n' % (citys[i], citys[j]))
                k += 1
