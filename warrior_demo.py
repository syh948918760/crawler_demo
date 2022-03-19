from selenium import webdriver
import time
import datetime
import smtplib, ssl
from apscheduler.schedulers.blocking import BlockingScheduler

import warnings
warnings.filterwarnings('ignore')

def search_product(driver):
    time.sleep(8)
    message = ""
    # driver.find_elements_by_class_name('color-selector-button')[1].click()
    rst_flag = False
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print(ts)
    for btn in driver.find_elements_by_class_name('size-selector-button')[1:4]:
        btn.click()
        cur_val = driver.find_element_by_class_name('size-selector-value').text
        flag = cur_val == btn.accessible_name.split(' ')[-1]
        label = 'YES' if flag else 'NO'
        print(btn.accessible_name, label)
        message += "{}: {}\n".format(btn.accessible_name, label)
        rst_flag |= flag
    return message, rst_flag


def notifiy(message):
    l = []
    with open('pwd.txt', 'r') as f:
        for line in f.readlines():
            l.append(line)
        account = l[0][:-1]
        pwd = l[1]
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = account
    receiver_email = account
    password = pwd

    msg = """\
    Subject: Warriors Jerseys Update 

{}
    """.format(message)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg)


def search_and_notify():
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }

    options.add_argument('--headless')  # 无界面

    driver = webdriver.Chrome(executable_path='/usr/local/chromedriver/chromedriver', chrome_options=options)
    driver.get(
        'https://store.nba.com/golden-state-warriors/mens-golden-state-warriors-stephen-curry-fanatics-branded-royal-fast-break-replica-player-jersey-icon-edition/t-25478496+p-703951021365+z-8-2082842818?_ref=p-DLP:m-GRID:i-r0c0:po-0')

    message, flag = search_product(driver)
    driver.close()

    # 邮件通知
    if flag:
        notifiy(message)


def dojob():
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # 添加任务,时间间30mins
    scheduler.add_job(search_and_notify, 'interval', seconds=60 * 5, next_run_time=datetime.datetime.now())
    scheduler.start()


dojob()
