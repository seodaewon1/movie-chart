from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"Lottecinema/LottecinemaChart_{current_date}.json"
# 웹드라이브 설치
options = ChromeOptions()
options.add_argument("--headless")
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.get('https://www.lottecinema.co.kr/NLCHS/Movie/List?flag=1')
# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "movie_screen_box"))
)
# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')
# 데이터 추출
music_data = []
# 각 .movie_list.type2 요소에 대해 반복문 실행
tracks = soup.select(".movie_screen_box .movie_list.type2")
for track in tracks:
    # 현재 요소 안에 있는 .screen_add_box 클래스를 모두 선택
    screen_add_boxes = track.select(".screen_add_box")
    # 각 .screen_add_box 요소에 대해 반복문 실행
    for box in screen_add_boxes:
        # 각 .screen_add_box 요소 안에 있는 .num_info 클래스 선택하여 rank 추출
        rank = box.select_one(".num_info").text.strip()
        # 이미지 URL 추출
        image_element = box.select_one(".poster_info img")
        image_url = image_element.get('src') if image_element else "No image available"
        # .tit_info 클래스가 존재하는지 확인
        title_element = box.select_one(".tit_info")
        title = title_element.text.strip() if title_element else "No title available"
        music_data.append({
            "rank": rank,
            "title": title,
            "imageURL": image_url,
        })
print(music_data)
# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(music_data, f, ensure_ascii=False, indent=4)
# 브라우저 종료
browser.quit()
