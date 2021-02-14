from selenium import webdriver
import schedule
import time
 
print('10분마다 프라이탁 홈페이지를 갱신하며, 신제품 여부를 확인합니다.\n')
driver = webdriver.Chrome('C:/dev/chromedriver')
 
preLinks = []
newLinks = []
 
 
def writeComment():
 
    global preLinks
    global newLinks
    url = 'https://jaiboy.tistory.com/2'
    driver.get(url)
 
    driver.find_elements_by_css_selector('div.field > input')[0].send_keys("MYID")
    driver.find_elements_by_css_selector('div.field > input')[1].send_keys("PW")
    driver.find_elements_by_css_selector('textarea')[0].send_keys("신제품이 등록되었습니다.")
    driver.find_elements_by_css_selector('div.submit button.btn')[0].click()
    preLinks = newLinks.copy()
 
    print(time.strftime('%c', time.localtime(time.time())) + ' ::: 신제품이 나와 댓글을 작성했습니다.')
 
 
def getFreitag():
    print(time.strftime('%c', time.localtime(time.time())) + ' ::: 프라이탁에서 새로 불러옵니다.')
    global newLinks
    global preLinks
    url = 'https://www.freitag.ch/en/f11'
    driver.get(url)
 
    for item in driver.find_elements_by_css_selector('ul.products-list > li > a > img'):
        newLinks.append([item.get_attribute('src')])
 
    newItems = [x for x in newLinks if x not in preLinks]
 
 
    if len(newItems) != 0:
        writeComment()
    else:
        print("신제품이 없습니다.")
 
# 첨에 일단 실행
getFreitag()
 
# 10분에 한번씩 실행
schedule.every(5).minutes.do(getFreitag)
 
while True:
    schedule.run_pending()
    time.sleep(1)

