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
# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"CineQ/CineQChart_{current_date}.json"
# 웹드라이브 설치
options = ChromeOptions()
options.add_argument("--headless")
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.get('https://www.cineq.co.kr/Movie/BoxOffice')
# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".section.group.section-movie-list.boxoffice"))
)
# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')
# 데이터 추출
movie_data = []
# '.section.group.section-movie-list.boxoffice' 안의 모든 'li' 태그 중 'data-moviecode' 속성을 가진 항목을 찾음
movie_items = soup.select(".section.group.section-movie-list.boxoffice ul li[data-moviecode]")
for item in movie_items:
    # 영화 제목 추출
    rank = item.select_one(".movie-desc .label").text.strip() if item.select_one(".movie-desc .label") else "No title available"
    # .movie-desc에서 모든 텍스트 추출
    all_texts = item.select_one(".movie-desc").get_text(" ", strip=True)
    # 개별 텍스트 노드만 리스트로 분리
    text_nodes = [text for text in item.select_one(".movie-desc").stripped_strings]
    # "범죄도시4"는 첫 번째와 두 번째 span 태그의 텍스트 뒤에 올 것이므로
    # 세 번째 텍스트 노드를 추출하고 싶은 경우
    specific_description = text_nodes[2] if len(text_nodes) > 2 else "No specific description available"
    # # 이미지 URL 추출
    image_element = item.select_one(".section.group.section-movie-list.boxoffice ul li[data-moviecode] img.posterlist")  # 'img' 태그에 적용된 클래스명을 사용
    image_url = image_element['src'] if image_element else "No image available"
    # # data-moviecode 속성값 추출
    # movie_code = item['data-moviecode']
    movie_data.append({
        "title": specific_description,
        "rank": rank,
        "imageURL": image_url
    })
# 결과 출력
print(movie_data)
# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(movie_data, f, ensure_ascii=False, indent=4)
# 브라우저 종료
browser.quit()
