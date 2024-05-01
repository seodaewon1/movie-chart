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
filename = f"Megabox/MegaboxChart_{current_date}.json"


# 웹드라이브 설치
options = ChromeOptions()
options.add_argument("--headless")
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.get('https://www.megabox.co.kr/movie')


# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "inner-wrap"))
)

# "더보기" 버튼을 찾아 클릭
try:
    for _ in range(4):
        more_button_container = browser.find_element(By.CSS_SELECTOR, ".btn-more.v1")
        more_button = more_button_container.find_element(By.CSS_SELECTOR, "button")

        if more_button:
            more_button.click()
            print("Clicked '더보기' button.")
            time.sleep(3)
except Exception as e:
    print("Error clicking '더보기':", e)

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')


# 데이터 추출
music_data = []
tracks = soup.select(".inner-wrap .movie-list .list li")
for track in tracks:
    rank = track.select_one(".rank").text.strip()
    title = track.select_one(".tit").text.strip()
    rate = track.select_one(".rate").text.strip()
    date = track.select_one(".date").text.strip()
    image_url = track.select_one(".movie-list-info img").get('src')

    music_data.append({
        "rank": rank,
        "title": title,
        "rate": rate,
        "date": date,
        "imageURL": image_url,
    })
    print(music_data)
# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(music_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
