"""
파일명: Ex18-02-beautifulsoup.py

BeautifulSoup
    Html, XML 등 마크업 언어를 파싱하는 라이브러리
    ex) <태그>내용</태그>

파싱(Parsing)
    데이터를 분석해서 원하는 형태로 변환하는 과정
    원본데이터 -> [파싱] -> 구조화된 데이터

BeautifulSoup 설치방법
    pip install beautifulsoup4

"""

import requests
from bs4 import BeautifulSoup

# 네이버 랭킹뉴스 URL
url = 'https://news.naver.com/main/ranking/popularDay.naver'

# 헤더 설정 (User-Agent 없으면 접속 거부될 수 있음)
headers = {
    'User-Agent': 'Mozilla/5.0'
}

# HTML 요청
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 기사 제목 찾기
titles = soup.select('.rankingnews_list .list_title')

print("📌 기사 제목 목록:")
for idx, title_tag in enumerate(titles, 1):
    print(f"{idx}. {title_tag.get_text(strip=True)}")
