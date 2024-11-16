import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urlencode

# temp ="https://builder.hufs.ac.kr/user/indexSub.action?codyMenuSeq=129898191&siteId=soft&menuType=T&uId=9&sortChar=A&linkUrl=06-3.html&mainFrame=right"

# def crawl_notices():
#   options = webdriver.ChromeOptions()
#   options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
#   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#  # 프레임셋 페이지 URL로 이동
#   driver.get("https://soft.hufs.ac.kr/")

#     # 프레임셋 내에서 첫 번째 프레임으로 전환
#   driver.switch_to.frame("homepage_frame")  # 프레임 이름 사용

#     # 프레임 내부에서 'more'로 시작하는 <a> 태그 찾기
#   items = driver.find_elements(By.CSS_SELECTOR, "a[class^='more']")

#     # 결과 출력
#   for item in items:
#         print(item.text)

#     # 브라우저 종료
#   driver.quit()

# def crawl_notices(notice_organ):
#   # 브라우저 설정
#   options = webdriver.ChromeOptions()
#   options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # 사용자 에이전트 추가
#   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#   url = 'https://soft.hufs.ac.kr/'  # 크롤링할 페이지
#   driver.get(url)
#   # 로그인 버튼 클릭 (로그인 페이지로 이동)
#   login_button = driver.find_element(By.XPATH, '//*[@id="pageTop"]/div[1]/ul/li[2]/a')  # 로그인 버튼의 XPath로 변경
#   login_button.click()

#   # 로그인 폼이 로드될 때까지 대기
#   WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "userId")))  # 로그인 폼의 username 필드를 기다림

#   # 로그인 과정
#   username = driver.find_element(By.NAME, "userId")  # 로그인 폼의 아이디
#   password = driver.find_element(By.NAME, "userPw")  # 로그인 폼의 비밀번호
#   username.send_keys("202101175")
#   password.send_keys("Hufshyewon0608@")
#   password.send_keys(Keys.RETURN)
#   # 로그인 후 페이지가 로드될 때까지 대기
#   WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pageRightT")))  # 로그인 후 나타나는 요소 대기
#   # 로그인 후 세션 쿠키 얻기
#   cookies = driver.get_cookies()
#   print(cookies)




#   # session = requests.Session()
#   # for cookie in cookies:
#   #   session.cookies.set(cookie['name'], cookie['value'])

#   # # 페이지 로딩 후 원하는 데이터 가져오기
#   # page_content = session.get(url).text  # 세션을 사용하여 페이지를 가져옴
#   # print(page_content)

#   driver.quit()

def crawl_notices():
  url='https://builder.hufs.ac.kr/user/indexSub.action?codyMenuSeq=135456840&siteId=oia3&menuType=T&uId=8&sortChar=A&menuFrame=left&linkUrl=7_1.html&mainFrame=right'
  
  headers = {
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
}
  response = requests.get(url, headers=headers)
  if response.status_code != 200:
      print(f"Failed to retrieve the page: {response.status_code}")
      return
    
  soup = BeautifulSoup(response.text, "lxml") # 가져온 HTML 문서를 파서를 통해 BeautifulSoup 객체로 만듦
  parent_div = soup.find("div", class_="contents_area")
  all_list=parent_div.find("tbody")
  lists = all_list.find_all("tr")[:6]
  result=[]
  for list in lists:
     contents=list.find_all("td")[:2]
     title=contents[0].find('a').text.strip()
     date=contents[1].text.strip()
     temp_url=contents[0].find('a').get('href')
     parsed_url = urlparse("?" + temp_url.split("?", 1)[1])  # '?'를 앞에 추가해 parse_qs와 호환되게 만듦
     query_params = parse_qs(parsed_url.query)
     board_id = query_params.get('boardId', [''])[0]
     page = query_params.get('page', [''])[0]
     command = query_params.get('command', [''])[0]
     board_seq = query_params.get('boardSeq', [''])[0]
     new_url=f"&dum=dum&boardId={board_id}&page={page}&command={command}&boardSeq={board_seq}"
     result.append({"title": title, "date": date, "url": url+new_url})
     
  print(result)


# 국제교류원 + 외국어교육센터 + 플렉스센터
def crawl_notices_foreign():
  # 외국어교육센터
  # url='https://builder.hufs.ac.kr/user/indexSub.action?framePath=unknownboard&siteId=flec2&dum=dum&boardId=98772159&page=1&command=list'
  #국제교류원
  url='https://builder.hufs.ac.kr/user/indexSub.action?codyMenuSeq=135456840&siteId=oia3&menuType=T&uId=8&sortChar=A&menuFrame=left&linkUrl=7_1.html&mainFrame=right'
  url='https://builder.hufs.ac.kr/user/indexSub.action?codyMenuSeq=84761504&siteId=flex2&menuType=T&uId=6&sortChar=A&linkUrl=4_1.html&mainFrame=right'
  headers = {
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
}
  response = requests.get(url, headers=headers)
  if response.status_code != 200:
      print(f"Failed to retrieve the page: {response.status_code}")
      return
    
  soup = BeautifulSoup(response.text, "lxml") # 가져온 HTML 문서를 파서를 통해 BeautifulSoup 객체로 만듦
  tbody=soup.find('tbody')
  lists=tbody.find_all('tr')[:9]
  result=[]
  for list in lists:
     title=list.find("td", attrs={"class":"title"}).get_text().strip()
     new_url=list.find('a').get('href')
     date=list.find_all('td')[3].get_text().strip()
     parsed_url = urlparse("?" + new_url.split("?", 1)[1])  # '?'를 앞에 추가해 parse_qs와 호환되게 만듦
     query_params = parse_qs(parsed_url.query)
     board_id = query_params.get('boardId', [''])[0]
     page = query_params.get('page', [''])[0]
     command = query_params.get('command', [''])[0]
     board_seq = query_params.get('boardSeq', [''])[0]
     new_url=f"&dum=dum&boardId={board_id}&page={page}&command={command}&boardSeq={board_seq}"
     result.append({'title': title, 'url':url+new_url, 'date': date})
  
  
  print(result)
  return list

def crawl_notices_foreign_special():
  #특수외국어
  url='https://cfl.ac.kr/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000001&menuId=MNU_0000000000000024'
  headers = {
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
}
  response = requests.get(url, headers=headers)
  if response.status_code != 200:
      print(f"Failed to retrieve the page: {response.status_code}")
      return
    
  soup = BeautifulSoup(response.text, "lxml") # 가져온 HTML 문서를 파서를 통해 BeautifulSoup 객체로 만듦
  tbody=soup.find('tbody')
  lists=tbody.find_all('tr')[:9]
  result=[]
  for list in lists:
     title=list.find("td", attrs={"class":"title"}).get_text().strip()
     new_url=list.find('a').get('href')
     date=list.find_all('td')[3].get_text().strip()
     parsed_url = urlparse(new_url) 
     query_params = parse_qs(parsed_url.query)
     nttNo = query_params.get("nttNo", [None])[0]
     pageIndex = query_params.get("pageIndex", [None])[0]
     menuId = query_params.get("menuId", [None])[0]
     bbsId = query_params.get("bbsId", [None])[0]
     new_url=f"https://cfl.ac.kr/cop/bbs/selectBoardArticle.do?nttNo={nttNo}&pageIndex={pageIndex}&menuId={menuId}&bbsId={bbsId}"
     result.append({'title': title, 'url':new_url, 'date': date})
  
  
  print(result)
  return list

def crawl_notices_foreign_cfl():
  #진로취업센터
  url='https://job.hufs.ac.kr/job/comm/board/d9acb88b1a000472132dd8b0c1e1cf65/index.do#;'
  headers = {
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
}
  response = requests.get(url, headers=headers)
  if response.status_code != 200:
      print(f"Failed to retrieve the page: {response.status_code}")
      return
    
  soup = BeautifulSoup(response.text, "lxml") # 가져온 HTML 문서를 파서를 통해 BeautifulSoup 객체로 만듦
  tbody=soup.find('tbody')
  lists=tbody.find_all('tr')[:9]
  result=[]
  temp=lists[0].find("a")["onclick"]
  number = re.search(r"\d+", temp).group()  # 숫자만 추출
  print(number)
  for list in lists:
     title=list.find("td", attrs={"class":"title"}).get_text().strip()
     new_url=list.find("a")["onclick"]
     date=list.find_all('td')[2].get_text().strip()
     number=re.search(r"\d+", new_url).group()
     new_url=f"https://job.hufs.ac.kr/job/comm/board/d9acb88b1a000472132dd8b0c1e1cf65/view.do?typeSeq=&teamSeq=&ptfolUrl=&currentPageNo=1&searchType=0001&searchValue=&dataSeq={number}&parentSeq={number}"
     result.append({'title': title, 'url':new_url, 'date': date})
  
  
  print(result)
  return list

def crawl_notices_department():
  #학과
  url='https://philosophy.hufs.ac.kr/philosophy/5820/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGcGhpbG9zb3BoeSUyRjEwODklMkZhcnRjbExpc3QuZG8lM0Y%3D'
  url='https://english.hufs.ac.kr/english/4069/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGZW5nbGlzaCUyRjc1OSUyRmFydGNsTGlzdC5kbyUzRg%3D%3D'
  headers = {
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
}
  response = requests.get(url, headers=headers)
  if response.status_code != 200:
      print(f"Failed to retrieve the page: {response.status_code}")
      return
    
  soup = BeautifulSoup(response.text, "lxml") # 가져온 HTML 문서를 파서를 통해 BeautifulSoup 객체로 만듦
  tbody=soup.find('tbody')
  lists=tbody.find_all('tr')[4:9]
  print(lists[0].find("td", attrs={"class":"td-subject"}).get_text().strip())
  print(lists[0].find("td", attrs={"class":"td-date"}).get_text().strip())
  print(lists[0].find('a').get('href'))
  result=[]
  for list in lists:
     title=list.find("td", attrs={"class":"td-subject"}).get_text().strip()
     new_url=list.find('a').get('href')
     date=list.find("td", attrs={"class":"td-date"}).get_text().strip()
     base_url="https://english.hufs.ac.kr/"
     result.append({'title': title, 'url':base_url+new_url, 'date': date})
  
  
  print(result)
  return list