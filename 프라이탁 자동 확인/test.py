from selenium import webdriver
from datetime import datetime
import schedule
import time
 
 #프라이탁 신상 확인 코드 v2.0 
 #새로운 가방이 등록되었을 때, 티스토리 댓글 아이디 및 비밀번호가 중복으로 입력되는 것을 수정한 버전 입니다.
print('10분마다 프라이탁 홈페이지를 갱신하며, 신제품 여부를 확인합니다.\n')
driver = webdriver.Chrome('/Users/jeonje/chromedriver')
 
preLinks = []
newLinks = []
 
def writeUserInfo():
    url = 'https://jaiboy.tistory.com/2' #티스토리 블로그 주소
    driver.get(url) 
 
    driver.find_element_by_css_selector('.inp_name').send_keys("test") #티스토리 댓글에 적용될 아이디 입니다.
    driver.find_element_by_css_selector('.inp_password').send_keys("1234") #티스토리 댓글에 적용될 비밀번호 입니다.
    driver.find_elements_by_css_selector('textarea')[0].send_keys("프라이탁 신상 확인 프로그램 시작 날짜 정보 : " + datetime.today().strftime("%Y%m%d%H%M"))
    driver.find_element_by_css_selector('.btn_register').click() #티스토리 댓글 등록 버튼 동작

def writeComment():
 
    global preLinks
    global newLinks
    url = 'https://jaiboy.tistory.com/2'
    driver.get(url)
 
    driver.find_elements_by_css_selector('textarea')[0].send_keys("새로운 가방이 등록되었습니다.")
    driver.find_elements_by_css_selector('div.submit button.btn')[0].click() #티스토리 댓글 등록 버튼 동작
    preLinks = newLinks.copy() #기존 정보를 새로운 정보로 교체
 
    print(time.strftime('%c', time.localtime(time.time())) + ' ::: 새로운 가방이 나와 댓글을 작성했습니다.')
 
 
def getFreitag():
    print(time.strftime('%c', time.localtime(time.time())) + ' ::: 프라이탁에서 새로 불러옵니다.')
    global newLinks
    global preLinks
    url = 'https://www.freitag.ch/en/f11'
    driver.get(url)
 
    for item in driver.find_elements_by_css_selector('ul.products-list > li > a > img'):
        newLinks.append([item.get_attribute('src')])
 
    newItems = [x for x in newLinks if x not in preLinks] #기존 정보에 없는 가방이 나왔을 시에 newItems에 등록
 
 
    if len(newItems) != 0: # 새로운 가방 정보들의 길이가 0이 아닐때 댓글 달아주기 실행
        writeComment()
    else:
        print("새로운 가방이 없습니다.")
 
# 첨에 일단 실행
getFreitag() #프라이탁 사이트 접속 후 정보 가져오기
writeUserInfo() #새롭게 시작할때 티스토리 댓글 유저 아이디 비밀번호 입력


 
# 10분에 한번씩 실행
schedule.every(10).minutes.do(getFreitag)
 
while True:
    schedule.run_pending()
    time.sleep(1)