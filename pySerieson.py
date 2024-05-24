from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"Serieson/serieson_chart{current_date}.json"

# 웹드라이브 설치
options = ChromeOptions()
options.add_argument("--window-size=1920,1080") 
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

# 페이지 열기
browser.get('https://serieson.naver.com/v3/movie/ranking/realtime')

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "RankingPage_ranking_wrap__GB855"))
)

# 천천히 스크롤 다운
scroll_pause_time = 1  # 1초 대기
pixels_to_scroll_vertically = 1000  # 수직 스크롤할 픽셀 수
pixels_to_scroll_horizontally = 300  # 수평 스크롤할 픽셀 수
max_time_limit = 40  # 전체 작업 시간 제한 (40초)
start_time = time.time()  # 작업 시작 시간

def scroll_down():
    """현재 위치에서 지정된 픽셀 수만큼 아래로 스크롤"""
    browser.execute_script(f"window.scrollBy(0, {pixels_to_scroll_vertically});")

def scroll_right():
    """현재 위치에서 지정된 픽셀 수만큼 오른쪽으로 스크롤"""
    browser.execute_script(f"window.scrollBy({pixels_to_scroll_horizontally}, 0);")

while (time.time() - start_time) < max_time_limit:
    scroll_down()
    scroll_right()
    time.sleep(scroll_pause_time)
    # 스크롤 이동 후 새로운 높이와 너비를 계산
    new_height = browser.execute_script("return document.body.scrollHeight")
    new_width = browser.execute_script("return document.body.scrollWidth")
    if new_height == browser.execute_script("return window.pageYOffset + window.innerHeight") and \
       new_width == browser.execute_script("return window.pageXOffset + window.innerWidth"):
        break  # 페이지 끝에 도달

# 페이지 소스 가져오기
page_source = browser.page_source

# BeautifulSoup를 사용하여 페이지 소스를 파싱
soup = BeautifulSoup(page_source, 'html.parser')

# 데이터 추출
movie_data = []
tracks = soup.select(".RankingList_ranking_list__N4QsH li")
for i, track in enumerate(tracks, start=1):
    rank = track.select_one(".RankingNumber_rank__zZLNC").text.strip() if track.select_one(".RankingNumber_rank__zZLNC") else "N/A"
    title = track.select_one(".Title_title__s9o0D").text.strip() if track.select_one(".Title_title__s9o0D") else "N/A"
    price = track.select_one(".Price_price__GqXqo").text.strip() if track.select_one(".Price_price__GqXqo") else "N/A"
    
    # 이미지 URL 추출 부분
    image_tag = track.select_one("img.Thumbnail_image__TxHd0")
    if image_tag:
        image_url = image_tag.get('src') or image_tag.get('data-src', "No image available")
    else:
        image_url = "No image available"

    movie_data.append({
        "rank": rank,
        "title": title,
        "price": price,
        "imageURL": image_url,
    })

# 출력 확인
print(json.dumps(movie_data, ensure_ascii=False, indent=4))

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(movie_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
