from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import pandas as pd
import re
# href=[]
# videos=[]
# driver = webdriver.Chrome('chromedriver.exe')
# url="https://www.youtube.com/channel/UC-Bsa2ivAGWq7bsSPrPGFVA/videos"
# driver.get(url)
# time.sleep(2)

# rcv_data = driver.page_source
# soupData = BeautifulSoup(rcv_data, "html.parser")
# body = driver.find_element_by_tag_name('body')#스크롤하기 위해 소스 추출

# num_of_pagedowns = 6
# #10번 밑으로 내리는 것
# while num_of_pagedowns:
#     body.send_keys(Keys.PAGE_DOWN)
#     time.sleep(2)
#     num_of_pagedowns -= 1
# time.sleep(2)

# for storelist in soupData.findAll('div', {'id':'contents'}):
#     for link in storelist.find_all('a'):
#         href.append(link.get('href'))
# print(href)
# for i in range(0,len(href),2):
#     videos.append(href[i])
# print(len(videos))
# # driver.find_element_by_css_selector("#video-title").click() #CSS_selector 가 다 갖고옴.
# time.sleep(1000)

start_url  = 'https://www.youtube.com/channel/UC5XuQ-xiWAB6f-qu6gJMDBQ/videos'
youtube_url="https://www.youtube.com/"
delay=3
browser = webdriver.Chrome('chromedriver.exe')
browser.implicitly_wait(delay)

browser.get(start_url)  
browser.maximize_window()

body = browser.find_element_by_tag_name('body')#스크롤하기 위해 소스 추출

num_of_pagedowns = 6
#10번 밑으로 내리는 것
while num_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    num_of_pagedowns -= 1

html0 = browser.page_source
html = BeautifulSoup(html0,'html.parser')
video_ls=html.find_all('ytd-grid-video-renderer',{'class':'style-scope ytd-grid-renderer'})
b = html.find('div',{'id':'items','class':'style-scope ytd-grid-renderer'})

tester_url = []
for i in range(len(video_ls)):
    url = youtube_url+video_ls[i].find('a',{'id':'thumbnail'})['href']
    tester_url.append(url)
print(len(tester_url))
time.sleep(1.5)
video_info = pd.DataFrame({'title':[],
                          'view':[],
                          'like':[],
                          'unlike':[],
                          'comment':[],
                          'date':[]})

for i in range(0,200):
    browser.get(tester_url[i])
    time.sleep(1.5)

    body = browser.find_element_by_tag_name('body')#스크롤하기 위해 소스 추출

    num_of_pagedowns = 1
    while num_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1.5)
        num_of_pagedowns -= 1

    time.sleep(1.5)

    soup0 = browser.page_source
    time.sleep(1.5)
    soup = BeautifulSoup(soup0,'html.parser')
    
    info1 = soup.find('div',{'id':'info-contents'})
    
    try:
        comment = soup.find('yt-formatted-string',{'class':'count-text style-scope ytd-comments-header-renderer'}).text
    except:
        comment = '댓글x'
    title = info1.find('h1',{'class':'title style-scope ytd-video-primary-info-renderer'}).text
    view =info1.find('yt-view-count-renderer',{'class':'style-scope ytd-video-primary-info-renderer'}).find_all('span')[0].text
    like = info1.find('div',{'id':'top-level-buttons'}).find_all('yt-formatted-string')[0].text
    unlike = info1.find('div',{'id':'top-level-buttons'}).find_all('yt-formatted-string')[1].text
    date = info1.find('div',{'id':'date'}).find_all('yt-formatted-string')[0].text
    print(title)

    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\u2640-\u2642"
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"
            u"\U0001F198"
            u"\U0001F947"
            u"\U0001F940"
            u"\U0001F98B"
            u"\U0001F98E"
            u"\U0001F92F"
            u"\U0001F923"
            u"\U0001F959"
            u"\U0001F96A"
            u"\U0001F9DF"
            u"\U0001F9E1"
            u"\U0001F957"
            u"\U0001F926"
            u"\U0001F9DA"
            u"\xa0"
            u"\U0001F9D8"
            u"\U0001F9C4"
            u"\U0001F99C"
            "]+", flags=re.UNICODE)

#분석에 어긋나는 불용어구 제외 (특수문자, 의성어)
    han = re.compile(r'[\n\r#\ufe0f\u200d\U0001f487]')

    comment_result = []

    tokens = re.sub(emoji_pattern,"",title)
    tokens = re.sub(han,"",tokens)
    comment_result.append(tokens)

    insert_data = pd.DataFrame({'title':comment_result,
                          'view':[view],
                          'like':[like],
                          'unlike':[unlike],
                          'comment':[comment],
                          'date':[date]})
    print(insert_data,"\n")
    video_info = video_info.append(insert_data)

video_info.to_csv('영상정보_흥삼(200개).csv',index=False,encoding='CP949')

# comment_list=[]
# for i in video_info["title"]:
#     comment_list.append(i)
# #이모티콘 제거
# emoji_pattern = re.compile("["
#         u"\U0001F600-\U0001F64F"  # emoticons
#         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#         u"\U0001F680-\U0001F6FF"  # transport & map symbols
#         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#         u"\U00002702-\U000027B0"
#         u"\U000024C2-\U0001F251"
#         u"\U0001f926-\U0001f937"
#         u"\U00010000-\U0010ffff"
#         u"\u2640-\u2642"
#         u"\u2600-\u2B55"
#         u"\u200d"
#         u"\u23cf"
#         u"\u23e9"
#         u"\u231a"
#         u"\ufe0f"
#         u"\u3030"
#         "]+", flags=re.UNICODE)

# #분석에 어긋나는 불용어구 제외 (특수문자, 의성어)
# han = re.compile(r'[ㄱ-ㅎㅏ-ㅣ!?~,".\n\r#\ufe0f\u200d\U0001f487]')

# comment_result = []

# for i in comment_list:
#     tokens = re.sub(emoji_pattern,"",i)
#     tokens = re.sub(han,"",tokens)
#     comment_result.append(tokens)
# print(comment_result)
# comment_result = pd.DataFrame(comment_result, columns=["title"])
# print(comment_result)

# result3 = pd.concat([comment_result,insert_data],axis=1)
# result3.to_csv('영상정보_씬님(이모티콘제거후).csv',index=False,encoding='CP949')

time.sleep(1000)