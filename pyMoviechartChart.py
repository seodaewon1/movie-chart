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

current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"Moviechart/MoviechartChart_{current_date}.json"

# 웹드라이버 설치
options = ChromeOptions()
options.add_argument("--headless")
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

# CGV 페이지 열기
browser.get('https://www.moviechart.co.kr/rank/realtime/index/image')

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "movieBox"))
)

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')
# 데이터 추출
music_data = []

# 첫 번째 tracks
tracks = soup.select(".movieBox-list .movieBox-item")

for track in tracks:
    rank = track.select_one(".rank.realtime_rank23").text.strip()
    title = track.select_one(".movie-title h3 a").text.strip()
    rate = track.select_one(".ticketing span").text.strip()   
    date = track.select_one(".movie-launch").text.strip()
    image_url = track.select_one(".movieBox-item img").get('src')

    music_data.append({
        "rank": rank,
        "title": title,
        "rate": rate,
        "date": date,
        "imageURL": image_url
    })

print(music_data)

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(music_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
