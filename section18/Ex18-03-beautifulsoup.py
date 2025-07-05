"""
파일명: Ex18-03-beautifulsoup.py

url
https://news.nate.com/rank/interest?sc=ent

<h2 class="tit">손예진♥현빈♥아들 가족사진 공개한 팬, 정체는 AI? "손 어색·팔 사...
</h2>
<h2 class="tit">시신 아홉 토막 낸 살인마, 장기 적출까지 '충격'…체포 당시 환각제 ...
</h2>

"""

import requests
from bs4 import BeautifulSoup

url = 'https://news.nate.com/rank/interest'
# ?sc=ent
params = {
    'sc':'ent'
}

response = requests.get(url, params=params)
html = response.text

soup = BeautifulSoup(html, 'html.parser')
tit_list = soup.select('h2')
for idx, tit in enumerate(tit_list, 1):
    print(f'{idx}: {tit.text.strip()}')

