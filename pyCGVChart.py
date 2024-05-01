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
filename = f"CGV/CGVChart_{current_date}.json"

# 웹드라이버 설치
options = ChromeOptions()
options.add_argument("--headless")
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

# CGV 페이지 열기
browser.get('http://www.cgv.co.kr/movies/?lt=1&ft=0')

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, "contents"))
)

# "더보기" 버튼을 찾아 클릭
try:
    more_button = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "btn-more-fontbold"))
    )
    if more_button:
        more_button.click()  # 변경된 부분: execute_script 대신 click 메서드 사용
        print("Clicked '더보기' button.")
        time.sleep(3)  # 버튼 클릭 후 잠시 대기
except Exception as e:
    print("Error clicking '더보기':", e)

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
music_data = []

# 첫 번째 tracks
tracks1 = soup.select(".wrap-movie-chart .sect-movie-chart li")
for track in tracks1:
    rank = track.select_one(".rank").text.strip()
    title = track.select_one(".title").text.strip()
    rate = track.select_one(".percent span").text.strip()   
    date = track.select_one(".txt-info").text.strip().split()[0]
    image_url = track.select_one(".thumb-image img").get('src')

    music_data.append({
        "rank": rank,
        "title": title,
        "rate": rate,
        "date": date,
        "imageURL": image_url,
    })

# 두 번째 tracks
tracks2 = soup.select(".sect-movie-chart .list-more li")
for track in tracks2:
    title = track.select_one(".title").text.strip()
    rate = track.select_one(".percent span").text.strip()   
    date = track.select_one(".txt-info").text.strip().split()[0]
    image_url = track.select_one(".thumb-image img").get('src')

    music_data.append({  
        "title": title,
        "rate": rate,
        "date": date,
        "imageURL": image_url,
    })

# music_data 리스트를 한 번에 출력
print(music_data)

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(music_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
